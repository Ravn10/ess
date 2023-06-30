<template>
    <div>
      <button @click="getLocation">Get Location</button>
      <p v-if="locationError">{{ locationError }}</p>
      <p v-if="location">{{ location }}</p>
    </div>
  </template>

  <script>
  export default {
    data() {
      return {
        location: null,
        locationError: null
      };
    },
    methods: {
      getLocation() {
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(
            this.handleSuccess,
            this.handleError
          );
        } else {
          this.locationError = "Geolocation is not supported by this browser.";
        }
      },
      handleSuccess(position) {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;
        this.location = `Latitude: ${latitude}, Longitude: ${longitude}`;
      },
      handleError(error) {
        switch (error.code) {
          case error.PERMISSION_DENIED:
            this.locationError = "User denied the request for geolocation.";
            break;
          case error.POSITION_UNAVAILABLE:
            this.locationError = "Location information is unavailable.";
            break;
          case error.TIMEOUT:
            this.locationError = "The request to get location timed out.";
            break;
          case error.UNKNOWN_ERROR:
            this.locationError = "An unknown error occurred.";
            break;
        }
      }
    }
  };
  </script>
