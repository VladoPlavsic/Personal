<template>
<div id="home">
        <Header v-on="$listeners" firstSelect="About" secondSelect="Contact" thirdSelect="Articles" firstSelectHref="about" secondSelectHref="contact" thirdSelectHref="articles"/>
    <div class="body">
    <div v-if="this.$parent.edit">
        Select a photo for home page: <br>
        <input type="file" accept=".jpg" id="imageFile">
        <br>
        <button v-on:click="insertHomeImage">Insert</button>
        <button v-on:click="updateHomeImage">Update</button>
        <button v-on:click="deleteHomeImage">Delete</button>
    </div>
    <div>
      <img :src="homeImage">
    </div>
    </div>
</div>
</template>

<script>
import Header from '@/components/Header'

import axios from 'axios'
import EasyYandexS3 from 'easy-yandex-s3'
import swal from 'sweetalert'

export default {
  name: 'Home',
  data() {
      return {
         homeImage: '',
         homeImageId: 0,
         homeImageKey: '',
      }
  },
beforeCreate()
    {
        axios.get(process.env.VUE_APP_REST_API_IP + "/api/public/get/home").then((response) => {
            var image = response.data[Math.floor(Math.random() * response.data.length)];
            this.homeImage = image.image_url;
            this.homeImageId = image.id;
            this.homeImageKey = image.image_key;
        })
  },
  methods:{
      noFile(){
        swal({
            title: "Fail!",
            text: "Plese select a file",
            icon: "error",
        })
      },
      insertHomeImage(){
            var fileBuffer = document.getElementById("imageFile").files[0];

            if (!fileBuffer){
                this.noFile();
                return;
            }

            var s3 = new EasyYandexS3({
                auth:{
                    accessKeyId: process.env.VUE_APP_ACCESS_KEY_ID,
                    secretAccessKey: process.env.VUE_APP_SECRET_ACCESS_KEY,
                },
                Bucket: 'vlado',
            })

            s3.Upload({
                buffer: fileBuffer,
                name: fileBuffer.name,
            }, '/home/').then((response) => {
                axios.post(process.env.VUE_APP_REST_API_IP + "/api/public/create/home", {
                    new_home: {
                        image_key: response.key
                    }
                }).then((response) => {
                    var image = response.data
                    this.homeImage = image.image_url;
                    this.homeImageId = image.id;
                    this.homeImageKey = image.image_key;
                }).catch((error) => {

                })
            })
      },
      updateHomeImage(){
           var fileBuffer = document.getElementById("imageFile").files[0];

            if (!fileBuffer){
                this.noFile();
                return;
            }

            var s3 = new EasyYandexS3({
                auth:{
                    accessKeyId: process.env.VUE_APP_ACCESS_KEY_ID,
                    secretAccessKey: process.env.VUE_APP_SECRET_ACCESS_KEY,
                },
                Bucket: 'vlado',
            })

            s3.Upload({
                buffer: fileBuffer,
                name: fileBuffer.name,
            }, '/home/').then((response) => {
                axios.put(process.env.VUE_APP_REST_API_IP + "/api/public/update/home", {
                    updated_home: {
                        id: this.homeImageId,
                        old_key: this.homeImageKey,
                        image_key: response.key,
                    }
                }).then((response) => {
                    var image = response.data
                    this.homeImage = image.image_url;
                    this.homeImageId = image.id;
                    this.homeImageKey = image.image_key;
                }).catch((error) => {

                })
            })
      },
      deleteHomeImage(){
          axios.delete(process.env.VUE_APP_REST_API_IP + "/api/public/delete/home?id=" + this.homeImageId
          ).then((response) => {
            axios.get(process.env.VUE_APP_REST_API_IP + "/api/public/get/home").then((response) => {
                var image = response.data[Math.floor(Math.random() * response.data.length)];
                this.homeImage = image.image_url;
                this.homeImageId = image.id;
                this.homeImageKey = image.image_key;
            })
        })
      }
  },
  components:{
      Header,   
    },


}
</script>

<style scoped>

#home{
    display: flex;
    flex-direction: column;
}

#home img{
    max-height: 70vh;
    max-width: 80vw;
    display: block;
    margin-left: auto;
    margin-right: auto;
    flex-shrink: 0;
    min-width: 100%;
    min-height: 100%;
}

.body{
    text-align: center;
    align-self: center;
}

.body *{
    margin-top: 30px;
}

.body button{
    margin-right: 4px;
    margin-left: 4px;
}


</style>