<script setup lang="ts">

import {
    ref,
    onMounted
} from 'vue'


import {
    getStreams,
    type StreamInfo
} from '@/api/streams'


const streams =
    ref<StreamInfo[]>([])


const loading =
    ref(false)



async function loadStreams(){

    loading.value=true


    try{

        const res =
            await getStreams()


        streams.value =
            res.data.streams


    }
    catch(error){

        console.error(error)

    }
    finally{

        loading.value=false

    }

}



onMounted(()=>{

    loadStreams()

})


</script>