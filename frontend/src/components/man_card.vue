<template>
    <div class="card" style="width:18rem">
        <div class="card-header text-center" style="background-color: rgb(170, 216, 152);font-size:1.5rem"><b>{{ item.product_name }}</b></div>
        <div class="card-body justify-content-between" style="background-color: rgb(239, 244, 175);">
            <div class="container-fluid text-center">
              <div class="row">
                  <div class="col">
                    <label><b>Price</b></label>
                  </div>
                  <div class="col">
                    ₹ {{ item.rate }}/{{ item.unit }}
                  </div>
              </div>
              <br>
              <div v-if="item.quantity > 0">
                <div class="row">
                  <div class="col-7">
                    <label><b>Available units</b></label>
                  </div>
                  <div class="col-3" v-if="item.quantity > 0">
                    {{ item.quantity }}
                  </div>
                </div>
              </div>
              <div class="text-center" v-else>
                <i>OUT OF STOCK</i>
              </div>
              <br>
            </div>
        </div>
        <div class="card-footer" style="background-color: rgb(156, 127, 115);">
            <div class="d-grid gap-2 col-6 mx-auto">
              <button class="btn btn-light btn-sm" @:click="updateItem(item.product_name)"><b>Update</b></button>
              <button class="btn btn-light btn-sm" @:click="deleteItem(item.product_name)"><b>Delete</b></button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
  name: 'ItemCard',
  props: ['item'],
  data () {
    return {
      quantity: 0
    }
  },
  methods: {
    updateItem (value) {
      this.$router.push(`/UpdateProduct/${value}`)
    },
    deleteItem (value) {
      alert('Do you want to delete this item??')
      const token = sessionStorage.getItem('access_token')
      fetch(`http://127.0.0.1:5000/api/Product/${value}/`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          Authorization: 'Bearer ' + token
        }
      })
        .then(response => response.json())
        .then(data => {
          if (data.msg === 'Successful') {
            console.log('Item Deletion Successful')
            this.$router.push('/ManagementHome')
          } else {
            console.error('Request Deletion Unsuccessful')
          }
        })
        .catch(error => {
          console.error('Error : ', error)
        })
    }
  },
  components: {}
}
</script>

<style>
  .card{
    margin-bottom: 1rem;
  }
</style>
