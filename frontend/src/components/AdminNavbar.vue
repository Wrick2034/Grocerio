<template>
  <nav class="navbar navbar-expand-lg" style="background-color:#33CC66">
    <div class="container-fluid display-6" >
        <b style="float:left;font-family:'Gabarito'">Welcome {{ name }},</b>
        <b style="float:right"><router-link to="/AdminHome" @click="ActionDecider('people')"><i class="bi bi-people"></i></router-link>        |       <router-link to="/AdminHome" @click="ActionDecider('request')"><i class="bi bi-file-text-fill"></i></router-link>        |       <router-link to="/" @:click="Logout"><i class="bi bi-box-arrow-right"></i></router-link></b>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'AdminNavbar',
  data () {
    return {
    }
  },
  components: {},
  props: ['name'],
  methods: {
    Logout () {
      sessionStorage.removeItem('access_token')
      console.log('Logout Successful')
      this.$router.push('/')
    },
    ActionDecider (value) {
      if (value === 'people') {
        this.$emit('view-request', false)
      } else if (value === 'request') {
        this.$emit('view-request', true)
      }
    }
  }
}
</script>
