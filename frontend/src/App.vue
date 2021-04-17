<template>
  <div id="app">
    <router-view @toggle="toggleLoggedIn"></router-view>
  </div>
</template>

<style lang="scss">
@import "assets/css/main.css";
@import "assets/scss/home.scss";
@import "assets/scss/about.scss";
@import "assets/scss/signin.scss";

</style>


<script>
export default {
  name: 'app',
  data: () => ({
      loggedIn: false,
  }),
  methods:{
    toggleLoggedIn(){
      this.loggedIn = !this.loggedIn;
    }
  },
}
</script>