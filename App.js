import React from 'react';
import { StyleSheet, Text, View, FlatList, TextInput, KeyboardAvoidingView, TouchableOpacity } from 'react-native';
import {send, subscribe} from  'react-native-training-chat-server';


const NAME1 = '254746439178';
const NAME2 = '420776044994';
// const NAME1 = process.env.NAME1;
// const NAME2 = process.env.NAME2;
const CHANNEL = 'Table11';

export default class App extends React.Component {

  state= {
    typing: "",
    messages: [],
    name: true,
    user1: "",
    user2: "",
  };

  componentWillMount() {
    let arr = [];
    let messages = []
    let newMsg;
    subscribe(CHANNEL, () => {
      // this.setState({messages})
      let comp = this;
      fetch(`https://cqrwltdl4g.execute-api.us-east-1.amazonaws.com/chat/${NAME1}/messages`)
      .then(function(response) {
        return response.json();
      })
      .then(function(myJson) {
        
        myJson.forEach((messageObj) => {
          newMsg = {
          sender: messageObj.from_user,
          message: messageObj.message,
        }
         messages.push(newMsg)
        });
        comp.setState({messages: messages});
      });
      fetch(`https://cqrwltdl4g.execute-api.us-east-1.amazonaws.com/chat/${NAME2}/messages`)
      .then(function(response) {
        return response.json();
      })
      .then(function(myJson) {
        
        myJson.forEach((messageObj) => {
          newMsg = {
          sender: messageObj.from_user,
          message: messageObj.message,
        }
         messages.push(newMsg)
        });
        comp.setState({messages: messages});
      });
      
    });
  }

  async sendMessage() {
    
      fetch(`https://cqrwltdl4g.execute-api.us-east-1.amazonaws.com/chat/${NAME1}/messages`, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
      },
        body: JSON.stringify({
          "type": "text",
	        "to_user": NAME1,
	        "message": this.state.typing,
        })
      })
      await send({
        channel: CHANNEL,
        sender: NAME1,
        message: this.state.typing
      });
      this.setState({typing: ''});

  }

  renderItem({item}) {
    return (
      <View style={styles.row}>
        <Text style={styles.sender}>{item.sender}</Text>
        <Text style={styles.message}>{item.message}</Text>
      </View>
    )
  }
  
  render() {
    return (
      <View style={styles.container}>
        <FlatList
          data={this.state.messages}
          renderItem={this.renderItem}
          inverted
        />
        <KeyboardAvoidingView behavior='padding'>
          <View style={styles.footer}>
            <TextInput
              value={this.state.typing}
              onChangeText={text => this.setState({typing: text})}
              style={styles.input}
              underlineColorAndroid="transparent"
              placeholder="Type something nice"
            />
            <TouchableOpacity onPress={this.sendMessage.bind(this)}>
              <Text style={styles.send}>Send</Text>
            </TouchableOpacity>
          </View>
        </KeyboardAvoidingView>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  row: {
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  message: {
    fontSize: 18,
  },
  sender: {
    fontWeight: 'bold',
    paddingRight: 10,
  },
  footer: {
    flexDirection: 'row',
    backgroundColor: '#eee',
  },
  input: {
    paddingHorizontal: 20,
    paddingVertical: 10,
    fontSize: 18,
    flex: 1,
  },
  send: {
    alignSelf: 'center',
    color: 'lightseagreen',
    fontSize: 16,
    fontWeight: 'bold',
    padding: 20,
  }
});


