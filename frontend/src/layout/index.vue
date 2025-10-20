<template>
  <div class="menu-wrapper">
    <link
      rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css"
      integrity="sha512-DTOQO9RWCH3ppGqcWaEA1BIZOC6xxalwEsw9c2QQeAIftl+Vegovlnee1c9QX4TctnWMn13TZye+giMm8e2LwA=="
      crossorigin="anonymous"
      referrerpolicy="no-referrer"
    />
    <div class="floating-menu">
      <nav class="menu-container">
        <div class="menu">
          <div :class="['nav-group', 'center-nav', { 'nav-group-dark': isUserPage }]">
            <router-link :class="['nav-item', { 'nav-item-dark': isUserPage }]" to="/home">
              <span class="nav-text">Home</span>
            </router-link>
            <router-link :class="['nav-item', { 'nav-item-dark': isUserPage }]" to="/event">
              <span class="nav-text">Event Map</span>
            </router-link>
            <router-link :class="['nav-item', { 'nav-item-dark': isUserPage }]" to="/about">
              <span class="nav-text">About</span>
            </router-link>
          </div>

          <div :class="['login-area', { 'login-area-dark': isUserPage }]">
            <button v-if="!isLoggedIn" class="btn btn-login" @click="goToLogin">
              <i class="fas fa-key"></i>
              Log in
            </button>
            <button v-if="isLoggedIn" :class="['btn', 'btn-profile', { 'btn-profile-dark': isUserPage }]" @click="goToUser">
              <i class="fas fa-user"></i>
              My Profile
            </button>
            <button v-if="isLoggedIn" :class="['btn', 'btn-logout', { 'btn-logout-dark': isUserPage }]" @click="showLogoutConfirm">
              <i class="fas fa-sign-out-alt"></i>
              Log out
            </button>
          </div>
        </div>
      </nav>
    </div>
    <router-view />

    <!-- Logout Confirmation Dialog -->
    <el-dialog
      title="Confirm Logout"
      :visible.sync="logoutDialogVisible"
      width="400px"
      custom-class="logout-dialog"
    >
      <p>Are you sure you want to log out?</p>
      <span slot="footer" class="dialog-footer">
        <el-button @click="logoutDialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="confirmLogout">Confirm</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { checkLoggedIn, removeToken } from "@/utils/auth";

export default {
  name: "MenuLayout",
  data() {
    return {
      isLoggedIn: true,
      logoutDialogVisible: false,
    };
  },
  computed: {
    isUserPage() {
      return this.$route.path === '/user';
    }
  },
  created() {
    this.init();
  },
  watch: {
    $route() {
      this.init();
    },
  },
  methods: {
    init() {
      const isLoggedIn = checkLoggedIn();
      this.isLoggedIn = isLoggedIn;
    },
    goToLogin() {
      this.$router.push("/login");
    },
    goToUser() {
      this.$router.push("/user").catch((err) => {
        if (err.name !== "NavigationDuplicated") {
          throw err;
        }
      });
    },
    showLogoutConfirm() {
      this.logoutDialogVisible = true;
    },
    confirmLogout() {
      removeToken();
      this.$message.success("Logged out successfully");
      this.logoutDialogVisible = false;
      this.$router.push("/home");
    },
  },
};
</script>

<style scoped>
.menu-wrapper {
  text-align: center;
  position: relative;
  width: 100%;
  height: 100vh;
}

.floating-menu {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
  pointer-events: none;
  padding: 15px 0;
}

.menu-container {
  position: relative;
  width: 100%;
  padding: 10px 20px;
  box-sizing: border-box;
  pointer-events: none;
}

.menu {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  height: 60px;
  border: none;
  pointer-events: auto;
}

.nav-group {
  display: inline-flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 0 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.2);
  pointer-events: auto;
  transition: all 0.3s ease;
}

.center-nav {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1;
  padding: 0;
  overflow: hidden;
}

.nav-item {
  height: 50px;
  line-height: 50px;
  padding: 0 20px;
  color: #333;
  text-decoration: none;
  transition: all 0.3s ease;
  border-radius: 12px;
  margin: 0 2px;
  position: relative;
  overflow: hidden;
}

.nav-item:hover {
  background-color: rgba(255, 255, 255, 0.25);
  color: #333;
  transform: translateY(-2px);
}

.nav-item.active {
  background-color: rgba(64, 158, 255, 0.2);
  color: #333;
  font-weight: 600;
  box-shadow: 0 4px 15px rgba(64, 158, 255, 0.15);
  transform: translateY(-2px);
}

.nav-text {
  position: relative;
  font-weight: 500;
  transition: all 0.3s ease;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.active .nav-text {
  font-weight: 600;
  letter-spacing: 0.3px;
}

.login-area {
  position: absolute;
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 5px 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.btn {
  position: relative;
  height: 40px;
  padding: 0 16px;
  font-size: 14px;
  font-weight: 500;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
  background: transparent;
  backdrop-filter: none;
  -webkit-backdrop-filter: none;
}

.btn::before {
  display: none;
}

.btn:hover {
  transform: translateY(0);
  background: rgba(255, 255, 255, 0.1);
}

.btn:active {
  transform: scale(0.98);
}

.btn-login {
  color: #409eff;
  text-shadow: 0 1px 1px rgba(255, 255, 255, 0.5);
  box-shadow: none;
}

.btn-login:hover {
  background: rgba(64, 158, 255, 0.15);
  box-shadow: none;
}

.btn-profile {
  color: #e6a23c;
  text-shadow: 0 1px 1px rgba(255, 255, 255, 0.5);
  box-shadow: none;
}

.btn-profile:hover {
  background: rgba(230, 162, 60, 0.15);
  box-shadow: none;
}

.btn-logout {
  color: #f56c6c;
  text-shadow: 0 1px 1px rgba(255, 255, 255, 0.5);
  box-shadow: none;
}

.btn-logout:hover {
  background: rgba(245, 108, 108, 0.15);
  box-shadow: none;
}

/* Remove custom icon styles */
.icon-key::before,
.icon-user::before,
.icon-logout::before {
  display: none;
}

@media (max-width: 768px) {
  .nav-group {
    padding: 0 10px;
  }

  .nav-item {
    padding: 0 15px;
  }

  .btn {
    padding: 8px 12px;
    font-size: 13px;
  }

  .login-area {
    right: 10px;
  }
}

/* Dark theme styles for user page */
.nav-group-dark {
  background: rgba(0, 0, 0, 0.4) !important;
  border: 1px solid rgba(255, 255, 255, 0.3) !important;
}

.nav-item-dark {
  color: white !important;
}

.nav-item-dark:hover {
  background-color: rgba(255, 255, 255, 0.15) !important;
  color: white !important;
}

.nav-item-dark.active {
  background-color: rgba(255, 255, 255, 0.2) !important;
  color: white !important;
}

.login-area-dark {
  background: rgba(0, 0, 0, 0.4) !important;
  border: 1px solid rgba(255, 255, 255, 0.3) !important;
}

.btn-profile-dark {
  color: #ffd591 !important;
  text-shadow: 0 1px 1px rgba(0, 0, 0, 0.5) !important;
}

.btn-profile-dark:hover {
  background: rgba(255, 213, 145, 0.15) !important;
}

.btn-logout-dark {
  color: #ffa39e !important;
  text-shadow: 0 1px 1px rgba(0, 0, 0, 0.5) !important;
}

.btn-logout-dark:hover {
  background: rgba(255, 163, 158, 0.15) !important;
}

/* Dialog styles */
:deep(.logout-dialog) {
  background: rgba(255, 255, 255, 0.2) !important;
  backdrop-filter: blur(10px) !important;
  -webkit-backdrop-filter: blur(10px) !important;
  border-radius: 16px !important;
  border: 1px solid rgba(255, 255, 255, 0.3) !important;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1) !important;
  overflow: hidden !important;
}

:deep(.logout-dialog .el-dialog__header) {
  padding: 20px !important;
  background: rgba(255, 255, 255, 0.1) !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

:deep(.logout-dialog .el-dialog__title) {
  color: #333 !important;
  font-weight: 500 !important;
  font-size: 18px !important;
}

:deep(.logout-dialog .el-dialog__body) {
  padding: 20px !important;
  background: rgba(255, 255, 255, 0.1) !important;
  color: #333 !important;
}

:deep(.logout-dialog .el-dialog__footer) {
  padding: 15px 20px !important;
  background: rgba(255, 255, 255, 0.1) !important;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
}

/* Dialog buttons */
:deep(.logout-dialog .el-dialog__footer .el-button) {
  height: 40px;
  padding: 0 20px;
  border-radius: 12px;
  font-weight: 500;
  transition: all 0.3s ease;
}

:deep(.logout-dialog .el-dialog__footer .el-button--default) {
  background: rgba(144, 147, 153, 0.15);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: #606266;
}

:deep(.logout-dialog .el-dialog__footer .el-button--default:hover) {
  background: rgba(144, 147, 153, 0.25);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

:deep(.logout-dialog .el-dialog__footer .el-button--primary) {
  background: rgba(64, 158, 255, 0.15);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: #409eff;
}

:deep(.logout-dialog .el-dialog__footer .el-button--primary:hover) {
  background: rgba(64, 158, 255, 0.25);
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(64, 158, 255, 0.15);
}

/* Global modal backdrop style */
:deep(.v-modal) {
  background: rgba(0, 0, 0, 0.2) !important;
  backdrop-filter: blur(10px) !important;
  -webkit-backdrop-filter: blur(10px) !important;
  opacity: 1 !important;
}

/* Override Element UI's default modal styles */
:root {
  --el-dialog-modal-color: rgba(0, 0, 0, 0.2) !important;
}

/* Additional override for Element UI v2 */
.v-modal {
  background: rgba(0, 0, 0, 0.2) !important;
  backdrop-filter: blur(10px) !important;
  -webkit-backdrop-filter: blur(10px) !important;
  opacity: 1 !important;
}

/* Ensure modal backdrop is properly styled even after page refresh */
body > .v-modal {
  background: rgba(0, 0, 0, 0.2) !important;
  backdrop-filter: blur(10px) !important;
  -webkit-backdrop-filter: blur(10px) !important;
  opacity: 1 !important;
}
</style>
