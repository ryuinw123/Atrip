<template>
  <div>
    <div id="map"></div>
  </div>
</template>

<script>
export default {
  name: "Listmap",
  props: ["loca"],
  data() {
    return {
      map: null,
      markers: [],
      directionsService: new google.maps.DirectionsService(),
      directionsRenderer: new google.maps.DirectionsRenderer({
        draggable: true,
      }),
      coordinates: {
        getlat: 0,
        getlng: 0,
      },
      recenter: [
        {
          lat: 0,
          lng: 0,
        },
      ],
    };
  },
  created: function() {
    this.$getLocation({})
      .then((coordinates) => {
        this.coordinates = coordinates;
        this.recenter[0].lat = coordinates.lat;
        this.recenter[0].lng = coordinates.lng;
        this.initMap();
      })
      .catch((error) => alert(error));
  },
  
  methods: {
    initMap() {
      this.map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: this.recenter[0].lat, lng: this.recenter[0].lng },
        zoom: 12,
        mapTypeID: google.maps.MapTypeId.ROADMAP,
        zoomControl: false,
        mapTypeControl: false,
        scaleControl: false,
        streetViewControl: true,
        rotateControl: false,
        fullscreenControl: false,
        disableDefaultUi: false,
      });

      // Click on the Map To Mark
    },
    displayRoute(origin) {
      var WPS =[]
      for (let i = 0; i < origin.length; i++) {
        this.removeMarker(origin[i]);
      }
      for (let j = 1; j < origin.length - 1; j++) {
        WPS.push({ location: { lat: origin[j].lat, lng: origin[j].lng } });
      }
      this.directionsService= new google.maps.DirectionsService();
      this.directionsRenderer= new google.maps.DirectionsRenderer({
        draggable: true,
      });
      this.directionsService.route(
        {
          origin: origin[0],
          destination: origin[origin.length - 1],
          waypoints: WPS,
          travelMode: google.maps.TravelMode.DRIVING,
          avoidTolls: true,
        },
        (result, status) => {
          if (status === "OK" && result) {
            this.directionsRenderer.setDirections(result);
          } else {
            alert("Could not display directions due to: " + status);
          }
        }
      );
      this.directionsRenderer.setMap(this.map);
    },
    clearRoute() {
      if (this.directionsRenderer != null) {
        this.directionsRenderer.setMap(null);
        this.directionsRenderer = null;
      }
    },
    addMarker: function(getlat, getlng) {
      var markLatLng = new google.maps.LatLng(getlat, getlng);
      this.markers[markLatLng] = new google.maps.Marker({
        position: markLatLng,
        map: this.map,
        draggable: false,
        animation: google.maps.Animation.DROP,
      });
    },
    removeMarker(lat, long) {
      try {
        this.markers[new google.maps.LatLng(lat, long)].setMap(null);
      } catch (e) {}
    },
    moveToLocation(lat, lng) {
      const center = new google.maps.LatLng(lat, lng);
      this.map.panTo(center);
    },
  },
};
</script>
<style scoped>
#map {
  width: 32vw;
  height: 800px;
}
</style>
