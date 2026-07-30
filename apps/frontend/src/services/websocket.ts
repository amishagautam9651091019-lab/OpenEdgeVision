import type {
    DetectionEvent,
    DetectionPayload,
    DetectionObject
}
from '@/types/detection'



type MessageCallback =
    (
        event: DetectionEvent
    )=>void





/**
 * WebSocket原始消息
 *
 * 兼容：
 *
 * 1.
 * Pipeline Result
 *
 * {
 *   version:"1.0",
 *   task_type:"detection",
 *   objects:[]
 * }
 *
 *
 * 2.
 * Event Envelope
 *
 * {
 *   event_type:"detection",
 *   data:{
 *       objects:[]
 *   }
 * }
 *
 */
interface RawDetectionMessage {


    event_type?:string


    event_id?:string


    version?:string


    task_type?:string


    stream_name:string


    timestamp?:number


    frame_id?:number


    plugin_id?:string


    model?:string|null



    performance?:{

        capture_ms?:number

        preprocess_ms?:number

        inference_ms?:number

        postprocess_ms?:number

        pipeline_ms?:number

    }



    objects?:DetectionObject[]



    data?:any


}






/**
 * AI事件统一转换
 *
 * 所有模型输出
 *
 *        ↓
 *
 * DetectionEvent
 *
 */
function normalizeDetectionEvent(
    raw:RawDetectionMessage
):DetectionEvent {



    /*
     *
     * 已经是标准事件
     *
     */
    if(
        raw.event_type
        &&
        raw.data
    ){


        const payload =
            raw.data



        return {


            event_type:
                raw.event_type,



            event_id:
                raw.event_id
                ??
                crypto.randomUUID(),



            timestamp:
                raw.timestamp
                ??
                Date.now(),



            stream_name:
                raw.stream_name,



            plugin_id:
                raw.plugin_id
                ??
                "",



            data:{


                stream_name:
                    payload.stream_name
                    ??
                    raw.stream_name,



                frame_id:
                    payload.frame_id
                    ??
                    raw.frame_id
                    ??
                    0,



                timestamp:
                    payload.timestamp
                    ??
                    raw.timestamp
                    ??
                    Date.now(),



                plugin_id:
                    payload.plugin_id
                    ??
                    raw.plugin_id
                    ??
                    "",




                inference_time_ms:
                    payload.performance
                    ?.inference_ms
                    ??
                    raw.performance
                    ?.inference_ms
                    ??
                    0,



                pipeline_time_ms:
                    payload.performance
                    ?.pipeline_ms
                    ??
                    raw.performance
                    ?.pipeline_ms
                    ??
                    0,



                detections:
                    payload.detections
                    ??
                    payload.objects
                    ??
                    []



            }


        }


    }






    /*
     *
     * Pipeline原始结果
     *
     */
    return {



        event_type:
            "detection",



        event_id:
            crypto.randomUUID(),



        timestamp:
            raw.timestamp
            ??
            Date.now(),



        stream_name:
            raw.stream_name,



        plugin_id:
            raw.plugin_id
            ??
            "",




        data:{



            stream_name:
                raw.stream_name,



            frame_id:
                raw.frame_id
                ??
                0,



            timestamp:
                raw.timestamp
                ??
                Date.now(),



            plugin_id:
                raw.plugin_id
                ??
                "",



            inference_time_ms:
                raw.performance
                ?.inference_ms
                ??
                0,



            pipeline_time_ms:
                raw.performance
                ?.pipeline_ms
                ??
                0,



            detections:
                raw.objects
                ??
                []



        }



    }



}








export class WebSocketService {



    private socket:
        WebSocket | null = null




    private url:string




    private callback:
        MessageCallback | null = null





    constructor(
        url:string
    ){

        this.url=url

    }





    connect(){



        if(this.socket){

            return

        }




        this.socket =
            new WebSocket(
                this.url
            )





        this.socket.onopen=()=>{


            console.log(
                "WebSocket connected:",
                this.url
            )


        }





        this.socket.onmessage =
        (
            message
        )=>{


            try{


                const raw:
                    RawDetectionMessage =
                    JSON.parse(
                        message.data
                    )



                const event =
                    normalizeDetectionEvent(
                        raw
                    )



                if(this.callback){


                    this.callback(
                        event
                    )


                }



            }
            catch(error){


                console.error(
                    "WebSocket parse error",
                    error
                )


            }



        }






        this.socket.onerror =
        (
            error
        )=>{


            console.error(
                "WebSocket error",
                error
            )


        }






        this.socket.onclose = ()=>{


            console.log(
                "WebSocket closed"
            )


            this.socket=null


        }



    }





    onMessage(
        callback:MessageCallback
    ){


        this.callback =
            callback


    }







    disconnect(){



        if(this.socket){


            this.socket.close()


            this.socket=null


        }


    }





}