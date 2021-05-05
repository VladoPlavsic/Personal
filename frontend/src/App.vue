<template>
  <div id="app">
    <router-view @re-render="reRender" @enable-edit="enableEdit"></router-view>
  </div>
</template>

<style lang="scss">
@import "assets/css/main.css";
@import "assets/scss/contact.scss";
@import "assets/scss/header.scss";
@import "assets/scss/form.scss";

</style>

<script>
import axios from 'axios'

export default {
  name: 'app',
  data: () => ({
      admin: false,
      edit: false,
  }),
  methods:
  {
  reRender() {
      this.admin = false;
  },
  enableEdit(){
    if (this.admin){
      this.edit = !this.edit;
    }
    else{
      this.edit = false;
    }
  },
  },
  beforeCreate: function() {
    if (this.$cookies.loggedIn === "true"){
      axios.get(process.env.VUE_APP_REST_API_IP + "/api/authentication/admin/check?token=" + this.$cookies.jwt).then((response) => {
          this.admin = response.data;
      }).catch((error) => {
          if(error.response){
            console.log(error.response);
            if (error.response.status == 401){
              this.$setCookie('loggedIn', false);
              this.$removeCookie('jwt');
            }
          }
     });
    }else{
      this.$setCookie('loggedIn', false);
      this.admin = false;
    }
  }
}
</script>