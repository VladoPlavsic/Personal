import Vue from 'vue'
import Router from 'vue-router'
import Home from '../views/Home'
import SignIn from '../views/SignIn'
import SignUp from '../views/SignUp'

import About from '../views/About'
import Contact from '../views/Contact'
import Articles from '../views/Articles'


Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/sign/in',
      name: 'SignIn',
      component: SignIn
    },
    {
      path: '/sign/up',
      name: 'SignUp',
      component: SignUp
    },
    {
      path: '/about',
      name: 'About',
      component: About
    },
    {
      path: '/contact',
      name: 'Contact',
      component: Contact
    },
    {
      path: '/articles',
      name: 'Articles',
      component: Articles
    },
    
  ]
})
