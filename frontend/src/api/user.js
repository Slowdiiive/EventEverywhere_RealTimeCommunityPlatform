import request from "@/utils/request";
import qs from "qs"

export function login(data) {
  return request({
    url: "/user/login",
    method: "post",
    data: qs.stringify(data),
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  });
}

export function register(data) {
  return request({
    url: "/user/",
    method: "post",
    data,
  });
}

export function getUser(userId) {
  return request({
    url: `/user/${userId}`,
    method: "get",
  });
}

export function updateUser(userId, data) {
  return request({
    url: `/user/${userId}`,
    method: "patch",
    data,
  });
}

export function deleteUser(userId) {
  return request({
    url: `/user/${userId}`,
    method: "delete",
  });
}

export function updateUserPassword(userId, passwordData) {
  return request({
    url: `/user/${userId}/password`,
    method: "post",
    data: passwordData
  });
}
