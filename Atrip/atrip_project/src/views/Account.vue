<template>
  <v-content>
    <TripBar />
    <div class="Account">
      <v-row>
        <v-col cols = "5" class="profileZone">
          <v-card class="profileCard">
            <div>
              <v-avatar color="primary" width="350" height="350" class="profileAvatar">
                <v-img :src= "this.$store.getters.StatePicture" fab></v-img>
              </v-avatar>
            </div>
            <v-col class="profileName my-10">
              {{this.$store.getters.StateNickname}}
            </v-col>
            <v-btn class="editProfile-btn white--text" 
                    width="37%" height="50px" 
                    style="font-size: 27px;" color="green"
                    @click="profileOverlay = !profileOverlay">
              แก้ไขโปรไฟล์
              <v-icon class="ml-3" size = "30px">mdi-account-edit-outline</v-icon>
            </v-btn>
            <v-btn class="changePassword-btn white--text" 
                    width="37%" height="50px" 
                    style="font-size: 27px;" color="error"
                    @click="profileOverlay = !profileOverlay">
              เปลี่ยนรหัสผ่าน
              <v-icon class="ml-3" size = "30px">mdi-account-edit-outline</v-icon>
            </v-btn>
          </v-card>
        </v-col>
        <v-col cols = "7" class="tripZone">
          <v-scale-transition>
            <v-card class="savedTripCard mr-10">ทริปที่บันทึก</v-card>
          </v-scale-transition>

          <v-sheet class="savedTripSheet">
            <v-slide-group class="px-4" height = "500" show-arrows>
              <v-slide-item
                v-for="(trip, i) in savedTrips"
                :key="i"
                v-slot="{active,toggle}"
                class="savedTripSlide"
              >
                <v-card class="oneTripCard mx-3" @click="toggle">
                  <v-img :src = "trip.image" height="200px">
                    <v-scale-transition>
                      <v-btn v-if="active" text fab size="35px" class="deleteTrip-btn ma-2" @click="selectDelete(i,trip.keyID)">
                        <v-icon color = "error" size="45">mdi-close-circle-outline</v-icon>
                      </v-btn>
                    </v-scale-transition>
                  </v-img>
                    <v-card-title>
                      {{trip.nameTH}}
                    </v-card-title>                    
                    <v-card-title class="subTitle">
                      {{trip.Username}}
                      <v-spacer></v-spacer>
                      <v-chip class="mx-2" color="#FF9100" outlined>
                        {{trip.status}}
                      </v-chip>
                    </v-card-title>
                    <v-divider class="mx-5"></v-divider>
                    <v-card-title class="placeTitle black--text">สถานที่ภายในทริป<v-card-subtitle class="mt-1">{{trip.numPlace}} สถานที่</v-card-subtitle></v-card-title>
                    <v-row
                      v-for="(place, j) in trip.placeList.split(',')"
                      :key="j"
                      class="mx-10"
                    >
                      <h5 class="placeSubTitle" style="color: grey;">{{place}}</h5>
                    </v-row>
                    <v-row class="oneTripAction">
                      <v-scale-transition>
                        <v-btn color="#FF9100" outlined class="ma-2" style="font-size: 17px;" @click="goTripInfo(trip.keyID)">
                          ข้อมูลเพิ่มเติม
                          <v-icon class="ml-2">mdi-clipboard-text-search-outline</v-icon>
                        </v-btn>
                      </v-scale-transition>
                    </v-row>
                </v-card>
              </v-slide-item>
            </v-slide-group>
          </v-sheet>
        </v-col>
      </v-row>
      <v-overlay
        :z-index=0
        :value="profileOverlay"
      >
        <v-card class="editCard">
          <v-card-title class="white--text" style="font-size: 30px;">
            แก้ไขโปรไฟล์
            <v-spacer></v-spacer>
            <v-btn
              class="white--text"
              color="error"
              @click="profileOverlay = false"
            >
              X
            </v-btn>
          </v-card-title>
          <v-divider></v-divider>
          <v-card class="imageCard">
            <img id="showImage" class="imagePic">
            <input type="file" @change="handleImage" ref="fileInput" style="display: none;">    
          </v-card>
          <v-btn color="primary" class="uploadButton" @click="$refs.fileInput.click()">อัพโหลดรูปภาพ</v-btn>
          <v-form class="edit-form">
            <v-text-field
              v-model = "nickName"
              placeholder="ชื่อเล่น"
              regular
              class="mt-7 mb-3"
              style="font-color: black; width: 400px; margin-left: 40px; color: black;"
              prepend-icon="mdi-account"
              label="ชื่อเล่น"
            ></v-text-field>
            <v-text-field
              v-model = "firstName"
              placeholder="ชื่อ"
              regular
              class="mt-7 mb-3"
              style="font-color: black; width: 400px; margin-left: 40px; color: black;"
              prepend-icon="mdi-account"
              label="ชื่อ"
            ></v-text-field>
            <v-text-field
              v-model = "lastName"
              placeholder="นามสกุล"
              regular
              class="mt-7 mb-3"
              style="font-color: black; width: 400px; margin-left: 40px; color: black;"
              prepend-icon="mdi-account"
              label="นามสกุล"
            ></v-text-field>
            <v-row justify="center" style="margin-top: 10px; margin-bottom: 10px;">
              <v-btn
                class="ok-btn white--text"
                color="green"
                height="50px"
                @click="editData()"
              >
                ยืนยัน
              </v-btn>
              <v-btn
                class="no-btn white--text"
                color="error"
                height="50px"
                @click="profileOverlay = false"
              >
                ยกเลิก
              </v-btn>
            </v-row>
          </v-form>
        </v-card>
      </v-overlay>

      <v-overlay
        :z-index=0
        :value="tripOverlay"
      >
        <v-card class="deleteCard">
          <v-card-title class="white--text" style="font-size: 30px;">
            ต้องการลบทริป ใช่หรือไม่
          </v-card-title>
          <v-row justify="center" style="margin-top: 10px; margin-bottom: 10px;">
            <v-btn
              class="okDelete-btn white--text"
              color="green"
              height="50px"
              @click="deleteTrip()"
            >
              ยืนยัน
            </v-btn>
            <v-btn
              class="noDelete-btn white--text"
              color="error"
              height="50px"
              @click="tripOverlay = false"
            >
              ยกเลิก
            </v-btn>
          </v-row>
        </v-card>
      </v-overlay>
    </div>
  </v-content>
</template>

<script>
// @ is an alias to /src
import TripBar from "../components/TripBar";
import axios from "axios";

export default {
  name: "Account",
  components: {
    TripBar,
  },

  data: () => ({
    savedTrips: [],
    tripName: "",
    profileOverlay: false,
    tripOverlay: false,
    nickName: "myNickName",
    firstName: "myFirstName",
    lastName: "myLastName",
    selectIndex: "",
    selectID: ""
  }),

  methods: {
    async editData(){
      try {
        await this.$store.dispatch("editData",{"id" : this.$store.getters.StateID ,"nickName" : this.nickName,"firstName" : this.firstName ,"lastName" : this.lastName , "image" : document.getElementById('showImage').src});
        console.log(this.$store.getters.StateFirstName)
        console.log(this.$store.getters.StateNickname)
        console.log(this.$store.getters.StateLastName)
        console.log(this.$store.getters.StatePicture)
        this.profileOverlay = false
      }
      catch(error){
        console.log(error)
      }
    },
    selectDelete(index,keyID){
      this.tripOverlay = !this.tripOverlay;
      this.selectIndex = index;
      this.selectID = keyID;
    },
    deleteTrip: async function(){
      this.savedTrips.splice(this.selectIndex,1);
      await axios.post("/deleteTrip",{"keyID" : this.selectID , "id" : this.$store.getters.StateID}).then((res) => alert(res.data.msg))
      this.tripOverlay = false;
    },
    goTripInfo(keyID){
      this.$router.push("/TripInfo/" + keyID);
    },
    async callTrips(){
      await axios.post("myTrip",{"query":"","id" : this.$store.getters.StateID}).then((res)=>this.savedTrips = res.data);
    },
    handleImage(e){
      var selectedImage = e.target.files[0];
      this.createBase64Image(selectedImage);
    },
    async createBase64Image(fileObject){
      var reader = new FileReader();
      reader.readAsDataURL(fileObject);
      reader.onload = async function(){
        var result = reader.result;
        // console.log(result);
        // this.imageExample = result;
        // console.log(this.imageExample);
        document.getElementById('showImage').src = result;
      };
    }
  },
  created: function(){
    this.callTrips()
    this.nickName = this.$store.getters.StateNickname;
    this.firstName = this.$store.getters.StateFirstName;
    this.lastName = this.$store.getters.StateLastName;
  }
};
</script>

<style scoped>
  .Account{
    position: relative;
    background-image: linear-gradient(to top, #77cee3, #6bc4dd, #60bad7, #55afd1, #4ba5cb, #439ec7, #3b96c3, #338fbf, #2c88bc, #2681ba, #227ab6, #2073b3);
  }

  .profileZone{
    width: 100%;
    height: calc(100vh + 12px);
  }

  .profileCard{
    width: 90%;
    height: 830px;
    margin-top: 100px;
    margin-left: 40px;
    border-radius: 50px;
    text-align: center;
  }

  .profileAvatar{
    margin-top: 50px;
  }

  .profileName{
    font-size: 45px;
  }

  .editProfile-btn{
    position: absolute;
    left: 8%;
    bottom: 50px;
    font-size: 25px;
  }

  .changePassword-btn{
    position: absolute;
    left: 55%;
    bottom: 50px;
    font-size: 25px;
  }

  .editCard{
    width: 55vw;
    height: 70vh;
  }

  .deleteCard{
    width: 30vw;
    height: 30vh;
  }

  .tripZone{
    width: 100%;
    height: calc(100vh + 12px);
  }

  .savedTripCard{
    margin-top: 100px;
    margin-bottom: 20px;
    margin-left: 70px;
    width: 84%;
    height: 100px;
    font-size: 45px;
    font-weight: 300;
    text-align: center;
    padding-top: 15px;
    border-radius: 50px 50px 0px 0px;
  }

  .savedTripSheet{
    margin-left: 70px;
    width: 84%;
    min-height: 710px;
    border-radius: 0px 0px 50px 50px;
  }

  .savedTripSlide{
    top: 10%;
  }

  .oneTripCard{
    width: 370px;
    height: 650px;
    border-radius: 30px;
  }

  .subTitle{
    font-size: 17px;
    font-weight: 450;
    color: rgba(255, 153, 0, 0.822);
    margin-top: -25px;
  }

  .deleteTrip-btn{
    position: absolute;
    right: 0px;
  }

  .placeTitle{
    margin-top: -10px;
  }

  .placeSubTitle{
    margin-top: -10px;
    margin-bottom: 15px;
  }

  .oneTripAction{
    position: absolute;
    right: 30px;
    bottom: 80px;
  }

  .imageCard{
    margin-top: 50px;
    margin-left: 50px;
    margin-right: 100px;
    width: 400px;
    min-height: 300px;
  }

  .imagePic{
    width: 400px;
    height: 410px;
    size: cover;
  }

  .uploadButton {
    margin-left: 150px;
    margin-top: 50px;
    margin-bottom: 10px;
    /* color: #ff9100; */
    font-size: 20px;
  }

  .edit-form {
    position: absolute;
    width: 500px;
    height: 410px;
    top: 120px;
    left: 500px;
    background-color: rgb(80, 131, 80);
  }

  .ok-btn{
    margin-top: 40px; 
    margin-left: 50px; 
    margin-right: 50px; 
    width: 150px;
    font-size: 20px;
  }

  .no-btn{
    margin-top: 40px; 
    margin-right: 50px; 
    width: 150px;
    font-size: 20px;
  }

  .okDelete-btn{
    position: absolute;
    bottom: 40px; 
    left: 40px; 
    width: 150px;
    font-size: 20px;
  }

  .noDelete-btn{
    position: absolute;
    bottom: 40px; 
    right: 40px; 
    width: 150px;
    font-size: 20px;
  }
</style>