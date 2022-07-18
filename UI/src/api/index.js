import axios from "axios";

const API_URL = "https://6934-197-52-79-189.eu.ngrok.io/";

const headers = {
  Accept: `application/json`,
};

const api = axios.create({
  baseURL: API_URL,
  timeout: 0,
  headers: headers,
});

export { api };
