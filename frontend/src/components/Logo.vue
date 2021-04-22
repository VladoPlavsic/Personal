<template>
        <div class="logo">
            <router-link :to="{name: 'Home'}"> 
            <span>VP</span>
            </router-link>
        </div>
</template>

<script>

export default {
    name: "Logo",
}
</script>

<style scoped>
.logo{
    padding-top: 10px;
    padding-right: 10px;
    font-family: "ShadowsIntoLight", cursive;
    align-content: center;
    font-size: 50px;
    overflow: hidden;
    transition: 0.2s;
    max-height: fit-content;
    max-width: fit-content;
    transform: rotate(0deg);
    cursor: pointer;
}

.logo:hover{
    box-shadow: 1px 1px 20px black;
    animation: rotation 0.4s linear;
    animation-iteration-count: 5;
}

.logo:active{
    transition: 0.2s;
    transform: rotate(-8deg);
    animation: rotation 0.4s linear;
    animation-iteration-count: 5;
}

@keyframes rotation {
  30% {
    transform: rotate(4deg);
  }
  60% {
    transform: rotate(-4deg);
  }
  100% {
    transform: rotate(0deg);
  }
}

</style>