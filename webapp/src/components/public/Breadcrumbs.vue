<template>
<!-- 
    This code derivative of:
https://medium.com/@fagnersaraujo/automated-breadcrumbs-with-vuejs-7e1051de8028
https://github.com/iFgR/vue-breadcrumbs
 -->
  <div class="breadcrumb">
    <ul>
      <li
        v-for="(breadcrumb, idx) in breadcrumbList"
        :key="idx"
        @click="routeTo(idx)"
        :class="{'linked': !!breadcrumb.link}">

        {{ breadcrumb.name }}

      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'Breadcrumb',
  data () {
    return {
      breadcrumbList: []
    }
  },
  mounted () { this.updateList() },
  watch: { '$route' () { this.updateList() } },
  methods: {
    routeTo (pRouteTo) {
      if (this.breadcrumbList[pRouteTo].link) this.$router.push(this.breadcrumbList[pRouteTo].link).catch(()=>{});
    },
    updateList () { 
        this.breadcrumbList = this.$route.meta.breadcrumb 
        }
  }
}
</script>

<style scoped>
  .breadcrumb {}
  ul {
    display: flex;
    justify-content: left;
    list-style-type: none;
    margin: 0;
    padding: 0;
  }
  ul > li {
    display: flex;
    float: left;
    height: 10px;
    width: auto;
    color: $default;
    /* font-weight: bold; */
    font-size: .8em;
    cursor: default;
    align-items: center;
  }
  ul > li:not(:last-child)::after {
    content: '/';
    float: right;
    font-size: .8em;
    margin: 0 .5em;
    color: $light-default;
    cursor: default;
  }
  .linked {
    cursor: pointer;
    font-size: 1em;
    font-weight: normal;
  }
</style>