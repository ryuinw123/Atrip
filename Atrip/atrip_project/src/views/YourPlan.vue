<template>
  <v-content>
    <TripBar/>
    <div class="YourPlan">
      <img class="bg-img">
      <div class="rec"></div>
      <v-col cols="9">
        <v-form class="form">
          <v-row>
            <v-col cols="6"><div class="text-start">START</div> </v-col>
            <v-col cols="6"><div class="text-des">DESTINATION</div></v-col>
          </v-row>
          <v-row>
            <v-col cols="6">
              <v-text-field solo placeholder="Where your journey start ?" class="start-field"></v-text-field>
            </v-col>
            <v-col cols="6">
              <v-text-field solo placeholder="Where you want to go ?" class="des-field"></v-text-field>
            </v-col>
          </v-row>
          <v-btn class="plan-btn" link to="/ListTrip">PLAN TRIP</v-btn>
        </v-form>
      </v-col>
    </div>
  </v-content>
</template>

<script>
// @ is an alias to /src
import TripBar from "../components/TripBar";

export default {
  name: "YourPlan",
  components: {
    TripBar
  },
};
</script>

<style scoped>
  .YourPlan{
    position: relative;
  }

  .bg-img{
    position: absolute;
    width: 100vw;
    height: calc(100vh - 64px);
    left: -1px;
    top: 64px;
    
    background: url(../assets/mountain1.jpg);
    background-repeat: no-repeat;
    background-size: 100%;
    overflow: hidden;
  }

  .rec{
    position: absolute;
    width: 100vw;
    height: calc(100vh - 64px);
    top: 64px;
    background: linear-gradient(180deg, #FFFFFF 0%, rgba(255, 255, 255, 0) 100%);
    overflow: hidden;
  }

  .form{
    position: absolute;
    width: 1100px;
    height: 300px;
    left: calc(50% - 550px);
    top: 600px;
    background-color: rgba(255, 255, 255,0.3);
    border-radius: 31px;
  }

  .text-start{
    font-size: 30px;
    font-weight: 400;
    margin-left: 225px;
    margin-top: 30px;
  }

  .text-des{
    font-size: 30px;
    font-weight: 400;
    margin-left: 180px;
    margin-top: 30px;
  }

  .start-field{
    background-color: rgba(255, 255, 255,1);
    width: 300px;
    height: 48px;
    margin-left: 125px;
    margin-top: 10px;
  }

  .des-field{
    background-color: rgba(255, 255, 255,1);
    width: 300px;
    height: 48px;
    margin-left: 125px;
    margin-top: 10px;
  }

  .plan-btn{
    width: 200px;
    height: 60px;
    margin-left: 450px;
    margin-top: 50px;
    font-size: 20px;
  }
</style>