import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import SignIn from '../views/SignIn.vue'
import Register from '../views/Register.vue'
import AllPlan from '../views/AllPlan.vue'
import YourPlan from '../views/YourPlan.vue'
import Account from '../views/Account.vue'
import Landing from '../views/Landing.vue'
import About from '../views/About.vue'
import PlaceInfo from '../views/PlaceInfo.vue'
import TripInfo from '../views/TripInfo.vue'
import ListTrip from '../views/ListTrip.vue'
import AddPlace from '../views/AddPlace.vue'
import ApprovePlace from '../views/ApprovePlace.vue'
import ApproveInfo from '../views/ApproveInfo.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/Home',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    component: About
  },
  {
    path: '/SignIn',
    name: 'SignIn',
    component: SignIn
  },
  {
    path: '/Register',
    name: 'Register',
    component: Register
  },
  {
    path: '/AllPlan',
    name: 'AllPlan',
    component: AllPlan
  },
  {
    path: '/YourPlan',
    name: 'YourPlan',
    component: YourPlan
  },
  {
    path: '/Account',
    name: 'Account',
    component: Account
  },
  {
    path: '/',
    name: 'Landing',
    component: Landing
  },
  {
    path: '/PlaceInfo/:keyID',
    name: 'PlaceInfo',
    component: PlaceInfo,
    props: true
  },
  {
    path: '/TripInfo/:keyID',
    name: 'TripInfo',
    component: TripInfo,
    props: true
  },
  {
    path: '/ListTrip',
    name: 'ListTrip',
    component: ListTrip
  },
  {
    path: '/AddPlace',
    name: 'AddPlace',
    component: AddPlace
  },
  {
    path: '/ApprovePlace',
    name: 'ApprovePlace',
    component: ApprovePlace
  },
  {
    path: '/ApproveInfo/:keyID',
    name: 'ApproveInfo',
    component: ApproveInfo,
    props: true
  }
]

const router = new VueRouter({
  routes
})

export default router
