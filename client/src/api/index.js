import axios from "axios";

const API_URL = "http://127.0.0.1:5000";

const headers = {
  Accept: `application/json`,
};

const api = axios.create({
  baseURL: API_URL,
  timeout: 0,
  headers: headers,
});

export { api };
