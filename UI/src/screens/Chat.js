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
import * as Calendar from "expo-calendar";
import * as Permissions from "expo-permissions";

const aneesAvatar = require("../../assets/images/aneesAvatar.png");
const userAvatar = require("../../assets/images/userAvatar.png");

const Chat = ({ navigation }) => {
  const [messages, setMessages] = useState([]);
  const [isAneesTyping, setIsAneesTyping] = useState(false);
  const [token, setToken] = useContext(TokenContext);

  const [calendarId, setCalendarId] = useState(null);

  const [notificationPermissions, setNotificationPermissions] = useState(
    PermissionStatus.UNDETERMINED
  );
  const [calendarPermissions, setCalendarPermissions] = useState(false);

  const scheduleNotification = (seconds, items) => {
    const schedulingOptions = {
      content: {
        title: "تحب تقييم الافلام؟",
        body: "اضغط هنا لتقييم الافلام",
        sound: true,
        data: { items },
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
    const { data } = notification.request.content;
    Alert.alert("", "تحب تقيم الافلام اللي اقترحتها عليك؟", [
      { text: "لا", onPress: () => console.log("OK Pressed") },
      {
        text: "ماشي",
        onPress: () => navigation.navigate("Rating", { items: data.items }),
      },
    ]);
  };

  const requestNotificationPermissions = async () => {
    const { status } = await Notifications.requestPermissionsAsync();
    setNotificationPermissions(status);
    return status;
  };

  const requestCalendarPermissions = async () => {
    const { status } = await Calendar.requestCalendarPermissionsAsync();
    if (status === "granted") {
      const calendars = await Calendar.getCalendarsAsync(
        Calendar.EntityTypes.EVENT
      );
      setCalendarPermissions(status);
    }
  };

  const getDefaultCalendarSource = async () => {
    const defaultCalendar = await Calendar.getDefaultCalendarAsync();
    return defaultCalendar.source;
  };

  const createCalendar = async () => {
    const defaultCalendarSource =
      Platform.OS === "ios"
        ? await getDefaultCalendarSource()
        : { isLocalAccount: true, name: "Anees" };

    const calendarID = await Calendar.createCalendarAsync({
      title: "Anees",
      color: "blue",
      entityType: Calendar.EntityTypes.EVENT,
      sourceId: defaultCalendarSource.id,
      source: defaultCalendarSource,
      name: "Anees",
      ownerAccount: "personal",
      accessLevel: Calendar.CalendarAccessLevel.OWNER,
      timeZone: "Africa/Cairo",
    });
    console.log(calendarID);
    return calendarID;
  };

  const addEventToCalendar = async (title, time, text) => {
    const startDate = new Date(new Date(time).getTime() - 60000 * 120);
    const endDate = new Date(new Date(time).getTime() - 60000 * 60);

    const events = await Calendar.getEventsAsync(
      [calendarId],
      startDate,
      endDate
    );

    if (events.length === 0) {
      const eventIdInCalendar = await Calendar.createEventAsync(calendarId, {
        title,
        startDate,
        endDate,
      });

      setMessages((previousMessages) =>
        GiftedChat.append(previousMessages, [
          {
            _id: messages.length + 1,
            text: text,
            createdAt: new Date(),
            user: {
              _id: 0,
              name: "أنيس",
              avatar: aneesAvatar,
            },
          },
        ])
      );
    } else {
      setMessages((previousMessages) =>
        GiftedChat.append(previousMessages, [
          {
            _id: messages.length + 1,
            text: "مقدرتش اضيف المعاد للنتيجة لان عندك مواعيد تانية في نفس الفترة",
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
  };

  useEffect(() => {
    requestNotificationPermissions();
    requestCalendarPermissions();

    (async function () {
      const calendarId = await createCalendar();
      setCalendarId(calendarId);
    })();
  }, []);

  useEffect(() => {
    if (notificationPermissions !== PermissionStatus.GRANTED) return;
    const listener =
      Notifications.addNotificationReceivedListener(handleNotification);
    return () => listener.remove();
  }, [notificationPermissions]);

  useEffect(() => {
    if (calendarPermissions !== "granted" || calendarId === null) return;
  }, [calendarPermissions]);

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
      setIsAneesTyping(false);
      setTimeout(() => {
        setToken("");
      }, 1000);
    });
  };

  useEffect(() => {
    api
      .post("/history", { username: token })
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
      setIsAneesTyping(true);
      if (messages[0].text === "سلام") {
        onLogout();
        return;
      }
      
      api
        .post("/getResponse", {
          username: token,
          text: messages[0].text,
        })
        .then((res) => {
          if (res.data.intent === "recommendation-movies") {
            scheduleNotification(3, res.data.response.movies);
          }

          if (res.data.intent === "schedule") {
            addEventToCalendar(
              res.data.response.content,
              res.data.response.edited_time,
              res.data.response.text
            );
            return;
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

          setIsAneesTyping(false);
        })
        .catch((err) => {
          console.log(err);
          setIsAneesTyping(false);
        });
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
