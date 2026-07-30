<template>

<div class="video-container">


    <iframe

        v-if="streamName"

        :src="playerUrl"

        class="video-frame"

        allow="autoplay; fullscreen"

    />


    <el-empty
        v-else
        description="无视频流"
    />



</div>


</template>



<script setup lang="ts">


import {
    computed
}
from 'vue'



interface Props {


    streamName:string


}



const props =
defineProps<Props>()



const playerUrl =
computed(()=>{


    return (

        `http://127.0.0.1:8889/${props.streamName}`

    )


})



</script>



<style scoped>


.video-container{


    width:100%;


    height:100%;


    position:relative;


    overflow:hidden;


    background:#000;


}




.video-frame{


    width:100%;


    height:100%;


    border:none;


    display:block;


}



</style>