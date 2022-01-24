<template>
  <v-content>
    <TripBar/>
    <div class="AddPlace">
      <v-row>
        <v-col cols = "6" class="mapZone">
          <v-card class="mapCard pb-7">
            <v-card-title class="mx-4">แผนที่</v-card-title>
            <v-card class="mx-10 mb-7">
              <Addmap @changeLat="placeLat = $event" @changeLng="placeLng = $event"/>
            </v-card>
            <v-text-field v-model = "placeLat" class="mx-9" placeholder="Latitude"></v-text-field>
            <v-spacer></v-spacer>
            <v-text-field v-model = "placeLng" class="mx-9" placeholder="Longitude"></v-text-field>
            <v-divider class="mx-5"></v-divider>
            <v-card-title class="mx-4">เว็บไซต์</v-card-title>
            <v-text-field v-model = "form.website" class="mx-9" placeholder="www.example.com" ></v-text-field>
            <v-divider class="mx-5"></v-divider>
            <v-card-title class="mx-4">เบอร์โทรศัพท์</v-card-title>
            <v-text-field v-model = "form.phone" class="mx-9" placeholder="xxxxxxxxxx"></v-text-field>
            <v-divider class="mx-5"></v-divider>
            <v-card-title class="mx-4">ประเภท</v-card-title>
            <v-autocomplete
              v-model="form.type"
              :items="types"
              class="chooseType"
            ></v-autocomplete>
            <!-- <v-card-title class="mx-4">เวลาทำการ</v-card-title>
            <v-row>
              <v-card-subtitle class="ml-15 mr-15 subtitle">วันจันทร์</v-card-subtitle>
              <v-card-subtitle class="ml-8 mr-15 subtitle">วันอังคาร</v-card-subtitle>
              <v-card-subtitle class="ml-10 mr-15 subtitle">วันพุธ</v-card-subtitle>
              <v-card-subtitle class="ml-10 mr-15 subtitle">วันพฤหัส</v-card-subtitle>
            </v-row>
            <v-row>
              <v-chip class="ma-2 ml-12 mr-10" color="#FF9100" outlined>10:00 - 20.00</v-chip>
              <v-chip class="ma-2 mx-10" color="#FF9100" outlined>10:00 - 20.00</v-chip>
              <v-chip class="ma-2 mx-10" color="#FF9100" outlined>10:00 - 20.00</v-chip>
              <v-chip class="ma-2 mx-10" color="#FF9100" outlined>10:00 - 20.00</v-chip>
            </v-row>
            <v-row>
              <v-card-subtitle class="ml-16 mr-15 subtitle">วันศุกร์</v-card-subtitle>
              <v-card-subtitle class="ml-11 mr-15 subtitle">วันเสาร์</v-card-subtitle>
              <v-card-subtitle class="ml-9 mr-15 subtitle">วันอาทิตย์</v-card-subtitle>  
            </v-row>
            <v-row>
              <v-chip class="ma-2 ml-12 mr-10" color="#FF9100" outlined>10:00 - 20.00</v-chip>
              <v-chip class="ma-2 mx-10" color="#FF9100" outlined>10:00 - 20.00</v-chip>
              <v-chip class="ma-2 mx-10" color="#FF9100" outlined>10:00 - 20.00</v-chip>
            </v-row> -->
          </v-card>
        </v-col>
        <v-col cols = "6" class="imageZone">
          <v-card class="imageCard">
            <img id="showImage" class="imagePic">
            <input type="file" @change="handleImage" ref="fileInput" style="display: none;">
            <v-btn color="primary" class="uploadButton" @click="$refs.fileInput.click()">อัพโหลดรูปภาพ</v-btn>
            <v-divider></v-divider>
            <v-card-title class="imageTitle">
              <v-text-field v-model = "form.placeName" label="ชื่อสถานที่" :rules="placeNameRule"></v-text-field>
              <v-spacer></v-spacer>
              <v-autocomplete
                v-model="form.province"
                :items="provinceNames"
                label="จังหวัด"
              ></v-autocomplete>
            </v-card-title>
            <v-divider class="mx-2"></v-divider>
            <v-card-text class="imageText">
                <v-textarea  v-model = "form.description" filled label="ข้อมูลสถานที่เพิ่มเติม" height="250px" class="mr-2"></v-textarea>
                </v-card-text>
                <v-btn @click = "sendData" color="primary" class="recommend-btn mx-5 my-5" height="50px" >
                    แนะนำสถานที่
                <v-icon class="ml-2" size="30" >mdi-bookmark-plus</v-icon>
            </v-btn>
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
import Addmap from "../components/Addmap";
export default {
  name: "AddPlace",
  components: {
    TripBar,
    Addmap,
  },

  data: () => ({
    image: require("../assets/passage1.jpg"),
    imageExample: "",
    types: ["จุดชมวิว","ดอย","ตลาด","น้ำตก","ร้านอาหาร","วัด","ศาลเจ้า","สวนสาธารณะ", "สวนสัตว์","อุทยานแห่งชาติ", "อื่นๆ"],
    provinces: [],
    placeLat: "",
    placeLng: "",
    provinceNames: [],
    placeNameRule: [
        v => !!v || 'จำเป็น',
    ],
    form : {
      website : "",
      phone : "",
      placeName : "",
      province : "",
      description : "",
      type : "",
    },
  }),

  methods : {
    async sendData(){
      console.log(this.form.phone)
      await axios.post("addLocation",{"website" : this.form.website , "phone" : this.form.phone , "placeName" : this.form.placeName , "province" : this.form.province , "description" : this.form.description , "image" : document.getElementById('showImage').src, "latitude" : this.placeLat, "longtitude" : this.placeLng , "User" : this.$store.getters.StateID , "type" : this.form.type})
      .then((res) => 
      {
        alert(res.data.msg)
        console.log(res.data)
        if (res.data.isSuccess){
          this.form.website = ""
          this.form.phone = ""
          this.form.placeName = ""
          this.form.province = ""
          this.form.description = ""
          this.form.type = ""
          document.getElementById('showImage').src = "";
        }
      })
    },
    async callProvinces(){
      await axios.get("province").then((res)=>this.provinces = res.data);
      var i;
      for(i=0;i<this.provinces.length;i++){
        this.provinceNames.push(this.provinces[i].provinceTH);
      }
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
    this.callProvinces();
  }
};
</script>

<style scoped>
  .AddPlace{
    min-height: 115vh;
    background-image: linear-gradient(to top, #77cee3, #6bc4dd, #60bad7, #55afd1, #4ba5cb, #439ec7, #3b96c3, #338fbf, #2c88bc, #2681ba, #227ab6, #2073b3);
  }

  .mapZone{
    width: 100%;
  }

  .mapCard{
    margin-top: 100px;
    margin-left: 100px;
    margin-right: 50px;
    min-height: 600px;
  }

  .mapPic{
    width: 100%;
    height: 300px;
  }

  .chooseType{
    margin-left: 35px;
    margin-right: 35px;
    margin-top: 0px;
  }

  .imageZone{
    width: 100%;
  }

  .imageCard{
    margin-top: 100px;
    margin-left: 50px;
    margin-right: 100px;
    min-height: 850px;
  }

  .imagePic{
    width: 100%;
    height: 410px;
    size: cover;
  }

  .uploadButton {
    margin-left: 295px;
    margin-top: 0px;
    margin-bottom: 10px;
    /* color: #ff9100; */
    font-size: 20px;
  }

  .imageTitle{
    font-size: 45px;
    font-weight: 300;
  }

  .imageSubTitle{
    font-size: 20px;
    font-weight: 450;
  }

  .imageText{
    margin-left: 5px;
    font-size: 20px;
    font-weight: 400;
    line-height: 30px;
    height: 275px;
  }

  .recommend-btn{
      width: calc(100% - 40px);
      font-size: 23px;
  }

  .subtitle{
    font-size: 17px;
    font-weight: 450;
  }
</style>