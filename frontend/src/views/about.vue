<template>
  <div class="about-page" @click="goBack">
    <div class="background-image"></div>
    <div class="gradient-overlay"></div>

    <div class="content-container">
      <h1 class="title">About Us</h1>
      <div class="description-box">
        <div class="description">
          <p class="paragraph">
            Event Everywhere is a dynamic web-based platform designed to keep
            communities connected and informed about what's happening around
            them.
          </p>

          <div class="features-section">
            <p class="features-intro">With Event Everywhere, you can:</p>
            <ul class="features-list">
              <li class="feature-item">
                Report incidents instantly - Share what's happening near you in
                real time.
              </li>
              <li class="feature-item">
                Stay informed - Browse the latest events and updates in your
                neighborhood.
              </li>
              <li class="feature-item">
                Engage with your community - Join discussions and collaborate
                with others.
              </li>
            </ul>
          </div>

          <p class="paragraph">
            We bring you the freshest, most relevant local events, ensuring
            you're always in the know. Discover what's trending in your city and
            never miss a beat with Event Everywhere!
          </p>

          <p class="closing">Have fun with us!</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "AboutPage",
  methods: {
    goBack() {
      this.$router.go(-1);
    }
  }
};
</script>

<style scoped>
.about-page {
  position: relative;
  height: 100vh;
  width: 100%;
  overflow: hidden;
  margin-top: 0;
}

.background-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url("../assets/images/new-york-nightview.jpg");
  background-size: cover;
  background-position: center;
  z-index: 1;
}

.content-container {
  position: relative;
  z-index: 3;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  padding: 20px;
  width: 100%;
  box-sizing: border-box;
  overflow-y: auto;
}

.title {
  font-size: 4rem;
  font-weight: 400;
  color: white;
  font-family: "Times New Roman", Times, serif;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
  margin-bottom: 1.5rem;
  text-align: center;
}

.description-box {
  background: rgba(255, 255, 255, 0.25);
  border-radius: 16px;
  padding: 40px;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(1px);
  -webkit-backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  max-width: 787px;
  width: 100%;
  box-sizing: border-box;
}

.description {
  text-align: left;
  color: white;
  font-size: 1.25rem;
}

.paragraph {
  margin-bottom: 1.1rem;
  line-height: 1.6;
}

.features-section {
  margin: 1.1rem 0;
}

.features-intro {
  margin-bottom: 0.6rem;
  font-weight: bold;
  font-size: 1.25rem;
}

.features-list {
  padding-left: 1.1rem;
  margin-bottom: 1.1rem;
}

.feature-item {
  margin-bottom: 0.4rem;
  line-height: 1.5;
  font-size: 1.10rem;
}

.closing {
  font-style: italic;
  margin-top: 0.75rem;
  font-size: 1.10rem;
}

.gradient-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    135deg,
    rgba(43, 79, 187, 0.394) 0%,
    rgba(141, 68, 173, 0.195) 40%,
    rgba(43, 79, 187, 0.188) 100%
  );
  background-size: 200% 200%;
  z-index: 2;
  animation: gradientShift 10s ease infinite;
  pointer-events: none;
}

@keyframes gradientShift {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}
</style>
