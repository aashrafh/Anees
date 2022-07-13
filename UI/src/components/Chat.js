import React, { useEffect, useCallback, useState } from "react";
import { GiftedChat, Bubble } from "react-native-gifted-chat";
import { View, KeyboardAvoidingView, Platform } from "react-native";
import axios from "axios";
import { api } from "../api";

// {
//   _id: 1,
//   text: "Hello 1",
//   createdAt: new Date(),
//   user: {
//     _id: 2,
//     name: "React Native",
//     avatar: "https://placeimg.com/140/140/any",
//   },
// },
const Chat = () => {
  const aneesAvatar = "https://placeimg.com/140/140/any"
  const [messages, setMessages] = useState([]);

  const renderBubble = (props) => {
    const wrapperStyle = {
      padding: "0.5rem",
    };
    const bottomContainerStyle = {
      display: "none",
    };
    return (
      <Bubble
        {...props}
        wrapperStyle={{ right: { ...wrapperStyle }, left: { ...wrapperStyle } }}
        bottomContainerStyle={{
          right: {
            ...bottomContainerStyle,
          },
          left: {
            ...bottomContainerStyle,
          },
        }}
      />
    );
  };

  const onSend = useCallback((messages = []) => {
    setMessages((previousMessages) =>
      GiftedChat.append(previousMessages, messages)
    );
  }, []);

  useEffect(() => {
    api.post("/history",{username : "Ahmed"}).then((res)=>{
      const history = res.data.response
      setMessages(history.reverse())
    }).catch((err)=>{console.log(err)})
  },[])

  useEffect(() => {
    if (messages.length > 0 && messages[0]?.user?._id === 1) {
      api
        .post("/getResponse", {
            username: "Ahmed",
            text: messages[0].text
        })
        .then((res) => {
          console.log(res);
            setMessages((previousMessages) =>
              GiftedChat.append(previousMessages, [
                {
                  _id: messages.length + 1,
                  text: res.data.response.text,
                  createdAt: new Date(),
                  user: {
                    _id: 0,
                    name: "أنيس",
                    avatar: aneesAvatar,
                  },
                },
              ])
            );
        })
        .catch((err) => {
          console.log(err);
        });

    }
  }, [messages]);

  return (
    <View style={{ flex: 1 }}>
      <GiftedChat
        messages={messages}
        showAvatarForEveryMessage={false}
        showUserAvatar={false}
        onSend={(messages) => onSend(messages)}
        messagesContainerStyle={{
          backgroundColor: "#fff",
        }}
        user={{
          _id: 1,
          avatar: "https://i.pravatar.cc/300",
        }}
        renderBubble={renderBubble}
      />
      {Platform.OS === "android" && <KeyboardAvoidingView behavior="padding" />}
    </View>
  );
};

export default Chat;
