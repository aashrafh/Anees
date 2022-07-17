import axios from "axios";

const API_URL = "https://83db-102-44-194-191.eu.ngrok.io/";

const headers = {
  Accept: `application/json`,
};

const api = axios.create({
  baseURL: API_URL,
  timeout: 0,
  headers: headers,
});

export { api };
