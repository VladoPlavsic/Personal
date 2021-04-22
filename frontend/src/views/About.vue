<template>
<div id="about">
    <Header v-on="$listeners" firstSelect="Home" secondSelect="Contact" thirdSelect="Articles"/>
    <div class="body">
        <div class="card" v-for="card in cards" :key="card">
            <div class="card-front"><img :src="card.image_url" /></div>
            <div class="card-back">
                <h2>{{card.title}}</h2>
                <br>
                <span>{{card.body}}</span>
            </div>
        </div>
    </div>

</div>


</template>

<script>
import Header from '@/components/Header'
import axios from 'axios'

export default {
  name: 'About',
  methods:{
      log() {
          console.log("press")
      }
  },
  data() {
      return {
        cards: []
      }
  },
  beforeCreate()
  {
        axios.get("http://localhost:8000/api/public/get/about").then((response) => {
            this.cards = response.data;
            console.log(this.cards);
        });
  },
  components:{
      Header
  },
}
</script>

<style scoped>

#about{
    display: flex;
    flex-direction: column;
}

.body{
    display: flex;
    flex-direction: row;
    text-align: center;
    margin-top: 80px;
    align-self: center;
    min-height: 50vh;
    min-width: 50vw;
    justify-content: center;
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
    background-color: #000000;
    backface-visibility: hidden;
    transform: rotateY(0deg);
    transition: 0.75s;
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
    background-color: white;
    backface-visibility: hidden;
    transform: rotateY(180deg);
    transition: 0.75s;
    color: black;
    text-align: center;
}

</style>