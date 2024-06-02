<template>
    <div class="Cart">
        <div class="cart" v-if="isCart">
            <div class="cart-header" style="background-color:rgb(172, 230, 139);">
              <h1 class="cart-title spread space-around" style="background-color:rgb(172, 230, 139)">
                  <span style="float:left">
                    <b>&ensp;Cart
                    <i class="bi bi-cart4"></i></b>
                  </span>
                  <RouterLink to="Home"><em style="float:right" @:click="CartToggler"><i class="bi bi-x-circle"></i></em></RouterLink>
              </h1>
            </div>
            <br><br><br>
            <div class="cart-body" v-if="CartLength()>=1">
                <table class='table'>
                    <thead>
                        <tr class="table-success">
                            <th scope="col">Product</th>
                            <th scope="col">Quantity</th>
                            <th scope="col">Rate</th>
                            <th scope="col">Cost</th>
                        </tr>
                    </thead>
                    <tbody v-for="item in results" :key="item.product">
                        <tr>
                            <td scope="col">{{ item.product }}</td>
                            <td scope="col">{{ item.quantity }}</td>
                            <td scope="col">{{ item.rate }}</td>
                            <td scope="col">₹ {{ item.cost }}</td>
                            <td scope="col"><router-link to="/Home" @click="deleteItem(item.id)"><i class="bi bi-trash3-fill"></i></router-link></td>
                        </tr>
                    </tbody>
                    <tbody>
                      <tr>
                          <th scope="col" colspan="3">Total Cost</th>
                          <td scope="col">₹ {{ total }}</td>
                      </tr>
                    </tbody>
                </table>

                <br><br>
                <div id="submit-button" class="d-grid gap-2 d-md-flex justify-content-md-center">
                  <RouterLink to="/Confirm"><button class="btn btn-outline-success">Buy Now</button></RouterLink>
                </div>
            </div>
            <div class="cart-body" v-else style="text-align:center;">
                <br><br><br><br><br>
                <i>No items in the cart</i>
            </div>
        </div>
    </div>
</template>

<script>
export default {
  name: 'UserCart',
  data () {
    return {
      isCart: true,
      itemCount: 0,
      total: 0,
      results: [],
      isUpdate: false
    }
  },
  props: ['visibility'],
  watch: {
    visibility: {
      immediate: true,
      handler (newValue) {
        this.isCart = newValue
      }
    }
  },
  methods: {
    CartToggler () {
      this.isCart = !this.isCart
      this.$emit('set-visibility', this.isCart)
    },
    get () {
      this.isCart = this.visibility
    },
    CartLength () {
      this.itemCount = this.results.length
      return this.itemCount
    },
    deleteItem (value) {
      const token = sessionStorage.getItem('access_token')
      fetch(`http://127.0.0.1:5000/api/Cart/${value}/`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          Authorization: 'Bearer ' + token
        }
      })
        .then(response => response.json())
        .then(data => {
          if (data.msg === 'Success') {
            console.log('Cart Item Deletion Successful')
            this.CartToggler()
          } else {
            console.error('Cart Item Deletion Unsuccessful')
          }
        })
        .catch(error => {
          console.error('Error : ', error)
        })
    },
    getCartData () {
      const token = sessionStorage.getItem('access_token')
      fetch('http://127.0.0.1:5000/api/Cart/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          Authorization: 'Bearer ' + token
        }
      })
        .then(response => response.json())
        .then(data => {
          if (data.items.length !== 0) {
            this.EmptyStore = false
            this.results = data.items
            this.total = data.total_cost
            console.log('Cart Setup Successful')
          } else {
            console.error('Cart Setup Unsuccessful')
          }
        })
        .catch(error => {
          console.error('Error : ', error)
        })
    }
  },
  mounted () {
    this.getCartData()
  }
}
</script>

<style>

</style>
