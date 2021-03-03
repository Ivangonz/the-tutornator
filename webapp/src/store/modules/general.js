const state = {
  alertType: "",
  alertMsg: "",
  displayAlert: false,
  newRouteRequest: ""
}

const mutations = {
    SET_ALERT: function (state, payload) {
      state.alertType = payload.status;
      state.alertMsg = payload.alertMsg;
      state.displayAlert = true;
      payload.newRouteRequest ? state.newRouteRequest = payload.newRouteRequest : state.newRouteRequest = ""
    },
    CLEAR_NEW_ROUTE_REQ: function (state) {
      state.newRouteRequest = ""
    }

  }

  export default {
    mutations, state
  }
  