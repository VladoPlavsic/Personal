<template>
    <div id="header" class="home">
        <!-- first row -->
        <div id="login" class="home">
            <Login v-if="$cookies.loggedIn === 'false'"/>
            <Logout v-if="$cookies.loggedIn === 'true'"/>
        </div>
        <!-- second row -->
        <div id="content-picker">
            <div class="item">
                <router-link :to="{name: 'About'}">
                    About
                </router-link>
            </div>
            <div class="item">
                <router-link :to="{name: 'Articles'}">
                    Articles
                </router-link>
            </div>
            <div class="item">
                <router-link :to="{name: 'Contact'}">
                    Contact
                </router-link>
            </div>
        </div>
    </div>
</template>

<script>
import Login from '@/components/Login'
import Logout from '@/components/Logout'

import axios from 'axios'

export default {
  name: 'Home',
  methods:{
      log() {
          console.log("press")
      }
  },
  components:{
      Login,
      Logout
    }
}
</script>