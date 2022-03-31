<template>
  <v-container fluid>
    <v-form>
      <v-row>
        <v-col cols="12" md="6">
          <v-text-field
            solo
            label="Where do you want to look?"
            append-icon="mdi-map-marker"
            v-model="queryInfo.location"
            :loading="!queryInfo.lat"
            @click:append="getCurrentLocation"
          >
          </v-text-field>
        </v-col>
        <v-col cols="12" md="3">
          <v-text-field solo v-model="queryInfo.keyword" label="What are you craving?"> </v-text-field>
        </v-col>
        <v-col cols="12" md="3">
          <v-select solo v-model="queryInfo.radius" label="How far away?" :items="radii">
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
                v-model="queryInfo.rating"
                background-color="white"
                color="yellow accent-4"
                dense
                half-increments
                hover
                size="24"
              ></v-rating>
            </v-card-title>
            <v-card-actions>
              <v-btn @click="findButtonPressed"
              :disabled="!queryInfo.lat"
              >Find Nearby</v-btn>
            </v-card-actions>
          </v-card>
        </v-row>
        <v-list two-line width="100%" class="overflow-y-auto" max-height="600">
          <v-list-item v-for="place in places" :key="place.id">
            <v-list-item-content>
              <v-list-item-title>{{ place.name }}</v-list-item-title>
              <v-list-item-subtitle>{{ place.vicinity.slice(0, 65) }}</v-list-item-subtitle>
            </v-list-item-content>
            <p class="text-caption pt-4 pl-2" v-if="place.user_ratings_total">
              ({{ place.user_ratings_total }})
            </p>
            <v-rating
              v-model="place.rating"
              background-color="white"
              color="yellow accent-4"
              half-increments
              hover
              size="18"
              readonly
            ></v-rating>
          </v-list-item>
        </v-list>
        <div>debug area: {{ coordinates }}</div>
      </v-col>
      <v-divider vertical></v-divider>
      <v-col>
        <div v-if="markers.length > 0">
          <Gmap-Map
            style="width: 600; height: 800px"
            :zoom="12"
            :center="{lat: queryInfo.lat, lng: queryInfo.lon}"
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
import {
  GooglePlacesService
} from "@/services/api.service";
export default {
  name: 'Home',
  components: {
  },
  data: () => {
    return {
        location: 'Current Location',
        radii: ['5', '10', '15', '20'],
        places: [{name: 'Your results will appear here', vicinity: 'type something to get started'}],
        markers: [],
        queryInfo: {
          lat: null,
          lon: null,
          radius: null,
          keyword: null,
          rating: 4.5
      }
    }
  },
  computed: {
    coordinates() {
      return `${this.queryInfo.lat}, ${this.queryInfo.lon}`;
    }
  },
  methods: {
    getCurrentLocation () {
      navigator.geolocation.getCurrentPosition(
        position => {
          this.queryInfo.lat = position.coords.latitude;
          this.queryInfo.lon = position.coords.longitude;
          console.log(this.queryInfo.lat, this.queryInfo.lon)
        },
        error => {
          console.log('Something is broken.', error);
        }
      )
    },
    findButtonPressed () {
      GooglePlacesService.query(this.queryInfo).then(
          response => {
              console.log(response)
              this.places = response.data
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
      this.markers = []
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
    this.getCurrentLocation()
  }
}
</script>
<style>
div.vue-map-container {
  margin-top: 0px;
}
</style>