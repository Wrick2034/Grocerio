<template>
    <div class="search">
        <NavBar :name="name" />
        <div v-if="SuccessfulSearch">
            <br><br>
            <div class="row" v-if="type==='Category'" style="display:flex;flex-direction:column;flex-wrap:wrap;justify-content:space-around;">
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
            <div v-else>
                <div v-for="product in results" :key="product.name" style="display:flex;flex-direction:row;flex-wrap:wrap;justify-content:space-around;overflow-x:auto;overflow-y:hidden">
                    <ItemCard :item="product"/>
                </div>
            </div>
        </div>
        <div class="display-5 text-center" v-else>
            <br><br><br>
            No Such Product or category exists....
        </div>
    </div>
</template>
<script>
import NavBar from '@/components/navbar.vue'
import ItemCard from '@/components/card.vue'
export default {
  name: 'SearchResults',
  data () {
    return {
      SuccessfulSearch: false,
      results: [],
      name: '',
      type: ''
    }
  },
  methods: {
    Search (value) {
      const token = sessionStorage.getItem('access_token')
      fetch(`http://127.0.0.1:5000/api/Search/${value}/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          Authorization: 'Bearer ' + token
        }
      })
        .then(response => response.json())
        .then(data => {
          if (data.msg === 'Success') {
            this.SuccessfulSearch = true
            this.type = data.type
            this.name = data.user
            if (this.type === 'Category') {
              this.results = data.results.items
            } else {
              this.results = data.results
            }
            console.log('Search Successful')
          } else {
            console.log('Search Unsuccessful')
            this.SuccessfulSearch = false
            this.name = data.user
          }
        })
        .catch(error => {
          console.error('Error : ', error)
        })
    }
  },
  mounted () {
    this.Search(this.$route.params.value)
  },
  components: {
    NavBar,
    ItemCard
  }
}
</script>
