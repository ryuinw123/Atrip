<template>
  <div class="Register">
    <img class="img1" />
    <v-form class="register-form" v-model="valid">
      <span class="text1">สมัครสมาชิก</span>
      <v-text-field
        v-model = "form.username"
        label="ชื่อผู้ใช้"
        placeholder="Username"
        :rules = "usernameRule"
        regular
        class = "mb-3"
        required
      ></v-text-field>
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
      <v-row>
        <v-col cols="6">
          <v-text-field
            v-model = "form.firstname"
            label="ชื่อ"
            placeholder="Firstname"
            :rules = "firstnameRule"
            regular
            class="mt-7 mb-3"
          ></v-text-field>
        </v-col>
        <v-col cols="6">
          <v-text-field
            v-model = "form.lastname"
            label="นามสกุล"
            placeholder="Lastname"
            :rules = "lastnameRule"
            regular
            class="mt-7 mb-3"
          ></v-text-field>
        </v-col>
      </v-row>
      <v-menu v-model="dateMenu" absolute>
        <template v-slot:activator = "{on,attrs}">
          <v-text-field
            v-model="birthdayText"
            label="วัน-เดือน-ปี เกิด"
            placeholder="yy/mm/dd"
            regular
            class="mt-7 mb-3"
            prepend-icon="mdi-calendar-range"
            slot = "activator"
            v-bind="attrs"
            v-on="on"
          ></v-text-field>
        </template>
        <v-date-picker v-model="form.birthday"></v-date-picker>
      </v-menu>
      <v-text-field
        v-model = "form.email"
        label="อีเมล"
        placeholder="myEmail@hotmail.com"
        regular
        class="mt-7 mb-3"
      ></v-text-field>
      <v-btn @click = "register" text color = "#F57F17" class="btn1" style="font-size: 27px;">ยืนยัน</v-btn>
    </v-form>
  </div>
</template>

<script>
export default {
  name: "Register",
  methods: {
    async register(){
      try {
        await this.$store.dispatch("Register",this.form);
        if (this.$store.getters.StateMsg == "You have successfully registered!"){
          this.$store.dispatch("removeMsg")
          this.$router.push("/SignIn");
        }
      } catch (error) {
        console.log(error)
      }
    }
  },
  data: () => ({
    form: {
        username: "",
        password : "",
        firstname : "",
        lastname : "",
        birthday : "",
        email : ""
     },
    valid: false,
    showPassword: false,
    usernameRule: [
        v => !!v || 'Username is required',
        v => v.length > 7 || 'Username must be at least 8 characters',
        v => v.length < 16 || 'Username must be at most 15 characters',
    ],
    passwordRule: [
        v => !!v || 'Password is required',
        v => v.length > 7 || 'Password must be at least 8 characters',
        v => v.length < 26 || 'Password must be at most 25 characters',
    ],
    firstnameRule: [
        v => !!v || 'Firstname is required',
        v => v.length < 26 || 'Firstname must be at most 25 characters',
    ],
    lastnameRule: [
        v => !!v || 'Lastname is required',
        v => v.length < 26 || 'Lastname must be at most 25 characters',
    ]
  }),
  computed: {
    birthdayText(){
      return this.form.birthday;
    }
  }
};
</script>


<style scoped>
  .text1{
    font-weight: 500;
    font-size: 40px;
    line-height: 129px;
    text-align: center;
    color: #000000;
    text-shadow: 0px 6px 4px rgba(0, 0, 0, 0.10);
    transition: 770ms cubic-bezier(0.55, 0.055, 0.675, 0.19)
  }

  .img1 {
    position: absolute;
    width: 45vw;
    height: 100vh;
    left: -1px;
    top: 1px;
    background: url(../assets/temple1.jpg);
    background-repeat: no-repeat;
    background-size: cover;
    background-position: center;
  }

  .btn1{
    left: 300px;
    top: 30px;
    font-size: 20px;
  }

  .register-form {
    position: absolute;
    width: 400px;
    right: 17vw;
    top: 10vh;
  }
</style>
