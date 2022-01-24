<template>
  <div class="TripBar">
    <v-toolbar>
      <v-toolbar-title class="headline text-uppercase mx-5 mt-1">
        <v-btn link to="/Home" class="mb-2 mr-5" icon><v-icon size="35">mdi-home</v-icon></v-btn>
        <span >A Trip</span>
      </v-toolbar-title>
      <v-btn plain link to="/AllPlan" class="mx-5">View All Plan</v-btn>
      <v-btn plain link to="/ListTrip" class="mx-5">Start your plan</v-btn>
      <v-btn plain link to="/AddPlace" class="mx-5">Recommend Place</v-btn>
      <v-btn v-if="this.$store.getters.StateRole == 'Admin'" plain link to="/ApprovePlace" class="mx-5">Approve Place</v-btn>
      <v-spacer></v-spacer>
      <v-btn plain link to="/Account" class="mx-5">account</v-btn>
      <v-btn plain @click = "logout" class="mx-5" color="error">log out</v-btn>
    </v-toolbar>
  </div>
</template>
<script>
export default {
  data() {
    return {
      
    }
  },
  methods: {
    logout(){
      this.$store.dispatch("LogOut")
      this.$router.push("/");
    }
  },
};
</script>


<style scoped>
  .TripBar{
    position: fixed;
    width: 100%;
    z-index: 99;
  }
</style>

