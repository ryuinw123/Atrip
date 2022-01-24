<template>
  <v-content>
    <TripBar />
    <div class="ApproveInfo">
      <v-row>
        <v-col cols="4" class="mapZone">
          <v-card class="mapCard pb-7">
            <v-card-title class="mx-4">แผนที่</v-card-title>
            <v-card class="mx-10 mb-7">
              <Approvemap v-bind:Lat="this.place.latitude" v-bind:Lng="this.place.longitude" />
              
            </v-card>
            <v-divider class="mx-5"></v-divider>
            <v-card-title class="mx-4">เว็บไซต์</v-card-title>
            <v-card-subtitle class="mx-7 subtitle">{{
              place.website
            }}</v-card-subtitle>
            <v-divider class="mx-5"></v-divider>
            <v-card-title class="mx-4">เบอร์โทรศัพท์</v-card-title>
            <v-card-subtitle class="mx-7 subtitle">{{
              place.phoneNumber
            }}</v-card-subtitle>
            <!-- <v-divider class="mx-5"></v-divider>
            <v-card-title class="mx-4">เวลาทำการ</v-card-title>
            <v-row>
              <v-card-subtitle class="ml-15 mr-15 subtitle">วันจันทร์</v-card-subtitle>
              <v-card-subtitle class="ml-12 mr-15 subtitle">วันอังคาร</v-card-subtitle>
              <v-card-subtitle class="ml-12 mr-15 subtitle">วันพุธ</v-card-subtitle>
            </v-row>
            <v-row>
              <v-chip class="ma-2 ml-12 mr-10" color="#FF9100" outlined>10:00 - 20.00</v-chip>
              <v-chip class="ma-2 mx-10" color="#FF9100" outlined>10:00 - 20.00</v-chip>
              <v-chip class="ma-2 mx-10" color="#FF9100" outlined>10:00 - 20.00</v-chip>
            </v-row>
            <v-row>
              <v-card-subtitle class="ml-14 mr-15 subtitle">วันพฤหัส</v-card-subtitle>
              <v-card-subtitle class="ml-13 mr-15 subtitle">วันศุกร์</v-card-subtitle>
              <v-card-subtitle class="ml-14 mr-15 subtitle">วันเสาร์</v-card-subtitle>
            </v-row>
            <v-row>
              <v-chip class="ma-2 ml-12 mr-10" color="#FF9100" outlined>10:00 - 20.00</v-chip>
              <v-chip class="ma-2 mx-10" color="#FF9100" outlined>10:00 - 20.00</v-chip>
              <v-chip class="ma-2 mx-10" color="#FF9100" outlined>10:00 - 20.00</v-chip>
            </v-row>
            <v-row justify="center">
              <v-card-subtitle class="mx-6 mr-15 subtitle">วันอาทิตย์</v-card-subtitle> 
            </v-row>
            <v-row>
              <v-chip class="ma-2" style="left: 227px;" color="#FF9100" outlined>10:00 - 20.00</v-chip>
            </v-row> -->
          </v-card>
        </v-col>
        <v-col cols="4" class="imageZone">
          <v-card class="imageCard">
            <v-img :src="place.pictureURL" class="imagePic"></v-img>
            <v-divider></v-divider>
            <v-card-title class="imageTitle">
              {{ place.nameTH }}
            </v-card-title>
            <v-card-title class="imageSubTitle grey--text">
              {{ place.typeTH }}
              <v-spacer></v-spacer>
              <v-chip class="mx-2" color="#FF9100" outlined>{{
                place.provinceTH
              }}</v-chip>
            </v-card-title>
            <v-divider class="mx-2"></v-divider>
            <v-card-text class="imageText">
              {{ place.descriptionTH }}
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="4" class="buttonZone">
          <v-btn
            color="green"
            class="approve-btn white--text"
            height="100px"
            @click="Approve"
            >Approve</v-btn
          >
          <v-btn
            color="error"
            class="decline-btn"
            height="100px"
            @click="Decline"
            >Decline</v-btn
          >
        </v-col>
      </v-row>
    </div>
  </v-content>
</template>

<script>
// @ is an alias to /src
import TripBar from "../components/TripBar";
import axios from "axios";
import Approvemap from "../components/Approvemap";
export default {
  props: ["keyID"],
  name: "ApproveInfo",
  components: {
    TripBar,
    Approvemap,
  },
  data: () => ({
    place: [],
  }),
  methods: {
    goNext(title) {
      this.$router.push("/PlaceInfo/" + title);
    },
    async getInfo() {
      await axios
        .get("placeInfo/" + this.keyID)
        .then((res) => (this.place = res.data[0]));
      console.log(this.place);

    },
    async Approve() {
      await axios
        .post("validate", { key: this.keyID, status: 1 })
        .then((res) => {
          console.log(res.data);
          this.$router.push("/ApprovePlace");
        });
    },
    async Decline() {
      await axios
        .post("validate", { key: this.keyID, status: 0 })
        .then((res) => {
          console.log(res.data);
          this.$router.push("/ApprovePlace");
        });
    },

  },
  created: function() {
    this.getInfo();
  },

};
</script>

<style scoped>
.ApproveInfo {
  min-height: 110vh;
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
#map {
  width: 27vw;
  height: 220px;
}
.mapZone {
  width: 100%;
  height: calc(100vh + 12px);
}

.mapCard {
  margin-top: 83px;
  margin-left: 25px;
  margin-right: 5px;
}

.mapPic {
  width: 100%;
  height: 300px;
}

.imageZone {
  width: 100%;
  height: calc(100vh + 12px);
}

.imageCard {
  margin-left: 20px;
  margin-top: 83px;
  min-height: 600px;
}

.imagePic {
  width: 100%;
  height: 400px;
}

.imageTitle {
  margin-top: 10px;
  font-size: 45px;
  font-weight: 300;
}

.imageSubTitle {
  margin-top: -10px;
  margin-left: 5px;
  font-size: 20px;
  font-weight: 450;
}

.imageText {
  margin-left: 5px;
  font-size: 20px;
  font-weight: 400;
  line-height: 30px;
}

.buttonZone {
  width: 100%;
  height: calc(100vh + 12px);
}

.approve-btn {
  margin-top: 50%;
  margin-bottom: 20px;
  margin-left: 35px;
  width: 84%;
  font-size: 30px;
}

.decline-btn {
  margin-top: 83px;
  margin-bottom: 20px;
  margin-left: 35px;
  width: 84%;
  font-size: 30px;
}
</style>
