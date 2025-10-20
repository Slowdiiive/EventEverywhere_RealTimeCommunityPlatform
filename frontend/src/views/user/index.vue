<template>
  <div class="user-container">
    <div class="background-overlay"></div>
    <div v-if="!isEditing" class="profile-display">
      <div class="profile-header">
        <h1 class="profile-name">{{ userInfo?.name || 'Loading...' }}</h1>
        <p class="profile-username">@{{ userInfo?.username }}</p>
      </div>

      <div class="profile-content">
        <div class="info-card">
          <div class="info-section">
            <h3><i class="el-icon-user"></i> About Me</h3>
            <p>{{ userInfo?.content || 'No content available' }}</p>
          </div>

          <!-- <div class="info-section">
            <h3><i class="el-icon-info"></i> User Details</h3>
            <ul class="info-list">
              <li>
                <span class="info-label">User ID:</span>
                <span class="info-value">#{{ userInfo?.id }}</span>
              </li>
              <li>
                <span class="info-label">Username:</span>
                <span class="info-value">{{ userInfo?.username }}</span>
              </li>
              <li>
                <span class="info-label">Name:</span>
                <span class="info-value">{{ userInfo?.name }}</span>
              </li>
            </ul>
          </div> -->

          <el-button 
            type="primary" 
            class="edit-button"
            @click="startEditing"
            icon="el-icon-edit"
          >
            Edit Profile
          </el-button>
        </div>
      </div>
    </div>

    <!-- Edit Form Section -->
    <el-card v-else class="edit-form-card">
      <div class="edit-header">
        <h2>Edit Profile</h2>
        <el-button icon="el-icon-back" @click="cancelEditing">Back to Profile</el-button>
      </div>

      <el-tabs type="border-card">
        <el-tab-pane label="Profile Information">
          <el-form v-if="userInfo" :model="userInfo" label-width="120px" class="user-form">
            <el-form-item label="Username">
              <el-input v-model="userInfo.username"></el-input>
            </el-form-item>
            
            <el-form-item label="Name">
              <el-input v-model="userInfo.name"></el-input>
            </el-form-item>

            <el-form-item label="About Me">
              <el-input
                type="textarea"
                v-model="userInfo.content"
                :rows="4"
              ></el-input>
            </el-form-item>

            <el-form-item>
              <el-button type="success" @click="saveChanges" :loading="loading">
                Save Changes
              </el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <el-tab-pane label="Change Password">
          <el-form :model="passwordForm" label-width="140px" class="password-form">
            <el-form-item label="Current Password">
              <el-input 
                v-model="passwordForm.currentPassword" 
                type="password"
                show-password
              ></el-input>
            </el-form-item>
            
            <el-form-item label="New Password">
              <el-input 
                v-model="passwordForm.newPassword" 
                type="password"
                show-password
              ></el-input>
            </el-form-item>
            
            <el-form-item label="Confirm Password">
              <el-input 
                v-model="passwordForm.confirmPassword" 
                type="password"
                show-password
              ></el-input>
            </el-form-item>

            <el-form-item>
              <el-button 
                type="primary" 
                @click="changePassword"
                :loading="passwordLoading"
              >
                Change Password
              </el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script>
import { getUser, updateUser, updateUserPassword } from '@/api/user';
import { getUserId } from "@/utils/auth";

export default {
  name: "UserPage",
  data() {
    return {
      userInfo: null,
      isEditing: false,
      loading: false,
      passwordLoading: false,
      originalUserInfo: null,
      passwordForm: {
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      },
      loggedUserId: null,
    };
  },
  created() {
    this.init();
  },
  methods: {
    init() {
      const loggedUserId = getUserId();
      if (!loggedUserId) {
        this.$message.error("You have not logged in!");
        this.$router.push("/login");
      }
      else {
        this.loggedUserId = loggedUserId;
      }

      this.fetchUserInfo();
    },
    async fetchUserInfo() {
      try {
        // Try to get user info from backend
        const userId = this.loggedUserId;
        const response = await getUser(userId);
        this.userInfo = response;
      } catch (error) {
        console.error('Failed to fetch user info:', error);
        // Use mock data if API fails
        this.userInfo = {
          username: "jiaojh",
          name: "JoJo",
          content: "I have an super-power that I am RICH!",
          id: 11
        };
      }
      // Store original data for cancellation
      this.originalUserInfo = JSON.parse(JSON.stringify(this.userInfo));
    },
    startEditing() {
      this.isEditing = true;
    },
    cancelEditing() {
      this.userInfo = JSON.parse(JSON.stringify(this.originalUserInfo));
      this.isEditing = false;
    },
    async saveChanges() {
      try {
        this.loading = true;
        await updateUser(this.userInfo.id, this.userInfo);
        this.originalUserInfo = JSON.parse(JSON.stringify(this.userInfo));
        this.isEditing = false;
        this.$message.success('User information updated successfully');
      } catch (error) {
        this.$message.error('Failed to update user information');
        console.error('Update error:', error);
      } finally {
        this.loading = false;
      }
    },
    async changePassword() {
      if (!this.validatePasswordForm()) {
        return;
      }

      try {
        this.passwordLoading = true;
        
        const response = await updateUserPassword(this.userInfo.id, {
          currentPassword: this.passwordForm.currentPassword,
          newPassword: this.passwordForm.newPassword
        });
        
        if (response.success) {
          this.$message.success(response.message);
          this.resetPasswordForm();
        } else {
          this.$message.error(response.message);
        }
      } catch (error) {
        this.$message.error('Failed to change password');
      } finally {
        this.passwordLoading = false;
      }
    },
    validatePasswordForm() {
      if (!this.passwordForm.currentPassword) {
        this.$message.warning('Please enter your current password');
        return false;
      }
      if (!this.passwordForm.newPassword) {
        this.$message.warning('Please enter a new password');
        return false;
      }
      if (this.passwordForm.newPassword !== this.passwordForm.confirmPassword) {
        this.$message.warning('New passwords do not match');
        return false;
      }
      return true;
    },
    resetPasswordForm() {
      this.passwordForm = {
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      };
    }
  }
};
</script>

<style scoped>
.user-container {
  position: relative;
  min-height: 100vh;
  background-image: url('https://images.unsplash.com/photo-1503179008861-d1e2b41f8bec?q=80&w=3869&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  padding: 80px 20px 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
}

.background-overlay {
  display: none;
}

.profile-display,
.edit-form-card {
  position: relative;
  z-index: 2;
  width: 100%;
  max-width: 800px;
}

.profile-header {
  text-align: center;
  color: white;
  margin-bottom: 40px;
  position: relative;
  padding: 30px;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  transform: translateY(0);
  transition: all 0.3s ease;
}

.profile-header:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.25);
}

.profile-name {
  font-size: 2.8em;
  margin: 10px 0;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
  background: linear-gradient(135deg, #ffffff, #e0e0e0);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 700;
  letter-spacing: 1px;
}

.profile-username {
  font-size: 1.3em;
  color: rgba(255, 255, 255, 0.9);
  margin: 10px 0;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
  letter-spacing: 1px;
}

.profile-content {
  max-width: 800px;
  margin: 0 auto;
  position: relative;
}

.info-card {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.info-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.25);
}

.info-section {
  margin-bottom: 30px;
  color: white;
}

.info-section h3 {
  color: white;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 1.4em;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

.info-section i {
  color: #409EFF;
  font-size: 1.2em;
  text-shadow: 0 0 10px rgba(64, 158, 255, 0.5);
}

.info-section p {
  line-height: 1.6;
  font-size: 1.1em;
  color: rgba(255, 255, 255, 0.95);
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}

.edit-button {
  width: 100%;
  margin-top: 30px;
  height: 48px;
  font-size: 16px;
  background: rgba(64, 158, 255, 0.2);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  border-radius: 12px;
  transition: all 0.3s ease;
  font-weight: 500;
  letter-spacing: 0.5px;
}

.edit-button:hover {
  background: rgba(64, 158, 255, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(64, 158, 255, 0.3);
}

.edit-form-card {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  padding: 30px;
}

.edit-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.edit-header h2 {
  margin: 0;
  color: white;
  font-size: 1.8em;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}

.user-form,
.password-form {
  max-width: 600px;
  margin: 20px auto;
}

/* Override Element UI styles for glassmorphism */
:deep(.el-tabs) {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
}

:deep(.el-tabs__header) {
  background: rgba(255, 255, 255, 0.15) !important;
  backdrop-filter: blur(15px) !important;
  -webkit-backdrop-filter: blur(15px) !important;
  border-radius: 12px !important;
  border: 1px solid rgba(255, 255, 255, 0.2) !important;
  padding: 5px !important;
  margin-bottom: 25px !important;
}

:deep(.el-tabs__nav-wrap) {
  margin-bottom: 0 !important;
}

:deep(.el-tabs__nav-wrap::after) {
  display: none !important;
}

:deep(.el-tabs__nav) {
  border: none !important;
  display: flex !important;
  width: 100% !important;
  background: transparent !important;
}

:deep(.el-tabs__content) {
  background: rgba(255, 255, 255, 0.08) !important;
  backdrop-filter: blur(10px) !important;
  -webkit-backdrop-filter: blur(10px) !important;
  border-radius: 12px !important;
  padding: 20px !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
}

:deep(.el-tabs__item) {
  color: rgba(255, 255, 255, 0.8) !important;
  transition: all 0.3s ease !important;
  padding: 0 20px !important;
  height: 40px !important;
  line-height: 40px !important;
  border: none !important;
  margin: 0 4px !important;
}

:deep(.el-tabs__item.is-active) {
  color: white !important;
  font-weight: 600 !important;
  background: rgba(64, 158, 255, 0.2) !important;
  border-radius: 8px !important;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2) !important;
  border: none !important;
}

:deep(.el-tabs__item:hover) {
  color: white !important;
  background: rgba(64, 158, 255, 0.1) !important;
  border-radius: 8px !important;
}

:deep(.el-tabs__active-bar) {
  display: none !important;
}

/* Back button style */
.edit-header .el-button {
  background: rgba(64, 158, 255, 0.2) !important;
  backdrop-filter: blur(15px) !important;
  -webkit-backdrop-filter: blur(15px) !important;
  border: 1px solid rgba(255, 255, 255, 0.2) !important;
  color: white !important;
  border-radius: 12px !important;
  height: 40px !important;
  padding: 0 20px !important;
  transition: all 0.3s ease !important;
  font-weight: 500 !important;
  letter-spacing: 0.5px !important;
}

.edit-header .el-button:hover {
  background: rgba(64, 158, 255, 0.3) !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 20px rgba(64, 158, 255, 0.3) !important;
}

.edit-header .el-button i {
  margin-right: 6px !important;
}

:deep(.el-form-item__label) {
  color: rgba(255, 255, 255, 0.95) !important;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3) !important;
  font-weight: 500 !important;
  letter-spacing: 0.5px !important;
  white-space: nowrap !important;
}

:deep(.el-input__inner) {
  background: rgba(255, 255, 255, 0.15) !important;
  border: 1px solid rgba(255, 255, 255, 0.2) !important;
  color: white !important;
  backdrop-filter: blur(10px) !important;
  -webkit-backdrop-filter: blur(10px) !important;
  border-radius: 10px !important;
  height: 42px !important;
  padding: 0 15px !important;
}

:deep(.el-textarea__inner) {
  background: rgba(255, 255, 255, 0.15) !important;
  border: 1px solid rgba(255, 255, 255, 0.2) !important;
  color: white !important;
  backdrop-filter: blur(10px) !important;
  -webkit-backdrop-filter: blur(10px) !important;
  border-radius: 10px !important;
  padding: 10px 15px !important;
}

:deep(.el-input__inner:focus),
:deep(.el-textarea__inner:focus) {
  border-color: rgba(64, 158, 255, 0.5) !important;
  box-shadow: 0 0 10px rgba(64, 158, 255, 0.2) !important;
}

:deep(.el-button) {
  backdrop-filter: blur(15px) !important;
  -webkit-backdrop-filter: blur(15px) !important;
  border: 1px solid rgba(255, 255, 255, 0.2) !important;
  transition: all 0.3s ease !important;
  border-radius: 10px !important;
  height: 42px !important;
  padding: 0 20px !important;
}

:deep(.el-button--primary) {
  background: rgba(64, 158, 255, 0.3) !important;
  color: white !important;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2) !important;
}

:deep(.el-button--success) {
  background: rgba(103, 194, 58, 0.3) !important;
  color: white !important;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2) !important;
}

:deep(.el-button:hover) {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2) !important;
}

:deep(.el-button--primary:hover) {
  background: rgba(64, 158, 255, 0.4) !important;
}

:deep(.el-button--success:hover) {
  background: rgba(103, 194, 58, 0.4) !important;
}

@media (max-width: 768px) {
  .user-container {
    padding: 70px 15px 20px;
  }

  .profile-name {
    font-size: 2em;
  }

  .profile-username {
    font-size: 1.1em;
  }

  .info-section h3 {
    font-size: 1.2em;
  }

  .edit-form-card {
    padding: 20px;
  }

  .profile-header {
    padding: 20px;
  }

  :deep(.el-tabs__header) {
    padding: 3px !important;
  }

  :deep(.el-tabs__item) {
    padding: 0 10px !important;
    font-size: 13px !important;
  }

  :deep(.el-form-item__label) {
    font-size: 14px !important;
  }
}
</style>
