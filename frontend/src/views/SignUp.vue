<template>
<div class="box">
    <h2 id="sign-in-header">Sign Up</h2>
    <div class="inputBox">
      <input id="sign-up-email" type="email" name="email" required onkeyup="this.setAttribute('value', this.value);" value="">
      <label>Email</label>
    </div>
    <div class="inputBox">
      <input id="sign-up-username" type="text" name="username" required onkeyup="this.setAttribute('value', this.value);" value="">
      <label>Username</label>
    </div>
    <div class="inputBox">
      <input id="sign-up-password" type="password" name="password" required value=""
             onkeyup="this.setAttribute('value', this.value);"
             pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"
             title="Must contain at least one number and one uppercase and lowercase letter, and at least 8 or more characters">
      <label>Password</label>
    </div>
     <div class="inputBox">
      <input id="sign-up-password-repeat" type="password" name="password" required value=""
             onkeyup="this.setAttribute('value', this.value);"
             pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"
             title="Must contain at least one number and one uppercase and lowercase letter, and at least 8 or more characters">
      <label>Repeat password</label>
    </div>
    <div id="sign-in-div" v-on:click="signUp()" >
        <SignButton label='SignUp'/>
    </div>
</div>
</template>

<script>
import SignButton from "@/components/buttons/CustomButton.vue"
import axios from 'axios'

import swal from 'sweetalert'
import { raiseSuccess, raiseError } from '../scripts/allertHandlers'

export default {
    name: 'SignUp',
    methods: {
        signUp(){
            var email_regex = new RegExp('@.'); // I don't care about this!
            var email = document.getElementById("sign-up-email").value;
            var username = document.getElementById("sign-up-username").value;
            var password = document.getElementById("sign-up-password").value;
            var repeatedPassword = document.getElementById("sign-up-password-repeat").value;

            if (!email.match(email_regex)){
                raiseError("Invalid email")
                return;
            }
            else if (username.length  < 5 || username.length > 15) {
                raiseError("Invalid username")
                return;
            }
            else if(password != repeatedPassword){
                raiseError("Passwords do not match!")
                return;
            }
            else if (password.length  < 5) {
                raiseError("Password to short")
                return;
            }

            axios.post(process.env.VUE_APP_REST_API_IP + "/api/authentication/register", 
            {
                new_user: 
                {
                    username: username,
                    email: email,
                    password: password
                }
            }).then(function (response){

                raiseSuccess("Congrats! You've become a member of most useles site in site history!").then(() => { 
                    window.location.href = '/';
                });

            }).catch(function (error){
                if(error.response){
                    // Request made and server responsed
                    if (error.response.status === 409){
                        raiseError(error.response.data.detail);
                    }
                } else if (error.request){
                    // Request mad no server response received
                } else{
                    // Unhandled error
                }
            });
        }
    },
    components:{
        SignButton
    }
}
</script>
