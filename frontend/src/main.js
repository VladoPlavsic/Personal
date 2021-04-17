import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import VueReactiveCookie from 'vue-reactive-cookie'

Vue.config.productionTip = false;

Vue.use(VueReactiveCookie)

new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
}).$mount('#app')
