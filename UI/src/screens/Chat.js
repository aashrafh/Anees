import React, { useEffect, useCallback, useState, useContext } from "react";
import { GiftedChat, Bubble, MessageText } from "react-native-gifted-chat";
import { View, KeyboardAvoidingView, Platform, StyleSheet } from "react-native";
import HtmlView from "react-native-htmlview";
import { api } from "../api";
import * as SecureStore from "expo-secure-store";
import { TokenContext } from "../../context";

const aneesAvatar = require("../../assets/images/aneesAvatar.png");
const userAvatar = require("../../assets/images/userAvatar.png");

const Chat = () => {
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

  const renderMessageText = (props) => {
    const { currentMessage } = props;
    const containsHtml = /<\/?[a-z][\s\S]*>/i.test(currentMessage.text);
    if (containsHtml) {
      return <HtmlView value={currentMessage.text} stylesheet={htmlMsg} />;
    }
    return <MessageText {...props} />;
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
          if (res.data.response.intent === "search") {
            console.log("Search", res.data.response);
          } else {
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
          }
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
        renderMessageText={renderMessageText}
      />
      {Platform.OS === "android" && <KeyboardAvoidingView behavior="padding" />}
    </View>
  );
};

const htmlMsg = StyleSheet.create({
  ul: {
    padding: "5%",
  },
  ol: {
    padding: "5%",
  },
  a: {
    fontWeight: "300",
    color: "#2B9BED", // make links coloured pink
  },
});

export default Chat;
