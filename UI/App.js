import React from "react";

import { createStackNavigator } from "@react-navigation/stack";
import { NavigationContainer } from "@react-navigation/native";
import Chat from "./src/screens/Chat";
import Login from "./src/screens/Login";
import Signup from "./src/screens/Signup";

const Stack = createStackNavigator();

const App = () => {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        {/* <Stack.Screen
          name="Login"
          component={Login}
          options={{
            title: "تسجيل الدخول",
          }}
        /> */}
        {/* <Stack.Screen
          name="Signup"
          component={Signup}
          options={{
            title: "تسجيل مستخدم جديد",
          }}
        /> */}
        <Stack.Screen
          name="Chat"
          component={Chat}
          options={{
            title: "اتكلم مع انيسsdfsfdsfds",
          }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default App;
