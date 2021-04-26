<template>
<div id="articles">
    <Header v-on="$listeners" firstSelect="Home" secondSelect="Contact" thirdSelect="About" firstSelectHref="home" secondSelectHref="contact" thirdSelectHref="about"/>
    
    <div  v-if="$cookies.loggedIn === 'true'" class="body">
        Access Allowed
    </div>
    <div  v-if="$cookies.loggedIn === 'false'" class="body">
        <div id="centered-text">
          Access denied!
        </div>
    </div>
</div>
</template>

<script>
import Header from '@/components/Header'

export default {
  name: 'Articles',
  components:{
      Header,   
    }
}
</script>

<style scoped>

#articles{
    display: flex;
    flex-direction: column;
}

.body{
    margin-top: 80px;
    align-self: center;
    display: table;
    min-height: 50vh;
    min-width: 50vw;
    text-align: center;
}

#centered-text{
  display: table-cell;
  vertical-align: middle;
}

</style>