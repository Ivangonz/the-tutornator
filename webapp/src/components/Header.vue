<template>
<div>
  <nav class="navbar navbar-default">
    <div class="container-fluid">
      <transition name="fade">
        <div
          id="flash"
          v-if="this.$store.state.general.displayAlert"
          v-bind:class="classObject"
          role="alert"
        >
          {{ this.$store.state.general.alertMsg }}
        </div>
      </transition>
      <div class="navbar-header">
        <router-link to="/" class="navbar-brand"><div class="navbar_text">Home</div></router-link>
      </div>
      <div>
        <ul class="nav navbar-nav navbar-right">
          <li v-show="this.$store.getters.authenticated">
            <a href="#" @click="profile">{{ this.$store.state.auth.email }}</a>
          </li>
          <li>
            <a href ="#" @click="calendar"><div class="navbar_text">Calendar</div></a>
          </li>
          <li>
            <a href ="#" @click="tutors"><div class="navbar_text">Tutors</div></a>
          </li>
           <li>
            <a href ="#" @click="login"><div class="navbar_text">Login</div></a>
          </li>
           <li>
            <a href ="#" @click="admintools"><div class="navbar_text">Admin Tools</div></a>
          </li>
           <li>
            <a href ="#" @click="manageaccount"><div class="navbar_text">Manage Account</div></a>
          </li>
          <li v-show="this.$store.getters.authenticated">
            <a href="#" @click="logOut">Logout</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
  <nav aria-label="breadcrumb">
    <breadcrumbs />
  </nav>
  </div>
</template>

<script>
import Breadcrumbs from './public/Breadcrumbs.vue'

export default {
  components: {
    Breadcrumbs
  },
  data() {
    return {
      isDropdownOpen: false,
      toggle: false,
    };
  },
  computed: {
    classObject: function() {
      return {
        alert: true,
        "alert-success": this.$store.state.general.alertType == "success",
        "alert-danger":
          this.$store.state.general.alertType == "danger" ||
          (this.$store.state.general.alertType != "success" &&
            this.$store.state.general.alertType != "danger" &&
            this.$store.state.general.alertType != "info"),
        "alert-info": this.$store.state.general.alertType == "info",
      };
    },
        crumbs: function() {
      let pathArray = this.$route.path.split("/")
      pathArray.shift()
      let breadcrumbs = pathArray.reduce((breadcrumbArray, path, idx) => {
        breadcrumbArray.push({
          path: path,
          to: breadcrumbArray[idx - 1]
            ? "/" + breadcrumbArray[idx - 1].path + "/" + path
            : "/" + path,
          text: this.$route.matched[idx].meta.breadCrumb || path,
        });
        return breadcrumbArray;
      }, [])
      return breadcrumbs;
    }
  },
  // this is needed for the fade effect
  watch: {
    "$store.state.general.displayAlert"(val) {
      if (val === true) {
        setTimeout(
          () => (this.$store.state.general.displayAlert = false),
          5000
        );
      }
    },
  },
  methods: {
    logOut: function() {
      this.$store.dispatch("setToken", "");
    },
    profile: function() {
      this.$router.replace({ name: "profile" });
    },
    calendar: function()
    {
      this.$router.replace({ name: "calendar" });
    },
    admintools: function()
    {
     this.$router.replace({ name: "admintools" });
    },
    tutors: function()
    {
     this.$router.replace({ name: "tutors" });
    },
    manageaccount: function()
    {
       this.$router.replace({ name: "manageaccount" });
    },
    login: function()
    {
      this.$router.replace({ name: "login" });
    }
  },
};
</script>

<style scoped>
#flash {
  text-align: center;
  width: 40%;
  margin-left: auto;
  margin-right: auto;
  position: absolute;
  left: 0;
  right: 0;
  top: 40px;
  z-index: 10;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 1.3s ease;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
.navbar{
background-color: purple;
}

.breadcrumb
{
visibility: invisible;
}
a
{
color: red;
}

.navbar_text
{
color:white;
}

</style>
