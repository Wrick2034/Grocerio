
<template>
    <div class="u_home">
        <NavBar :visibility = "isVisible" @set-visibility="visibleToggler" :name = "uname" />
        <br>
        <div v-if="EmptyStore">
            <div class="container">
                <p align="center" style="font-size:large">There are no products available right now...</p>
                <p align="center">Please Try Again Later...</p>
            </div>
        </div>
        <div v-else class="row">
          <div class="col" style="display:flex;flex-direction:column;flex-wrap:wrap;justify-content:space-around;">
            <div class="categories" v-for="item in results" :key="item.name">
              <div class="card" style="display:flex;flex-direction:column;flex-wrap:wrap;justify-content:space-around;overflow-x:auto;overflow-y:hidden;width:auto">
                <div class="card-header text-center" style="background-color: rgb(239, 244, 175);"><h1>{{ item.name }}</h1></div>
                <div class="body" style="display:flex;flex-direction:row;flex-wrap:wrap;justify-content:space-around;overflow-x:auto;overflow-y:hidden;">
                  <div class="card-body" v-for="product in item.products" :key="product.name" style="display:flex;flex-direction:row;flex-wrap:wrap;justify-content:space-around;overflow-x:auto;overflow-y:hidden;background-color: rgb(233, 233, 233);">
                    <ItemCard :item="product"/>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="col" v-if="isVisible" style="width: 5%; border-radius: 25px;">
            <UserCart @set-visibility="visibleToggler" :visibility = "isVisible" />
          </div>
        </div>
    </div>
</template>

<script>
import NavBar from '@/components/navbar.vue'
import ItemCard from '@/components/card.vue'
import UserCart from '@/components/cart.vue'
export default {
  name: 'UserHome',
  data () {
    return {
      isVisible: false,
      EmptyStore: false,
      results: [],
      uname: ''
    }
  },
  methods: {
    visibleToggler (value) {
      this.isVisible = value
    }
  },
  mounted () {
    const token = sessionStorage.getItem('access_token')
    fetch('http://127.0.0.1:5000/api/Home/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        Authorization: 'Bearer ' + token
      }
    })
      .then(response => response.json())
      .then(data => {
        if (data.result.items.length !== 0) {
          this.EmptyStore = false
          this.results = data.result.items
          this.uname = data.name
          console.log('Home Setup Successful')
        } else {
          console.error('Home Setup Unsuccessful')
        }
      })
      .catch(error => {
        console.error('Error : ', error)
      })
  },
  components: {
    NavBar,
    ItemCard,
    UserCart
  }
}
</script>

<style>
.header-contents {
    font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
    font-size: 40px;
    text-align: center;
}

.m_login {
    background-image: url("@/assets/background.jpeg");
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-size: cover;
    height: 100vh;
}

a:link {
    color: rgb(3, 4, 10);
    text-decoration: none;
}

a:visited {
    color: rgb(5, 6, 10);
    text-decoration: none;
}

a:active {
    color: rgb(4, 5, 13);
    text-decoration: none;
}

a:hover {
    color: red;
    text-decoration: none;
}

a:hover[class="float"] {
    color: red;
    text-decoration: none;
}
</style>
