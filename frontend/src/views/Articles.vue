<template>
<div id="articles">
    <Header v-on="$listeners" firstSelect="About" secondSelect="Contact" thirdSelect="Articles" firstSelectHref="about" secondSelectHref="contact" thirdSelectHref="articles"/>
    
    <div  v-if="$cookies.loggedIn === 'true'" class="body">
      <div class="body">
        <!-- Content -->
        <div id="articleSub" >
          <div class="list" v-for="(subgroup, i) in subgroups" :key="i">
              <div class="listItems">
                <div class="listItem">
                  <a :href="subgroup.url">
                    <div class="num">
                        <p>{{i + 1}}</p>
                        <h3>{{subgroup.name}}</h3>
                    </div>
                  </a>
                </div>
                <!-- Delete -->
                <div v-if="$parent.edit" class="articleSubEdit" v-on:click="deleteSubgroup" :id="subgroup.id">
                  <svg height="20" width="20" viewBox="0 0 512 512" :id="subgroup.id">
                    <path d="m511.058 60.811-60.811-60.811-194.718 194.718-194.718-194.718-60.811 60.811 194.718 194.718-194.718 
                    194.718 60.811 60.811 194.718-194.718 194.718 194.718 60.811-60.811-194.718-194.718z" :id="subgroup.id"/>
                  </svg>
                </div>
              </div>
            </div>
          </div>
        
        <!-- Add content -->
        <div v-if="$parent.edit" id="articleSubAdd">
          <textarea placeholder="Subgroup name" id="subgroupName" cols="30" rows="1"></textarea>
          <button v-on:click="addSubgroup">Add</button>
        </div>
      </div>
    </div>
    <div  v-if="$cookies.loggedIn === 'false'" class="body">
        <div id="centeredText">
          <a href="/sign/in"> Access denied!</a>
        </div>
    </div>
</div>
</template>

<script>
import Header from '@/components/Header'

import axios from 'axios'
import { raiseError, raiseAllertDelete } from '../scripts/allertHandlers'

export default {
  name: 'Articles',
  data() {
    return {
      subgroups: []
    }
  },
  beforeCreate() {
    axios.get(process.env.VUE_APP_REST_API_IP + "/api/articles/get/subgroup"
    ).then((response) => {
      this.subgroups = response.data;
    })
  },
  methods: {
    addSubgroup() {
      var name = document.getElementById("subgroupName").value;
      var names = this.subgroups.map(subgroup => subgroup.name.toLowerCase());

      if(names.includes(name.toLowerCase())){
        this.raiseError("This subgroup already exists!");
        return;
      }

      axios.post(process.env.VUE_APP_REST_API_IP + "/api/articles/create/subgroup?token=" + this.$cookies.jwt,{
        new_subgroup: {
          name: name,
          url: "articles/" + name.toLowerCase()
        }
      }).then((response) => {
         this.subgroups.push(response.data);
      }).catch((error) => {

      })
    },
    deleteSubgroup(e) {

      raiseAllertDelete("Are you sure?").then((response) => {
        if (response){
          axios.delete(process.env.VUE_APP_REST_API_IP + "/api/articles/delete/subgroup?token=" + this.$cookies.jwt + "&id=" + e.target.id
          ).then((response) => {
              axios.get(process.env.VUE_APP_REST_API_IP + "/api/articles/get/subgroup"
              ).then((response) => {
                this.subgroups = response.data;
              })
          })
        }
      })

    },
  },
  components:{
      Header,   
    }
}
</script>

<style scoped>
#articleSubAdd{
  margin-top: 30px;
  display: flex;
  flex-direction: row;
  justify-content: center;
}

textarea{
    border: none;
    resize: none;
    border: none;
    box-shadow: 1px 1px 2px gray;
}

textarea:focus{
    outline: 0;
    box-shadow: 1px 1px 2px black;
}

#articleSubAdd *{
  margin-left: 5px;
  margin-right: 5px;
  background-color: #FBF0D9;
}

#articles{
    display: flex;
    flex-direction: column;
}

.articleSubEdit *{
  margin-left: 10px;
  cursor: pointer;
}

.articleSubEdit:hover{
  fill: red;
}

#articleSub{
  margin-top: 50px;
}

.body{
    display: flex;
    flex-wrap: wrap;
    flex-direction: row;
    align-self: center;
    display: table;
    min-height: 50vh;
    min-width: 50vw;
}

.list .num {
  padding: 0.5rem 2rem;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  transition: 0.25s;
}

.listItems{
  display: flex;
  align-items: stretch;
  flex-direction: row;
}

.listItem{
  flex: 1;
}

.list .num p{
  font-size: 3rem;
  font-weight: bold;
  color: #000;
  width: 2rem;
  opacity: 0.05;
  transition: 0.25s;
}

.list .num h3 {
  position: relative;
  font-weight: 600;
  left: -1.5rem;
  color: #3d3d3d;
  font-size: 1.5rem;
  transition: 0.25s;
}

.list .num:hover {
  background-color: #FBF0AF;
  cursor: pointer;
}

.list .num:hover p {
  opacity: 0.6;
}

.list .num:hover:before {
  opacity: 0.2;
}

.list .num:hover h3 {
  left: 1rem;
}

#centeredText{
  display: flex;
  margin-top: 30vh;
  justify-content: center;
}

</style>