import React, { useContext } from "react";
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
import * as SecureStore from "expo-secure-store";
import { TokenContext } from "../../context";

const Login = ({ navigation }) => {
  const [username, setUsername] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [token, setToken] = useContext(TokenContext);

  const handleUsername = (text) => {
    setUsername(text);
  };
  const handlePassword = (text) => {
    setPassword(text);
  };
  const handleLogin = () => {
    api
      .post("/login", { username, password })
      .then(async (res) => {
        console.log(res.data);
        await SecureStore.setItemAsync("username", username);
        setToken(username);
      })
      .catch((err) => {
        console.log(err.response);
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
          onPress={() => handleLogin()}
          text="يلا نتكلم"
        />

        <AppButton
          buttonStyle={styles.loginBtn}
          textStyle={styles.loginTxt}
          onPress={() => navigation.navigate("Signup")}
          text="لسة جديد؟ اعمل اكونت دلوقتي!"
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

export default Login;
