/* global google */

// Google Maps API loading status
// eslint-disable-next-line no-unused-vars
let isGoogleMapsLoaded = false;
let mapLoadCallbacks = [];

// NYC default position
const defaultPosition = { lat: 40.751712448459844, lng: -73.98179241229592 };

// Cache for storing user location
let cachedUserPosition = null;

// Default styles
const defaultStyles = [
  {
    featureType: "poi",
    elementType: "labels",
    stylers: [{ visibility: "off" }],
  },
];

/**
 * Load Google Maps API
 * @param {Function} callback Callback function after loading is complete
 */
export function loadGoogleMapsAPI(callback) {
  // If already loaded, directly call the callback
  // eslint-disable-next-line no-undef
  if (typeof google !== "undefined" && typeof google.maps !== "undefined") {
    isGoogleMapsLoaded = true;
    if (callback) callback();
    return;
  }

  // If loading, add to callback queue
  if (document.querySelector('script[src*="maps.googleapis.com/maps/api"]')) {
    if (callback) mapLoadCallbacks.push(callback);
    return;
  }

  // Add callback to the queue
  if (callback) mapLoadCallbacks.push(callback);

  // Global callback function
  window.initGoogleMap = () => {
    isGoogleMapsLoaded = true;
    mapLoadCallbacks.forEach((cb) => cb());
    mapLoadCallbacks = [];
  };

  // Create script tag and load
  const script = document.createElement("script");
  script.src =
    "https://maps.googleapis.com/maps/api/js?key=AIzaSyBZ1cnugGu4jiIWn3PipPsmG1Vli9hTEmo&libraries=geometry&callback=initGoogleMap&language=en&region=US&loading=async";
  script.async = true;
  script.defer = true;

  script.onerror = () => {
    console.error("Google Maps API loading failed");
    mapLoadCallbacks.forEach((cb) =>
      cb(new Error("Google Maps API loading failed"))
    );
    mapLoadCallbacks = [];
  };

  document.head.appendChild(script);
}

/**
 * Get map styles
 */
export function getMapStyles() {
  return defaultStyles;
}

/**
 * Get user location (using cache)
 * @param {Object} options Options
 * @param {boolean} options.forceRefresh Whether to force refresh (ignore cache)
 * @param {boolean} options.highAccuracy Whether to use high-accuracy positioning
 * @param {Function} options.onSuccess Success callback
 * @param {Function} options.onError Error callback
 */
export function getUserLocation({
  forceRefresh = false,
  highAccuracy = true,
  onSuccess,
  onError,
}) {
  // If there is a cached position and not forcing refresh, use the cache directly
  if (cachedUserPosition && !forceRefresh) {
    if (onSuccess) onSuccess(cachedUserPosition);
    return;
  }

  if (!navigator.geolocation) {
    if (onError) onError(new Error("Browser does not support geolocation"));
    return;
  }

  navigator.geolocation.getCurrentPosition(
    (position) => {
      const userPosition = {
        lat: position.coords.latitude,
        lng: position.coords.longitude,
      };

      // Cache user position
      cachedUserPosition = userPosition;

      if (onSuccess) onSuccess(userPosition);
    },
    (error) => {
      console.warn("Failed to get location:", error.message);
      if (onError) onError(error);
    },
    {
      enableHighAccuracy: highAccuracy,
      timeout: 10000,
      maximumAge: highAccuracy ? 0 : 300000,
    }
  );
}

/**
 * Get cached user position
 * @returns {Object|null} User position or null
 */
export function getCachedUserPosition() {
  return cachedUserPosition;
}

/**
 * Create user location marker
 * @param {Object} map Google map instance
 * @param {Object} position Position coordinates {lat, lng}
 * @param {Object} options Options
 * @returns {Object} Marker object
 */
export function createUserLocationMarker(map, position, options = {}) {
  // eslint-disable-next-line no-undef
  const marker = new google.maps.Marker({
    position,
    map,
    title: options.title || "Your Location",
    icon: {
      // eslint-disable-next-line no-undef
      path: google.maps.SymbolPath.CIRCLE,
      scale: 10,
      fillColor: "#4285F4",
      fillOpacity: 1,
      strokeColor: "#FFFFFF",
      strokeWeight: 2,
    },
  });

  // Add accuracy circle
  if (options.showAccuracyCircle !== false) {
    // eslint-disable-next-line no-undef
    new google.maps.Circle({
      map,
      center: position,
      radius: options.radius || 100,
      fillColor: "#4285F4",
      fillOpacity: 0.15,
      strokeColor: "#4285F4",
      strokeOpacity: 0.3,
      strokeWeight: 1,
    });
  }

  return marker;
}

/**
 * Get marker icon based on event type
 * @param {string} type Event type
 * @returns {Object} Icon configuration
 */
export function getIconForEventType(type) {
  // Normalize type to lowercase and trim spaces
  const normalizedType = (type || "").toLowerCase().trim();

  // Create icon configuration
  const iconConfig = {
    // Icon size
    scaledSize: new google.maps.Size(32, 32),
    // Icon anchor - centers the bottom of the icon at the coordinate
    anchor: new google.maps.Point(16, 32),
  };

  // Set icon based on event type
  if (normalizedType.includes("outdoor concert") || normalizedType.includes("concert")) {
    iconConfig.url = "/concert.png";
  } else if (normalizedType.includes("dance battle") || normalizedType.includes("dance")) {
    iconConfig.url = "/dance.png";
  } else if (normalizedType.includes("magic show") || normalizedType.includes("magic")) {
    iconConfig.url = "/magic.png";
  } else if (normalizedType.includes("art exhibition") || normalizedType.includes("art")) {
    iconConfig.url = "/art.png";
  } else if (normalizedType.includes("food festival") || normalizedType.includes("food festival")) {
    iconConfig.url = "/food.png";
  } else if (normalizedType.includes("movie screening") || normalizedType.includes("movie")) {
    iconConfig.url = "/movie.png";
  } else if (normalizedType.includes("carnival")) {
    iconConfig.url = "/carnival.png";
  } else if (normalizedType.includes("performance")) {
    iconConfig.url = "/performance.png";
  } else if (normalizedType.includes("food truck")) {
    iconConfig.url = "/foodtruck.png";
  } else if (normalizedType.includes("parade")) {
    iconConfig.url = "/parade.png";
  } else {
    // Default to concert icon
    iconConfig.url = "/concert.png";
  }

  return iconConfig;
}

/**
 * Create event marker
 * @param {Object} map Google map instance
 * @param {Object} event Event data
 * @param {Function} onClick Click callback
 * @returns {Object} Marker object
 */
export function createEventMarker(map, event, onClick) {
  if (!event.position) return null;

  // eslint-disable-next-line no-undef
  const marker = new google.maps.Marker({
    position: event.position,
    map,
    title: event.title,
    icon: getIconForEventType(event.category),
    // eslint-disable-next-line no-undef
    animation: google.maps.Animation.DROP,
  });

  if (onClick) {
    marker.addListener("click", () => onClick(event));
  }

  return marker;
}

/**
 * Get default position
 * @returns {Object} Default position coordinates
 */
export function getDefaultPosition() {
  return { ...defaultPosition };
}
