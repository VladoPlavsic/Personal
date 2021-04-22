<template>
<div id="home">
    <Header v-on="$listeners" firstSelect="About" secondSelect="Contact" thirdSelect="Articles"/>
    <div class="body">
      
    </div>
</div>
</template>

<script>
import Header from '@/components/Header'

import axios from 'axios'

export default {
  name: 'Home',
  components:{
      Header,   
    }
}
</script>

<style scoped>

#home{
    display: flex;
    flex-direction: column;
}

.body{
    text-align: center;
    margin-top: 80px;
    align-self: center;
    min-height: 50vh;
    min-width: 50vw;
    border: 2px solid black;
}

</style>