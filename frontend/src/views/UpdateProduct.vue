<template>
    <ManNavbar :name="uname" />
    <br>
    <div class="update-body" style="width: 80%; align-items: center; margin-left: 130px">
            <div class="display-5 text-center">
                Update the Product
            </div>
            <hr><br>
            <div>
                <form id="update" @submit.prevent="updateProduct(this.$route.params.value)">
                    <div id="product_name" class="form-outline mb-4">
                        <input type="text" v-model="product" placeholder="Enter product name" class="form-control">
                    </div>
                    <br>
                    <div id="unit_selection" class="form-outline mb-4">
                        <label for="unit">Choose a unit : </label>
                        <select v-model="unit_sel" name="unit" id="unit" class="form-control">
                            <option value="select">Select</option>
                            <option value="kg">₹/kg</option>
                            <option value="g">₹/g</option>
                            <option value="dozen">₹/dozen</option>
                            <option value="Litre">₹/Litre</option>
                            <option value="Unit">₹/Unit</option>
                        </select>
                    </div>
                    <br>
                    <div id="rate" class="form-outline mb-4">
                        <input type="text" v-model="rate" placeholder={{rate}} class="form-control">
                    </div>
                    <br>
                    <div id="quantity" class="form-outline mb-4">
                        <input type="text" v-model="quantity" placeholder={{quantity}} class="form-control">
                    </div>
                    <br>
                    <div id="submit-button" class="d-grid gap-2 d-md-flex justify-content-md-center">
                        <button type="submit" class="btn btn-outline-success">Update</button>
                    </div>
                </form>
            </div>
        </div>
</template>

<script>
import ManNavbar from '@/components/ManNavbar.vue'
export default {
  name: 'UpdateProduct',
  components: {
    ManNavbar
  },
  data () {
    return {
      product: '',
      unit_sel: '',
      rate: '',
      quantity: '',
      name: '',
      uname: ''
    }
  },
  methods: {
    getProductDetail (value) {
      const token = sessionStorage.getItem('access_token')
      fetch(`http://127.0.0.1:5000/api/Product/${value}/`, {
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
            this.name = value
            this.product = data.result.name
            this.rate = data.result.rate
            this.unit = data.result.unit
            this.quantity = data.result.quantity
            this.uname = data.name
            console.log('Product Load Successful')
          } else {
            console.error('Product Load Unsuccessful')
          }
        })
        .catch(error => {
          console.error('Error : ', error)
        })
    },
    updateProduct (value) {
      const token = sessionStorage.getItem('access_token')
      fetch(`http://127.0.0.1:5000/api/Product/${value}/`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          Authorization: 'Bearer ' + token
        },
        body: JSON.stringify({
          product_name: this.product,
          unit: this.unit_sel,
          rate: this.rate,
          quantity: this.quantity
        })
      })
        .then(response => response.json())
        .then(data => {
          if (data.msg === 'Successful') {
            console.log('Product Update Successful')
            this.$router.push('/ManagementHome')
          } else {
            console.error('Product Update Unsuccessful')
          }
        })
        .catch(error => {
          console.error('Error : ', error)
        })
    }
  },
  mounted () {
    this.getProductDetail(this.$route.params.value)
  }
}
</script>
