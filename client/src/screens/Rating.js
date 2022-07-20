import React, { useContext, useEffect, useState } from "react";
import { StyleSheet, View, Text, FlatList, Alert } from "react-native";
import { AirbnbRating } from "react-native-ratings";
import AppButton from "../components/AppButton";
import { TokenContext } from "../../context";
import { api } from "../api";

const RatingCard = ({ movie, index, ratingCompleted }) => {
  return (
    <View style={styles.item}>
      <Text style={styles.titleText}>{movie.title}</Text>
      <AirbnbRating
        size={25}
        reviewColor="#f7c300"
        selectedColor="#f7c300"
        onFinishRating={(rating) => ratingCompleted(rating, index)}
        reviews={["سئ جدا", "سئ", "كويس", "كويس جدا", "عظيم"]}
      />
    </View>
  );
};

const CustomRating = ({ navigation, route }) => {
  const [movies, setMovies] = useState([]);
  const [token, setToken] = useContext(TokenContext);

  const ratingCompleted = (rating, index) => {
    console.log(rating, index);
    const newMovies = movies.map((movie, idx) => {
      if (index === idx) {
        return {
          ...movie,
          rating: rating,
        };
      }
      return movie;
    });
    setMovies([...newMovies]);
  };
  const renderItem = ({ item }) => (
    <RatingCard
      movie={item}
      ratingCompleted={ratingCompleted}
      index={item.id}
    />
  );

  const submitRating = () => {
    api
      .put("/update_movie_rating", {
        username: token,
        movies: movies.map((movie) => ({
          movie_name: movie.title,
          rating: movie.rating,
        })),
      })
      .then((res) => {
        // console.log(res);
        navigation.navigate("Chat");
      })
      .catch((err) => {
        console.log(err);
        Alert.alert("", "حصل مشكلة 😥", [
          { text: "حاول تاني", onPress: () => console.log("OK Pressed") },
        ]);
      });
  };

  useEffect(() => {
    setMovies(
      route?.params.items?.map((item, idx) => ({
        id: idx,
        title: item,
        rating: 3,
      })) || []
    );
  }, [route.params.items]);

  return (
    <View style={styles.container}>
      <FlatList
        data={movies}
        renderItem={renderItem}
        keyExtractor={(item) => item.id}
        showsVerticalScrollIndicator={false}
      />
      <AppButton
        buttonStyle={styles.loginBtn}
        textStyle={styles.loginTxt}
        onPress={() => submitRating()}
        text="تمام كدا 👍"
      />
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
  baseText: {
    fontFamily: "Cochin",
  },
  titleText: {
    fontSize: 30,
    fontWeight: "bold",
  },
  item: {
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
    padding: "7%",
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
});

export default CustomRating;
