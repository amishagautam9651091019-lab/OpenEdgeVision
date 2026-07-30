<template>


<div class="ai-stream-player">


    <!-- 视频层 -->

    <VideoPlayer

        :stream-name="streamName"

    />



    <!-- AI检测框层 -->

    <DetectionOverlay

        :stream-name="streamName"

        :source-width="sourceWidth"

        :source-height="sourceHeight"

    />


</div>



</template>





<script setup lang="ts">


import {

    onMounted,

    onBeforeUnmount

}

from 'vue'





import VideoPlayer

from './VideoPlayer.vue'





import DetectionOverlay

from './DetectionOverlay.vue'





import {

    WebSocketService

}

from '@/services/websocket'





import {

    useDetectionStore

}

from '@/stores/detection'







interface Props {


    /**
     * 视频流名称
     */

    streamName:string



    /**
     * AI输入尺寸
     *
     * 根据模型调整
     */

    sourceWidth?:number


    sourceHeight?:number


}







const props =

withDefaults(

    defineProps<Props>(),

    {


        sourceWidth:1920,


        sourceHeight:1080


    }

)








const streamName =

    props.streamName





const sourceWidth =

    props.sourceWidth





const sourceHeight =

    props.sourceHeight







const detectionStore =

    useDetectionStore()






let websocket:

WebSocketService | null = null








function createWebSocketURL(){



    const protocol =

        window.location.protocol === 'https:'

        ?

        'wss'

        :

        'ws'





    return (

        `${protocol}://${window.location.hostname}:8000/ws/streams/${streamName}`

    )



}









onMounted(()=>{



    console.log(

        "AIStreamPlayer mounted:",

        streamName

    )





    websocket =

        new WebSocketService(

            createWebSocketURL()

        )







    websocket.onMessage(

        (event)=>{



            if(!event){


                return

            }






            console.log(

                "AI EVENT:",

                event

            )







            detectionStore.updateDetection(

                event

            )





        }

    )







    websocket.connect()



})









onBeforeUnmount(()=>{



    if(websocket){



        websocket.disconnect()



        websocket=null



    }



})





</script>







<style scoped>



.ai-stream-player{


    position:relative;


    width:100%;


    height:100%;


    overflow:hidden;



}



</style>