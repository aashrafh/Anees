import React, { useState, useCallback, useEffect } from 'react'
import { View , Text} from 'react-native';
import { GiftedChat } from 'react-native-gifted-chat'

export function Home() {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    setMessages([
      {
        _id: 1,
        text: 'Hello developer',
        createdAt: new Date(),
        user: {
          _id: 2,
          name: 'React Native',
          avatar: 'https://placeimg.com/140/140/any',
        },
      },
    ])
  }, [])

  const onSend = useCallback((messages = []) => {
    setMessages(previousMessages => GiftedChat.append(previousMessages, messages))
  }, [])

  return (
    <View>
    <GiftedChat
      messages={messages}
      onSend={messages => onSend(messages)}
      user={{
          _id: 1,
        }}
        />
    <Text>hello</Text>
    </View>
  )
}
export default Home