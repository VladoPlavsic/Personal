<template>
    <div id="inner-login-div">
    <!-- Logo -->
        <div class="logo">
            <router-link :to="{name: 'Home'}"> 
            <span>VP</span>
            </router-link>
        </div>
        <div class="buttons">
            <div>
                <router-link :to="{name: 'SignIn'}">
                    <SignButton label="Sign In"/>
                </router-link>
            </div>
            <div>
                <router-link :to="{name: 'SignUp'}">
                    <SignButton label="Sign Up"/>
                </router-link>
            </div>
        </div>
    </div>
</template>

<script>
import SignButton from '@/components/buttons/SignButton'

export default {
    name: "Login",
    methods:{
        signIn() {

        },
        singUp() {

        },
    },
    components: {
        SignButton
    }
}
</script>
