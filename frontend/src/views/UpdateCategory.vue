<template>
    <ManNavbar :name="uname" />
    <br>
    <div class="update-body" style="width: 80%; align-items: center; margin-left: 130px">
            <div class="display-5 text-center">
                Update Category
            </div>
            <hr><br>
            <div>
                <form id="add" @submit.prevent="updateCategory">
                    <div id="category_name" class="form-outline mb-4">
                        <input type="text" v-model="category" :placeholder="this.$route.params.category" class="form-control">
                    </div>
                    <br>
                    <div id="submit-button" class="d-grid gap-2 d-md-flex justify-content-md-center">
                        <button type="submit" class="btn btn-outline-success">Update Category</button>
                    </div>
                </form>
            </div>
        </div>
</template>

<script>
import ManNavbar from '@/components/ManNavbar.vue'
export default {
  name: 'AddCategory',
  components: {
    ManNavbar
  },
  data () {
    return {
      category: '',
      uname: ''
    }
  },
  methods: {
    updateCategory () {
      const token = sessionStorage.getItem('access_token')
      fetch('http://127.0.0.1:5000/api/Requests/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          Authorization: 'Bearer ' + token
        },
        body: JSON.stringify({
          type: 'UPDATE',
          new_name: this.category,
          old_name: this.$route.params.category
        })
      })
        .then(response => response.json())
        .then(data => {
          if (data.msg === 'Successful') {
            console.log('Request Sent Successful')
            this.$router.push('/ManagementHome')
          } else {
            console.error('Request Sent Unsuccessful')
          }
        })
        .catch(error => {
          console.error('Error : ', error)
        })
    }
  },
  mounted () {
    this.uname = this.$route.params.value
  }
}
</script>
