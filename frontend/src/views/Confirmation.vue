<template>
    <div class="confirm-body">
        <NavBar :name="user"/>
        <br><br><br>
        <div class="container-fluid shadow p-3 mb-5 bg-body-tertiary rounded" style="border:1px solid;border-radius:30px;background-color:aliceblue;width:73%">
            <div class="header-contents">
                Confirmation Page
            </div>
            <hr><br><br>
            <div>
                <form>
                    <div class="display-5 text-center">Your Total : ₹ {{ total }}</div>
                    <br>
                    <div id="address" class="form-outline mb-4">
                        <input type="text" v-model="address" placeholder="Enter your Address" class="form-control" required>
                    </div>
                    <br>
                    <div id="payment_method" class="form-outline mb-4">
                        <label for="payment">Choose a payment method : </label>
                        <select v-model="mop" name="payment" id="unit" class="form-control">
                            <option value="cash">Cash</option>
                            <option value="upi">UPI</option>
                            <option value="credit card">Credit Card</option>
                            <option value="debit card">Debit Card</option>
                        </select>
                    </div>
                    <div class="display-8 text-center">Every payment will be taken on delivery</div>
                    <br><br>
                    <div id="submit-button" class="d-grid gap-2 d-md-flex justify-content-md-center">
                        <button type="submit" @click="confirmOrder" class="btn btn-outline-success">Submit</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import NavBar from '@/components/navbar.vue'
export default {
  name: 'OrderConfirmation',
  data () {
    return {
      total: 0,
      mop: '',
      address: '',
      user: ''
    }
  },
  methods: {
    visibleToggler (value) {
      this.isVisible = value
    },
    confirmOrder () {
      if (!this.address || !this.mop) {
        alert('Please enter a valid address or mode of payment')
        return
      }
      const token = sessionStorage.getItem('access_token')
      fetch('http://127.0.0.1:5000/api/Confirm/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          Authorization: 'Bearer ' + token
        },
        body: JSON.stringify({
          address: this.address,
          mop: this.mop
        })
      })
        .then(response => response.json())
        .then(data => {
          if (data.msg === 'Order Successful') {
            console.log('Order Placed Successful')
          } else {
            console.error('Order Placed Unsuccessful')
          }
        })
        .catch(error => {
          console.error('Error : ', error)
        })
      alert('Thank You For shopping with us')
      this.$router.push('/Home')
    }
  },
  mounted () {
    const token = sessionStorage.getItem('access_token')
    fetch('http://127.0.0.1:5000/api/Confirm/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        Authorization: 'Bearer ' + token
      }
    })
      .then(response => response.json())
      .then(data => {
        if (data.total !== 0) {
          this.total = data.total
          this.user = data.user
          console.log('Confirmation Page Setup Successful')
        } else {
          console.error('Confirmation Page Setup Unsuccessful')
        }
      })
      .catch(error => {
        console.error('Error : ', error)
      })
  },
  components: {
    NavBar
  }
}
</script>
