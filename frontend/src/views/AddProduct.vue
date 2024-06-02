<template>
    <ManNavbar :name="uname" />
    <br>
    <div class="update-body" style="width: 80%; align-items: center; margin-left: 130px">
            <div class="display-5 text-center">
                Add a Product
            </div>
            <hr><br>
            <div>
                <form id="update" @submit.prevent="addProduct(this.$route.params.value)">
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
                        <input type="text" v-model="rate" placeholder="Enter product rate" class="form-control">
                    </div>
                    <br>
                    <div id="quantity" class="form-outline mb-4">
                        <input type="text" v-model="quantity" placeholder="Enter product quantity" class="form-control">
                    </div>
                    <br>
                    <div id="submit-button" class="d-grid gap-2 d-md-flex justify-content-md-center">
                        <button type="submit" class="btn btn-outline-success">Add Product</button>
                    </div>
                </form>
            </div>
        </div>
</template>

<script>
import ManNavbar from '@/components/ManNavbar.vue'
export default {
  name: 'AddProduct',
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
    addProduct () {
      const token = sessionStorage.getItem('access_token')
      fetch('http://127.0.0.1:5000/api/Products/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          Authorization: 'Bearer ' + token
        },
        body: JSON.stringify({
          product_name: this.product,
          unit: this.unit_sel,
          rate: this.rate,
          quantity: this.quantity,
          category_name: this.name
        })
      })
        .then(response => response.json())
        .then(data => {
          if (data.msg === 'Successful') {
            console.log('Product Add Successful')
            this.$router.push('/ManagementHome')
          } else {
            console.error('Product Add Unsuccessful')
          }
        })
        .catch(error => {
          console.error('Error : ', error)
        })
    }
  },
  mounted () {
    this.uname = this.$route.params.value
    this.name = this.$route.params.category
  }
}
</script>
