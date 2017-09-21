/**
 * Created by kalen on 2017/5/4.
 */


import Api from "./utils/api"
import { drawChart } from "./chart"
import { getDate } from './utils/time'


new Vue({
   el: '#app',
   data: {
     districts: [],
     selected_district: "",
     selected_location: "",
     locations: []
   },
   computed: {
     selectedDistrict: {
       get() {
        return this.selected_district;
       },
       set(district) {
         this.selected_district = district;
         for (var i = 0; i < this.districts.length; i++) {
           if(this.selected_district == this.districts[i].name) {
             this.locations = JSON.parse(this.districts[i].locations);
             this.selectedLocation = this.locations[0];
           }
         }
       }
     },
     selectedLocation: {
       get(){
         return this.selected_location;
       },
       set(loc) {
         this.selected_location = loc;
         this.getSum();
       }
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
       Api.get("/api/sum", {location: this.selected_location}, (data) => {
         if (data != null) {
           let dates = [], maxs = [], mins = [], avgs = [], house_nums=[];
           data.forEach((item)=>{
             dates.push(getDate(item.time))
             maxs.push(item.max);
             mins.push(item.min);
             avgs.push(item.avg);
             house_nums.push(item.house_num)
           })
           drawChart(dates, maxs, mins, avgs, house_nums)
         } else {
           alert("Error Occurred");
         }
       })
     }
   }
})
