<template>
<div>
    <div id="header" class="about">
        <!-- first row -->
        <div id="login" class="about">
            <Login v-if="$cookies.loggedIn === 'false'"/>
            <Logout v-if="$cookies.loggedIn === 'true'"/>
        </div>
    </div>
    <div id="body" class="about">
        <!-- Scroll -->
        <div class="scroll">
            <!-- About page -->
            <div class="about page">
                <div id="title">
                    Page
                </div>
                <div id="content">
                    Lorem ipsum about me ips sa asd sda asd as das dasasd asd asd asd asd asd as d
                    Lorem ipsum about me ips sa asd sda asd as das dasasd asd asd asd asd asd as d
                    Lorem ipsum about me ips sa asd sda asd as das dasasd asd asd asd asd asd as d
                    Lorem ipsum about me ips sa asd sda asd as das dasasd asd asd asd asd asd as d
                    Lorem ipsum about me ips sa asd sda asd as das dasasd asd asd asd asd asd as d
                    Lorem ipsum about me ips sa asd sda asd as das dasasd asd asd asd asd asd as d
                    Lorem ipsum about me ips sa asd sda asd as das dasasd asd asd asd asd asd as d
                    Lorem ipsum about me ips sa asd sda asd as das dasasd asd asd asd asd asd as d
                    Lorem ipsum about me ips sa asd sda asd as das dasasd asd asd asd asd asd as d
                    Lorem ipsum about me ips sa asd sda asd as das dasasd asd asd asd asd asd as d
                    Lorem ipsum about me ips sa asd sda asd as das dasasd asd asd asd asd asd as d

                </div>
            </div>
        </div>
        <div class="scroll">
            <!-- About me -->
            <div class="about me">
                <div id="title">
                    Me
                </div>
                <div id="content">
                    Lorem ipsum about me
                    Lorem ipsum about me ips sa asd sda asd as das dasasd asd asd asd asd asd as d
                    Lorem ipsum about me ips sa asd sda asd as das dasasd asd asd asd asd asd as d
                    Lorem ipsum about me ips sa asd sda asd as das dasasd asd asd asd asd asd as d
                    Lorem ipsum about me ips sa asd sda asd as das dasasd asd asd asd asd asd as d
                    Lorem ipsum about me ips sa asd sda asd as das dasasd asd asd asd asd asd as d
                    Lorem ipsum about me ips sa asd sda asd as das dasasd asd asd asd asd asd as d
                    Lorem ipsum about me ips sa asd sda asd as das dasasd asd asd asd asd asd as d
                    Lorem ipsum about me ips sa asd sda asd as das dasasd asd asd asd asd asd as d
                    Lorem ipsum about me ips sa asd sda asd as das dasasd asd asd asd asd asd as d
                    Lorem ipsum about me ips sa asd sda asd as das dasasd asd asd asd asd asd as d

                </div>
            </div>
        </div>
    </div>
</div>
</template>
<script>

import Login from "@/components/Login.vue"
import Logout from "@/components/Logout.vue"

export default {
  name: 'About',
  components: {
      Login,
      Logout
  }
}
</script>