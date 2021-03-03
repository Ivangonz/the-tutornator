<template>
  <div id="login">
    <div class="row">
      <div class="col-sm-3 col-md-3 col-lg-3 col-centered"></div>
      <div class="col-sm-7 col-md-6 col-lg-5 col-centered">
        <h2>Login</h2>
        <div class="form-group  ">
          <label for="login" class="control-label">Login name</label>

          <input
            class="form-control"
            id="login"
            type="text"
            v-model="input.username"
            placeholder="Username"
          />
        </div>
        <div class="form-group  ">
          <label for="password" id="password" class="control-label"
            >Password</label
          >

          <input
            class="form-control"
            type="password"
            v-model="input.password"
            placeholder="Password"
          />
        </div>

        <button

          class="btn btn-default btn-primary"
          type="button"
          v-on:click="login()"
        >
          Login
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Login",
  data() {
    return {
      input: {
        username: "lfernandez",
        password: "white",
      },
    };
  },
  methods: {
    login() {
      if (this.input.username != "" && this.input.password != "") {
        this.$store.dispatch("login", this.input);
      } else {
        this.$store.commit('SET_ALERT', { status: 'error', alertMsg: 'A username and password must be present' })
      }
    },
  },
};
</script>

<style scoped>

</style>
