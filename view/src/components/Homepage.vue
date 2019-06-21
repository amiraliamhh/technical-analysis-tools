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
            v-model="aggregate"
            label="Hour aggregation"
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
            v-model="connorsRsiPeriod"
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
            v-model="overbought"
            label="Overbough percentage"
          />
        </v-flex>
        <v-flex xs4>
          <v-text-field
            v-model="oversell"
            label="Oversold percentage"
          />
        </v-flex>
        <!-- <v-flex xs4>
          <v-text-field
            v-model="budget"
            label="Starting budget ($)"
          />
        </v-flex> -->
        <v-btn color="info" @click="simulateConnors" >Simulate</v-btn>

        <v-flex xs4>
          <h3 class="simulation-results" v-if="simulationResult" >
            value: ${{ Math.round(simulationResult * 100) / 100 }} (starting with $1000)
          </h3>
        </v-flex>
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
import qs from 'query-string';

const BaseURL = 'http://127.0.0.1:4000';

export default {
  data() {
    return {
      active: null,
      aggregate: 4,
      budget: 1000,
      closePrices: [],
      closePricesJSON: null,
      coin: 'BTC',
      connorsRsiPeriod: 3,
      errorMsg: null,
      lastNHours: 2000,
      lookbackPeriod: 100,
      overbought: 70,
      oversell: 30,
      results: null,
      rsiClosePrices: [],
      rsiPeriod: 14,
      simulationResult: null,
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
      this.results = null;
      const active = parseInt(this.active, 0);
      this.active = (active < 2 ? active + 1 : 0);
    },
    async simulateConnors() {
      const query = qs.stringify({
        coin: this.coin,
        limit: this.lastNHours,
        aggregate: this.aggregate,
        lookback_period: this.lookbackPeriod,
        period: this.connorsRsiPeriod,
        overbought: this.overbought,
        oversell: this.oversell,
      });
      try {
        const { data: { results } } = await this.$http.get(`${BaseURL}/gateway/v1.0/simulate/connors?${query}`);
        this.simulationResult = results;
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

<style lang="css" scoped>
.tab-item, .results, .simulation-results {
  margin-top: 2em;
}
</style>

