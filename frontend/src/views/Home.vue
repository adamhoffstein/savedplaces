/* eslint-disable */
<template>
  <v-container fluid>
    <v-row>
      <v-text-field
        solo
        placeholder="Enter an address"
        prepend-icon="mdi-map-marker"
        v-model="coordinates"
        @click:prepend="locatorButtonPressed"
      >
      </v-text-field>
    </v-row>
    <v-row>
      <v-col>
        <v-select v-model="type" label="type" :items="types"> </v-select>
      </v-col>
      <v-col>
        <v-select v-model="radius" label="distance" :items="radii"> </v-select>
      </v-col>
      <v-col>
        <v-btn @click="findButtonPressed">Find Nearby</v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
      <v-list two-line>
        <v-list-item  v-for="place in places"
        :key="place.id"
        >
          <v-list-item-content>
            <v-list-item-title>{{ place.name }}</v-list-item-title>
            <v-list-item-subtitle>{{ place.vicinity }}</v-list-item-subtitle
            >
          </v-list-item-content>
          <v-rating
          v-model="place.rating"
          background-color="white"
          color="yellow accent-4"
          dense
          half-increments
          hover
          size="18"  
          readonly        
          ></v-rating>
          <p class="text-caption pt-4 pl-2" v-if="place.user_ratings_total">({{ place.user_ratings_total }})</p>
        </v-list-item>
        
      </v-list>
      </v-col>
      <v-col>
      <div v-if="markers.length > 0">
        <Gmap-Map style="width: 600px; height: 300px;" :zoom="12" :center="{lat: lat, lng: lon}">
          <Gmap-Marker v-for="(marker, index) in markers"
          :key="index"
          :position="marker.position"
          ></Gmap-Marker>
        </Gmap-Map>
      </div>
      </v-col>
    </v-row>
  </v-container>
</template>
<script>
import axios from "axios";
export default {
  name: 'Home',
  components: {
  },
  data: () => {
    return {
      type: "",
        types: ['restaurant'],
        radii: ['5', '10', '15', '20'],
        radius: "",
        lat: 0,
        lon: 0,
        rating: 4.3,
        key: "AIzaSyDHA6k6vxs0CpJCXNHo0C9I_1Svd_aifMY",
        places: [{name: 'Your results will appear here', vicinity: 'type something to get started'}],
        markers: []
    }
  },
  computed: {
    coordinates() {
      return `${this.lat}, ${this.lon}`;
    }
  },
  methods: {
    locatorButtonPressed () {
      navigator.geolocation.getCurrentPosition(
        position => {
          this.lat = position.coords.latitude;
          this.lon = position.coords.longitude;
        },
        error => {
          console.log('Something is broken.', error);
        }
      )
    },
    initMap(){

    },
    findButtonPressed () {
      this.markers = []
      // Change this to backend API request
      const URL = `https://cors-anywhere.herokuapp.com/https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=${this.lat},${this.lon}&type=${this.type}&radius=${this.radius*1000}&key=${this.key}`;
      axios.get(URL).then(
        response => {
          this.places = response.data.results
          this.addMapLocations()
          console.log(this.places)
        }
      ).catch(
        error => {
          console.log(error.message)
        }
      )
    },
    addMapLocations () {
      this.places.forEach((place) => {
        this.markers.push({
            position: {
              lat: place.geometry.location.lat,
              lng: place.geometry.location.lng,
            }
          })
        });
      console.log('markers: ', this.markers)
    }
  },
  mounted(){
    this.initMap();
  }
}
</script>
