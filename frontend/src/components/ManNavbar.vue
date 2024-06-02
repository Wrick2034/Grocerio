<template>
  <nav class="navbar navbar-expand-lg" style="background-color:#33CC66">
    <div class="container-fluid display-6" >
        <b style="float:left;font-family:'Gabarito'">Welcome {{ name }},</b>
        <b style="float:right"><router-link to="/ManagementHome" @click="ActionDecider('home')"><i class="bi bi-house-fill"></i></router-link>        |       <router-link to="/ManagementHome" @click="ActionDecider('request')"><i class="bi bi-chat-square-text"></i></router-link>        |       <router-link to="/" @:click="Logout"><i class="bi bi-box-arrow-right"></i></router-link></b>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'ManNavbar',
  data () {
    return {
      isVisible: false,
      cartVisible: true,
      search: ''
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
      if (value === 'home') {
        this.$emit('view-home', true)
      } else if (value === 'request') {
        this.$emit('view-home', false)
      }
    }
  }
}
</script>
