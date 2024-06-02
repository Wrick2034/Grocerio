<template>
  <div id="land" class="container-fluid">
    <nav class="navbar navbar-expand-lg">
      <div class="container-fluid display-6" style="font-size:30px;font-family:Quicksand;color:white">
        <b style="float:left"></b>
        <b style="float:right;"><router-link to='/User'><button class="btn btn-outline-light" style="font-family:Verdana, Geneva, Tahoma, sans-serif;">Login <i class="bi bi-box-arrow-in-right"></i></button></router-link></b>
      </div>
    </nav>
    <br><br><br><br>
    <div class="container-fluid">
      <div class="display-1 text-center"
        style="font-family:'Playfair Display';font-size:160px;color:white;margin:5px 150px;text-shadow:2px 2px 30px">
        GROCERIO
        <br>
        <h2><small class="text-body-white text-center">Your one stop solution for every grocery need...</small></h2>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LandingPage',
  data () {
    return {

    }
  },
  components: {}
}
</script>

<style>
#land {
  background-image: url("@/assets/background.jpeg");
  background-repeat: no-repeat;
  background-attachment: fixed;
  background-size: cover;
  height: 100vh;
}

a.router-link-active {
  color: white;
  text-decoration: none;
}

router-link:hover {
  color: red;
  text-decoration: none;
}

router-link:hover[class="float"] {
  color: red;
  text-decoration: none;
}

.header-contents {
  font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
  font-size: 40px;
  text-align: center;
}
</style>
