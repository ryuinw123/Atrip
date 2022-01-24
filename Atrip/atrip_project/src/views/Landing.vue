<template>
  <div class="Landing">
    <img class="img1">
    <div class="rec2"></div>
    <img class="img2">
    <div class="rec"></div>
    <span class="text1">START YOUR PLAN</span>
    <span class="text2">START YOUR JOURNEY</span>
    <v-btn plain class="btn_register" link to="/Register">สมัครสมาชิก</v-btn>
    <v-btn plain class="btn_signin" @click = "Login">เข้าสู่ระบบ</v-btn>
  </div>
</template>

<script>
  export default {
    data: () => ({
       
    }),
    methods: {
      Login(){
        if (this.$store.getters.StateIsLogIn == true){
          this.$router.push("/Home")
        }
        else{
          this.$router.push("/SignIn")
        }
      }
    },
  }
</script>
<style scoped>
  .Landing{
    position: relative;
  }

  .rec {
    position: absolute;
    width: 100vw;
    height: 35vh;
    left: 0px;
    top: 20vh;
    /* background: rgba(201, 96, 96, 0.58); */
    background: rgba(255, 255, 255, 0.58);
    overflow: hidden;
  }

  .text1 {
    position: absolute;
    left: 100px;
    top: 25vh;
    font-weight: bold;
    font-size: 80px;
    line-height: 129px;
    text-align: center;
    color: #ffffff;
    text-shadow: 0px 6px 4px rgba(0, 0, 0, 0.25);
    -webkit-text-stroke: 2px #7D6B6B;
    -webkit-text-fill-color: white;
  }

  .text2 {
    position: absolute;
    left: 100px;
    top: 40vh;
    font-weight: bold;
    font-size: 55px;
    line-height: 82px;
    display: flex;
    align-items: center;
    text-align: center;
    color: #ffffff;
    /* border: 4px solid #7D6B6B; */
    text-shadow: 0px 6px 4px rgba(0, 0, 0, 0.25);
    -webkit-text-stroke: 2px #7D6B6B;
    -webkit-text-fill-color: white;
  }

  .btn_register{
    position: absolute;
    right: 300px;
    top: 20px;
    font-size: 30px;
    font-weight: 700;
  }

  .btn_signin{
    position: absolute;
    right: 50px;
    top: 20px;
    font-size: 30px;
    font-weight: 700;
  }

  .rec2{
    position: absolute;
    width: 35vw;
    height: 100vh;
    left: 0px;
    top: 0px;
    background: linear-gradient(
        0deg,
        rgba(238, 181, 141, 0.78),
        rgba(238, 181, 141, 0.78)
      );
    overflow: hidden;
  }

  .img1 {
    position: absolute;
    width: 35vw;
    height: 100vh;
    left: 0px;
    top: 0px;
    background: url(../assets/sea1.jpg);
    background-repeat: no-repeat;
    background-size: cover;
  }

  .img2 {
    position: absolute;
    width: 70vw;
    height: 70vh;
    right: 0px;
    top: 8vh;

    background: url(../assets/sea1.jpg);
    filter: drop-shadow(0px 4px 4px rgba(0, 0, 0, 0.25));
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
  }
</style>