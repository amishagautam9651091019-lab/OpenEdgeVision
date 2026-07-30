import {
    WebSocketService
}
from './websocket'


import {
    useDetectionStore
}
from '@/stores/detection'


import type {
    DetectionEvent
}
from '@/types/detection'





export class DetectionListener {


    private ws:
        WebSocketService



    private store



    constructor(
        url:string
    ){


        this.ws =
            new WebSocketService(
                url
            )


        this.store =
            useDetectionStore()


    }





    start(){


        this.ws.onMessage(
            (
                event:DetectionEvent
            )=>{


                this.handleEvent(
                    event
                )


            }
        )


        this.ws.connect()


    }






    private handleEvent(

        event:DetectionEvent

    ){


        if(
            event.event_type
            !==
            'detection'
        ){

            return

        }



        if(
            !event.data
            ||
            !event.data.detections
        ){

            return

        }



        this.store.updateDetection(

            event.stream_name,

            event.data.detections,

            event.timestamp

        )


    }






    stop(){


        this.ws.disconnect()


        this.store.clear()


    }


}