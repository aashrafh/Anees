import axios from "axios";

const API_URL = "https://714c-41-37-144-111.eu.ngrok.io/";

const headers = {
  Accept: `application/json`,
};

const api = axios.create({
  baseURL: API_URL,
  timeout: 0,
  headers: headers,
});

export { api };
