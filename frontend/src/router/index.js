import Vue from "vue";
import VueRouter from "vue-router";
import Layout from "@/layout";

Vue.use(VueRouter);

const routes = [
  {
    path: "",
    redirect: "home",
  },
  {
    path: "/home",
    name: "home",
    component: (resolve) => require(["@/views/home"], resolve),
  },
  {
    path: "/about",
    name: "about",
    component: (resolve) => require(["@/views/about"], resolve),
  },
  {
    path: "/login",
    name: "login",
    component: (resolve) => require(["@/views/login"], resolve),
  },
  {
    path: "/register",
    name: "register",
    component: (resolve) => require(["@/views/register"], resolve),
  },
  {
    path: "/",
    component: Layout,
    children: [
      
      {
        path: "/event",
        name: "event",
        component: (resolve) => require(["@/views/event"], resolve),
      },
      {
        path: "/event/:id",
        name: "eventDetail",
        component: (resolve) => require(["@/views/event/detail"], resolve),
      },
      
      {
        path: "/user",
        name: "user",
        component: (resolve) => require(["@/views/user"], resolve),
      },
    ],
  },
];

const router = new VueRouter({
  mode: "history",
  routes,
});

export default router;
