import Vue from 'vue';
import Vuex from 'vuex';


import auth from './modules/auth.js'
import general from './modules/general.js'
import admin from './modules/admin.js'

import * as actions from './actions';

Vue.use(Vuex);

export const store = new Vuex.Store({
  actions,
  modules: {
    auth,
    general,
    admin
  }
})

// store.watch(store.authenticated, () => {
//   alert("yaba daba in store.js");
// })

// store.watch((state) => state.token, (oldValue, newValue) => {
//   console.log('search string is changing')
//   console.log(oldValue)
//   console.log(newValue)
//   alert("dddddddddddddddddddddd")
// })

// see: https://forum.vuejs.org/t/correct-way-to-use-store-watch-in-vuex/1800/5
// store.watch(
//   // When the returned result changes...
//   function (state) {
//     return state.auth.token
//   },
//   // Run this callback
//   function(){
//     alert("dddddddddddddddddddd");
//     // Vue.router.replace({ name: "login" });
//   }
// )