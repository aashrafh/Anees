import React, { useEffect, useCallback, useState, useContext } from "react";
import {
  GiftedChat,
  Bubble,
  MessageText,
  Send,
  Composer,
} from "react-native-gifted-chat";
import { View, StyleSheet, Alert, TouchableOpacity, Image } from "react-native";
import HtmlView from "react-native-htmlview";
import { api } from "../api";
import * as SecureStore from "expo-secure-store";
import { TokenContext } from "../../context";
import { PermissionStatus } from "expo-modules-core";
import * as Notifications from "expo-notifications";
const aneesAvatar = require("../../assets/images/aneesAvatar.png");
const userAvatar = require("../../assets/images/userAvatar.png");

const Chat = ({ navigation }) => {
  const [messages, setMessages] = useState([]);
  const [isAneesTyping, setIsAneesTyping] = useState(false);
  const [token, setToken] = useContext(TokenContext);

  const [notificationPermissions, setNotificationPermissions] = useState(
    PermissionStatus.UNDETERMINED
  );

  const scheduleNotification = (seconds, items) => {
    const schedulingOptions = {
      content: {
        title: "This is a notification",
        body: "This is the body",
        itmes: items,
        sound: true,
        priority: Notifications.AndroidNotificationPriority.HIGH,
        color: "blue",
      },
      trigger: {
        seconds: seconds,
      },
    };
    Notifications.scheduleNotificationAsync(schedulingOptions);
  };

  const handleNotification = (notification) => {
    const { items } = notification.request.content;
    console.log(items);
    Alert.alert("", "تحب تقيم الافلام اللي اقترحتها عليك؟", [
      { text: "لا", onPress: () => console.log("OK Pressed") },
      { text: "ماشي", onPress: () => navigation.navigate("Rating") },
    ]);
  };

  const requestNotificationPermissions = async () => {
    const { status } = await Notifications.requestPermissionsAsync();
    setNotificationPermissions(status);
    return status;
  };

  useEffect(() => {
    requestNotificationPermissions();
  }, []);

  useEffect(() => {
    if (notificationPermissions !== PermissionStatus.GRANTED) return;
    const listener =
      Notifications.addNotificationReceivedListener(handleNotification);
    return () => listener.remove();
  }, [notificationPermissions]);

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
          if (res.data.intent === "recommendation-movies") {
            scheduleNotification(3, res.data.response.movies);
          }
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

  const renderSend = (props) => {
    return <Send {...props} label={"ابعت"} />;
  };

  const renderComposer = (props) => {
    return <Composer {...props} placeholder={"بتفكر في ايه؟"} />;
  };

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
        renderSend={renderSend}
        renderComposer={renderComposer}
      />
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
    color: "#2B9BED",
  },
});

export default Chat;
