<template>
  <v-container grid-list-md>
    <v-flex xs12>
      <v-textarea
          outline
          name="input-7-4"
          label="Insert Close Prices"
          placeholder="[7435.21, 7436.01, 7433.94, ...]"
          :model="closePrices"
      />
    </v-flex>

    <v-flex xs12>
      <v-btn color="info" @click="calculateRSI" >Calculate RSI</v-btn>
      <v-btn color="info" >Calculate Connors</v-btn>
      <v-btn color="info" >Simulate</v-btn>
    </v-flex>

    <v-flex xs12 v-if="simulate">
      asdasd
    </v-flex>

    <v-alert :value="!!errorMsg" type="error" >
      {{ errorMsg }}
    </v-alert>

    <v-flex xs12  v-if="results">
      <v-textarea
          outline
          name="results"
          value="results"
      />
    </v-flex>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      closePrices: [],
      closePricesJSON: null,
      errorMsg: null,
      results: null,
      simulate: false,
    };
  },
  methods: {
    async calculateRSI() {
      if (!this.validateClosePrices()) {
        return;
      }
      try {
        const { data } = await this.$http.get('https://google.com');
        this.errorMsg = null;
        if (data) {
          this.results = data.data;
        }
      } catch (e) {
        const error = e.toJSON();
        this.errorMsg = error.message.toString();
      }
    },
    validateClosePrices() {
      try {
        this.closePricesJSON = JSON.stringify(this.closePrices);
        return true;
      } catch (e) {
        const error = e.toJSON();
        this.errorMsg = error.message.toString();
        return false;
      }
    },
  },
};
</script>
