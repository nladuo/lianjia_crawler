/**
 * Created by kalen on 2017/5/4.
 */


import Api from "./utils/api"
// import { drawChart } from "./chart"


new Vue({
   el: '#app',
   data: {
     districts: [],
     selectedDistrict: "",
     selectedLocation: null
   },
   computed: {
     locations() {
       for (var i = 0; i < this.districts.length; i++) {
         if(this.selectedDistrict == this.districts[i].name) {
           console.log(this.districts[i].locations);
           let _locations = JSON.parse(this.districts[i].locations);
           this.selectedLocation = _locations[0].location;
           return _locations;
         }
       }
       return [];
     }
   },
   ready() {
     this.getDistricts();
   },
   methods: {
     getDistricts() {
       Api.get("/api/districts", {}, (data) => {
         if (data != null) {
           this.districts = data;
           this.selectedDistrict = this.districts[0].name;
         }
       })
     },

     getSum() {
       Api.get("/api/sum", {location: this.selectedLocation}, (data) => {
         console.log(data);
         if (data != null) {

         }
       })
     }
   }
})
