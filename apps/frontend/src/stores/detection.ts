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


    detections:
    Record<
        string,
        DetectionObject[]
    >



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


    if(!event){

        return

    }



    const objects =

        event.data?.detections

        ??

        event.data?.objects

        ??

        []




    this.detections[
        event.stream_name
    ] = objects



    this.timestamps[
        event.stream_name
    ] =
        event.timestamp



}






}

})