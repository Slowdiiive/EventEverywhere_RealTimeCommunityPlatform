import request from "@/utils/request";

// create comment
export function createComment(data) {
  return request({
    url: "/comment/",
    method: "post",
    data,
  });
}

// get specific comment
export function getComment(commentId) {
  return request({
    url: `/comment/${commentId}`,
    method: "get",
  });
}

// update comment
export function updateComment(commentId, data) {
  return request({
    url: `/comment/${commentId}`,
    method: "patch",
    data,
  });
}

// delete comment
export function deleteComment(commentId) {
  return request({
    url: `/comment/${commentId}`,
    method: "delete",
  });
}

// get user comments
export function getUserComments(userId) {
  return request({
    url: `/comment/user/${userId}`,
    method: "get",
  });
}
