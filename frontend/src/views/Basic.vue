<template>
  <v-container fluid>
   <div id="map">
    <h1>Autocomplete Example</h1>
    <label>
      AutoComplete
      <gmap-autocomplete
        placeholder="This is a placeholder text"
        @place_changed="setPlace"
        :options="{fields: ['geometry', 'address_components', 'url', 'place_id']}"
        >
      </gmap-autocomplete>
      <button @click="usePlace">Add</button>
    </label>
    <br/>

    <Gmap-Map style="width: 600px; height: 300px;" :zoom="7" :center="{lat: 13.75, lng: 100.4667}">
      <Gmap-Marker v-for="(marker, index) in markers"
        :key="index"
        :position="marker.position"
        ></Gmap-Marker>
      <Gmap-Marker
        v-if="this.place"
        label="&#x2605;"
        :position="{
          lat: this.place.geometry.location.lat(),
          lng: this.place.geometry.location.lng(),
        }"
        ></Gmap-Marker>
    </Gmap-Map>
   </div>
  </v-container>
</template>
<script>
export default {
  name: 'Home',
  components: {
  },
  data: () => {
    return {
        markers: [],
        place: null,
    }
  },
  methods: {
      setDescription(description) {
        this.description = description;
      },
      setPlace(place) {
        this.place = place
      },

      usePlace() {
        if (this.place) {
          console.log(this.place)
          this.markers.push({
            position: {
              lat: this.place.geometry.location.lat(),
              lng: this.place.geometry.location.lng(),
            }
          })
          this.place = null;
        }
      }
  },
  mounted(){
  }
}
</script>
