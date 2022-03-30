<template>
  <v-container fluid>
    <v-form>
      <v-row>
        <v-col cols="12" md="6">
          <v-text-field
            solo
            placeholder="Enter an address"
            append-icon="mdi-map-marker"
            v-model="coordinates"
            @click:append="locatorButtonPressed"
          >
          </v-text-field>
        </v-col>
        <v-col cols="12" md="3">
          <v-select solo v-model="type" label="type" :items="types"> </v-select>
        </v-col>
        <v-col cols="12" md="3">
          <v-select solo v-model="radius" label="distance" :items="radii">
          </v-select>
        </v-col>
      </v-row>
    </v-form>
    <v-divider></v-divider>
    <v-row class="mt-6">
      <v-col>
        <v-row>
          <v-card class="mx-3 mb-6 mt-3 elevation-0 rounded-0" width="100%">
            <v-card-title>
              Rating Filter:
              <v-rating
                v-model="rating"
                background-color="white"
                color="yellow accent-4"
                dense
                half-increments
                hover
                size="24"
              ></v-rating>
            </v-card-title>
            <v-card-actions>
              <v-btn @click="findButtonPressed">Find Nearby</v-btn>
            </v-card-actions>
          </v-card>
        </v-row>
        <v-list two-line width="100%" class="overflow-y-auto" max-height="600">
          <v-list-item v-for="place in places" :key="place.id">
            <v-list-item-content>
              <v-list-item-title>{{ place.name }}</v-list-item-title>
              <v-list-item-subtitle>{{ place.vicinity }}</v-list-item-subtitle>
            </v-list-item-content>
            <v-rating
              v-model="place.rating"
              background-color="white"
              color="yellow accent-4"
              half-increments
              hover
              size="18"
              readonly
            ></v-rating>
            <p class="text-caption pt-4 pl-2" v-if="place.user_ratings_total">
              ({{ place.user_ratings_total }})
            </p>
          </v-list-item>
        </v-list>
      </v-col>
      <v-divider vertical></v-divider>
      <v-col>
        <div v-if="markers.length > 0">
          <Gmap-Map
            style="width: 600; height: 800px"
            :zoom="12"
            :center="{lat: lat, lng: lon}"
          >
            <Gmap-Marker
              v-for="(marker, index) in markers"
              :key="index"
              :position="marker.position"
            ></Gmap-Marker>
          </Gmap-Map>
        </div>
        <div v-else>
          <Gmap-Map
            style="width: 600; height: 800px"
            :zoom="12"
            :center="{lat: 0, lng: 0}"
          >
          </Gmap-Map>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>
<script>
import axios from "axios";
import {
  GooglePlacesService
} from "@/services/api.service";
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
    findButtonPressed () {
      const queryInfo = {
        lat: this.lat,
        lon: this.lon,
        radius: this.radius,
        type: this.type,
        rating: this.rating
      }
      GooglePlacesService.query(queryInfo).then(
          response => {
              console.log(response)
              this.places = response.data.results
              this.addMapLocations()
              console.log(this.places)
          },
          error => {
            this.me =
              (error.response && error.response.dataset) ||
              error.message ||
              error.toString();
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

  }
}
</script>
<style>
div.vue-map-container {
  margin-top: 0px;
}
</style>