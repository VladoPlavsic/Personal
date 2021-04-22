<template>
  <div id="app">
    <router-view @re-render="reRender"></router-view>
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
      admin: false
  }),
  methods:
  {
  reRender() {
      this.admin = false;
  }
  },
  beforeCreate: function() {
    if (this.$cookies.loggedIn === "true"){
      axios.get("http://localhost:8000/api/authentication/admin/check?token=" + this.$cookies.jwt).then((response) => {
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
      this.admin = false;
    }
  }
}
</script>