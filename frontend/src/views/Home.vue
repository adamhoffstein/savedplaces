<template>
  <v-container fluid>
    <v-form>
      <v-row>
        <v-col cols="12" md="6">
          <v-text-field
            solo
            clearable
            label="Where do you want to look?"
            append-icon="mdi-map-marker"
            v-model="queryInfo.location"
            :loading="!queryInfo.lat"
            @click:append="getCurrentLocation"
          >
          </v-text-field>
        </v-col>
        <v-col cols="12" md="3">
          <v-text-field
            solo
            v-model="queryInfo.keyword"
            clearable
            label="What are you craving?"
          >
          </v-text-field>
        </v-col>
        <v-col cols="12" md="3">
          <v-select
            solo
            v-model="queryInfo.radius"
            label="How far away?"
            :items="radii"
          >
          </v-select>
        </v-col>
      </v-row>
    </v-form>
    <v-divider></v-divider>
    <v-row class="mt-6">
      <v-col>
        <v-row class="mx-0 mb-3">
          <v-btn @click="findButtonPressed" :disabled="!queryInfo.lat"
          class="mr-4"
            >Find Nearby</v-btn
          >
          <v-btn>
            Save Items
          </v-btn>
        </v-row>
        <v-list two-line width="100%" class="overflow-y-auto" max-height="600"
        v-if="places.length>0"
        >
          <v-list-item-group
            v-model="selected"
            active-class="primary--text"
            multiple
          >
            <template v-for="(place, index) in places">
              <v-list-item v-bind:key="place.id">
                <template>
                  <v-list-item-content>
                    <v-list-item-title v-text="place.name"></v-list-item-title>
                    <v-list-item-subtitle
                      v-text="place.vicinity.slice(0, 65)"
                    ></v-list-item-subtitle>
                  </v-list-item-content>
                  <p
                    class="text-caption pt-4 pl-2"
                    v-if="place.user_ratings_total"
                  >
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
                </template>
              </v-list-item>
              <v-divider
                v-if="index < places.length - 1"
                :key="index"
              ></v-divider>
            </template>
          </v-list-item-group>
        </v-list>
        <div>debug area: {{ coordinates }}</div>
        <div>{{ selectedPlace }}</div>
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
        places: [],
        markers: [],
        priceranges: ['$','$$','$$$'],
        queryInfo: {
          lat: null,
          lon: null,
          radius: null,
          keyword: null,
          rating: 4.5
      },
      selected: []
    }
  },
  computed: {
    coordinates() {
      return `${this.queryInfo.lat}, ${this.queryInfo.lon}`;
    },
    selectedPlace() {
      if (this.selected.length>0) {
        var items = []
        for (let i = 0; i < this.selected.length; i++) {
          items.push(this.places[i].place_id)
        }
        return items
      }
      else {
        return undefined
      }
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
