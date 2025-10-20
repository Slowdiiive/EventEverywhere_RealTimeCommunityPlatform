<template>
  <div class="event-detail-page">
    <div class="page-background"></div>
    <div class="event-detail-container">
      <!-- Header with back button and actions -->
      <div class="detail-header">
        <div class="header-left">
          <el-button class="back-btn" icon="el-icon-back" @click="backToList">Back</el-button>
          <h1>{{ event.title }}</h1>
        </div>
        <div class="header-actions" v-if="isEventOwner">
          <el-button
            type="primary"
            size="small"
            @click="openEditDialog"
            icon="el-icon-edit"
            class="edit-btn"
            >Edit</el-button
          >
          <el-button
            type="danger"
            size="small"
            @click="confirmDelete"
            icon="el-icon-delete"
            class="delete-btn"
            >Delete</el-button
          >
        </div>
      </div>

      <!-- Loading skeleton -->
      <div v-if="loading" class="loading-state">
        <el-skeleton style="width: 100%" :rows="10" animated />
      </div>

      <!-- Event content -->
      <div v-else class="event-content glass-container">
        <!-- Event meta info -->
        <div class="event-meta">
          <div class="event-user">
            <i class="el-icon-user"></i>
            <span>{{ event.user?.name || "Anonymous" }}</span>
          </div>
          <div class="event-date">
            <i class="el-icon-time"></i>
            <span>{{ formatDateFull(event.created_at) }}</span>
          </div>
          <div class="event-category">
            <el-tag size="small" effect="dark">{{ event.category }}</el-tag>
          </div>
        </div>

        <!-- Event times -->
        <div class="event-times" v-if="event.start_at || event.end_at">
          <div v-if="event.start_at" class="event-time">
            <strong>Starts:</strong> {{ formatDateFull(event.start_at) }}
          </div>
          <div v-if="event.end_at" class="event-time">
            <strong>Ends:</strong> {{ formatDateFull(event.end_at) }}
          </div>
        </div>

        <!-- Event location -->
        <div class="event-location">
          <i class="el-icon-location"></i>
          <span>{{ event.address || "No address available" }}</span>
        </div>

        <!-- Event image -->
        <div class="event-image">
          <el-image
            :src="getImageUrl(event.img)"
            fit="cover"
            :alt="event.title"
          >
            <div slot="error" class="image-placeholder">
              <i class="el-icon-picture-outline"></i>
            </div>
          </el-image>
        </div>

        <!-- Event content -->
        <div class="event-description">
          <p>{{ event.content }}</p>
        </div>

        <!-- Event actions -->
        <div class="event-actions">
          <div class="likes-action" @click="toggleLike">
            <i
              :class="[
                isLiked ? 'el-icon-star-on' : 'el-icon-star-off',
                'like-icon',
              ]"
            ></i>
            <span>{{ event.like_count || 0 }} Likes</span>
          </div>
          <div class="comments-count" @click="focusCommentInput">
            <i class="el-icon-chat-line-square"></i>
            <span>{{ event.comment_count || 0 }} Comments</span>
          </div>
        </div>

        <!-- Map toggle button -->
        <div class="map-toggle" @click="toggleMap">
          <span>{{ showMap ? "Hide Map" : "Show Map" }}</span>
          <i :class="showMap ? 'el-icon-arrow-up' : 'el-icon-arrow-down'"></i>
        </div>

        <!-- Expandable map -->
        <div v-show="showMap" class="map-container">
          <div id="detailMap" class="map"></div>
        </div>

        <!-- Comments section -->
        <div class="comments-section">
          <div class="section-header">
            <h3>
              <i class="el-icon-chat-line-square"></i>
              Comments ({{ event.comment_count || 0 }})
            </h3>
            <el-button
              type="primary"
              icon="el-icon-plus"
              class="add-comment-btn"
              @click="openCommentDialog"
            >
              Add Comment
            </el-button>
          </div>

          <div class="comments-list">
            <div
              v-if="event.comments && event.comments.length"
              class="comment-items"
            >
              <div
                v-for="(comment, index) in event.comments"
                :key="comment.id || index"
                class="comment-item"
              >
                <div class="comment-header">
                  <div class="comment-user">
                    <strong>{{
                      comment.user?.name || comment.name || "Anonymous"
                    }}</strong>
                  </div>
                  <div class="comment-actions" v-if="isCommentOwner(comment)">
                    <el-button
                      type="text"
                      icon="el-icon-edit"
                      @click="openEditCommentDialog(comment)"
                      size="mini"
                    ></el-button>
                    <el-button
                      type="text"
                      icon="el-icon-delete"
                      @click="confirmDeleteComment(comment)"
                      size="mini"
                    ></el-button>
                  </div>
                </div>
                <div class="comment-content">{{ comment.content }}</div>
                <div class="comment-time">
                  {{ formatTime(comment.created_at) }}
                </div>
              </div>
            </div>
            <div v-else class="no-comments">
              No comments yet. Be the first to comment!
            </div>
          </div>
        </div>

        <!-- Related events section if any -->
        <div
          v-if="event.related_events && event.related_events.length"
          class="related-events"
        >
          <h3>
            <i class="el-icon-connection"></i>
            Related Events ({{
              event.related_count || event.related_events.length
            }})
          </h3>
          <div class="related-events-list">
            <div
              v-for="relatedEvent in event.related_events"
              :key="relatedEvent.id"
              class="related-event-card"
              @click="navigateToEvent(relatedEvent.id)"
            >
              <div class="related-image">
                <el-image
                  :src="getImageUrl(relatedEvent.img)"
                  fit="cover"
                  :alt="relatedEvent.title"
                >
                  <div slot="error" class="image-placeholder-small">
                    <i class="el-icon-picture-outline"></i>
                  </div>
                </el-image>
              </div>
              <div class="related-info">
                <h4>{{ relatedEvent.title }}</h4>
                <div class="related-meta">
                  <span>{{ relatedEvent.category }}</span>
                  <span>{{
                    formatDateShort(
                      relatedEvent.start_at || relatedEvent.created_at
                    )
                  }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Comment Dialog -->
    <el-dialog
      title="Add Comment"
      :visible.sync="commentDialogVisible"
      width="500px"
      :before-close="closeCommentDialog"
    >
      <el-form :model="commentForm">
        <el-form-item>
          <el-input
            type="textarea"
            v-model="commentForm.content"
            :rows="4"
            placeholder="Share your thoughts..."
            class="styled-input"
          ></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="closeCommentDialog">Cancel</el-button>
        <el-button type="primary" @click="submitComment">Post</el-button>
      </span>
    </el-dialog>

    <!-- Edit Comment Dialog -->
    <el-dialog
      title="Edit Comment"
      :visible.sync="editCommentDialogVisible"
      width="500px"
    >
      <el-form :model="editCommentForm">
        <el-form-item>
          <el-input
            type="textarea"
            v-model="editCommentForm.content"
            :rows="4"
            class="styled-input"
          ></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="editCommentDialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="updateComment">Update</el-button>
      </span>
    </el-dialog>

    <!-- Edit Event Dialog -->
    <el-dialog
      title="Edit Event"
      :visible.sync="editEventDialogVisible"
      width="650px"
      custom-class="edit-event-dialog"
    >
      <el-form :model="editEventForm" label-position="top">
        <div class="form-section-title">Title</div>
        <el-input
          v-model="editEventForm.title"
          placeholder="Enter event title"
          class="styled-input"
        ></el-input>

        <div class="form-section-title">Category</div>
        <el-select
          v-model="editEventForm.category"
          placeholder="Select category"
          class="styled-input"
        >
          <el-option
            v-for="category in categories"
            :key="category"
            :label="category"
            :value="category"
          ></el-option>
        </el-select>

        <div class="form-section-title">Content</div>
        <el-input
          type="textarea"
          v-model="editEventForm.content"
          :rows="4"
          placeholder="Describe the event..."
          class="styled-input"
        ></el-input>

        <div class="form-row">
          <div class="form-col">
            <div class="form-section-title">Start Date</div>
            <el-date-picker
              v-model="editEventForm.start_at"
              type="datetime"
              placeholder="Select start date and time"
              class="styled-input"
            ></el-date-picker>
          </div>
          <div class="form-col">
            <div class="form-section-title">End Date</div>
            <el-date-picker
              v-model="editEventForm.end_at"
              type="datetime"
              placeholder="Select end date and time"
              class="styled-input"
            ></el-date-picker>
          </div>
        </div>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="editEventDialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="updateEvent">Save Changes</el-button>
      </span>
    </el-dialog>

    <!-- Confirm Delete Dialog -->
    <el-dialog
      title="Confirm Delete"
      :visible.sync="deleteConfirmVisible"
      width="400px"
    >
      <p>
        Are you sure you want to delete this event? This action cannot be
        undone.
      </p>
      <span slot="footer" class="dialog-footer">
        <el-button @click="deleteConfirmVisible = false">Cancel</el-button>
        <el-button type="danger" @click="deleteEvent">Delete</el-button>
      </span>
    </el-dialog>

    <!-- Confirm Delete Comment Dialog -->
    <el-dialog
      title="Confirm Delete Comment"
      :visible.sync="deleteCommentConfirmVisible"
      width="400px"
    >
      <p>Are you sure you want to delete this comment?</p>
      <span slot="footer" class="dialog-footer">
        <el-button @click="deleteCommentConfirmVisible = false"
          >Cancel</el-button
        >
        <el-button type="danger" @click="deleteComment">Delete</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
/* global google */
import { getEvent, updateEvent, deleteEvent } from "@/api/event";
import * as MapUtils from "@/utils/map";
import { getUserId, getUserFromToken, checkLoggedIn } from "@/utils/auth";

export default {
  name: "EventDetailPage",
  data() {
    return {
      loading: true,
      event: {},
      newComment: "",
      map: null,
      eventMarker: null,
      showMap: false,

      // Like functionality
      isLiked: false,
      likeLoading: false,

      // Comment dialog
      commentDialogVisible: false,
      commentForm: {
        content: "",
      },

      // Edit comment dialog
      editCommentDialogVisible: false,
      editCommentForm: {
        id: null,
        content: "",
      },

      // Edit event dialog
      editEventDialogVisible: false,
      editEventForm: {
        title: "",
        category: "",
        content: "",
        start_at: null,
        end_at: null,
      },

      // Delete confirmations
      deleteConfirmVisible: false,
      deleteCommentConfirmVisible: false,
      currentCommentId: null,

      // Available categories for event editing
      categories: [
        "Outdoor Concert",
        "Dance Battle",
        "Magic Show",
        "Art Exhibition",
        "Food Festival",
        "Movie Screening",
        "Carnival",
        "Performance",
        "Food Truck",
        "Parade",
      ],
    };
  },

  computed: {
    eventId() {
      return this.$route.params.id;
    },

    isEventOwner() {
      // return true;
      const currentUser = this.getCurrentUser();
      console.log("currentUser:", currentUser.id);
      console.log("event:", this.event);
      const isOwner =(
        currentUser &&
        this.event &&
        (currentUser.id == this.event.user_id ||
          (this.event.user && currentUser.id == this.event.user.id))
      );
      console.log("isOwner:", isOwner);
      return isOwner;
    },
  },

  mounted() {
    this.fetchEventDetail();
    
    // Listen for route changes to properly handle map positioning
    this.$router.afterEach(() => {
      // Reset map state when route changes
      if (this.map) {
        this.handleMapResize();
      }
    });
  },

  methods: {
    fetchEventDetail() {
      this.loading = true;
      console.log("Fetching event details:", this.eventId);

      getEvent(this.eventId)
        .then((response) => {
          this.event = response;
          console.log("Event original data:", JSON.stringify(this.event));
          console.log("Event likes data:", this.event.likes);

          // Ensure position property is set
          if (
            !this.event.position &&
            this.event.latitude &&
            this.event.longitude
          ) {
            this.event.position = {
              lat: parseFloat(this.event.latitude),
              lng: parseFloat(this.event.longitude),
            };
          }

          // Ensure comments exist
          if (!this.event.comments) {
            this.event.comments = [];
          }

          // Use setTimeout to ensure data is fully loaded
          setTimeout(() => {
            // Check if user has liked the event
            this.checkIfLiked();
          }, 100);

          this.loading = false;
        })
        .catch((error) => {
          console.error("Failed to get event details:", error);
          this.$message.error("Failed to get event details: " + error.message);
          this.loading = false;
        });
    },

    toggleMap() {
      this.showMap = !this.showMap;

      if (this.showMap) {
        // Add loading class
        const mapEl = document.querySelector('.map');
        if (mapEl) {
          mapEl.classList.add('loading');
        }

        // Add visible class after a short delay to trigger animation
        setTimeout(() => {
          const container = document.querySelector('.map-container');
          if (container) {
            container.classList.add('visible');
          }
        }, 50);

        // Initialize map if not already done
        this.$nextTick(() => {
          if (!this.map) {
            this.initMap();
          } else {
            // Force immediate resize and centering after display
            setTimeout(() => {
              this.handleMapResize();
              // Additional resize to ensure correct display
              setTimeout(() => {
                this.handleMapResize();
              }, 300);
            }, 100);
          }

          // Remove loading class after map is ready
          setTimeout(() => {
            const mapEl = document.querySelector('.map');
            if (mapEl) {
              mapEl.classList.remove('loading');
            }
          }, 500);
        });
      } else {
        // Remove visible class when hiding
        const container = document.querySelector('.map-container');
        if (container) {
          container.classList.remove('visible');
        }
      }
    },

    initMap() {
      if (!window.google) {
        MapUtils.loadGoogleMapsAPI(() => {
          // Wait for next tick to ensure container is rendered
          this.$nextTick(() => {
            this.createMap();
          });
        });
        return;
      }

      this.$nextTick(() => {
        this.createMap();
      });
    },

    createMap() {
      const mapContainer = document.getElementById("detailMap");
      if (!mapContainer) {
        console.error("Map container not found");
        return;
      }

      // Create map instance with improved options
      // eslint-disable-next-line no-undef
      this.map = new google.maps.Map(mapContainer, {
        center: this.event.position || MapUtils.getDefaultPosition(),
        zoom: 15,
        styles: MapUtils.getMapStyles(),
        mapTypeControl: false,
        streetViewControl: false,
        fullscreenControl: false,
        gestureHandling: "cooperative", 
        keyboardShortcuts: false,
        maxZoom: 18,
        minZoom: 3,
        restriction: {
          latLngBounds: {
            north: 85,
            south: -85,
            west: -180,
            east: 180
          },
          strictBounds: true
        }
      });

      // Force layout recalculation to fix positioning
      setTimeout(() => {
        google.maps.event.trigger(this.map, 'resize');
        if (this.event.position) {
          this.centerMapOnEvent();
        }
      }, 100);

      // Add resize listener to handle window resizing
      window.addEventListener('resize', this.handleMapResize);
    },

    handleMapResize() {
      if (this.map) {
        // Force a resize to ensure proper rendering
        google.maps.event.trigger(this.map, 'resize');
        setTimeout(() => {
          if (this.event.position) {
            this.map.setCenter(this.event.position);
          }
        }, 50);
      }
    },

    // Clean up method
    beforeDestroy() {
      // Remove event listeners
      window.removeEventListener('resize', this.handleMapResize);
      
      // Clean up map instance
      if (this.map) {
        if (this.eventMarker) {
          this.eventMarker.setMap(null);
          this.eventMarker = null;
        }
        this.map = null;
      }
    },

    backToList() {
      this.$router.push("/event");
    },

    navigateToEvent(eventId) {
      if (eventId === this.eventId) return;
      this.$router.push(`/event/${eventId}`);
    },

    formatTime(timestamp) {
      if (!timestamp) return "";
      const date = new Date(timestamp + "Z");
      const now = new Date();
      const diffInSeconds = Math.floor((now - date) / 1000);

      if (diffInSeconds < 60) {
        return `${diffInSeconds} seconds ago`;
      } else if (diffInSeconds < 3600) {
        const minutes = Math.floor(diffInSeconds / 60);
        return `${minutes} minute${minutes > 1 ? "s" : ""} ago`;
      } else if (diffInSeconds < 86400) {
        const hours = Math.floor(diffInSeconds / 3600);
        return `${hours} hour${hours > 1 ? "s" : ""} ago`;
      } else {
        const days = Math.floor(diffInSeconds / 86400);
        return `${days} day${days > 1 ? "s" : ""} ago`;
      }
    },

    formatDateFull(dateString) {
      if (!dateString) return "";
      // Append "Z" so it's parsed as UTC
      const date = new Date(dateString + "Z");
      return date.toLocaleString("en-US", {
        timeZone: "America/New_York",
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    },

    formatDateShort(dateString) {
      if (!dateString) return "";
      const date = new Date(dateString + "Z");
      return date.toLocaleString("en-US", {
        timeZone: "America/New_York",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    },

    // get current user info
    getCurrentUser() {
      const user = getUserFromToken();
      console.log("Getting user info from token:", user);
      if (user) {
        return {
          id: user.userId,
          username: user.username || user.name || "User",
        };
      }
      return { id: null, username: "Guest" };
    },

    // check if user is logged in
    checkUserLogin() {
      return checkLoggedIn();
    },

    isCommentOwner(comment) {
      // return true;
      const currentUser = this.getCurrentUser();
      console.log("currentUser:", currentUser.id);
      console.log("comment:", comment);
      return (
        currentUser &&
        comment &&
        (currentUser.id == comment.user_id ||
          (comment.user && currentUser.id == comment.user.id))
      );
    },

    // Like functionality
    checkIfLiked() {
      try {
        // Get current user ID
        const userId = getUserId();
        console.log("Checking like status: Current user ID", userId);
        console.log(
          "Checking like status: Event likes array",
          this.event.likes
        );

        // If user is not logged in or there's no likes array, set as not liked
        if (!userId || !this.event.likes || !Array.isArray(this.event.likes)) {
          console.log("Not logged in or no like data, set as not liked");
          this.isLiked = false;
          return;
        }

        // Find current user's like record - match user_id or user.id with current userId
        const hasLiked = this.event.likes.some((like) => {
          const likeUserId = like.user_id || (like.user && like.user.id);
          console.log(
            "Comparing like user ID:",
            likeUserId,
            "Current user ID:",
            userId
          );
          return likeUserId == userId; // Use == instead of ===, in case of type inconsistency
        });

        this.isLiked = hasLiked;
        console.log(
          "Like status check result:",
          this.isLiked ? "Liked" : "Not liked"
        );
      } catch (error) {
        console.error("Error checking like status:", error);
        this.isLiked = false;
      }
    },

    async toggleLike() {
      // Return directly if a request is already in progress
      if (this.likeLoading) return;

      if (!this.checkUserLogin()) {
        this.$message.warning("Please login first before liking");
        return;
      }

      this.likeLoading = true;
      const previousIsLiked = this.isLiked;
      const previousCount = this.event.like_count || 0;

      try {
        const likeAPI = await import("@/api/like");
        const userId = getUserId();

        if (!previousIsLiked) {
          // === Like ===
          const res = await likeAPI.createLike({ event_id: this.event.id });
          // Update UI after successful request
          this.isLiked = true;
          this.event.like_count = previousCount + 1;

          if (res && res.data) {
            this.event.likes = this.event.likes || [];
            this.event.likes.push(res.data);
          }
          this.$message.success("Liked successfully");

          // Refresh event data after liking to ensure likes array is up-to-date
          await this.fetchEventDetail();
        } else {
          // === Unlike ===
          // Find the created/existing like record
          const userLike = (this.event.likes || []).find((like) => {
            const likeUserId = like.user_id || (like.user && like.user.id);
            return likeUserId == userId;
          });

          if (userLike && userLike.id) {
            await likeAPI.deleteLike(userLike.id);
            // Update UI after successful request
            this.isLiked = false;
            this.event.like_count = Math.max(0, previousCount - 1);
            this.event.likes = this.event.likes.filter(
              (l) => l.id !== userLike.id
            );
            this.$message.success("Unlike successful");
          } else {
            // If like ID cannot be found, show error message and refresh data
            this.$message.error("Unable to unlike, like record not found");
            // Refresh event data to ensure UI state is correct
            await this.fetchEventDetail();
          }
        }
      } catch (err) {
        console.error("toggleLike error:", err);
        // Rollback UI and refresh data on error
        this.isLiked = previousIsLiked;
        this.event.like_count = previousCount;
        this.$message.error("Operation failed, please try again later");
        await this.fetchEventDetail();
      } finally {
        this.likeLoading = false;
      }
    },

    // Comment handling
    focusCommentInput() {
      this.openCommentDialog();
    },

    openCommentDialog() {
      if (!this.checkUserLogin()) {
        this.$message.warning("Please login first to add a comment");
        this.$router.push("/login");
        return;
      }

      this.commentForm.content = "";
      this.commentDialogVisible = true;
    },

    closeCommentDialog() {
      this.commentDialogVisible = false;
      this.commentForm.content = "";
    },

    submitComment() {
      if (!this.commentForm.content.trim()) {
        this.$message.warning("Please enter a comment");
        return;
      }

      if (!this.checkUserLogin()) return;

      this.loading = true;

      // create comment data
      const commentData = {
        content: this.commentForm.content,
        event_id: this.event.id,
      };

      // use comment API
      import("@/api/comment")
        .then((commentAPI) => {
          commentAPI
            .createComment(commentData)
            .then((response) => {
              console.log("Comment creation response:", response);
              this.closeCommentDialog();
              this.$message.success("Comment added successfully");
              
              // reload
              this.fetchEventDetail();
            })
            .catch((error) => {
              console.error("Error adding comment:", error);
              if (error.response && error.response.status === 401) {
                localStorage.removeItem("token");
                this.$message.error(
                  "Your session has expired. Please login again."
                );
              } else {
                this.$message.error("Failed to add comment");
              }
              this.loading = false;
            });
        })
        .catch((error) => {
          console.error("Failed to load comment API:", error);
          this.$message.error("Comment functionality unavailable");
          this.loading = false;
        });
    },

    // Edit comment
    openEditCommentDialog(comment) {
      this.editCommentForm.id = comment.id;
      this.editCommentForm.content = comment.content;
      this.editCommentDialogVisible = true;
    },

    updateComment() {
      if (!this.editCommentForm.content.trim()) {
        this.$message.warning("Comment cannot be empty");
        return;
      }

      this.loading = true;

      import("@/api/comment")
        .then((commentAPI) => {
          commentAPI
            .updateComment(this.editCommentForm.id, {
              content: this.editCommentForm.content,
            })
            .then((response) => {
              console.log("Comment update response:", response);

              // Update the comment in the UI
              const commentIndex = this.event.comments.findIndex(
                (c) => c.id === this.editCommentForm.id
              );
              if (commentIndex >= 0) {
                this.event.comments[commentIndex].content =
                  this.editCommentForm.content;
                if (response && response.data) {
                  Object.assign(
                    this.event.comments[commentIndex],
                    response.data
                  );
                }
              }

              this.editCommentDialogVisible = false;
              this.loading = false;
              this.$message.success("Comment updated successfully");
            })
            .catch((error) => {
              console.error("Error updating comment:", error);
              this.$message.error("Failed to update comment");
              this.loading = false;
            });
        })
        .catch((error) => {
          console.error("Failed to load comment API:", error);
          this.$message.error("Comment update functionality unavailable");
          this.loading = false;
        });
    },

    // Delete comment
    confirmDeleteComment(comment) {
      this.currentCommentId = comment.id;
      this.deleteCommentConfirmVisible = true;
    },

    deleteComment() {
      if (!this.currentCommentId) return;

      this.loading = true;

      import("@/api/comment")
        .then((commentAPI) => {
          commentAPI
            .deleteComment(this.currentCommentId)
            .then(() => {
              // Remove the comment from the UI
              this.event.comments = this.event.comments.filter(
                (c) => c.id !== this.currentCommentId
              );
              this.event.comment_count = Math.max(
                0,
                (this.event.comment_count || 0) - 1
              );

              this.deleteCommentConfirmVisible = false;
              this.currentCommentId = null;
              this.loading = false;
              this.$message.success("Comment deleted successfully");
            })
            .catch((error) => {
              console.error("Error deleting comment:", error);
              this.$message.error("Failed to delete comment");
              this.loading = false;
            });
        })
        .catch((error) => {
          console.error("Failed to load comment API:", error);
          this.$message.error("Comment deletion functionality unavailable");
          this.loading = false;
        });
    },

    // Edit event
    openEditDialog() {
      this.editEventForm = {
        title: this.event.title || "",
        category: this.event.category || "",
        content: this.event.content || "",
        start_at: this.event.start_at ? new Date(this.event.start_at) : null,
        end_at: this.event.end_at ? new Date(this.event.end_at) : null,
      };

      this.editEventDialogVisible = true;
    },

    updateEvent() {
      if (!this.editEventForm.title || !this.editEventForm.content) {
        this.$message.warning("Title and content are required");
        return;
      }

      this.loading = true;

      const updateData = {
        title: this.editEventForm.title,
        category: this.editEventForm.category,
        content: this.editEventForm.content,
      };

      // process start_at and end_at
      if (this.editEventForm.start_at) {
        const startDate = new Date(this.editEventForm.start_at);
        if (!isNaN(startDate.getTime())) {
          updateData.start_at = startDate.toISOString().replace("Z", "");
        }
      }

      if (this.editEventForm.end_at) {
        const endDate = new Date(this.editEventForm.end_at);
        if (!isNaN(endDate.getTime())) {
          updateData.end_at = endDate.toISOString().replace("Z", "");
        }
      }

      updateEvent(this.event.id, updateData)
        .then((response) => {
          console.log("Event update response:", response);

          // Update the event data in the UI
          Object.assign(this.event, updateData);

          this.editEventDialogVisible = false;
          this.loading = false;
          this.$message.success("Event updated successfully");
        })
        .catch((error) => {
          console.error("Error updating event:", error);
          this.$message.error(
            "Failed to update event: " + (error.message || "Unknown error")
          );
          this.loading = false;
        });
    },

    // Delete event
    confirmDelete() {
      this.deleteConfirmVisible = true;
    },

    deleteEvent() {
      this.loading = true;

      deleteEvent(this.event.id)
        .then(() => {
          this.deleteConfirmVisible = false;
          this.loading = false;
          this.$message.success("Event deleted successfully");
          this.$router.push("/event");
        })
        .catch((error) => {
          console.error("Error deleting event:", error);
          this.$message.error(
            "Failed to delete event: " + (error.message || "Unknown error")
          );
          this.loading = false;
        });
    },

    // get image URL, if not available, return local default image
    getImageUrl(url) {
      if (!url) {
        // use local default image
        return new URL("@/assets/no-image.png", import.meta.url).href;
      }
      // if URL starts with http, return it directly
      if (url && (url.startsWith("http://") || url.startsWith("https://"))) {
        return url;
      }
      // otherwise, add domain name
      return `${import.meta.env.VITE_API_URL}${url}`;
    },

    centerMapOnEvent() {
      if (!this.map || !this.event.position) return;

      // Center the map on the event
      this.map.setCenter(this.event.position);

      // Create or update marker
      if (this.eventMarker) {
        this.eventMarker.setPosition(this.event.position);
      } else {
        // eslint-disable-next-line no-undef
        this.eventMarker = new google.maps.Marker({
          position: this.event.position,
          map: this.map,
          title: this.event.title,
          // eslint-disable-next-line no-undef
          animation: google.maps.Animation.DROP,
          // Add custom marker options
          optimized: true,
          clickable: true
        });

        // Add click listener to marker
        this.eventMarker.addListener('click', () => {
          // Create info window content
          const content = `
            <div style="padding: 10px;">
              <h3 style="margin: 0 0 5px 0;">${this.event.title}</h3>
              <p style="margin: 0;">${this.event.address || 'No address available'}</p>
            </div>
          `;

          // Create and open info window
          // eslint-disable-next-line no-undef
          const infoWindow = new google.maps.InfoWindow({
            content: content,
            maxWidth: 200
          });
          infoWindow.open(this.map, this.eventMarker);
        });
      }
    },
  },
};
</script>

<style scoped>
.event-detail-page {
  width: 100%;
  min-height: 100vh;
  padding: 80px 20px 20px;
  position: relative;
  overflow-x: hidden;
}

.page-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: url('https://images.unsplash.com/photo-1499092346589-b9b6be3e94b2?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTR8fG5ldyUyMHlvcmt8ZW58MHx8MHx8fDA%3D') center/cover no-repeat fixed;
  z-index: 0;
}

.page-background::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.1));
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.event-detail-container {
  position: relative;
  max-width: 800px;
  margin: 0 auto;
  z-index: 1;
  padding-top: 40px;
}

/* Main glass container */
.glass-container {
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  padding: 30px;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
}

/* Header */
.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 30px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 15px;
}

.header-left h1 {
  margin: 0;
  font-size: 24px;
  color: #333;
  font-weight: 600;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.back-btn {
  height: 40px;
  padding: 0 16px;
  background: rgba(64, 158, 255, 0.15);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
  color: #409eff;
  font-weight: 500;
  display: flex;
  align-items: center;
}

.back-btn:hover {
  transform: translateY(-2px);
  background: rgba(64, 158, 255, 0.25);
  box-shadow: 0 4px 15px rgba(64, 158, 255, 0.15);
}

.back-btn:active {
  transform: scale(0.98);
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.edit-btn,
.delete-btn {
  height: 36px;
  padding: 0 16px;
  transition: all 0.3s ease;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  white-space: nowrap;
}

.edit-btn {
  background: rgba(64, 158, 255, 0.15);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: #409eff;
}

.edit-btn:hover {
  transform: translateY(-2px);
  background: rgba(64, 158, 255, 0.25);
  box-shadow: 0 4px 15px rgba(64, 158, 255, 0.15);
}

.delete-btn {
  background: rgba(245, 108, 108, 0.15);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: #f56c6c;
}

.delete-btn:hover {
  transform: translateY(-2px);
  background: rgba(245, 108, 108, 0.25);
  box-shadow: 0 4px 15px rgba(245, 108, 108, 0.15);
}

/* Event content */
.event-content {
  margin-top: 20px;
}

.event-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin-bottom: 20px;
  color: #333;
}

.event-user,
.event-date,
.event-location {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 15px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #333;
}

.event-times {
  margin-bottom: 15px;
  padding: 12px 15px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #333;
}

.event-image {
  margin: 25px 0;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.15);
}

.event-image .el-image {
  width: 100%;
  height: 400px;
  object-fit: cover;
}

.event-description {
  margin: 30px 0;
  padding: 20px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  line-height: 1.6;
  color: #333;
}

/* Event actions */
.event-actions {
  display: flex;
  gap: 20px;
  margin: 25px 0;
  padding: 15px 20px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.likes-action,
.comments-count {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #333;
  cursor: pointer;
  padding: 8px 16px;
  border-radius: 8px;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.2);
}

.likes-action:hover,
.comments-count:hover {
  transform: translateY(-2px);
  background: rgba(255, 255, 255, 0.3);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* Comments section */
.comments-section {
  margin-top: 30px;
  padding: 30px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
}

.comment-item {
  padding: 15px;
  margin-bottom: 15px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.comment-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  background: rgba(255, 255, 255, 0.25);
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.comment-content {
  margin-bottom: 10px;
  line-height: 1.5;
  color: #303133;
}

.comment-time {
  font-size: 12px;
  color: #909399;
}

.no-comments {
  padding: 30px;
  text-align: center;
  color: #333;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  margin: 20px 0;
}

.no-comments:hover {
  transform: translateY(-2px);
  background: rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
}

/* Related events */
.related-events {
  margin-top: 40px;
  padding-top: 20px;
  border-top: 1px solid #eaeaea;
}

.related-events h3 {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  color: #303133;
  margin-bottom: 20px;
}

.related-events-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
  gap: 15px;
}

.related-event-card {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.3s;
}

.related-event-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.related-image {
  height: 120px;
  overflow: hidden;
}

.related-image .el-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.related-info {
  padding: 12px;
}

.related-info h4 {
  margin: 0 0 8px 0;
  font-size: 14px;
  line-height: 1.4;
  max-height: 40px;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.related-meta {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #909399;
}

/* Dialog styles */
.form-section-title {
  color: #333;
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 10px;
  margin-top: 20px;
}

.styled-input {
  margin-bottom: 20px;
  width: 100%;
}

.styled-input :deep(.el-input__inner),
.styled-input :deep(.el-textarea__inner) {
  background: rgba(255, 255, 255, 0.3) !important;
  border: 1px solid rgba(255, 255, 255, 0.3) !important;
  border-radius: 12px !important;
  padding: 12px 15px !important;
  color: #333 !important;
  height: auto !important;
}

.styled-input :deep(.el-textarea__inner) {
  padding: 12px 15px !important;
  min-height: 120px !important;
}

/* Dialog buttons */
:deep(.el-dialog__footer .el-button) {
  height: 40px;
  padding: 0 20px;
  border-radius: 12px;
  font-weight: 500;
  transition: all 0.3s ease;
}

:deep(.el-dialog__footer .el-button--default) {
  background: rgba(144, 147, 153, 0.15);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: #606266;
}

:deep(.el-dialog__footer .el-button--default:hover) {
  background: rgba(144, 147, 153, 0.25);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

:deep(.el-dialog__footer .el-button--primary) {
  background: rgba(64, 158, 255, 0.15);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: #409eff;
}

:deep(.el-dialog__footer .el-button--primary:hover) {
  background: rgba(64, 158, 255, 0.25);
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(64, 158, 255, 0.15);
}

:deep(.el-dialog__footer .el-button--danger) {
  background: rgba(245, 108, 108, 0.15);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: #f56c6c;
}

:deep(.el-dialog__footer .el-button--danger:hover) {
  background: rgba(245, 108, 108, 0.25);
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(245, 108, 108, 0.15);
}

/* Form row for edit event */
.form-row {
  display: flex;
  gap: 15px;
  margin-bottom: 15px;
}

.form-col {
  flex: 1;
}

/* Map styles */
.map-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin: 25px 0 15px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  cursor: pointer;
  color: #333;
  transition: all 0.3s ease;
}

.map-toggle:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.map-container {
  height: 400px;
  margin: 25px 0;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  position: relative;
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.3s ease, transform 0.3s ease;
  /* Fix positioning issues */
  left: 0;
  right: 0;
  width: 100% !important;
  /* Remove nested glass effect */
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: none;
  -webkit-backdrop-filter: none;
}

.map-container.visible {
  opacity: 1;
  transform: translateY(0);
}

.map {
  width: 100% !important;
  height: 100% !important;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.1);
  position: relative !important;
  left: 0 !important;
  top: 0 !important;
}

/* Add loading state for map */
.map::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
  z-index: 1;
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
}

.map.loading::before {
  opacity: 1;
}

/* Dialog styles */
:deep(.el-dialog) {
  background: rgba(255, 255, 255, 0.2) !important;
  backdrop-filter: blur(10px) !important;
  -webkit-backdrop-filter: blur(10px) !important;
  border-radius: 16px !important;
  border: 1px solid rgba(255, 255, 255, 0.3) !important;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1) !important;
  overflow: hidden !important;
}

:deep(.el-dialog__header) {
  padding: 20px !important;
  background: rgba(255, 255, 255, 0.1) !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

:deep(.el-dialog__title) {
  color: #333 !important;
  font-weight: 500 !important;
  font-size: 18px !important;
}

:deep(.el-dialog__body) {
  padding: 20px !important;
  background: rgba(255, 255, 255, 0.1) !important;
  color: #333 !important;
}

:deep(.el-dialog__footer) {
  padding: 15px 20px !important;
  background: rgba(255, 255, 255, 0.1) !important;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
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

/* Comments section header */
.comments-section h3 {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
  font-size: 18px;
  color: #333;
}

.comments-section .section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

/* Event category tag override */
.event-category {
  display: inline-flex;
  align-items: center;
  padding: 8px 15px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.event-category :deep(.el-tag) {
  background: transparent !important;
  border: none !important;
  padding: 0 !important;
  height: auto !important;
  line-height: normal !important;
  color: #333 !important;
}

/* Add comment button */
.add-comment-btn {
  height: 36px;
  padding: 0 16px;
  background: rgba(64, 158, 255, 0.15);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
  color: #409eff;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  white-space: nowrap;
}

.add-comment-btn:hover {
  transform: translateY(-2px);
  background: rgba(64, 158, 255, 0.25);
  box-shadow: 0 4px 15px rgba(64, 158, 255, 0.15);
}

.add-comment-btn:active {
  transform: scale(0.98);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .event-detail-page {
    padding: 60px 15px 15px;
  }

  .header-left {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .header-left h1 {
    font-size: 20px;
  }

  .event-image .el-image {
    height: 250px;
  }

  .event-meta {
    flex-direction: column;
    gap: 10px;
  }

  .event-actions {
    flex-direction: column;
  }
}
</style>
