<template>
  <v-app>
    <v-content>
      <router-view></router-view>
    </v-content>
  </v-app>
</template>

<script>

import Home from "./views/Home";
import SignIn from "./views/SignIn";
import Register from "./views/Register";
import AllPlan from "./views/AllPlan";
import YourPlan from "./views/YourPlan";
import Account from "./views/Account";
import Landing from "./views/Landing";
import PlaceInfo from "./views/PlaceInfo";
import TripInfo from "./views/TripInfo";
import ListTrip from "./views/ListTrip";
import AddPlace from "./views/AddPlace";
import ApprovePlace from "./views/ApprovePlace";
import ApproveInfo from "./views/ApproveInfo";

export default {
  name: "App",

  components: {
    Home,Register,SignIn,AllPlan,YourPlan,Account,Landing,PlaceInfo,TripInfo,ListTrip,AddPlace,ApprovePlace,ApproveInfo
  },

  data: () => ({
    //
  }),
};
</script>


