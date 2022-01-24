<template>
  <v-content>
    <TripBar />
    <div class="ListTrip">
        <v-row class="chipBar">
          <v-autocomplete
            v-model="typeValue"
            :items="types"
            filled
            rounded
            label="ประเภท"
            color="#FF9100"
            class="mx-6"
          ></v-autocomplete>
          <v-autocomplete
            v-model="provinceValue"
            :items="provinceNames"
            filled
            rounded
            label="จังหวัด"
            color="#FF9100"
          ></v-autocomplete>
        </v-row>   
      <v-row>
        <div class="mapCard">
          <Listmap ref="Addmap" />
        </div>
        <v-col cols="3" class="listCard">
          <v-row v-for="(place, i) in places" :key="i">
            <v-card v-if="place.isVerify == '1'  
                          && keyNotUsed(place.keyID) 
                          && (place.typeTH.includes(typeValue) || typeValue == 'ทั้งหมด')
                          && (place.provinceTH.includes(provinceValue) || provinceValue == 'ทั้งหมด')"
                          class="ma-3">
              <v-img :src="place.pictureURL" class="placePic"></v-img>
              <v-card-title>
                {{ place.nameTH }}
              </v-card-title>
              <v-card-title class="subTitle">
                {{place.typeTH}}
                <v-spacer></v-spacer>
                <v-chip class="ma-2" color="#FF9100" outlined>{{
                  place.provinceTH
                }}</v-chip>
              </v-card-title>
              <v-btn color="#FF9100" outlined class="ma-2" @click = "showOverlay(place)" style="font-size: 20px;"
                >ดูข้อมูล
                <v-icon class="ml-2">mdi-clipboard-text-search-outline</v-icon>
              </v-btn>
              <v-btn
                color="#FF9100"
                outlined
                class="ma-2"
                style="font-size: 20px;"
                @click="addPlace(place),$refs.Addmap. moveToLocation(place.latitude,place.longitude),$refs.Addmap.addMarker(place.latitude,place.longitude)" 
                >เพิ่มเข้าทริป
                <v-icon class="ml-2">mdi-plus-outline</v-icon>
              </v-btn>
            </v-card>
          </v-row>
        </v-col>

        <v-col cols="5" class="tripCard">
          <v-card class="ma-3">
            <v-card-title class="yourTripTitle white--text"
              >ทริป</v-card-title
            >
            <v-divider></v-divider>
            <v-form class="mt-1">
              <v-row>
                <v-col cols="4">
                  <v-card-title>ชื่อทริป</v-card-title>
                </v-col>
                <v-col cols="6">
                  <v-text-field
                    v-model="tripName"
                    regular
                    placeholder="ทริปของฉัน"
                    color="orange"
                    required
                    clearable
                  ></v-text-field>
                </v-col>
              </v-row>
              <v-card-title class="subTitle">
                เลือกสถานที่ 3 ถึง 7 สถานที่
                <v-spacer></v-spacer>
                <v-autocomplete
                  v-model="mode"
                  :items="modes"
                  class="chooseMode"
                  color="orange"
                ></v-autocomplete>
              </v-card-title>
              <v-card class="scrollCard">
                <v-virtual-scroll
                  page-mode
                  :items="placesInTrip"
                  :item-height="150"
                  height="566"
                >
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
                      <v-col cols="5">
                        <v-card class="mt-3">
                          <v-row>
                            <v-card-title
                              class="ml-2"
                              style="font-weight: 200; font-size: 14px"
                              >{{notLong(place.item.nameTH)}}</v-card-title
                            >
                            <v-spacer></v-spacer>
                            <v-btn
                              icon
                              class="mt-3 mr-4"
                              @click="canclePlace(place.index) ,$refs.Addmap.removeMarker(place.item.latitude,place.item.longitude)"
                              ><v-icon color="error">mdi-close</v-icon></v-btn
                            >
                          </v-row>
                          <v-chip class="ma-2" color="#FF9100" outlined>{{
                            place.item.provinceTH
                          }}</v-chip>
                        </v-card>
                      </v-col>
                    </v-row>
                  </template>
                </v-virtual-scroll>
              </v-card>
              <v-row>
                <v-btn text class="makeTripButton" @click="placesInTrip.length >= 2 ? makeTrip() : makeFail()">สร้างทริป</v-btn>
                <v-spacer></v-spacer>
                <v-btn text class="updateButton"  @click="makeRoute() ">สร้างเส้นทาง</v-btn>
              </v-row>
            </v-form>
          </v-card>
        </v-col>
      </v-row>
      <!-- Overlay -->
      <v-overlay
        :z-index=0
        :value="overlay"
      >
        <v-card class="editCard">
          <v-card-title class="black--text" style="font-size: 30px;">
            {{overlayValue.nameTH}}
            <v-spacer></v-spacer>
            <v-btn
              class="white--text"
              color="error"
              @click="overlay = false"
            >
              X
            </v-btn>
            <v-btn
              class="white--text"
              color="error"
              @click="goPlaceInfo(overlayValue.keyID)"
            >
              Go
            </v-btn>
          </v-card-title>
        </v-card>
      </v-overlay>
    </div>
  </v-content>
</template>

<script>
// @ is an alias to /src
import TripBar from "../components/TripBar";
import axios from "axios";
import Listmap from "../components/Listmap";



export default {
  name: "ListTrip",
  components: {
    TripBar,
    Listmap,
  },

  data: () => ({
    scrolledToBottom: false,
    overlay: false,
    types: ["ทั้งหมด","จุดชมวิว","ดอย","ตลาด","น้ำตก","ร้านอาหาร","วัด","ศาลเจ้า","สวนสาธารณะ", "สวนสัตว์","อุทยานแห่งชาติ", "อื่นๆ"],
    typeValue: "ทั้งหมด",
    provinces: [],
    provinceNames: ["ทั้งหมด"],
    provinceValue: "ทั้งหมด",
    location: [
      
    ],
    waypoints:[],
    typeGroup: 0,
    tripName: "",
    placesInTrip: [],
    places: [],
    placesInTripTemp: [],
    bestPath: [],
    overlayValue: [],
    mode: "สั้นที่สุด",
    modes: ["สั้นที่สุด", "จุดเริ่มต้นเดิม","ปลายทางเดิม","เริ่มต้น ปลายทางเดิม"]
  }),
  methods: {
    scroll () {
  window.onscroll = () => {
    if ((Math.ceil(window.pageYOffset/475) + 2)%10 == 0) {
        //console.log(((Math.ceil(window.pageYOffset/475) + 2)));
        this.callPlaces();
        console.log(((Math.ceil(window.pageYOffset/475) + 2)/10+1)*10)
    }
 }
},

    addPlace: function(item) {
      this.placesInTrip.push(item); 
      // this.coordinates.push({ lat: item.latitude, lng: item.longitude });
      // for(let i =1;i<this.coordinates.length-1;i++){
      //   this.waypoints.push(this.coordinates[i])
      // }
    },
    canclePlace: function(index) {
      this.placesInTrip.splice(index, 1);
      //this.coordinates.splice(index, 1); 
    },
    notLong: function(placeName) {
      var reserve = ['ิ','ี','ึ','ื','ุ','ู','ั','่','้','๊','๋','็','์'];
      var i;
      var count = 0;
      for(i=0;i<placeName.length;i++){
        if(!reserve.includes(placeName[i])){
          count += 1;
        }
      }
      if(count > 25){
        placeName = placeName.slice(0,22+placeName.length-count) + "...";
      }
      return placeName;
    },
    getItem: function(items, item) {
      for (var i = 0; i < items.length; i++) {
        if (items[i].title == item) {
          return items[i];
        }
      }
    },
    showOverlay(place){
      this.overlayValue = place;
      this.overlay = !this.overlay;
    },
    goPlaceInfo(keyID){
      this.$router.push("/PlaceInfo/" + keyID);
    },
    async makeTrip (){
      console.log(this.placesInTrip)
      await axios.post("makeTrip",{"userID": this.$store.getters.StateID , "tripName": this.tripName, "placesInTrip": this.placesInTrip})
      .then((res)=>{
        alert(res.data.msg)
        })
      this.tripName = "";
      this.placesInTrip = []; 
      this.$refs.Addmap.clearRoute()
    },
    makeFail: function(){
      alert("Add Fail");
    },
    async makeRoute (){
      await axios.post("makeRoute",{"placesInTrip": this.placesInTrip,"command": this.mode}).then((res)=>this.bestPath = res.data['results'][0]);
      // Update Route //
      this.updateRoute();
    },
    updateRoute: function(){
      for (var i = 0; i < this.bestPath.length; i++) {
        for (var j = 0; j < this.placesInTrip.length; j++) {
          if(this.placesInTrip[j].keyID == this.bestPath[i]){
            this.placesInTripTemp.push(this.placesInTrip[j]);
          }
        }
      }
      this.placesInTrip = this.placesInTripTemp;
      this.placesInTripTemp = [];
      alert("Update Route");
      this.location = [];
      for(let i=0;i<this.placesInTrip.length;i++){
        this.location.push({ lat: this.placesInTrip[i].latitude, lng: this.placesInTrip[i].longitude });
      }
      this.$refs.Addmap.clearRoute()
      this.$refs.Addmap.displayRoute(this.location)
    },
    keyNotUsed: function(keyID){
      var i;
      for(i=0;i < this.placesInTrip.length;i++){
        // console.log(this.placesInTrip[i].keyID);
        if(keyID == this.placesInTrip[i].keyID){
          return false;
        }
      }
      return true;
    },
    async callPlaces(){
      await axios.post("location",{query:"","current": ((Math.ceil(window.pageYOffset/475) + 2)/10+1)*10}).then((res)=>this.places = res.data);
      console.log(this.places);
    },
    async callPlaces2(){
      await axios.post("location",{query:"","current": ((Math.ceil(window.pageYOffset/475) + 2)/10+1)*10}).then((res)=>{console.log(res.data);});
    },
    async callProvinces(){
      await axios.get("province").then((res)=>this.provinces = res.data);
      var i;
      for(i=0;i<this.provinces.length;i++){
        this.provinceNames.push(this.provinces[i].provinceTH);
      }
    }
  },
  created: function() {
    this.callPlaces();
    this.callProvinces();
    this.scroll();
  },
};
</script>

<style scoped>
.chipBar {
  margin: 10px;
  position: fixed;
  margin-top: 70px;
}

.chipActive {
  background-color: #ff9100;
}

.search-field {
  width: 200px;
}

.mapCard {
  position: fixed;
  margin-top: 140px;
  margin-left: 27px;
}

.mapPic {
  background-image: url(../assets/map1.png);
}

.listCard {
  position: absolute;
  margin-top: 7vh;
  left: 33vw;
}

.placePic {
  width: 800px;
  height: 280px;
}

.subTitle{
  font-size: 20px;
  font-weight: 450;
  color: grey;
}

.tripCard {
  position: fixed;
  top: 7%;
  left: calc(59% - 10px);
}

.yourTripTitle {
  background-color: #faae4b;
  font-size: 35px;
}

.subTitle{
  font-size: 17px;
  font-weight: 400;
  color: grey;
  margin-top: -25px;
}

.chooseMode{
  margin-left: 50px;
  margin-right: 35px;
  margin-top: 0px;
}

.numberCard {
  background-color: #faae4b;
  color: black;
  font-size: 45px;
  font-weight: 80;
  text-align: center;
  padding-top: 25%;
  height: 87%;
}

.scrollCard {
  margin-left: 20px;
  padding-left: 15px;
  padding-top: 15px;
  padding-bottom: 15px;
  width: 95%;
  height: 60vh;
}

.makeTripButton {
  margin-left: 45px;
  margin-top: 30px;
  margin-bottom: 15px;
  color: #ff9100;
  font-size: 20px;
}

.updateButton {
  margin-right: 40px;
  margin-top: 30px;
  margin-bottom: 15px;
  color: #ff9100;
  font-size: 20px;
}

.placeImage {
  width: 100%;
  height: 100px;
}

.editCard{
  width: 55vw;
  height: 70vh;
  background-color: white;
}
</style>
