<template>
<div class="box">
    <h2 id="sign-in-header">Sign In</h2>
    <div class="inputBox">
      <input id="sign-in-username" type="text" name="usaername" required onkeyup="this.setAttribute('value', this.value);" value="">
      <label>Username</label>
    </div>
    <div class="inputBox">
      <input id="sign-in-password" type="password" name="password" required value=""
             onkeyup="this.setAttribute('value', this.value);"
             pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"
             title="Must contain at least one number and one uppercase and lowercase letter, and at least 8 or more characters">
      <label>Password</label>
    </div>
    <div id="sign-in-div" v-on:click="signIn()" >
        <SignButton label='SignIn'/>
    </div>
</div>
</template>

<script>
import SignButton from "@/components/buttons/CustomButton.vue"
import axios from 'axios'

export default {
    name: 'SignIn',
    methods: {
        signIn(){
            var username = document.getElementById("sign-in-username").value;
            var password = document.getElementById("sign-in-password").value;
            var header = document.getElementById('sign-in-header');

            if (username.length  < 5 || username.length > 15) {
                header.style.color = "red"
                header.innerText = "Invalid username";
            }
            else if (password.length  < 5) {
                header.style.color = "red"
                header.innerText = "Password to short";   
            }
            else{
                header.style.color = "black"
                header.innerText = "Sign In";
            }


            axios.post("http://localhost:8000/api/authentication/login", 
            {
                user: 
                {
                    username: username,
                    password: password
                }
            }).then((response) => {
                this.$setCookie('loggedIn', true);
                this.$setCookie('jwt', response.data.jwt.access_token);
                window.location.href = '/';

            }).catch(function (error){
                if(error.response){
                    // Request made and server responsed
                    if (error.response.status === 409){
                        header.style.color = "red"
                        header.innerText = error.response.data.detail;   
                    } // Could remove this condition but let it stay for future something
                    else {
                        header.style.color = "red"
                        header.innerText = error.response.data.detail;   
                    }
                } else if (error.request){
                    // Request mad no server response received
                    console.log(error.request);
                } else{
                    // Unhandled error
                    console.log('Error', error.message);
                }
            });
        }
    },
    components:{
        SignButton
    }
}
</script>
