import axios from "axios";

const API_URL = "http://cf3e-41-37-144-111.ngrok.io";

const headers = {
  Accept: `application/json`,
};

const api = axios.create({
  baseURL: API_URL,
  timeout: 0,
  headers: headers,
});

export { api };
