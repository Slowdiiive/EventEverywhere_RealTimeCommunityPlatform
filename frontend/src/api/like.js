import request from "@/utils/request";

export function createLike(data) {
  return request({
    url: "/like/",
    method: "post",
    data,
  });
}

export function getLike(likeId) {
  return request({
    url: `/like/${likeId}`,
    method: "get",
  });
}

export function deleteLike(likeId) {
  return request({
    url: `/like/${likeId}`,
    method: "delete",
  });
}

export function getUserLikes(userId) {
  return request({
    url: `/like/user/${userId}`,
    method: "get",
  });
}