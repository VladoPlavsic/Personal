<template>
    <div id="inner-login-div">
    <!-- Logo -->
        <div class="logo">
            <router-link :to="{name: 'Home'}"> 
            <span>VP</span>
            </router-link>
        </div>
        <div class="buttons">
            <div v-on:click="logOut()">
                <SignButton label="Log out"/>
            </div>
        </div>
    </div>
</template>

<script>
import SignButton from '@/components/buttons/SignButton'

export default {
    name: "Login",
    methods: {
        logOut() {
            this.$setCookie('loggedIn', false);
            this.$removeCookie('jwt');
        }
    },
    components: {
        SignButton
    },
}
</script>
