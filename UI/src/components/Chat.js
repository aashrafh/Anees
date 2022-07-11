import React, { useEffect, useCallback, useState } from "react";
import { GiftedChat, Bubble } from "react-native-gifted-chat";
import { View, KeyboardAvoidingView, Platform } from "react-native";

const Chat = () => {
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

  useEffect(() => {
    setMessages([
      {
        _id: 1,
        text: "Hello 1",
        createdAt: new Date(),
        user: {
          _id: 2,
          name: "React Native",
          avatar: "https://placeimg.com/140/140/any",
        },
      },
      {
        _id: 3,
        text: "Hello 3",
        createdAt: new Date(),
        user: {
          _id: 2,
          name: "React Native",
          avatar: "https://placeimg.com/140/140/any",
        },
      },
      {
        _id: 2,
        text: "Hello 2",
        createdAt: new Date(),
        user: {
          _id: 1,
          name: "React Native",
          avatar: "https://placeimg.com/140/140/any",
        },
      },
    ]);
  }, []);

  const onSend = useCallback((messages = []) => {
    setMessages((previousMessages) =>
      GiftedChat.append(previousMessages, messages)
    );
  }, []);

  useEffect(() => {
    if (messages[0]?.user?._id === 1) {
      setMessages((previousMessages) =>
        GiftedChat.append(previousMessages, [
          {
            _id: messages.length + 1,
            text: "Recieved!",
            createdAt: new Date(),
            user: {
              _id: 2,
              name: "React Native",
              avatar: "https://placeimg.com/140/140/any",
            },
          },
        ])
      );
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
