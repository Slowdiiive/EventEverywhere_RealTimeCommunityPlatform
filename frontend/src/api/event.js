import request from "@/utils/request";

// Create a new event
export function createEvent(data) {
  return request({
    url: "/event/",
    method: "post",
    data,
  });
}

// Get event list (Map Page)
export function listEvent(params) {
  return request({
    url: "/event",
    method: "get",
    params,
  });
}

// Get event categories
export function getCategories() {
  return request({
    url: "/event/categories",
    method: "get",
  });
}

// Get event details
export function getEvent(eventId) {
  return request({
    url: `/event/${eventId}`,
    method: "get",
  });
}

// update event
export function updateEvent(eventId, data) {
  return request({
    url: `/event/${eventId}`,
    method: "patch",
    data,
  });
}

// delete event
export function deleteEvent(eventId) {
  return request({
    url: `/event/${eventId}`,
    method: "delete",
  });
}

// get user events
export function getUserEvents(userId) {
  return request({
    url: `/event/user/${userId}`,
    method: "get",
  });
}
