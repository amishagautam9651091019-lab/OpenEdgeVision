import axios from 'axios'


const http = axios.create({

    baseURL:
        'http://127.0.0.1:8000',

    timeout:5000,

})


http.interceptors.response.use(

    response => {

        return response.data

    },

    error => {

        console.error(
            'API Error:',
            error
        )

        return Promise.reject(error)

    }

)


export default http