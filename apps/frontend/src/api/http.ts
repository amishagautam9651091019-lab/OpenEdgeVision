import axios, {
    type AxiosRequestConfig
} from 'axios'

const axiosInstance = axios.create({

    baseURL: 'http://127.0.0.1:8000',

    timeout: 5000,

})

axiosInstance.interceptors.response.use(

    response => response.data,

    error => {

        console.error(
            'API Error:',
            error
        )

        return Promise.reject(error)

    }

)

const http = {

    get<T>(
        url: string,
        config?: AxiosRequestConfig
    ): Promise<T> {

        return axiosInstance.get<any, T>(
            url,
            config
        )

    },

    post<T>(
        url: string,
        data?: unknown,
        config?: AxiosRequestConfig
    ): Promise<T> {

        return axiosInstance.post<any, T>(
            url,
            data,
            config
        )

    },

    put<T>(
        url: string,
        data?: unknown,
        config?: AxiosRequestConfig
    ): Promise<T> {

        return axiosInstance.put<any, T>(
            url,
            data,
            config
        )

    },

    delete<T>(
        url: string,
        config?: AxiosRequestConfig
    ): Promise<T> {

        return axiosInstance.delete<any, T>(
            url,
            config
        )

    }

}

export default http