<template>
  <div>
      <GmapMap
        :center="coordinates"
        :zoom="16"
        style=" width: 37vw; height:300px;"
        :options="{
          zoomControl: false,
          mapTypeControl: false,
          scaleControl: false,
          streetViewControl: true,
          rotateControl: false,
          fullscreenControl: false,
          disableDefaultUi: false,
        }"
      >
        <GmapMarker
          v-for="(m, index) in userlocation"
          :key="index"
          :position="m"
          :clickable="true"
          :draggable="true"
          @click="coordinates = m"
        />
      </GmapMap>
    
  </div>
</template>

<script>
export default {
  data() {
    return {
      coordinates: {
        getlat: 0,
        getlng: 0,
      },
      recenter:{

      },
      userlocation: [
        {
          lat: 0,
          lng: 0,
        },
      ],
    };
  },

  // " Get Location User "
  created: function() {
    this.$getLocation({})
      .then((coordinates) => {
        this.coordinates = coordinates;
        this.userlocation[0].lat = coordinates.lat;
        this.userlocation[0].lng = coordinates.lng;

      })
      .catch((error) => alert(error));

    
  },
 
};
</script>
