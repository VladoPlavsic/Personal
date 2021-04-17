<template>
<div>
    <a href="javascript:;">
        <svg class="icon-arrow before">
            <use xlink:href="#arrow"></use>
        </svg>
        <span class="label">{{label}}</span>
        <svg class="icon-arrow after">
            <use xlink:href="#arrow"></use>
        </svg>
    </a>
    
    <svg style="display: none;">
      <defs>
        <symbol id="arrow" viewBox="0 0 35 15">
          <title>Arrow</title>
          <path d="M27.172 5L25 2.828 27.828 0 34.9 7.071l-7.07 7.071L25 11.314 27.314 9H0V5h27.172z "/>
        </symbol>
      </defs>
    </svg>
</div>
</template>

<script>
import App from '../../App.vue'
export default {
  components: { App },
  name: "SignButton",
  props: ['label'],
}
</script>

<style scoped>
html, body {
    display: grid;
    height: 100%;
}

a {
    border: 4px solid #3F3F3F;
    border-radius: 20px;
    color: #3F3F3F;
    display: inline-block;
    font-size: 15px;
    font-weight: bold;
    line-height: 15px;
    margin: auto;
    padding: 12px 32px 12px 82px;
    position: relative;
    text-decoration: none;
}

a .label,
a .icon-arrow {
    backface-visibility: hidden;
    transform: translateZ(0);
    perspective: 1000;
}

a .label {
    display: inline-block;
    transition: transform .5s cubic-bezier(0.86, 0, 0.07, 1);
}

a .icon-arrow {
    position: relative;
    fill: #3F3F3F;
    height: 15px;
    top: 13px;
    transition: transform .5s cubic-bezier(0.86, 0, 0.07, 1), opacity .4s cubic-bezier(0.86, 0, 0.07, 1);
    width: 15px;
}

a .icon-arrow.before {
    left: 32px;
    margin-right: 15px;
    position: absolute;
    transform-origin: left center;
}

a .icon-arrow.after {
    margin-left: 15px;
    opacity: 0;
    position: absolute;
    right: 32px;
    transform: translateX(75%) scaleX(0.1);
    transform-origin: right center;
}

a:hover .label {
    transform: translateX(-52px);
}

a:hover .icon-arrow.before {
    opacity: 0;
    transform: translateX(-75%) scaleX(0.1);
}

a:hover .icon-arrow.after {
    opacity: 1;
    transform: translateX(0) scaleX(1);
}

a:active {
    border-color: #69becf;
    color: #69becf;
}

a:active .icon-arrow {
    fill: #69becf;
}
</style>
