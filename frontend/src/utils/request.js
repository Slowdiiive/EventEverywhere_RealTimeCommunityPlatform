import axios from "axios";
import router from "@/router";
import { Message, Notification } from "element-ui";
import { getToken, removeToken } from "@/utils/auth";

axios.defaults.headers["Content-Type"] = "application/json;charset=utf-8";

const service = axios.create({
  baseURL: process.env.VUE_APP_BASE_API,
  timeout: 5000,
});

service.interceptors.request.use(
  (config) => {
    const token = getToken();
    if (token) {
      config.headers["Authorization"] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

service.interceptors.response.use(
  (response) => response.data,
  (error) => {
    console.error("API Error:", error);

    if (error.response && error.response.status === 401) {

      if (!error.response.config.url.includes("/login")) {
        removeToken();
        Message({
          message:
            "Your login session has expired or is no longer valid. Please log in again.",
          type: "error",
          duration: 5 * 1000,
        });
        router.push("/login");
      }

    } else if (error.response && error.response.status === 403) {
      Message({
        message: "The current user is not authorized.",
        type: "error",
        duration: 5 * 1000,
      });
      router.push("/");
    } else if (error.response && error.response.status) {
      const message =
        error.response.data.message ||
        error.response.data.msg ||
        error.response.data.error ||
        error.response.statusText ||
        "Unknown error";
      Notification.error({
        title: error.response.status + ": " + message,
      });
    }

    return Promise.reject(error);
  }
);

export default service;
