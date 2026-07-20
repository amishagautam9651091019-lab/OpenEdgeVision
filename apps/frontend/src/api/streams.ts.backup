import http from './http'


export interface StreamInfo {

    name:string

    ready:boolean

    source_type:string

    reader_count:number

    tracks:string[]

    rtsp_url:string

    webrtc_url:string

    hls_url:string

}


export interface StreamSummary {

    total:number

    online:number

    offline:number

    streams:StreamInfo[]

}



export async function getStreams(){

    return http.get<
        any,
        {
            code:number,
            data:StreamSummary
        }
    >(
        '/api/v1/streams'
    )

}