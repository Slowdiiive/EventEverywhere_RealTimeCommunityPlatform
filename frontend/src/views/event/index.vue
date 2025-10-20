<template>
  <div class="event-page">
    <div class="page-background"></div>
    <div class="event-container">
      <div class="map-container">
        <div id="map" class="map"></div>
      </div>

      <div class="event-sidebar" :class="{ collapsed: sidebarCollapsed }">
        <div class="sidebar-header">
          <div class="header-left">
            <div class="sidebar-toggle" @click="toggleSidebar">
              <div class="hamburger-icon">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
            <h2>Recent Events</h2>
          </div>
          <el-button class="custom-btn report-btn" @click="openCreateEventModal"
            >Report Event</el-button
          >
        </div>

        <!-- Event list container -->
        <div class="event-list-wrapper">
          <div class="search-filter">
            <div class="search-filter-row">
              <el-input
                placeholder="Search"
                v-model="searchText"
                prefix-icon="el-icon-search"
                clearable
                class="search-input"
              ></el-input>
              <el-select
                v-model="selectedCategory"
                placeholder="All Categories"
                clearable
                class="category-select"
              >
                <el-option label="All Categories" value=""></el-option>
                <el-option
                  v-for="category in categories"
                  :key="category"
                  :label="category"
                  :value="category"
                ></el-option>
              </el-select>
            </div>
          </div>

          <div class="event-list">
            <div
              v-for="event in displayEvents"
              :key="event.id"
              class="event-item"
              @click="navigateToEventDetail(event)"
            >
              <div
                class="event-dot"
                :class="getCategoryClass(event.category)"
              ></div>
              <div class="event-details">
                <h3>{{ event.title }}</h3>
                <div class="event-meta">
                  <div class="location-info">
                    <i class="el-icon-location"></i>
                    {{ event.address || "No location" }}
                  </div>
                  <div class="time-info nyc-time-display">
                    <i class="el-icon-time"></i>
                    {{ formatEventTime(event.start_at || event.created_at) }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Collapsed state toggle button -->
      <div
        v-if="sidebarCollapsed"
        class="collapsed-toggle"
        @click="toggleSidebar"
      >
        <div class="hamburger-icon">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>
    </div>

    <!-- Create event dialog -->
    <el-dialog
      title="Report Event"
      :visible.sync="createEventDialogVisible"
      width="1000px"
      :before-close="closeCreateEventDialog"
      custom-class="report-event-dialog"
    >
      <el-form :model="newEventForm" label-position="top" class="report-form">
        <div class="form-section-title">Image</div>
        <div class="upload-container">
          <el-upload
            action="#"
            :auto-upload="false"
            :limit="1"
            :show-file-list="false"
            :on-change="handleImageChange"
            :before-upload="beforeImageUpload"
            accept=".jpg,.jpeg,.png,.gif"
            class="full-width-upload"
          >
            <div v-if="!newEventForm.imageUrl" class="upload-box">
              <span>Choose an image (JPG, PNG, GIF)</span>
            </div>
            <div v-else class="image-preview">
              <img :src="newEventForm.imageUrl" alt="Preview" />
              <div class="image-overlay">
                <span>Click to change</span>
              </div>
            </div>
          </el-upload>
        </div>

        <div class="form-section-title">Category</div>
        <div class="category-container">
          <el-radio-group
            v-model="newEventForm.category"
            class="category-radio-group"
          >
            <el-radio
              v-for="category in categories"
              :key="category"
              :label="category"
              class="category-radio"
              :aria-label="category"
            >
              {{ category }}
            </el-radio>
          </el-radio-group>
        </div>

        <div class="form-section-title">Title</div>
        <el-input
          v-model="newEventForm.title"
          placeholder="Enter event title"
          class="styled-input"
        ></el-input>

        <div class="form-section-title">Content</div>
        <el-input
          type="textarea"
          v-model="newEventForm.content"
          :rows="4"
          placeholder="Describe the event..."
          class="styled-input"
        ></el-input>

        <div class="form-section-title">Start Time</div>
        <el-date-picker
          v-model="newEventForm.start_at"
          type="datetime"
          placeholder="Select start time"
          class="styled-input custom-date-picker"
          value-format="yyyy-MM-dd HH:mm:ss"
          :clearable="false"
          :prefix-icon="null"
        ></el-date-picker>

        <div class="form-section-title">End Time</div>
        <el-date-picker
          v-model="newEventForm.end_at"
          type="datetime"
          placeholder="Select end time"
          class="styled-input custom-date-picker"
          value-format="yyyy-MM-dd HH:mm:ss"
          :clearable="false"
          :prefix-icon="null"
        ></el-date-picker>

        <div class="form-section-title">Location</div>
        <div class="address-container">
          <div class="address-text">
            <i class="el-icon-location-outline location-icon"></i>
            <span id="addressOfMap">{{
              formattedAddress || selectedAddress
            }}</span>
          </div>
          <el-button size="small" class="location-btn" @click="useMyLocation">
            <i class="el-icon-position"></i> My Location
          </el-button>
        </div>
        <div id="createEventMap" class="create-map"></div>
      </el-form>

      <div slot="footer" class="dialog-footer">
        <el-button @click="closeCreateEventDialog" class="cancel-btn"
          >Cancel</el-button
        >
        <el-button @click="submitCreateEvent" class="submit-btn">
          Submit Report
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
/* global google */
import { listEvent, createEvent } from "@/api/event";
import * as MapUtils from "@/utils/map";
import OSS from 'ali-oss';
import { checkLoggedIn } from "@/utils/auth";

export default {
  name: "EventPage",
  data() {
    return {
      loading: false,
      sidebarCollapsed: false,
      searchText: "",
      selectedCategory: "",
      createEventDialogVisible: false,
      newEventForm: {
        title: "",
        category: "",
        content: "",
        image: null,
        imageUrl: null,
        start_at: "",
        end_at: "",
      },
      map: null,
      userMarker: null,
      eventMarkers: [],
      createMap: null,
      selectedMarker: null,
      selectedPosition: null,
      selectedAddress: "Select a location on the map",
      formattedAddress: "",
      geocoder: null,
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
      eventList: [],
      queryParams: {
        page: 1,
        limit: 10,
        category: "",
      },
      // Initialize OSS client
      ossClient: new OSS({
        accessKeyId: 'LTAI5tFHofvKn5NCYATVuqHA',
    accessKeySecret: 'hHKHe4abvekRLB89ia7bytaw8yZb1w',
        region: 'oss-us-east-1',
        bucket: 'event-everywhere'
      }),
    };
  },
  computed: {
    displayEvents() {
      let filteredEvents = this.eventList;

      if (this.searchText) {
        const searchLower = this.searchText.toLowerCase();
        filteredEvents = filteredEvents.filter(
          (event) =>
            event.title.toLowerCase().includes(searchLower) ||
            (event.location &&
              event.location.toLowerCase().includes(searchLower)) ||
            (event.content && event.content.toLowerCase().includes(searchLower))
        );
      }

      if (this.selectedCategory) {
        filteredEvents = filteredEvents.filter(
          (event) =>
            event.category &&
            event.category.toLowerCase() === this.selectedCategory.toLowerCase()
        );
      }

      return filteredEvents;
    },
  },
  mounted() {
    this.initMap();
    this.fetchEvents();
    this.fixDatePickerIcons();
  },
  updated() {
    this.fixDatePickerIcons();
  },
  methods: {
    fixDatePickerIcons() {
      // Fix date picker icons
      this.$nextTick(() => {
        const icons = document.querySelectorAll(".el-input__icon.el-icon-time");
        icons.forEach((icon) => {
          icon.style.display = "none";
        });

        const prefixes = document.querySelectorAll(".el-input__prefix");
        prefixes.forEach((prefix) => {
          prefix.style.display = "none";
        });
      });
    },

    getCategoryClass(category) {
      if (!category) return "category-default";

      const lowerCategory = category.toLowerCase();
      if (
        lowerCategory.includes("outdoor concert") ||
        lowerCategory.includes("dance battle") ||
        lowerCategory.includes("magic show") ||
        lowerCategory.includes("art exhibition")
      ) {
        return "category-red";
      } else if (
        lowerCategory.includes("food festival") ||
        lowerCategory.includes("movie screening") ||
        lowerCategory.includes("carnival")
      ) {
        return "category-yellow";
      } else if (
        lowerCategory.includes("performance") ||
        lowerCategory.includes("food") ||
        lowerCategory.includes("parade") ||
        lowerCategory === "food truck"
      ) {
        return "category-blue";
      }

      return "category-default";
    },

    fetchEvents() {
      this.loading = true;

      // Update query params with selected category if any
      if (this.selectedCategory) {
        this.queryParams.category = this.selectedCategory;
      } else {
        this.queryParams.category = "";
      }

      listEvent(this.queryParams)
        .then((response) => {
          // according to the response seen in the browser, the backend directly returns an array
          this.eventList = Array.isArray(response) ? response : [];
          console.log("Fetched events:", this.eventList);
          this.loading = false;
          this.addEventMarkers();
        })
        .catch((error) => {
          this.$message.error("Failed to fetch events: " + error.message);
          this.loading = false;
          // Mock event data if fetch fails
          this.eventList = [
            {
              id: "mock1",
              title: "Mock Event 1",
              category: "Mock Category",
              latitude: "37.7749",
              longitude: "-122.4194",
              address: "San Francisco, CA",
              location: "San Francisco, CA",
              distance: 1.2,
              content: "This is a mock event used when the backend fails.",
              comments: [
                {
                  id: "mock1-c1",
                  username: "Alice",
                  content: "Looking forward to this mock event!",
                  created_at: new Date().toISOString(),
                },
              ],
              img: "",
              created_at: new Date().toISOString(),
              start_at: new Date().toISOString(),
            },
            {
              id: "mock2",
              title: "Mock Event 2",
              category: "Mock Category",
              latitude: "34.0522",
              longitude: "-118.2437",
              address: "Los Angeles, CA",
              location: "Los Angeles, CA",
              distance: 2.5,
              content: "Another mock event for demonstration.",
              comments: [],
              img: "",
              created_at: new Date().toISOString(),
              start_at: new Date().toISOString(),
            },
          ];
          this.addEventMarkers();
        });
    },

    initMap() {
      MapUtils.loadGoogleMapsAPI(() => {
        this.createMapInstance();
      });
    },

    createMapInstance() {
      // Create map instance
      this.map = new google.maps.Map(document.getElementById("map"), {
        center: MapUtils.getDefaultPosition(),
        zoom: 12.8,
        styles: MapUtils.getMapStyles(),
        mapTypeControl: false,
        streetViewControl: false,
        fullscreenControl: false,
        gestureHandling: "greedy",
        keyboardShortcuts: false,
        reportError: false,
      });

      // Get user location - prioritize using cache
      const cachedPosition = MapUtils.getCachedUserPosition();
      if (cachedPosition) {
        // If there is a cached position, use it directly
        this.updateUserLocation(cachedPosition);
      } else {
        // No cache, retrieve location again
        MapUtils.getUserLocation({
          onSuccess: (position) => {
            this.updateUserLocation(position);
          },
          onError: (error) => {
            console.warn("Failed to get location:", error.message);
            this.$message.warning(
              "Could not get your location. Using default."
            );
          },
        });
      }

      // Do not add event markers here, but after fetchEvents completes
      // Do not call this.addEventMarkers();
    },

    updateUserLocation(position) {
      this.map.setCenter(position);

      if (this.userMarker) {
        this.userMarker.setPosition(position);
      } else {
        this.userMarker = MapUtils.createUserLocationMarker(this.map, position);
      }
    },

    addEventMarkers() {
      if (!this.map || !this.eventList.length) return;

      console.log("Adding markers for events:", this.eventList);

      // Clear existing markers
      this.eventMarkers.forEach((marker) => marker.setMap(null));
      this.eventMarkers = [];

      // Add new markers
      this.eventList.forEach((event) => {
        try {
          // check if latitude and longitude are valid
          if (event.latitude && event.longitude) {
            // try to convert string to number
            const lat = parseFloat(event.latitude);
            const lng = parseFloat(event.longitude);

            // ensure valid numbers
            if (!isNaN(lat) && !isNaN(lng)) {
              event.position = { lat, lng };
              console.log(
                `Created position for event ${event.id}:`,
                event.position
              );
            } else {
              console.warn(
                `Invalid coordinates for event ${event.id}:`,
                event.latitude,
                event.longitude
              );
            }
          } else {
            console.warn(`Missing coordinates for event ${event.id}`);
          }

          if (!event.position) return;

          const marker = MapUtils.createEventMarker(
            this.map,
            event,
            (clickedEvent) => {
              this.navigateToEventDetail(clickedEvent);
            }
          );

          if (marker) {
            this.eventMarkers.push(marker);
          }
        } catch (error) {
          console.error(`Error creating marker for event ${event.id}:`, error);
        }
      });

      console.log(`Added ${this.eventMarkers.length} markers to map`);
    },

    initCreateEventMap() {
      if (!this.createMap && google && google.maps) {
        // Initialize geocoder
        this.geocoder = new google.maps.Geocoder();

        // Use the user location from the main map or cached position
        let initialPosition;
        if (this.userMarker) {
          // If the main map has a user marker, use its position
          initialPosition = this.userMarker.getPosition();
        } else {
          // Otherwise, try to use the cached position
          const cachedPosition = MapUtils.getCachedUserPosition();
          if (cachedPosition) {
            initialPosition = cachedPosition;
          } else {
            // Finally, use the default position
            initialPosition = MapUtils.getDefaultPosition();
          }
        }

        this.selectedPosition = initialPosition;

        const mapEl = document.getElementById("createEventMap");
        if (!mapEl) return;

        this.createMap = new google.maps.Map(mapEl, {
          center: initialPosition,
          zoom: 14,
          styles: MapUtils.getMapStyles(),
          mapTypeControl: false,
          streetViewControl: false,
          fullscreenControl: false,
          gestureHandling: "greedy",
          keyboardShortcuts: false,
          reportError: false,
        });

        this.selectedMarker = new google.maps.Marker({
          position: initialPosition,
          map: this.createMap,
          title: "Selected location",
          draggable: true,
        });

        // Listen for marker drag events
        this.selectedMarker.addListener("dragend", (event) => {
          const position = {
            lat: event.latLng.lat(),
            lng: event.latLng.lng(),
          };
          this.updateSelectedPosition(position);
        });

        // Listen for map click events
        this.createMap.addListener("click", (event) => {
          const position = {
            lat: event.latLng.lat(),
            lng: event.latLng.lng(),
          };
          this.selectedMarker.setPosition(position);
          this.updateSelectedPosition(position);
        });

        // Immediately update position and get address
        this.updateSelectedPosition(initialPosition);
      }
    },

    updateSelectedPosition(position) {
      this.selectedPosition = position;

      // Update latitude and longitude display
      this.selectedAddress = `Lat: ${position.lat.toFixed(
        6
      )}, Lng: ${position.lng.toFixed(6)}`;
      this.formattedAddress = "Getting address..."; // Set loading state

      // Use reverse geocoding to get address
      if (this.geocoder) {
        this.geocoder.geocode({ location: position }, (results, status) => {
          if (status === "OK" && results[0]) {
            this.formattedAddress = results[0].formatted_address;
          } else {
            this.formattedAddress = "Unable to get address";
            console.warn("Geocoder failed due to: " + status);
          }
        });
      }
    },

    toggleSidebar() {
      this.sidebarCollapsed = !this.sidebarCollapsed;
    },

    navigateToEventDetail(event) {
      this.$router.push(`/event/${event.id}`);
    },

    showEventDetail(event) {
      // Navigate to event detail page from map marker click
      this.$router.push(`/event/${event.id}`);
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

    formatEventTime(dateString) {
      if (!dateString) return "";

      // Append "Z" so it's parsed as UTC
      const date = new Date(dateString + "Z");
      return date.toLocaleString("en-US", {
        timeZone: "America/New_York",
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    },

    openCreateEventModal() {
      if (!checkLoggedIn()) {
        this.$message.warning("Please login first to report an event");
        this.$router.push("/login");
        return;
      }

      this.createEventDialogVisible = true;
      // Reset form
      this.newEventForm = {
        title: "",
        category: "",
        content: "",
        image: null,
        imageUrl: null,
        start_at: "",
        end_at: "",
      };

      this.$nextTick(() => {
        this.initCreateEventMap();
        this.fixDatePickerIcons();
      });
    },

    closeCreateEventDialog() {
      // Clean up object URL when closing dialog
      if (this.newEventForm.imageUrl) {
        URL.revokeObjectURL(this.newEventForm.imageUrl);
      }
      this.createEventDialogVisible = false;
      // Reset form
      this.newEventForm = {
        title: "",
        category: "",
        content: "",
        image: null,
        imageUrl: null,
        start_at: "",
        end_at: "",
      };
    },

    beforeImageUpload(file) {
      // Check file type
      const isImage = file.type.startsWith('image/');
      const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
      const isAllowedType = allowedTypes.includes(file.type.toLowerCase());
      
      if (!isImage || !isAllowedType) {
        this.$message.error('Please upload a valid image file (JPG, PNG, GIF)');
        return false;
      }

      // Check file size (limit to 5MB)
      const maxSize = 5 * 1024 * 1024; // 5MB in bytes
      const isLessThan5M = file.size < maxSize;
      
      if (!isLessThan5M) {
        this.$message.error('Image size cannot exceed 5MB');
        return false;
      }

      return true;
    },

    handleImageChange(file) {
      // Only proceed if file is valid
      if (!this.beforeImageUpload(file.raw)) {
        return;
      }

      // Revoke the old object URL if it exists
      if (this.newEventForm.imageUrl) {
        URL.revokeObjectURL(this.newEventForm.imageUrl);
      }
      
      if (file) {
        this.newEventForm.image = file.raw;
        // Create an object URL for preview
        this.newEventForm.imageUrl = URL.createObjectURL(file.raw);
      } else {
        this.newEventForm.image = null;
        this.newEventForm.imageUrl = null;
      }
    },

    async uploadFile(file, folder = 'events') {
      try {
        // Set the folder path
        const folderPath = folder ? `${folder}/` : '';
        // Get the file name
        const fileName = file.name;
        // Generate a unique file name
        const uniqueFileName = `${folderPath}${Date.now()}-${fileName}`;
        
        // Use the Aliyun OSS to upload the file
        const result = await this.ossClient.put(uniqueFileName, file);
        console.log('Upload file Success:', result);
        return result.url;
      } catch (err) {
        console.error('Upload file failed:', err);
        throw err;
      }
    },

    async submitCreateEvent() {
      if (!this.validateEventForm()) {
        return;
      }

      this.loading = true;

      try {
        // Upload image first if exists
        let imageUrl = null;
        if (this.newEventForm.image) {
          imageUrl = await this.uploadFile(this.newEventForm.image);
        }

        // Create FormData object for the API request
        const formData = new FormData();
        formData.append("title", this.newEventForm.title);
        formData.append("category", this.newEventForm.category);
        formData.append("content", this.newEventForm.content);

        // Add the image URL if uploaded successfully
        if (imageUrl) {
          formData.append("img", imageUrl);
        }

        // process start_at and end_at
        if (this.newEventForm.start_at) {
          const startDate = new Date(this.newEventForm.start_at);
          if (!isNaN(startDate.getTime())) {
            formData.append("start_at", startDate.toISOString().replace("Z", ""));
          }
        }

        if (this.newEventForm.end_at) {
          const endDate = new Date(this.newEventForm.end_at);
          if (!isNaN(endDate.getTime())) {
            formData.append("end_at", endDate.toISOString().replace("Z", ""));
          }
        }

        formData.append("latitude", this.selectedPosition.lat);
        formData.append("longitude", this.selectedPosition.lng);
        formData.append("address", this.formattedAddress || this.selectedAddress);

        // Call the API to create the event
        await createEvent(formData);
        this.$message.success("Event created successfully!");
        this.closeCreateEventDialog();
        this.fetchEvents(); // Refresh the event list
      } catch (error) {
        this.$message.error(
          "Failed to create event: " +
            (error.response?.data?.detail || error.message)
        );
      } finally {
        this.loading = false;
      }
    },

    useMyLocation() {
      MapUtils.getUserLocation({
        onSuccess: (position) => {
          if (this.createMap && this.selectedMarker) {
            this.createMap.setCenter(position);
            this.selectedMarker.setPosition(position);
            this.updateSelectedPosition(position);
          }
        },
        onError: (error) => {
          this.$message.error("Failed to get location: " + error.message);
        },
      });
    },

    validateEventForm() {
      // Validate title
      if (!this.newEventForm.title) {
        this.$message.warning("Please enter an event title");
        return false;
      }

      if (this.newEventForm.title.length < 3) {
        this.$message.warning("Event title must be at least 3 characters");
        return false;
      }

      // Validate category
      if (!this.newEventForm.category) {
        this.$message.warning("Please select an event category");
        return false;
      }

      // Validate content
      if (!this.newEventForm.content) {
        this.$message.warning("Please enter event description");
        return false;
      }

      if (this.newEventForm.content.length < 10) {
        this.$message.warning(
          "Event description must be at least 10 characters"
        );
        return false;
      }

      // Validate start time and end time
      if (!this.newEventForm.start_at) {
        this.$message.warning("Please select a start time");
        return false;
      }

      if (!this.newEventForm.end_at) {
        this.$message.warning("Please select an end time");
        return false;
      }

      // Convert both values to Date objects for comparison
      const startDate =
        typeof this.newEventForm.start_at === "string"
          ? new Date(this.newEventForm.start_at)
          : this.newEventForm.start_at;

      const endDate =
        typeof this.newEventForm.end_at === "string"
          ? new Date(this.newEventForm.end_at)
          : this.newEventForm.end_at;

      if (startDate >= endDate) {
        this.$message.warning("End time must be after start time");
        return false;
      }

      // Validate location
      if (!this.selectedPosition) {
        this.$message.warning("Please select an event location");
        return false;
      }

      return true;
    },

    // get image URL, if not available, return local default image
    // getImageUrl(url) {
    //   if (!url) {
    //     // use local default image
    //     return new URL("@/assets/no-image.png", import.meta.url).href;
    //   }
    //   // if URL starts with http, return it directly
    //   if (url && (url.startsWith("http://") || url.startsWith("https://"))) {
    //     return url;
    //   }
    //   // otherwise, add domain name
    //   return `${import.meta.env.VITE_API_URL}${url}`;
    // },
  },
};
</script>

<style>
.event-page {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

.page-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    135deg,
    rgba(229, 245, 255, 0.5) 0%,
    rgba(243, 239, 255, 0.5) 100%
  );
  z-index: 0;
}

.event-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  z-index: 1;
}

.map-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.map {
  width: 100%;
  height: 100%;
}

.event-sidebar {
  position: fixed;
  right: 20px;
  top: 110px;
  width: 380px;
  height: calc(100% - 140px);
  
  border-radius: 16px;
  z-index: 100;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.event-sidebar.collapsed {
  width: 0;
  overflow: hidden;
  padding: 0;
  opacity: 0;
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 20px 10px 20px;
  margin-bottom: 10px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.header-left {
  display: flex;
  align-items: center;
}

.sidebar-header h2 {
  margin: 0 0 0 10px;
  font-size: 20px;
  font-weight: 500;
}

.report-btn {
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
  justify-content: center;
}

.report-btn:hover {
  transform: translateY(-2px);
  background: rgba(64, 158, 255, 0.25);
  box-shadow: 0 4px 15px rgba(64, 158, 255, 0.15);
}

.report-btn:active {
  transform: scale(0.98);
}

.sidebar-toggle {
  width: 35px;
  height: 35px;
  background: rgba(64, 158, 255, 0.15);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  color: #409eff;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-radius: 10px;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.sidebar-toggle:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  background: rgba(64, 158, 255, 0.25);
}

.hamburger-icon {
  width: 18px;
  height: 16px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.hamburger-icon span {
  display: block;
  height: 2px;
  width: 100%;
  background-color: #409eff;
  border-radius: 1px;
}

.collapsed-toggle {
  position: fixed;
  right: 0;
  top: 130px;
  width: 35px;
  height: 35px;
  background: rgba(64, 158, 255, 0.15);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  color: #409eff;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-radius: 10px 0 0 10px;
  z-index: 99;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-right: none;
}

.collapsed-toggle:hover {
  background: rgba(64, 158, 255, 0.25);
}

.event-list-wrapper {
  display: flex;
  flex-direction: column;
  height: calc(100% - 60px);
  padding: 0 20px 20px 20px;
  overflow-y: auto;
}

.search-filter {
  margin-bottom: 15px;
}

.search-filter-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.search-input {
  flex: 1;
}

.category-select {
  width: 180px;
}

.event-list {
  flex: 1;
  overflow-y: auto;
  padding-bottom: 20px;
}

.event-item {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  padding: 15px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.event-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  background: rgba(255, 255, 255, 0.4);
}

.event-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-right: 15px;
  flex-shrink: 0;
}

.category-red {
  background-color: #f56c6c;
}

.category-orange {
  background-color: #e6a23c;
}

.category-yellow {
  background-color: #f2c037;
}

.category-blue {
  background-color: #409eff;
}

.category-default {
  background-color: #909399;
}

.event-details {
  flex: 1;
}

.event-details h3 {
  color: #333;
  margin: 0 0 5px 0;
  font-weight: 500;
}

.event-meta {
  color: #555;
  font-size: 13px;
}

.location-info,
.time-info {
  margin-bottom: 5px;
}

#event-detail-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 15px;
  overflow-y: auto;
}

.detail-header {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.detail-header button {
  margin-right: 10px;
}

.detail-header h2 {
  margin: 0;
  font-size: 18px;
}

.detail-body {
  flex: 1;
}

.detail-event-image {
  margin: 15px 0;
  border-radius: 8px;
  overflow: hidden;
}

.detail-event-image .el-image {
  width: 100%;
}

.detail-event-content {
  margin-bottom: 20px;
  line-height: 1.5;
}

.detail-event-comments {
  margin-top: 20px;
}

.comment-form {
  margin-bottom: 15px;
}

.comment-form .el-button {
  margin-top: 10px;
}

.comment-items {
  margin-top: 15px;
}

.comment-item {
  padding: 10px;
  margin-bottom: 10px;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
}

.comment-username {
  font-weight: bold;
}

.comment-time {
  color: #999;
  font-size: 12px;
}

.comment-content {
  line-height: 1.4;
}

.no-comments {
  color: #999;
  font-style: italic;
  text-align: center;
  padding: 20px 0;
}

.create-map {
  height: 200px;
  margin-top: 10px;
  border-radius: 4px;
}

.address-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}
/* 
@media (max-width: 768px) {
  .event-sidebar {
    width: 100%;
    height: 50%;
    bottom: 0;
    top: auto;
    right: 0;
  }

  .event-sidebar.collapsed {
    height: 0;
    width: 100%;
  }

  .sidebar-toggle {
    width: 30px;
    height: 30px;
  }

  .collapsed-toggle {
    top: calc(50% - 15px);
    right: 0;
    width: 30px;
    height: 30px;
  }
} */

/* Add Report Event dialog styles */
.report-event-dialog {
  border-radius: 16px;
  overflow: hidden;
}

/* Form styles */
.report-form {
  padding: 10px 0;
  text-align: left;
}

.form-section-title {
  color: #333;
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 10px;
  margin-top: 20px;
  text-align: left;
}

.category-container {
  margin-bottom: 20px;
  text-align: left;
}

.styled-input {
  margin-bottom: 20px;
  width: 100%;
}

.styled-input .el-input__inner,
.styled-input .el-textarea__inner {
  background: rgba(255, 255, 255, 0.5);
  border-radius: 12px;
  padding: 12px 15px;
  border: 1px solid rgba(255, 255, 255, 0.5);
  font-size: 14px;
  color: #333;
}

.upload-container {
  width: 100%;
  margin-bottom: 20px;
}

.full-width-upload {
  width: 100%;
}

.upload-box {
  width: 100%;
  height: 70px;
  background: rgba(255, 255, 255, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #333;
  font-size: 14px;
  padding: 0;
  text-align: center;
  transition: all 0.3s ease;
}

.upload-box span {
  display: block;
  width: 100%;
  text-align: center;
}

.upload-box:hover {
  background: rgba(255, 255, 255, 0.7);
  border-color: rgba(255, 255, 255, 0.7);
}

.image-preview {
  width: 100%;
  height: 200px;
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s ease;
  border: 2px solid transparent;
}

.image-preview:focus-within {
  border-color: #409eff;
  outline: none;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
}

.image-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.image-overlay span {
  color: white;
  font-size: 14px;
  padding: 8px 16px;
  background: rgba(0, 0, 0, 0.5);
  border-radius: 4px;
}

.image-preview:hover .image-overlay,
.image-preview:focus-within .image-overlay {
  opacity: 1;
}

.category-radio-group {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.category-radio {
  margin: 0;
  padding: 0;
}

.el-radio {
  margin-right: 0;
  margin-bottom: 0;
}

.el-radio__input {
  display: none;
}

.el-radio__label {
  padding: 8px 16px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: #606266;
  transition: all 0.3s ease;
  font-weight: 500;
  cursor: pointer;
  display: block;
}

.el-radio__input.is-checked + .el-radio__label {
  background: rgba(64, 158, 255, 0.15);
  color: #409eff;
  border-color: rgba(64, 158, 255, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(64, 158, 255, 0.15);
}

.el-radio:hover .el-radio__label {
  transform: translateY(-2px);
  background: rgba(255, 255, 255, 0.3);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.el-radio__input.is-checked:hover .el-radio__label {
  background: rgba(64, 158, 255, 0.25);
}

.address-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  background: rgba(255, 255, 255, 0.5);
  padding: 10px 15px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.5);
}

.address-text {
  display: flex;
  align-items: center;
  flex: 1;
  overflow: hidden;
  color: #333;
}

.location-icon {
  color: #409eff;
  margin-right: 8px;
  font-size: 16px;
}

.location-btn {
  margin-left: 15px;
  background: rgba(64, 158, 255, 0.15) !important;
  backdrop-filter: blur(8px) !important;
  -webkit-backdrop-filter: blur(8px) !important;
  border-radius: 10px !important;
  border: 1px solid rgba(255, 255, 255, 0.3) !important;
  color: #409eff !important;
  font-weight: 500 !important;
  transition: all 0.3s ease;
}

.location-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  background: rgba(64, 158, 255, 0.25) !important;
}

.create-map {
  height: 220px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.dialog-footer {
  text-align: center;
  padding: 10px 0;
}

.cancel-btn {
  background: rgba(144, 147, 153, 0.15) !important;
  backdrop-filter: blur(8px) !important;
  -webkit-backdrop-filter: blur(8px) !important;
  border-radius: 10px !important;
  border: 1px solid rgba(255, 255, 255, 0.3) !important;
  color: #606266 !important;
  font-weight: 500 !important;
  transition: all 0.3s ease;
  padding-left: 15px;
  padding-right: 15px;
}

.cancel-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  background: rgba(144, 147, 153, 0.25) !important;
}

.submit-btn {
  background: rgba(64, 158, 255, 0.15) !important;
  backdrop-filter: blur(8px) !important;
  -webkit-backdrop-filter: blur(8px) !important;
  border-radius: 10px !important;
  border: 1px solid rgba(255, 255, 255, 0.3) !important;
  color: #409eff !important;
  font-weight: 500 !important;
  transition: all 0.3s ease;
  padding-left: 20px;
  padding-right: 20px;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  background: rgba(64, 158, 255, 0.25) !important;
}

/* Add custom date picker specific styles */
.custom-date-picker {
  width: 100%;
}

.custom-date-picker .el-input__inner {
  padding-left: 15px !important;
}

.custom-date-picker .el-input__prefix,
.custom-date-picker .el-input__suffix {
  display: none !important;
}

/* Alternative selectors */
.custom-date-picker /deep/ .el-input__prefix,
.custom-date-picker /deep/ .el-input__suffix {
  display: none !important;
}

.custom-date-picker ::v-deep .el-input__prefix,
.custom-date-picker ::v-deep .el-input__suffix {
  display: none !important;
}

/* Fix for date picker empty circles */
.el-date-picker .el-input__prefix {
  display: none;
}

/* Hide time icon in date picker */
.styled-input .el-input__icon.el-icon-time {
  display: none;
}

/* Also target the specific time icon */
.el-input__icon.el-icon-time {
  display: none !important;
}

/* Alternative selectors for different Vue versions */
.el-date-picker /deep/ .el-input__prefix {
  display: none;
}

.styled-input /deep/ .el-input__icon.el-icon-time {
  display: none;
}

.el-date-picker ::v-deep .el-input__prefix {
  display: none;
}

.styled-input ::v-deep .el-input__icon.el-icon-time {
  display: none;
}
</style>
