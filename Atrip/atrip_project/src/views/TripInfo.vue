<template>
  <v-content>
    <TripBar />

    <div class="TripInfo">
      <v-row>
        <v-col cols="5" class="tripZone">
          <v-card class="tripCard">
            <v-img
              :src="places[0].pictureURL"
              class="tripPic"
              v-if="showed"
            ></v-img>
            <Tripmap class="hidemap" v-if="showed" ref="Tripmap" />
            <Tripmap v-if="!showed" ref="Tripmap" />

            <v-divider></v-divider>
            <v-card-title class="tripTitle">
              {{ trip.nameTH }}
            </v-card-title>

            <v-card-title class="tripSubTitle">
              {{ trip.Username }}
              <v-spacer></v-spacer>
              <v-chip-group class="ma-2">
                <v-chip
                  v-for="province in trip.provinceTH_List.split(',')"
                  :key="province"
                  color="#FF9100"
                  outlined
                  >{{ province }}</v-chip
                >
                <v-chip color="#67A272" outlined @click="(showed = !showed), Showmap(),updateURL()" >แสดงแผนที่</v-chip>
                <v-chip color="#67A272" outlined v-if="!showed"><a v-bind:href="mapURL" target="_blank" rel="noopener">เริ่มเดินทาง</a></v-chip>
              </v-chip-group>
            </v-card-title>
            <v-divider class="mx-2" style="margin-top: -10px;"></v-divider>
            <v-col class="pb-15">
              <v-textarea
                v-if="this.$store.getters.StateUsername == this.trip.Username"
                v-model="description"
                filled
                label="ข้อมูลทริปเพิ่มเติม"
                height="250px"
                class="mr-2"
              ></v-textarea>
              <v-card-text v-else class="tripText">
                {{ description }}
              </v-card-text>
              <v-btn
                v-if="this.$store.getters.StateUsername == this.trip.Username"
                color="#FF9100"
                outlined
                class="saveTrip-btn ma-2"
                @click="saveChangeTrip"
              >
                บันทึก
                <v-icon class="ml-2">mdi-content-save</v-icon>
              </v-btn>
              <v-select
                v-if="this.$store.getters.StateUsername == this.trip.Username"
                v-model="status"
                :items="allStatus"
                label="สถานะ"
                class="chooseStatus ma-2"
              ></v-select>
            </v-col>
          </v-card>
        </v-col>
        <v-col cols="7" class="placeZone">
          <v-card class="placeCard mr-10">รายชื่อสถานที่</v-card>
          <v-card class="scrollCard">
            <v-virtual-scroll :items="places" :item-height="250" height="690">
              <template v-slot="place">
                <v-row>
                  <v-col cols="2" class="ml-2">
                    <v-card class="numberCard mb-5">
                      {{ place.index + 1 }}
                    </v-card>
                  </v-col>
                  <v-col cols="4">
                    <v-card class="mb-5">
                      <v-img
                        :src="place.item.pictureURL"
                        class="placeImage"
                      ></v-img>
                    </v-card>
                  </v-col>
                  <v-col>
                    <v-card class="placeInfoCard">
                      <v-card-title
                        class="ml-2"
                        style="font-weight: 400; font-size: 20px;"
                      >
                        {{ place.item.nameTH }}
                      </v-card-title>
                      <v-card-title
                        class="typeText ml-2 grey--text"
                        style="font-size: 18px;"
                      >
                        {{ place.item.typeTH }}
                        <v-spacer></v-spacer>
                        <v-chip class="mx-2" color="#FF9100" outlined>{{
                          place.item.provinceTH
                        }}</v-chip>
                      </v-card-title>
                      <v-btn
                        color="#FF9100"
                        outlined
                        class="viewInfo-btn ma-2"
                        style="font-size: 18px;"
                        @click="goPlaceInfo(place.item.keyID)"
                      >
                        ข้อมูลเพิ่มเติม
                        <v-icon class="ml-2"
                          >mdi-clipboard-text-search-outline</v-icon
                        >
                      </v-btn>
                    </v-card>
                  </v-col>
                </v-row>
              </template>
            </v-virtual-scroll>
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
import Tripmap from "../components/Tripmap";
export default {
  props: ["keyID"],
  name: "TripInfo",
  components: {
    TripBar,
    Tripmap,
  },

  data: () => ({
    trip: [],
    description: "",
    describe:
      "This is the text that should describe the hide-detail of this place but I don't know how to do it so I finally text this.This is the text that should describe the hide-detail of this place but I don't know how to do it so I finally text this.",
    places: [],
    location: [],
    status: "",
    allStatus: ["ส่วนตัว", "สาธารณะ"],
    showed: true,
    mapURL:"https://www.google.com/maps/dir/",
  }),

  methods: {
    count: function(item) {
      return item.length;
    },
    goPlaceInfo(keyID) {
      this.$router.push("/PlaceInfo/" + keyID);
    },
    updateURL() {
      this.mapURL= "https://www.google.com/maps/dir/"+this.$refs.Tripmap.getuserlat()+","+this.$refs.Tripmap.getuserlng();
      for(let i = 0; i < this.places.length; i++){
        this.mapURL+="/"+this.places[i].latitude+","+this.places[i].longitude
      }
      console.log(this.mapURL) 
    },
    Showmap() {
      //alert("Show");
      this.$refs.Tripmap.initMap();
      this.location = [];
      for (let i = 0; i < this.places.length; i++) {
        this.location.push({
          lat: this.places[i].latitude,
          lng: this.places[i].longitude,
        });
      }
      //this.$refs.Tripmap.clearRoute()
      this.$refs.Tripmap.displayRoute(this.location);
    },
    async saveChangeTrip() {
      await axios
        .post("tripInfo/" + this.keyID, {
          description: this.description,
          status: this.status,
        })
        .then((res) => {
          alert(res.data.msg);
          this.$router.push("/Account");
        });
    },
    async getInfo() {
      await axios
        .get("tripInfo/" + this.keyID)
        .then((res) => (this.trip = res.data[0]));
      await axios
        .post("getPlace", { place: this.trip.placeList })
        .then((res) => (this.places = res.data));
      console.log(this.trip);
      console.log(this.places);
      this.status = this.trip.status;
      this.description = this.trip.description;
    },
  },
  created: function() {
    this.getInfo();
  },
};
</script>

<style scoped>
.TripInfo {
  position: relative;
  min-height: 105vh;
  background-image: linear-gradient(
    to top,
    #77cee3,
    #6bc4dd,
    #60bad7,
    #55afd1,
    #4ba5cb,
    #439ec7,
    #3b96c3,
    #338fbf,
    #2c88bc,
    #2681ba,
    #227ab6,
    #2073b3
  );
}

.tripZone {
  width: 100%;
}

.tripCard {
  margin-left: 50px;
  margin-top: 100px;
  min-height: 825px;
}

.tripPic {
  width: 100%;
  height: 400px;
}

.tripTitle {
  margin-top: 20px;
  font-size: 45px;
  font-weight: 300;
}

.tripSubTitle {
  margin-left: 5px;
  margin-top: -20px;
  font-size: 20px;
  font-weight: 450;
  color: rgba(255, 153, 0, 0.822);
}

.tripText {
  margin-left: 5px;
  font-size: 20px;
  font-weight: 400;
  line-height: 30px;
}

.saveTrip-btn {
  position: absolute;
  left: 10px;
  bottom: 10px;
  font-size: 20px;
}

.chooseStatus {
  position: absolute;
  right: 10px;
  bottom: -5px;
  font-size: 20px;
}

.placeZone {
  width: 100%;
}

.placeCard {
  margin-top: 100px;
  margin-bottom: 20px;
  margin-left: 10%;
  width: 80%;
  height: 100px;
  font-size: 45px;
  font-weight: 300;
  text-align: center;
  padding-top: 15px;
}

.numberCard {
  background-color: #faae4b;
  color: black;
  font-size: 60px;
  font-weight: 80;
  text-align: center;
  padding-top: 40%;
  height: 90%;
}

.scrollCard {
  margin-left: 20px;
  padding-left: 15px;
  padding-top: 15px;
  padding-bottom: 15px;
  width: 95%;
  height: 73vh;
}

.placeImage {
  width: 100%;
  height: 200px;
}

.placeInfoCard {
  width: 470px;
  height: 90%;
}

.typeText {
  margin-top: -20px;
}
.hidemap {
  width: 0px;
  height: 0px;
}

.viewInfo-btn {
  position: absolute;
  left: 10px;
  bottom: 10px;
}
</style>
