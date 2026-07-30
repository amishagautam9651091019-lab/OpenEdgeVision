import {
    defineStore
}
from 'pinia'


import type {
    DetectionObject,
    DetectionEvent
}
from '@/types/detection'



interface DetectionState {


    // 每个视频流当前检测结果

    detections:
    Record<
        string,
        DetectionObject[]
    >



    // 每个流最后更新时间

    timestamps:
    Record<
        string,
        number
    >



}




export const useDetectionStore =
defineStore(
'detection',
{


state:():DetectionState=>({


    detections:{},


    timestamps:{}


}),




actions:{



    updateDetection(
        event:DetectionEvent
    ){



        if(
            !event.data
        ){

            return

        }



        this.detections[
            event.stream_name
        ] =
            event.data.detections



        this.timestamps[
            event.stream_name
        ] =
            event.timestamp



    }





}



})