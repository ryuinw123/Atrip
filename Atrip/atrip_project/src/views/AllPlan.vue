<template>
  <v-content>
    <TripBar />
    <div class="AllPlan">
      <v-row>
        <v-col cols="7" class="tripCol">
          <v-row class="ml-5 mt-1">
            <v-card class="allTripCard">
              <v-card-title class="tripTitle white--text">
                ทริปที่น่าสนใจ
                <v-spacer></v-spacer>
                <v-autocomplete
                  v-model="provinceValue"
                  :items="provinceNames"
                  filled
                  rounded
                  label="จังหวัด"
                  color="#FF9100"
                  class="searchByProvince mx-1"
                ></v-autocomplete>
                <v-autocomplete
                  v-model="tripNameValue"
                  :items="tripNames"
                  filled
                  rounded
                  label="ชื่อทริป"
                  color="#FF9100"
                  class="searchByName mx-1"
                ></v-autocomplete>
              </v-card-title>
            </v-card>
            <v-card class="backgroundCard">
              <v-card-title></v-card-title>
            </v-card>
          </v-row>
          <v-row v-for="(trip, i) in trips" :key="i">
            <v-card
              v-if="(trip.provinceTH_List.includes(provinceValue) || provinceValue == 'ทั้งหมด')
                    && (trip.nameTH.includes(tripNameValue) || tripNameValue == 'ทั้งหมด')"
              class="tripCard"
            >
              <v-img :src="trip.image" height="200px"></v-img>
              <v-card-title style="font-size: 25px;">
                {{ trip.nameTH }}
                <v-spacer></v-spacer>
                <v-chip-group class="ma-2">
                  <v-chip
                    v-for="province in trip.provinceTH_List.split(',')"
                    :key="province"
                    color="#FF9100"
                    outlined
                    >{{ province }}</v-chip
                  >
                </v-chip-group>
              </v-card-title>
              <v-card-subtitle style="font-size: 17px; font-weight: 450; color: rgba(255, 153, 0, 0.822);">
                {{ trip.Username }}
              </v-card-subtitle>
              <v-divider class="mx-5"></v-divider>
              <v-card-title class="black--text"
                >สถานที่ภายในทริป
                <v-card-subtitle class="mt-1"
                  >{{ trip.numPlace }} สถานที่
                  </v-card-subtitle>
                  <v-spacer></v-spacer>
                  <!-- <v-card-title>
                    Hello
                  </v-card-title> -->
                </v-card-title
              >
              <v-btn
                color="#FF9100"
                outlined
                class="viewInfo-btn ma-2"
                style="font-size: 18px"
                @click="goTripInfo(trip.keyID)"
              >
                ข้อมูลเพิ่มเติม
                <v-icon class="ml-2">mdi-clipboard-text-search</v-icon>
              </v-btn>
              <v-btn
                color="#FF9100"
                outlined
                class="saveTrip-btn ma-2"
                style="font-size: 18px"
                @click="saveTrip(trip.keyID)"
              >
                เซฟทริป
                <v-icon class="ml-2">mdi-book-plus</v-icon>
              </v-btn>

              <v-btn
                v-if="haveLiked(trip.keyID)"
                color="#FF9100"
                class="like-btn ma-2 white--text"
                style="font-size: 18px"
                @click="likeTrip(trip.keyID)"
              >
                ถูกใจ
                <v-icon class="ml-2">mdi-thumb-up-outline</v-icon>
              </v-btn>
              <v-btn
                v-else
                color="#FF9100"
                outlined
                class="like-btn ma-2"
                style="font-size: 18px"
                @click="likeTrip(trip.keyID)"
              >
                ถูกใจ
                <v-icon class="ml-2">mdi-thumb-up</v-icon>
              </v-btn>
            </v-card>
          </v-row>
        </v-col>
        <!-- RIGHT -->
        <v-col cols="4">
          <v-card class="adsCard">
            <v-img src="../assets/gallery1.jpg" height="200px"></v-img>
            <v-card-title>
              Musuem Of Contemporary Art (MOCA)
              <v-spacer></v-spacer>
              <v-chip color="#FF9100" outlined>กรุงเทพมหานคร</v-chip>
            </v-card-title>
            <v-divider class="mx-4"></v-divider>
            <v-card-text class="text--primary ma-2"
              >รายละเอียดสถานที่</v-card-text
            >
            <v-card-text>
              <!-- {{ trips[0] }} -->
            </v-card-text>
            <v-btn color="#FF9100" text class="viewPlace-btn ma-2"
              >ข้อมูลเพิ่มเติม</v-btn
            >
          </v-card>
        </v-col>
      </v-row>
    </div>
  </v-content>
</template>

<script>
// @ is an alias to /src
import TripBar from "../components/TripBar";
import axios from "axios";
export default {
  name: "AllPlan",
  components: {
    TripBar,
  },

  data: () => ({
    trips: [],
    provinceNames: ["ทั้งหมด"],
    provinceValue: "ทั้งหมด",
    tripNames: ["ทั้งหมด"],
    tripNameValue: "ทั้งหมด",
    liked: false
  }),
  methods: {
    count: function (item) {
      return item.length;
    },
    goTripInfo(keyID) {
      this.$router.push("/TripInfo/" + keyID);
    },
    haveLiked(keyID) {
      var i;
      for(i=0;i<this.$store.getters.StateLove.length;i++){
        if(this.$store.getters.StateLove[i] == keyID){
          return true;
        }
      }
      return false;
    },
    async saveTrip(keyID) {
      await axios.post("/saveTrip",{"key" : keyID,"id" : this.$store.getters.StateID}).then(res => {
        alert(res.data.msg)
      })
      this.$router.push("/Account");
    },
    async likeTrip(keyID) {
      await axios.post("/likeTrip",{"key" : keyID,"id" : this.$store.getters.StateID}).then(res => {
        if (res.data.msg == "success"){
          this.$store.dispatch("addLove",res.data.love);
        }
      })
    },
    async callTrips() {
      await axios
        .post("trip", { query: "" })
        .then((res) => (this.trips = res.data));
      var i;
      for (i = 0; i < this.trips.length; i++) {
        this.tripNames.push(this.trips[i].nameTH);
      }
    },
    async callProvinces() {
      await axios.get("province").then((res) => (this.provinces = res.data));
      var i;
      for (i = 0; i < this.provinces.length; i++) {
        this.provinceNames.push(this.provinces[i].provinceTH);
      }
    },
  },
  created: function () {
    this.callTrips();
    this.callProvinces();
  },
};
</script>

<style scoped>
.chipBar {
  margin: 10px;
  margin-top: 80px;
  width: 300px;
}

.tripCol{
  margin-top: 170px;
}

.allTripCard {
  position: fixed;
  margin-top: -110px;
  width: 55vw;
  min-height: 82px;
  z-index: 1;
  border-radius: 10px 50px 50px 0px;
}

.backgroundCard{
  position: fixed;
  margin-top: -70px;
  height: 875px;
  width: 55vw;
}

.tripCard {
  width: 80%;
  height: 440px;
  left: 10%;
  margin-bottom: 50px;
}

.tripTitle {
  background-color: #faae4b;
  font-size: 35px;
}

.searchByProvince {
  width: 0px;
  height: 55px;
}

.searchByName {
  width: 0px;
  height: 55px;
}

.choose-btn {
  margin-top: 73px;
}

.img_content {
  width: 250px;
  height: 125px;
}

.title {
  font-size: 100px;
}

.search-field {
  background-color: rgb(255, 255, 255, 100);
  width: 200px;
  height: 48px;
}

.inner-img {
  height: 200px;
}

.viewInfo-btn {
  position: absolute;
  bottom: 0px;
}

.saveTrip-btn {
  position: absolute;
  left: 200px;
  bottom: 0px;
}

.like-btn{
  position: absolute;
  right: 0px;
  bottom: 0px;
}

.adsCard {
  position: fixed;
  margin-top: 80px;
  margin-left: 90px;
  width: 650px;
  height: 500px;
}

.viewPlace-btn {
  position: absolute;
  bottom: 5px;
}

</style>