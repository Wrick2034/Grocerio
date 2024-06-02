<template>
  <nav class="navbar navbar-expand-lg" style="background-color:#33CC66">
    <div class="container-fluid display-6" >
        <b style="float:left;font-family:'Gabarito'">Welcome {{ name }},</b>
        <b style="float:right"><router-link to="/Home"><i class="bi bi-house-fill"></i></router-link>        |       <router-link to="/Home" @:click="toggleSearch"><i class="bi bi-search"></i></router-link>        |       <router-link to="/Home" @:click="cartToggle"><i class="bi bi-cart4"></i></router-link>        |       <router-link to="/" @:click="Logout"><i class="bi bi-box-arrow-right"></i></router-link></b>
    </div>
  </nav>
  <div v-if="isVisible" class="container-fluid" style="width:80%">
    <br>
    <form class="d-flex" role="search">
      <input v-model="search" class="form-control me-2" type="search" placeholder="Search Products" aria-describedby="basic-addon2" required>
      <router-link :to="`/Search/${search}`"><button class="btn btn-outline-success"><i class="bi bi-search"></i></button></router-link>
    </form>
  </div>
</template>

<script>
export default {
  name: 'NavBar',
  data () {
    return {
      isVisible: false,
      cartVisible: true,
      search: ''
    }
  },
  components: {},
  props: ['visibility', 'name'],
  watch: {
    visibility: {
      immediate: true,
      handler (newValue) {
        this.cartVisible = newValue
      }
    }
  },
  methods: {
    toggleSearch () {
      this.isVisible = !this.isVisible
    },
    cartToggle () {
      this.cartVisible = !this.cartVisible
      this.$emit('set-visibility', this.cartVisible)
    },
    get () {
      this.cartVisible = this.visibility
    },
    Logout () {
      sessionStorage.removeItem('access_token')
      console.log('Logout Successful')
      this.$router.push('/')
    }
  }
}
</script>
