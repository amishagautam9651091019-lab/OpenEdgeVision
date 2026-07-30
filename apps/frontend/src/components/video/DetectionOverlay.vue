<template>

<canvas
    ref="canvasRef"
    class="detection-overlay"
></canvas>

</template>



<script setup lang="ts">

import {
    ref,
    onMounted,
    onBeforeUnmount,
    watch,
    nextTick
}
from 'vue'



import {
    useDetectionStore
}
from '@/stores/detection'



import type {
    DetectionObject
}
from '@/types/detection'





interface Props {


    /**
     * 当前视频流名称
     */
    streamName:string



    /**
     * AI原始输入宽度
     *
     * 例如:
     * 1920
     */
    sourceWidth?:number



    /**
     * AI原始输入高度
     *
     * 例如:
     * 1080
     */
    sourceHeight?:number



    /**
     * 是否显示标签
     */
    showLabel?:boolean


}




const props =
withDefaults(
    defineProps<Props>(),
{

    sourceWidth:1920,

    sourceHeight:1080,

    showLabel:true

}

)





const canvasRef =
    ref<HTMLCanvasElement | null>(null)




const store =
    useDetectionStore()






let resizeObserver:
ResizeObserver | null = null







/**
 * 获取当前检测结果
 */
function getDetections()
:
DetectionObject[]
{


    return (

        store.detections[
            props.streamName
        ]
        ??
        []

    )


}








/**
 * Canvas尺寸同步
 */
function resizeCanvas(){


    const canvas =
        canvasRef.value


    if(!canvas){

        return

    }



    const parent =
        canvas.parentElement



    if(!parent){

        return

    }



    canvas.width =
        parent.clientWidth



    canvas.height =
        parent.clientHeight



    draw()



}







/**
 * 坐标映射
 */
function mapBBox(
    bbox:any
){


    const canvas =
        canvasRef.value



    if(!canvas){

        return null

    }



    const scaleX =
        canvas.width /
        props.sourceWidth



    const scaleY =
        canvas.height /
        props.sourceHeight




    return {


        x:
            bbox.x *
            scaleX,



        y:
            bbox.y *
            scaleY,



        width:
            bbox.width *
            scaleX,



        height:
            bbox.height *
            scaleY


    }


}








/**
 * 绘制检测框
 */
function draw(){


    const canvas =
        canvasRef.value



    if(!canvas){

        return

    }



    const ctx =
        canvas.getContext(
            "2d"
        )



    if(!ctx){

        return

    }



    ctx.clearRect(
        0,
        0,
        canvas.width,
        canvas.height
    )





    const detections =
        getDetections()



    detections.forEach(
        (
            item
        )=>{


            const box =
                mapBBox(
                    item.bbox
                )



            if(!box){

                return

            }




            ctx.lineWidth =
                2



            ctx.strokeStyle =
                "#00ff00"



            ctx.strokeRect(

                box.x,

                box.y,

                box.width,

                box.height

            )





            if(
                props.showLabel
            ){



                const text =
                    `${item.class_name} ${(item.confidence*100).toFixed(1)}%`



                ctx.font =
                    "16px Arial"



                ctx.fillStyle =
                    "#00ff00"



                ctx.fillText(

                    text,

                    box.x,

                    box.y - 5

                )


            }



        }

    )




}








watch(

    ()=>store.detections[props.streamName],


    ()=>{


        nextTick(
            ()=>{
                draw()
            }
        )


    },


    {
        deep:true
    }

)







onMounted(()=>{


    resizeCanvas()



    resizeObserver =
        new ResizeObserver(
            ()=>{
                resizeCanvas()
            }
        )



    if(canvasRef.value?.parentElement){


        resizeObserver.observe(

            canvasRef.value.parentElement

        )

    }


})







onBeforeUnmount(()=>{


    if(resizeObserver){


        resizeObserver.disconnect()


        resizeObserver=null

    }


})



</script>




<style scoped>


.detection-overlay{


    position:absolute;


    left:0;


    top:0;


    width:100%;


    height:100%;


    pointer-events:none;


}



</style>