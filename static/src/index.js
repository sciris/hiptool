import Vue from 'vue';
import './styles/index.scss';
import router from './router.js'
import store from './store.js'
import sciris from 'sciris-js';
import App from './app/App.vue';
import ScirisUIKit from 'sciris-uikit';

Vue.prototype.$toolName = 'hptool'

Vue.use(sciris.ScirisVue, {
  progressbar: {
    options: {
      color: 'rgb(0, 0, 255)',
      failedColor: 'red',
      thickness: '3px',
      transition: {
        speed: '0.2s',
        opacity: '0.6s',
        termination: 300
      }       
    }
  }
});

Vue.use(ScirisUIKit, {
	router: router
});

new Vue({
  el: '#app',
  router: router,
  store: store,
  render: h => h(App),
})
