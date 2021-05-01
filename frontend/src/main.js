import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import VueReactiveCookie from 'vue-reactive-cookie'
import CKEditor from '@ckeditor/ckeditor5-vue2';

Vue.config.productionTip = false;

Vue.use( VueReactiveCookie );
Vue.use( CKEditor );

new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
}).$mount('#app')
