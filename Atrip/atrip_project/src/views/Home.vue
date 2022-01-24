<template>
  <v-content>
    <TripBar/>
    <v-content>
      <div class="Home">
        <img class="img1">
        <div class="rec1"></div>
        <img class="img2">
        <v-card flat tile class="tripCard">
          <v-window
            v-model="tripIndex"
          >
            <v-window-item
              v-for="n in tripLength"
              :key="`card-${n}`"
            >
              <v-card class="tripPic">
                <v-row
                  class="fill-height"
                  align="center"
                  justify="center"
                >
                  <h1 style="font-size: 5rem;" class="white--text">
                    ทริป {{ n }}
                  </h1>
                  <v-item-group
                    v-model="tripIndex"
                    class="change-btn text-center"
                    mandatory
                  >
                    <v-item
                      v-for="n in tripLength"
                      :key="`btn-${n}`"
                      v-slot="{ active, toggle }"
                    >
                      <v-btn
                        :input-value="active"
                        icon
                        @click="toggle"
                      >
                        <v-icon color="white" >mdi-record</v-icon>
                      </v-btn>
                    </v-item>
                  </v-item-group>
                </v-row>
              </v-card>
            </v-window-item>
          </v-window>
        </v-card>

        <v-card flat tile class="placeCard">
          <v-window
            v-model="placeIndex"
          >
            <v-window-item
              v-for="n in placeLength"
              :key="`card-${n}`"
            >
              <v-card class="placePic">
                <v-row
                  class="fill-height"
                  align="center"
                  justify="center"
                >
                  <h1 style="font-size: 5rem;" class="white--text">
                    สถานที่ {{ n }}
                  </h1>
                  <v-item-group
                    v-model="placeIndex"
                    class="change-btn text-center"
                    mandatory
                  >
                    <v-item
                      v-for="n in placeLength"
                      :key="`btn-${n}`"
                      v-slot="{ active, toggle }"
                    >
                      <v-btn
                        :input-value="active"
                        icon
                        @click="toggle"
                      >
                        <v-icon color="white" >mdi-record</v-icon>
                      </v-btn>
                    </v-item>
                  </v-item-group>
                </v-row>
              </v-card>
            </v-window-item>
          </v-window>
        </v-card>
      </div>
    </v-content>
  </v-content>
</template>


<script>
// @ is an alias to /src
import TripBar from "../components/TripBar";

export default {
  name: "Home",
  components: {
    TripBar
  },
  data: () => ({
      tripLength: 3,
      tripIndex: 0,
      placeLength: 3,
      placeIndex: 0,
    }),

    methods: {
      
    },
};
</script>

<style scoped>
  .Home{
    position: relative;
    top: 63px;
  }

  .rec1{
    position: absolute;
    width: 50vw;
    height: calc(100vh - 63px);
    right: 0px;
    top: 0px;

    background: linear-gradient(0deg, rgba(255, 153, 154, 0.78), rgba(255, 153, 154, 0.78));
    overflow: hidden;
  }

  .img1 {
    position: absolute;
    width: 50vw;
    height: calc(100vh - 63px);
    right: 0px;
    top: 0px;

    background: url(../assets/road1.jpg);
    filter: drop-shadow(0px 4px 4px rgba(0, 0, 0, 0.25));
    background-size: 200%;
    background-repeat: no-repeat;
    background-position: center;
  }

  .img2 {
    position: absolute;
    width: 60vw;
    height: 60vh;
    left: calc(50% - 25vw);
    top: 10vh;
    
    background: url(../assets/road1.jpg);
    background-repeat: no-repeat;
    background-position: center;
    background-size: cover;
  }

  .change-btn{
    position: absolute;
    bottom: 0px;
  }

  .tripCard{
    position: absolute;
    left: 10vw;
    top: 55vh;
    width: 30vw;
  }

  .tripPic{
    height: 350px;
    background: url(../assets/temple1.jpg);
    background-repeat: no-repeat;
    background-size:cover;
    background-position: center;
  }

  .placeCard{
    position: absolute;
    left: 60vw;
    top: 55vh;
    width: 30vw;
  }

  .placePic{
    height: 350px;
    background: url(../assets/temple1.jpg);
    background-repeat: no-repeat;
    background-size:cover;
    background-position: center;
  }
</style>



