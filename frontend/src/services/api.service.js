import Vue from "vue";

const ApiService = {
    init() {
      Vue.axios.defaults.baseURL = 'http://localhost:8000/';
    },
    get(resource, param="") {
        return Vue.axios.get(`${resource}/${param}`).catch(error => {
          throw new Error(`ApiService ${error}`);
        });
      },
    query(resource, params) {
        return Vue.axios.get(`${resource}/${params}`).catch(error => {
          throw new Error(`ApiService ${error}`);
        });
      },
}

export default ApiService;


export const GooglePlacesService = {
    get() {
      console.log('GETTING')
      return ApiService.get("/")
    },
    query(queryInfo) {
        console.log('GETTING')
        const params = `?lat=${queryInfo.lat}&lon=${queryInfo.lon}&radius=${queryInfo.radius*1000}&type=${queryInfo.type}&rating=${queryInfo.rating}`
        return ApiService.query("/nearby", params)
      },
    
}