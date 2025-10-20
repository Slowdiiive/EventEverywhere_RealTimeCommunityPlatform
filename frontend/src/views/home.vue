<template>
  <div class="home-container">
    <div class="content-section">
      <h1 class="title-line">Event</h1>
      <h1 class="title-line">Every</h1>
      <h1 class="title-line">Where</h1>
      <p class="subtitle">Discover Real-Time The Newest Events in Your City</p>
    </div>
    <div class="button-group">
      <router-link to="/login" class="navi-button" v-if="!isLoggedIn"> Let's Go </router-link>
      <router-link to="/event" class="navi-button" v-if="!isLoggedIn"> Browse First </router-link>
      <router-link to="/event" class="navi-button" v-if="isLoggedIn"> Let's Go </router-link>
    </div>
  </div>
</template>

<script>
import * as MapUtils from "@/utils/map";
import { checkLoggedIn } from "@/utils/auth";

export default {
  name: "HomePage",
  data() {
    return {
      isLoggedIn: true,
    };
  },
  created() {
    this.init();
  },
  mounted() {
    this.preloadUserLocation();
    // console.log("HomePage mounted");
  },
  methods: {
    init() {
      const isLoggedIn = checkLoggedIn();
      this.isLoggedIn = isLoggedIn;
    },
    preloadUserLocation() {
      MapUtils.getUserLocation({
        forceRefresh: true,
        onSuccess: (position) => {
          console.log("User location cached:", position);
        },
        onError: (error) => {
          console.warn("Could not get user location:", error.message);
        },
      });
    },
  },
};
</script>

<style scoped>
.home-container {
  height: 100vh;
  width: 100%;
  margin: 0;
  padding: 0 10%;
  overflow: hidden;
  background: url("../assets/images/new-york-nightview.jpg") no-repeat center
    center;
  background-size: cover;
  display: flex;
  position: relative;
  box-sizing: border-box;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

body,
html {
  margin: 0;
  padding: 0;
  overflow: hidden;
}

.content-section {
  color: #c0c0c0;
  max-width: 600px;
  width: 100%;
  position: relative;
  z-index: 2;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  text-align: left;
  align-self: flex-start;
}

.title-line {
  font-family: "Arial Rounded MT Bold", "Arial", sans-serif;
  color: #ffffff;
  font-size: 6vw;
  font-weight: 790;
  margin: 0;
  line-height: 1.2;
  letter-spacing: 2px;
  margin-top: -5px;
  animation: fadeIn 1s ease-out;
  align-self: flex-start;
  width: 100%;
  text-align: left;
}

.title-line:first-child {
  font-size: 12vw;
  margin-bottom: -0.1em !important;
  text-shadow: 6px 6px 10px rgba(0, 0, 0, 0.5);
}

.title-line:nth-child(3) {
  font-family: "Arial Rounded MT Bold", "Hiragino Maru Gothic Pro",
    "Segoe UI Emoji", sans-serif;
  letter-spacing: 1.5px;
}

.subtitle {
  font-size: 1.7vw;
  font-weight: 300;
  margin-top: 30px;
  letter-spacing: 1px;
  animation: fadeIn 1.5s ease-out;
  font-family: "Times New Roman", Times, serif;
  font-style: italic;
  display: inline-block;
  text-align: left;
  align-self: flex-start;
}

.button-group {
  display: flex;
  gap: 10vh;
  align-items: center;
  z-index: 2;
}

.navi-button {
  display: inline-block;
  margin-top: 30px;
  padding: 12px 30px;
  background-color: #7235ff;
  color: #ffffff;
  border: 2px solid #7235ff;
  border-radius: 30px;
  font-family: "Arial Narrow", sans-serif;
  font-size: 1rem;
  text-decoration: none;
  text-transform: uppercase;
  letter-spacing: 1px;
  transition: all 0.3s ease;
  cursor: pointer;
  animation: fadeIn 1.8s ease-out;
  font-weight: 700;
  letter-spacing: 1.5px;
  border-width: 3px;
  align-self: flex-end;
}

.navi-button:hover {
  background-color: #ffffff;
  color: #7235ff;
  border-color: #ffffff;
  transform: translateY(-2px);
}

.home-container::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    135deg,
    rgba(67, 43, 187, 0.866) 15%,
    rgba(141, 68, 173, 0.075) 70%
  );
  z-index: 1;
  animation: gradientShift 8s ease infinite;
}

@keyframes gradientShift {
  0% {
    opacity: 0.8;
  }
  50% {
    opacity: 0.6;
  }
  100% {
    opacity: 0.8;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
