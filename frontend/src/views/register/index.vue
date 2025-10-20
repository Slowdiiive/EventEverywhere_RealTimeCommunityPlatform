<template>
  <div class="register-container">
    <div class="background-image"></div>
    <div class="register-box">
      <h2>Register</h2>
      <form @submit.prevent="handleRegister" class="register-form">
        <div class="form-group">
          <label for="username">Username</label>
          <input type="text" id="username" v-model="registerForm.username" required minlength="3" maxlength="20"
            placeholder="Please enter your username" />
        </div>
        <div class="form-group">
          <label for="name">name</label>
          <input type="name" id="name" v-model="registerForm.name" required placeholder="Please enter your name" />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" id="password" v-model="registerForm.password" required minlength="6"
            placeholder="Please enter your password" />
        </div>
        <div class="form-group">
          <label for="confirmPassword">Confirm Password</label>
          <input type="password" id="confirmPassword" v-model="registerForm.confirmPassword" required
            placeholder="Please confirm your password" />
        </div>
        <button type="submit" class="submit-btn" :disabled="loading">
          {{ loading ? "Registering..." : "Register" }}
        </button>
        <br />
        <div class="login-link">
          Already have an account?
          <router-link to="/login">Login now</router-link>
        </div>
        <div class="login-link">
          Prefer to skip?
          <router-link to="/event">Browse as a guest.</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { register } from "@/api/user";
import { checkLoggedIn } from "@/utils/auth";

export default {
  name: "RegisterPage",
  data() {
    return {
      registerForm: {
        username: "",
        name: "",
        password: "",
        confirmPassword: "",
      },
      loading: false,
    };
  },
  created() {
    this.init();
  },
  watch: {
    "registerForm.password": function (newPassword) {
      this.validatePassword(newPassword, this.registerForm.confirmPassword);
    },
    "registerForm.confirmPassword": function (newConfirmPassword) {
      this.validatePassword(this.registerForm.password, newConfirmPassword);
    },
  },
  methods: {
    init() {
      const isLoggedIn = checkLoggedIn();
      if (isLoggedIn) {
        this.$message.info("You are already logged in!");
        this.$router.push("/event");
      }
    },
    validatePassword(password, confirmPassword) {
      if (password && confirmPassword && password !== confirmPassword) {
        document
          .getElementById("confirmPassword")
          .setCustomValidity("Passwords do not match");
      } else {
        document.getElementById("confirmPassword").setCustomValidity("");
      }
    },
    async handleRegister() {
      this.loading = true;
      try {
        const response = await register(this.registerForm);

        if (response) {
          this.$message.success("Registration successful");
          this.$router.push("/login");
        } else {
          throw new Error('Unexpected status code: ' + response.status);
        }
      } catch (error) {
        console.error(error);
        const message =
          error.response?.data?.detail || error.message || "Unknown error";
        this.$message.error(message);
      } finally {
        this.loading = false;
      }



    },
  },
};
</script>

<style scoped>
.register-container {
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

.register-box {
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

.register-box h2 {
  text-align: center;
  margin-bottom: 30px;
  color: #fff;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.register-form {
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

.login-link {
  text-align: center;
  /* margin-top: 20px; */
  color: rgba(255, 255, 255, 0.9);
  font-weight: 400;
}

.login-link a {
  color: #fff;
  text-decoration: none;
  font-weight: 600;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.login-link a:hover {
  color: rgba(102, 177, 255, 1);
  text-decoration: underline;
}
</style>