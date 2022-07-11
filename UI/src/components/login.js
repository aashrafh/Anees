import { StatusBar } from "expo-status-bar";
import React, { Component } from "react";
import {
  StyleSheet,
  View,
  Text,
  TextInput,
  Image
} from "react-native";
import AppButton from './AppButton';
class Login extends Component {
  state = {
    email: '',
    password: ''
  }
  handleEmail = (text) => {
    this.setState({ email: text })
  }
  handlePassword = (text) => {
    this.setState({ password: text })
  }
  login = (email, pass) => {
    alert('email: ' + email + ' password: ' + pass)
  }
  render() {
    return (
      <View style={styles.container}>
        <Text style={styles.header}>تسجيل الدخول</Text>
        <Image source={require('../../Images/Anees.png')} style={styles.Image} />

        <View style={styles.form}>
          <TextInput
            style={styles.inputView}
            placeholder="ُEmail"
            placeholderTextColor="white"
            onChangeText={this.handleEmail}
          />
          <TextInput
            style={styles.inputView}
            placeholder="Password"
            placeholderTextColor="white"
            secureTextEntry={true}
            onChangeText={this.handlePassword}
          />
        </View>

        <AppButton buttonStyle={styles.loginBtn} textStyle={styles.loginTxt} text="ادخل" />

        <View style={{ flexDirection: "row" }}>
          <AppButton buttonStyle={styles.forgotButton} textStyle={styles.forgotText} text="نسيت الباسوورد ؟" />
          <AppButton buttonStyle={styles.forgotButton} textStyle={styles.forgotText} text="سجل ايميل جديد" />
        </View>

      </View>
    );
  }
}

export default Login;
const styles = StyleSheet.create({
  header: {
    fontSize: 50,
    marginBottom: "5%",
    fontWeight: "bold",
    color: 'purple',
    marginTop: '10%'
  },
  container: {
    paddingTop: "10%",
    backgroundColor: "#FFFDE7",
    alignItems: "center",
    justifyContent: "center",
    width: '100%',
    height: '100%'
  },

  inputView: {
    padding: "2%",
    backgroundColor: "#38052B",
    borderRadius: 10,
    width: "80%",
    height: "25%",
    marginTop: "5%",
    marginBottom: "5%",
    alignItems: "center",
    justifyContent: "center",
  },
  form: {
    height: '30%',
    width: '90%',
    borderColor: '#29B6F6',
    borderRadius: 20,
    borderStyle: 'solid',
    backgroundColor: "#FFF9C4",
    alignItems: "center",
    justifyContent: "center",
    borderWidth: 1,
  },
  TextInput: {
    height: 50,
    padding: 10,
    marginLeft: 20,
  },

  forgotButton: {
    backgroundColor: '#38052B',
    height: "10%",
    width: "40%",
    marginTop: "30%",
    marginLeft: "5%",
    marginRight: "5%",
    borderRadius: 30,
    alignItems: "center",
    justifyContent: "center",
    marginBottom: '10%'
  },
  forgotText: {
    color: "#fff"
  }
  ,
  loginTxt: {
    color: "#fff",
    fontSize: 20
  }
  ,
  loginBtn: {
    width: "60%",
    borderRadius: 25,
    height: 50,
    alignItems: "center",
    justifyContent: "center",
    marginTop: 20,
    backgroundColor: "#38052B",
    height: '5%',
    width: '50%'
  },
  Image: {
    resizeMode: 'contain',
    width: 200,
    height: 200,
  }
});