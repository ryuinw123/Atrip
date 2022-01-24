<template>
  <div>
    <div id="map"></div>
  </div>
</template>

<script>
export default {
  name: "Infomap",
  data() {
    return {
      map: null,
      marker: new google.maps.Marker(),
      markerlocation: null,
    
    };
  },
  
  methods: {
    initMap() {
      this.map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 13.405053591362147, lng: 101.00503381648156 },
        zoom: 14,
        mapTypeID: google.maps.MapTypeId.ROADMAP,
        zoomControl: false,
        mapTypeControl: false,
        scaleControl: false,
        streetViewControl: true,
        rotateControl: false,
        fullscreenControl: false,
        disableDefaultUi: false,
      });
      this.marker = new google.maps.Marker({
        position: { lat: 13.405053591362147, lng: 101.00503381648156 },
        map: this.map,
        animation: google.maps.Animation.DROP,
      });
      
      // Click on the Map To Mark
     
    },
    
  },
  mounted() {
    this.initMap();
  },

  // " Get Location User "
};
</script>
<style scoped>
#map {
  width: 27vw;
  height: 220px;
}
</style>
