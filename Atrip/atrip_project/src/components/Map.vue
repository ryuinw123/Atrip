<template>
  <div>
    <div v-if="Mark == 0">
      <GmapMap
        :center="coordinates"
        :zoom="16"
        style=" width: 32vw; height:800px;"
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
        <!-- <GmapMarker
          v-for="(m, index) in userlocation"
          :key="index"
          :position="m"
          :clickable="true"
          :draggable="false"
          @click="centerPosition = m"
        /> -->
      </GmapMap>
    </div>
    <div v-else>
      <GmapMap
        :center="centerPosition[Mark - 1]"
        :zoom="16"
        style=" width: 32vw; height:800px;"
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
          v-for="(m, index) in this.loca"
          :key="index"
          :position="m"
          :clickable="true"
          :draggable="false"
          @click="centerPosition = m"
        />
      </GmapMap>
    </div>
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
      centerPosition: this.loca,
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
  //props: ["loca", "Mark",],
};
</script>
