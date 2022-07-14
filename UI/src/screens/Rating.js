import React, { useEffect, useState } from "react";
import { Button, StyleSheet, View } from "react-native";

const Rating = ({ navigation }) => {
  return (
    <View style={styles.container}>
      <Button title="Notify" />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center",
    paddingLeft: 10,
    paddingRight: 10,
  },
});

export default Rating;
