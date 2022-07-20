import React, { useEffect, useContext } from "react";
import { TokenContext, TokenProvider } from "./context";
import { createStackNavigator } from "@react-navigation/stack";
import { NavigationContainer } from "@react-navigation/native";
import * as SecureStore from "expo-secure-store";
import Chat from "./src/screens/Chat";
import Login from "./src/screens/Login";
import Signup from "./src/screens/Signup";

import { I18nManager } from "react-native";
import Rating from "./src/screens/Rating";

const Stack = createStackNavigator();

const getSecureItem = async (key) =>
  (await SecureStore.getItemAsync(key)) || "";

const Screens = () => {
  const [token, setToken] = useContext(TokenContext);

  useEffect(async () => {
    const username = await getSecureItem("username");
    setToken(username);

    I18nManager.forceRTL(true);
    I18nManager.allowRTL(true);
  }, []);

  return (
    <NavigationContainer>
      <Stack.Navigator>
        {token == "" ? (
          <>
            <Stack.Screen
              name="Login"
              component={Login}
              options={{
                title: "تسجيل الدخول",
              }}
            />
            <Stack.Screen
              name="Signup"
              component={Signup}
              options={{
                title: "تسجيل مستخدم جديد",
              }}
            />
          </>
        ) : (
          <>
            <Stack.Screen
              name="Chat"
              component={Chat}
              options={{
                title: "اتكلم مع انيس",
              }}
            />
            <Stack.Screen
              name="Rating"
              component={Rating}
              options={{
                title: "تقييم الافلام",
              }}
            />
          </>
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
};

const App = () => {
  return (
    <TokenProvider>
      <Screens />
    </TokenProvider>
  );
};

export default App;
