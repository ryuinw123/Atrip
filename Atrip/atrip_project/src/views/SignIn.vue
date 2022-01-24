<template>
  <div class="SignIn">
      <img class="bg-img">
      <v-form class="sign-in-form">
        <v-row>
          <v-col cols="12">
            <h1 style="font-size: 30px;" class="grey--text">ลงชื่อเข้าใช้งาน</h1>
          </v-col>     
          <v-col cols="12">
            <v-text-field
              v-model = "form.username"
              label="ชื่อผู้ใช้"
              placeholder="Username"
              :rules = "usernameRule"
              regular
              class = "mb-3"
              required
            ></v-text-field>
          </v-col>
          <v-col cols="12">
            <v-text-field
              v-model = "form.password"
              label="รหัสผ่าน"
              placeholder="Password1234"
              :rules = "passwordRule"
              :append-icon = "showPassword ? 'mdi-eye' : 'mdi-eye-off'"
              :type = "showPassword ? 'text' : 'password'"
              regular
              class="mt-7 mb-3"
              @click:append = "showPassword = !showPassword"
            ></v-text-field>
          </v-col>
          <v-col cols="12">
            <v-btn @click = "Login" align-center color="info" style="font-size: 20px;">ถัดไป</v-btn>
          </v-col>
          <v-row class="optionZone">
            <v-btn text @click="forgetOverlay = !forgetOverlay" color="primary" class="option-btn">
              ลืมรหัสผ่านเหรอ กดไปดิงั้น
            </v-btn>
            <v-btn text link to="/Register" color="primary" class="option-btn">
              ยังไม่มีรหัสอีกเหรอ? กดตรงนี้สิ
            </v-btn>
          </v-row>
        </v-row>
      </v-form>

      <v-overlay
        :z-index=0
        :value="forgetOverlay"
      >
        <v-card class="forgetCard">
          <v-card-title class="white--text" style="font-size: 30px;">
            ลืมรหัสผ่าน
            <v-spacer></v-spacer>
            <v-btn
              class="white--text"
              color="error"
              @click="forgetOverlay = false"
            >
              X
            </v-btn>
          </v-card-title>
          <v-text-field
            v-model = "email"
            label="อีเมล"
            placeholder="example@hotmail.com"
            regular
            class="emailInput mt-7 mb-3"
          ></v-text-field>
          <v-menu v-model="dateMenu" absolute >
            <template v-slot:activator = "{on,attrs}">
              <v-text-field
                v-model="birthdayText"
                label="วัน-เดือน-ปี เกิด"
                placeholder="yy/mm/dd"
                regular
                class="birthdayInput mt-7 mb-3"
                prepend-icon="mdi-calendar-range"
                slot = "activator"
                v-bind="attrs"
                v-on="on"
              ></v-text-field>
            </template>
            <v-date-picker v-model="birthday"></v-date-picker>
          </v-menu>
          <v-row justify="center" style="margin-top: 10px; margin-bottom: 10px;">
            <v-btn class="ok-btn white--text" color="green" height="50px" @click="forgetSend">
              ยืนยัน
            </v-btn>
            <v-btn class="no-btn white--text" color="error" height="50px" @click="forgetOverlay = false">
              ยกเลิก
            </v-btn>
          </v-row>
        </v-card>
      </v-overlay>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from "axios";

export default {
  name: "SignIn",
  components: {},
  data() {
    return {
      form:{
        username: "",
        password : ""
      },
      birthday: "",
      email: "",
      showPassword: false,
      forgetOverlay: false,
      usernameRule: [
        v => !!v || 'Username is required',
        v => v.length > 7 || 'Username must be at least 8 characters',
        v => v.length < 16 || 'Username must be at most 15 characters',
      ],
      passwordRule: [
        v => !!v || 'Password is required',
        v => v.length > 7 || 'Password must be at least 8 characters',
        v => v.length < 26 || 'Password must be at most 25 characters',
      ]
    }
  },
  computed: {
    birthdayText(){
      return this.birthday;
    }
  },
  methods:{
    async forgetSend(){
      await axios.post("forgotpassword",{"email" : this.email , "birthday" : this.birthday}).then((res) => {
        if (res.data.msg){
          this.email = ""
          this.birthday = ""
          this.forgetOverlay = false;
        }
      })
    },
    async Login(){
      try {
        await this.$store.dispatch("LogIn",this.form);
        if (this.$store.getters.isAuthenticated){
          this.$router.push("/Home")
        }
      }
      catch(error){
        console.log(error)
      }
    },
  },
};
</script>

<style scoped>
  .bg-img{
    position: absolute;
    width: 100vw;
    height: 100vh;
    left: 0px;
    top: 0px;
    
    background: url(../assets/login_bg.png);
    background-repeat: no-repeat;
    background-size: 100%;
  }

  .sign-in-form{
    position: absolute;
    width: 400px;
    left: 11vw;
    top: 45vh;
  }

  .optionZone{
    margin-left: -5px;
    margin-top: 20px;
    /* background-color: blueviolet; */
  }

  .option-btn{
    margin-top: 30px;
    font-size: 20px;
  }

  .forgetCard{
    width: 30vw;
    min-height: 40vh;
  }

  .emailInput{
    margin-left: 50px; 
    margin-right: 50px; 
  }

  .birthdayInput{
    margin-left: 50px; 
    margin-right: 50px; 
  }

  .ok-btn{
    margin-top: 40px; 
    margin-left: 50px; 
    margin-right: 50px; 
    width: 200px;
    font-size: 20px;
  }

  .no-btn{
    margin-top: 40px; 
    margin-right: 50px; 
    width: 200px;
    font-size: 20px;
  }
</style>



