import Vue from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify';
import axios from "axios";
import VueGeolocation from 'vue-browser-geolocation'
import * as VueGoogleMaps from 'vue2-google-maps'

Vue.config.productionTip = false

axios.defaults.withCredentials = false
axios.defaults.headers.post['Access-Control-Allow-Origin'] = 'http://127.0.0.1:5000';
axios.defaults.headers.post['Access-Control-Allow-Methods'] = "GET,HEAD,PUT,PATCH,POST,DELETE";
axios.defaults.headers.post['Access-Control-Allow-Headers'] = "Content-Type, Access-Control-Allow-Origin, xxx";
axios.defaults.baseURL = 'http://localhost:34673/';

Vue.use(VueGeolocation)
Vue.config.productionTip = false
Vue.use(VueGoogleMaps, {
  load: {
    key: 'AIzaSyBh0haGGTrLgx7cGPivED1RaqBLMni9nlo',
    //libraries: 'places', // This is required if you use the Autocomplete plugin
    // OR: libraries: 'places,drawing'
    // OR: libraries: 'places,drawing,visualization'
    // (as you require)
 
    //// If you want to set the version, you can do so:
    //v: '3.26',
  },
 
  
})

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
