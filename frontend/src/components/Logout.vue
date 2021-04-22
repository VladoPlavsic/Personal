<template>
    <div v-on:click="logOut()">
        <SignButton label="Log out"/>
    </div>
</template>

<script>
import SignButton from '@/components/buttons/CustomButton'
import Logo from '@/components/Logo'


export default {
    name: "LogOut",
    methods: {
        logOut() {
            this.$setCookie('loggedIn', false);
            this.$removeCookie('jwt');
            this.$emit('re-render');
        }
    },
    components: {
        SignButton,
        Logo
    },
}
</script>
