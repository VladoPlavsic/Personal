<template>
<div id="aboutTemplate">
    <Header v-on="$listeners" firstSelect="About" secondSelect="Contact" thirdSelect="Articles" firstSelectHref="about" secondSelectHref="contact" thirdSelectHref="articles"/>
    
    <div class="body">
        <div v-if="$parent.edit" id="aboutEdit">
            <input type="number" min="1" id="orderNumberInput" placeholder="orderNumber" v-on:change="autoFill">
            <br>
            Select a photo: <br>
            <input type="file" accept=".jpg" id="imageFile">
            <br>
            <textarea id="titleInput" placeholder="Title" cols="40" rows="1"></textarea>
            <br>
            <textarea id="contentInput" placeholder="Content" cols="40" rows="5"></textarea>
            <br>
            <button v-on:click="insertAbout">Insert</button>
            <button v-on:click="updateAbout">Update</button>
            <button v-on:click="deleteAbout">Delete</button>
        </div>
        <div class="card" v-for="(card, i) in cards" :key="i">
            <div class="card-front">
                <img :src="card.image_url" />
            </div>
            <div v-if="$parent.edit" id="img-text">{{card.order}}</div>
            <div class="card-back">
                <h2>{{card.title}}</h2>
                <br>
                <span>
                    <p v-html="card.body"></p>
                </span>
            </div>
        </div>
    </div>

</div>


</template>

<script>
import Header from '@/components/Header'

import axios from 'axios'

import { getCloudClient } from '../scripts/cloudHandlers'
import { raiseError } from '../scripts/allertHandlers'

export default {
  name: 'About',
  data() {
      return {
        cards: [],
      }
  },
  beforeCreate()
  {
        axios.get(process.env.VUE_APP_REST_API_IP + "/api/public/get/about").then((response) => {
            this.cards = response.data;
        });
  },
  methods:{
    autoFill() {
        var orderNumber = parseInt(document.getElementById("orderNumberInput").value)

        var existingOrderNumbers = this.cards.map(order => order.order);

        if(existingOrderNumbers.includes(orderNumber)){

            var oldContent = this.cards.filter(card => card.order == orderNumber)[0];

            document.getElementById("titleInput").value = oldContent.title;
            document.getElementById("contentInput").value = oldContent.body;

        }else{
            document.getElementById("titleInput").value = "";
            document.getElementById("contentInput").value = "";

        }

    },
    insertAbout() {
        var fileBuffer = document.getElementById("imageFile").files[0];

        var orderNumber = parseInt(document.getElementById("orderNumberInput").value)
        var title = document.getElementById("titleInput").value
        var content = document.getElementById("contentInput").value

        var existingOrderNumbers = this.cards.map(order => order.order);

        var existingKeys = this.cards.map(key => key.image_key.split("/")[1]);

        if (!orderNumber){
            this.raiseError("Plese enter valid order number.");
            return;
        }else if(existingOrderNumbers.includes(orderNumber)){
            this.raiseError("Order number taken. \n Taken numbers: " + existingOrderNumbers);
            return;
        }else if(!fileBuffer){
            this.raiseError("Plese select a file.");
            return;
        }else if(existingKeys.includes(fileBuffer.name)){
            this.raiseError("File with given name already exists.\nPlease rename it or chose another one.");
            return;
        }else if (!title){
            this.raiseError("Please enter title.");
            return;
        }else if(!content){
            this.raiseError("Please enter some content.");
            return;
        }

        var s3 = getCloudClient();

        s3.Upload({
            buffer: fileBuffer,
            name: fileBuffer.name,
        }, '/about/').then((response) => {
            axios.post(process.env.VUE_APP_REST_API_IP + "/api/public/create/about?token=" + this.$cookies.jwt, {
                new_about: {
                    order: orderNumber,
                    image_key: response.key,
                    title: title.replace(/'/g, '`'),
                    body: content.replace(/'/g, '`'),
                }
            }).then((response) => {
                axios.get(process.env.VUE_APP_REST_API_IP + "/api/public/get/about").then((response) => {
                    this.cards = response.data;
                });
                
            }).catch((error) => {
                console.log(error);
            })
        })


    },
    updateAbout() {
        var fileBuffer = document.getElementById("imageFile").files[0];

        var orderNumber = parseInt(document.getElementById("orderNumberInput").value)
        var title = document.getElementById("titleInput").value
        var content = document.getElementById("contentInput").value

        var existingOrderNumbers = this.cards.map(order => order.order);

        // all existing keys exclude updating key (it can be the same)
        var existingKeys = this.cards.filter(key => key.order != orderNumber).map(key => key.image_key.split("/")[1]);

        var oldKey = this.cards.filter(key => key.order == orderNumber).map(key => key.image_key)[0];

        if (!orderNumber){
            this.raiseError("Plese enter valid order number.");
            return;
        }else if(!existingOrderNumbers.includes(orderNumber)){
            this.raiseError("Order number doesn't exist. \n Numbers: " + existingOrderNumbers);
            return;
        }else if(fileBuffer && existingKeys.includes(fileBuffer.name)){
            this.raiseError("File with given name already exists.\nPlease rename it or chose another one.");
            return;
        }

        if (fileBuffer){
            var s3 = getCloudClient()

            s3.Upload({
                buffer: fileBuffer,
                name: fileBuffer.name,
            }, '/about/').then((response) => {
                axios.put(process.env.VUE_APP_REST_API_IP + "/api/public/update/about?token=" + this.$cookies.jwt, {
                    updated_about: {
                        order: orderNumber,
                        image_key: response.key,
                        title: title.replace(/'/g, '`'),
                        body: content.replace(/'/g, '`'),
                        old_key: oldKey,
                    }
                }).then((response) => {
                    axios.get(process.env.VUE_APP_REST_API_IP + "/api/public/get/about").then((response) => {
                        this.cards = response.data;
                    });
                }).catch((error) => {
                    console.log(error);
                })
            })
        }else{
            axios.put(process.env.VUE_APP_REST_API_IP + "/api/public/update/about?token=" + this.$cookies.jwt, {
                updated_about: {
                    order: orderNumber,
                    title: title.replace(/'/g, '`'),
                    body: content.replace(/'/g, '`'),
                    old_key: oldKey,
                }
            }).then((response) => {
                axios.get(process.env.VUE_APP_REST_API_IP + "/api/public/get/about").then((response) => {
                    this.cards = response.data;
                });
            }).catch((error) => {
                console.log(error);
            })
        }

    }, 
    deleteAbout() {
        var orderNumber = parseInt(document.getElementById("orderNumberInput").value)
        
        var existingOrderNumbers = this.cards.map(order => order.order);

        if (!orderNumber){
            this.raiseError("Plese enter valid order number.");
            return;
        }
        else if(!existingOrderNumbers.includes(orderNumber)){
            this.raiseError("Order number doesn't exist. \n Numbers: " + existingOrderNumbers);
            return;
        }

        axios.delete(process.env.VUE_APP_REST_API_IP + "/api/public/delete/about?order=" + orderNumber + "&token="+ this.$cookies.jwt
        ).then((response) => {

            axios.get(process.env.VUE_APP_REST_API_IP + "/api/public/get/about").then((response) => {
                this.cards = response.data;
            });
                
        })

    },
  },
  components:{
      Header
  },
}
</script>

<style scoped>

#aboutTemplate{
    display: flex;
    flex-direction: column;
}

.body{
    display: flex;
    flex-wrap: wrap;
    flex-direction: row;
    text-align: center;
    margin-top: 80px;
    align-self: center;
    min-height: 50vh;
    min-width: 50vw;
    justify-content: center;
}

#aboutEdit{
    margin-top: 20px;
}


#aboutEdit textarea, #orderNumberInput{
    border: none;
    box-shadow: 1px 1px 2px gray;
}

textarea:focus, input:focus{
    outline: 0;
}

#aboutEdit *{
    background-color: #FBF0D9;
}

.card{
    margin: 50px;
    height: 400px;
    width: 300px;
    perspective: 600px;
    transition: 0.75s;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    border-radius: 20px;
}
.card:hover .card-front{
    transform: rotateY(-180deg);
}
.card:hover .card-back{
    transform: rotateY(0deg);
}
.card-front{
    height: 100%;
    width: 100%;
    background-position: 50% 50%;
    background-size: cover;
    position: absolute;
    top: 0;
    left: 0;
    backface-visibility: hidden;
    transform: rotateY(0deg);
    transition: 0.75s;
}

#img-text{
    color: white;
    text-shadow: 8px 8px 50px black;
    background: rgba(0, 0, 0, 10%);
    font-size: 30px;
    z-index: 0;
}

#titleInput{
    resize: none;
}

.card-front img{
    max-height: 400px;
    max-width: 300px;
    display: block;
    margin-left: auto;
    margin-right: auto;
    flex-shrink: 0;
    min-width: 100%;
    min-height: 100%
}

.card-back{
    height: 100%;
    width: 100%;
    position: absolute;
    top: 0;
    left: 0;
    background-color: #FBF0D9;
    backface-visibility: hidden;
    transform: rotateY(180deg);
    transition: 0.75s;
    color: black;
    text-align: center;
}

.body > #aboutEdit *{
    margin-top: 30px;
    margin-left: 20px;
}

.body button{
    margin-right: 4px;
    margin-left: 4px;
}

@media only screen and (max-width: 1000px) {

    .body{
        flex-direction: column;
    }
    .card:active .card-front{
    transform: rotateY(-180deg);
    }
    .card:active .card-back{
        transform: rotateY(0deg);
    }

}

</style>