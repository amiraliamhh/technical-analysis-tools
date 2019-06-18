<template>
  <v-container grid-list-md>
    <v-flex xs12>
      <v-tabs
      v-model="active"
      color="#2196f3"
      dark
      slider-color="yellow"
      @change="results = null"
    >
      <v-tab
        ripple
      >
        Calculate RSI
      </v-tab>
      <v-tab
        ripple
      >
        Calculate Connors
      </v-tab>
      <v-tab
        ripple
      >
        Simulate Trade
      </v-tab>

      <v-tab-item class="tab-item" >
        <v-flex xs4>
          <v-text-field
            v-model="rsiPeriod"
            label="Period"
          />
        </v-flex>
        <v-flex xs12>
          <v-textarea
            outline
            name="input-7-4"
            label="Insert Close Prices"
            placeholder="[7435.21, 7436.01, 7433.94, ...]"
            v-model="rsiClosePrices"
          />
        </v-flex>
        <v-btn color="info" @click="calculateRSI" >Calculate</v-btn>
      </v-tab-item>
      <v-tab-item class="tab-item" >
        <v-flex xs4>
          <v-text-field
            v-model="rsiPeriod"
            label="Period"
          />
        </v-flex>
        <v-flex xs4>
          <v-text-field
            v-model="lookbackPeriod"
            label="Lookback"
          />
        </v-flex>
        <v-flex xs12>
          <v-textarea
          outline
          name="input-7-4"
          label="Insert Close Prices"
          placeholder="[7435.21, 7436.01, 7433.94, ...]"
          :model="closePrices"
          />
        </v-flex>
        <v-btn color="info" @click="calculateConnors" >Calculate</v-btn>
      </v-tab-item>
      <v-tab-item class="tab-item" >
        <v-flex xs4>
          <v-text-field
            v-model="lastNHours"
            label="Data from last n hours"
          />
        </v-flex>
        <v-flex xs4>
          <v-text-field
            v-model="coin"
            label="Coin"
          />
        </v-flex>
        <v-flex xs4>
          <v-text-field
            v-model="rsiPeriod"
            label="RSI Period"
          />
        </v-flex>
        <v-flex xs4>
          <v-text-field
            v-model="lookbackPeriod"
            label="Lookback"
          />
        </v-flex>
        <v-flex xs4>
          <v-text-field
            v-model="budget"
            label="Starting budget ($)"
          />
        </v-flex>
        <v-btn color="info" >Simulate</v-btn>
      </v-tab-item>
    </v-tabs>
      
    </v-flex>

    <v-alert :value="!!errorMsg" type="error" >
      {{ errorMsg }}
    </v-alert>

    <v-flex xs12 class="results" v-if="results">
      <v-textarea
          outline
          name="results"
          :value="results"
      />
    </v-flex>
  </v-container>
</template>

<script>
const BaseURL = 'http://127.0.0.1:8000';

export default {
  data() {
    return {
      active: null,
      budget: 1000,
      closePrices: [],
      closePricesJSON: null,
      coin: 'BTC',
      errorMsg: null,
      results: null,
      rsiClosePrices: [],
      rsiPeriod: 14,
      lastNHours: 2000,
      lookbackPeriod: 100,
      simulate: false,
    };
  },
  methods: {
    async calculateRSI() {
      if (!this.validateClosePrices()) {
        this.errorMsg = 'Invalid JSON (close prices)';
        return;
      }
      try {
        const query = {
          close_prices: JSON.parse(this.rsiClosePrices),
          period: this.rsiPeriod,
        };
        const { data } = await this.$http.post(`${BaseURL}/calculate-rsi`, query);
        this.errorMsg = null;
        if (data) {
          this.results = (data.data || []).join('\n');
        }
      } catch (e) {
        const error = e.toJSON();
        this.errorMsg = error.message.toString();
      }
    },
    async calculateConnors() {
      if (!this.validateClosePrices()) {
        this.errorMsg = 'Invalid JSON (close prices)';
        return;
      }
      try {
        const query = {
          close_prices: JSON.parse(this.rsiClosePrices),
          lookback_period: this.lookbackPeriod,
          period: this.rsiPeriod,
        };
        const { data } = await this.$http.post(`${BaseURL}/calculate-connors`, query);
        this.errorMsg = null;
        if (data) {
          this.results = (data.data || []).join('\n');
        }
      } catch (e) {
        const error = e.toJSON();
        this.errorMsg = error.message.toString();
      }
    },
    next() {
      console.log('hereee');
      this.results = null;
      const active = parseInt(this.active, 0);
      this.active = (active < 2 ? active + 1 : 0);
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

<style lang="css" scoped>
.tab-item, .results {
  margin-top: 2em;
}
</style>

