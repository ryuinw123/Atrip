<template>
  <v-content>
    <TripBar/>
    <div class="about">
      <h1>This is an about page</h1>
    </div>
  </v-content>
</template>

<script>
// @ is an alias to /src
import TripBar from "../components/TripBar";

export default {
  name: "About",
  components: {
    TripBar
  },
};
</script>