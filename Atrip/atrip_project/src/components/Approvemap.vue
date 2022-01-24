<template>
  <div>
    <GmapMap
      :center="{ lat: this.Lat, lng: this.Lng }"
      :zoom="16"
      style=" width: 27vw; height:300px;"
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
        :position="{ lat: this.Lat, lng: this.Lng }"
      />
    </GmapMap>
  </div>
</template>

<script>
export default {
  props: ["Lat", "Lng"],
  data() {
    return {  
    };
  },


};
</script>
