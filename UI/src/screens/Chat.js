import React, { useEffect, useCallback, useState, useContext } from "react";
import { GiftedChat, Bubble } from "react-native-gifted-chat";
import { View, KeyboardAvoidingView, Platform } from "react-native";
import { api } from "../api";
import * as SecureStore from "expo-secure-store";
import { TokenContext } from "../../context";

const aneesAvatar = require("../../assets/images/aneesAvatar.png");
const userAvatar = require("../../assets/images/userAvatar.png");

const Chat = ({ navigation }) => {
  const [messages, setMessages] = useState([]);
  const [isAneesTyping, setIsAneesTyping] = useState(false);
  const [token, setToken] = useContext(TokenContext);

  const renderBubble = (props) => {
    const wrapperStyle = {
      padding: 0.5,
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

  const onLogout = () => {
    SecureStore.deleteItemAsync("username").then(() => {
      setMessages((previousMessages) =>
        GiftedChat.append(previousMessages, [
          {
            _id: messages.length + 1,
            text: "استمتعت بالكلام معاك، اتمنى اشوفك تاني",
            createdAt: new Date(),
            user: {
              _id: 0,
              name: "أنيس",
              avatar: aneesAvatar,
            },
          },
        ])
      );
      setTimeout(() => {
        setToken("");
      }, 1000);
    });
  };

  useEffect(() => {
    api
      .post("/history", { username: "Ahmed" })
      .then((res) => {
        const history = res.data.response;
        // console.log(history);
        setMessages(
          history.map((item, index) => ({
            _id: index,
            text: item.message,
            createdAt: item?.time || new Date(),
            user: {
              _id: parseInt(item.isUser),
              name: item.isUser ? "Ahmed" : "أنيس",
              avatar: item.isUser ? userAvatar : aneesAvatar,
            },
          }))
        );
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);

  useEffect(() => {
    if (messages.length > 0 && messages[0]?.user?._id === 1) {
      if (messages[0].text === "سلام") {
        onLogout();
        return;
      }

      setIsAneesTyping(true);
      console.log("after true " + isAneesTyping);
      api
        .post("/getResponse", {
          username: "Ahmed",
          text: messages[0].text,
        })
        .then((res) => {
          // console.log(res);
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
      setIsAneesTyping(false);
      console.log("after false " + isAneesTyping);
    }
  }, [messages]);

  return (
    <View style={{ flex: 1 }}>
      <GiftedChat
        isTyping={isAneesTyping}
        messages={messages}
        showAvatarForEveryMessage={false}
        showUserAvatar={false}
        onSend={(messages) => onSend(messages)}
        messagesContainerStyle={{
          backgroundColor: "#fff",
        }}
        user={{
          _id: 1,
          avatar: userAvatar,
        }}
        renderBubble={renderBubble}
      />
      {Platform.OS === "android" && <KeyboardAvoidingView behavior="padding" />}
    </View>
  );
};

export default Chat;
