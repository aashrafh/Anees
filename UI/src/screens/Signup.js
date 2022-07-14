import React from "react";
import {
  StyleSheet,
  View,
  TextInput,
  Image,
  Alert,
  I18nManager,
} from "react-native";
import { api } from "../api";
import AppButton from "../components/AppButton";
// import * as SecureStore from "expo-secure-store";

const Signup = ({ navigation }) => {
  const [username, setUsername] = React.useState("");
  const [password, setPassword] = React.useState("");

  const handleUsername = (text) => {
    setUsername(text);
  };
  const handlePassword = (text) => {
    setPassword(text);
  };
  const handleSignup = () => {
    api
      .post("/signup", { username, password })
      .then(async (res) => {
        console.log(res.data);
        // await SecureStore.setItemAsync("username", username);
        navigation.navigate("Chat");
      })
      .catch((err) => {
        console.log(err);
        Alert.alert("حصل مشكلة 😥", err.response.data.message, [
          { text: "حاول تاني", onPress: () => console.log("OK Pressed") },
        ]);
      });
  };
  return (
    <View style={styles.container}>
      <Image
        source={require("../../assets/images/Anees.png")}
        style={styles.Image}
      />

      <View style={styles.form}>
        <TextInput
          style={styles.inputView}
          placeholder="اسم المستخدم"
          placeholderTextColor="white"
          onChangeText={handleUsername}
        />
        <TextInput
          style={styles.inputView}
          placeholder="كلمة السر"
          placeholderTextColor="white"
          secureTextEntry={true}
          onChangeText={handlePassword}
        />
      </View>
      <View style={styles.actions}>
        <AppButton
          buttonStyle={styles.loginBtn}
          textStyle={styles.loginTxt}
          onPress={() => handleSignup()}
          text="يلا نتكلم"
        />

        <AppButton
          buttonStyle={styles.loginBtn}
          textStyle={styles.loginTxt}
          onPress={() => navigation.navigate("Login")}
          text="عندك اكونت؟ يلا نتكلم!"
        />
      </View>
    </View>
  );
};
const styles = StyleSheet.create({
  header: {
    fontSize: 50,
    marginBottom: "5%",
    fontWeight: "bold",
    color: "purple",
    marginTop: "10%",
  },
  container: {
    paddingTop: "3%",
    paddingBottom: "10%",
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center",
    width: "100%",
    height: "100%",
  },

  actions: {
    width: "90%",
    alignItems: "center",
    justifyContent: "center",
    borderWidth: 0,
    marginTop: "5%",
  },

  inputView: {
    padding: "2%",
    margin: "2%",
    alignItems: "center",
    justifyContent: "center",
    color: "#fff",
    backgroundColor: "#64B5F4",
    borderRadius: 10,
    width: "80%",
    textAlign: I18nManager.isRTL ? "right" : "left",
    writingDirection: I18nManager.isRTL ? "rtl" : "ltr",
  },
  form: {
    width: "90%",
    alignItems: "center",
    justifyContent: "center",
    borderWidth: 0,
  },
  TextInput: {
    height: 50,
    padding: 10,
    marginLeft: 20,
  },
  forgotButton: {
    backgroundColor: "#38052B",
    height: "10%",
    width: "40%",
    marginTop: "30%",
    marginLeft: "5%",
    marginRight: "5%",
    borderRadius: 30,
    alignItems: "center",
    justifyContent: "center",
    marginBottom: "10%",
  },
  forgotText: {
    color: "#fff",
  },
  loginTxt: {
    color: "#fff",
    fontSize: 20,
  },
  loginBtn: {
    borderRadius: 25,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#2B9BED",
    padding: "2%",
    margin: "2%",
    width: "90%",
  },
  Image: {
    resizeMode: "contain",
    width: 200,
    height: 200,
  },
});

export default Signup;
