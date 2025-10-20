<template>
  <div class="login-container">
    <div class="background-image"></div>
    <div class="login-box">
      <h2>Login</h2>
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username">Username</label>
          <input
            type="text"
            id="username"
            v-model="loginForm.username"
            placeholder="Please enter your username"
          />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input
            type="password"
            id="password"
            v-model="loginForm.password"
            placeholder="Please enter your password"
          />
        </div>
        <button type="submit" class="submit-btn" :disabled="loading">
          {{ loading ? "Logging in..." : "Login" }}
        </button>
        <br />
        <div class="register-link">
          Don't have an account?
          <router-link to="/register">Register now</router-link>
        </div>
        <div class="register-link">
          Prefer to skip?
          <router-link to="/event">Browse as a guest.</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { login } from "@/api/user";
import { setToken, checkLoggedIn } from "@/utils/auth";

export default {
  name: "LoginPage",
  data() {
    return {
      loginForm: {
        username: "",
        password: "",
      },
      loading: false,
    };
  },
  created() {
    this.init();
  },
  methods: {
    init() {
      const isLoggedIn = checkLoggedIn();
      if (isLoggedIn) {
        this.$message.info("You are already logged in!");
        this.$router.push("/event");
      }
    },
    handleLogin() {
      if (!this.loginForm.username) {
        this.$message.error("Username cannot be empty!");
        return;
      }
      if (!this.loginForm.password) {
        this.$message.error("Password cannot be empty!");
        return;
      }

      this.loading = true;

      const { username, password } = this.loginForm;
      login({ username, password })
        .then((response) => {
          try {
            const { access_token, token_type } = response;
            if (access_token && token_type === "bearer") {
              setToken(access_token);
              this.$message.success("Login successful!");
              this.loading = false;
              this.$router.push("/event");
            } else {
              throw new Error();
            }
          } catch (error) {
            this.$message.error("Login failed! Invalid token response.");
          }

          this.loading = false;
        })
        .catch((error) => {
          this.loading = false;
          const msg =
            error.response?.data?.detail || error.message || "Unknown error";
          this.$message.error(msg);
        });
    },
  },
};
</script>

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: hidden;
}

.background-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url("../../assets/images/manhattan.jpg");
  background-size: cover;
  background-position: center;
  z-index: 1;
  opacity: 0.9;
  filter: none;
}

.login-box {
  width: 400px;
  padding: 40px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 16px;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  z-index: 2;
  position: relative;
}

.login-box h2 {
  text-align: center;
  margin-bottom: 30px;
  color: #fff;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  color: #fff;
  font-size: 14px;
  font-weight: 500;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.form-group input {
  padding: 12px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  font-size: 14px;
  transition: all 0.3s;
  background-color: rgba(255, 255, 255, 0.2);
  color: #fff;
}

.form-group input::placeholder {
  color: rgba(255, 255, 255, 0.7);
}

.form-group input:focus {
  outline: none;
  border-color: rgba(255, 255, 255, 0.6);
  background-color: rgba(255, 255, 255, 0.25);
  box-shadow: 0 0 10px rgba(64, 158, 255, 0.3);
}

.submit-btn {
  padding: 12px;
  background-color: rgba(64, 158, 255, 0.7);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 500;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.submit-btn:hover {
  background-color: rgba(64, 158, 255, 0.9);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}

.submit-btn:disabled {
  background-color: rgba(160, 207, 255, 0.6);
  cursor: not-allowed;
}

.register-link {
  text-align: center;
  /* margin-top: 20px; */
  color: rgba(255, 255, 255, 0.9);
  font-weight: 400;
}

.register-link a {
  color: #fff;
  text-decoration: none;
  font-weight: 600;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.register-link a:hover {
  color: rgba(102, 177, 255, 1);
  text-decoration: underline;
}
</style>
