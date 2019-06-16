import Vue from 'vue';
import Vuetify from 'vuetify';
import axios from 'axios';
import 'vuetify/dist/vuetify.min.css';

import App from './App';
import router from './router';

Vue.config.productionTip = false;
Vue.prototype.$http = axios;

Vue.use(Vuetify);

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App },
});
