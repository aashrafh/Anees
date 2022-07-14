import React, { useState } from "react";

const TokenContext = React.createContext("token");

const TokenProvider = ({ children }) => {
  const [token, setToken] = useState("");

  return (
    <TokenContext.Provider value={[token, setToken]}>
      {children}
    </TokenContext.Provider>
  );
};

const TokenConsumer = TokenContext.Consumer;

export { TokenContext, TokenProvider, TokenConsumer };
