<template>
  <div>
    <AdminNavbar :name="name" @view-request="ViewRequest" />
    <br>
    <div class="body" v-if="viewRequest">
      <div class="requests" v-if="requestsVisible">
        <div class="requests-body" v-if="!EmptyStore">
          <br>
          <div class="display-5 text-center">Pending Requests</div>
          <br><br>
          <table class="table">
            <thead>
              <tr class="table-success">
                <th scope="col" style="text-align:center">Request Type</th>
                <th scope="col" style="text-align:center">Old Name</th>
                <th scope="col" style="text-align:center">New Name</th>
                <th scope="col" style="text-align:center">Request By</th>
                <th scope="col" style="text-align:center">Date</th>
                <th colspan="2" scope="col" style="text-align:center">Action</th>
              </tr>
            </thead>
            <tbody v-for="request in results" :key="request.id">
              <tr>
                <td scope="col" style="text-align:center">{{ request.type }}</td>
                <td scope="col" style="text-align:center">{{ request.old_name }}</td>
                <td scope="col" style="text-align:center">{{ request.new_name }}</td>
                <td scope="col" style="text-align:center">{{ request.by }}</td>
                <td scope="col" style="text-align:center">{{ request.date }}</td>
                <td scope="col" style="text-align:center"><button class="btn btn-outline-success" @click="approveRequest(request.id,request.type,request.old_name)">Approve</button></td>
                <td scope="col" style="text-align:center"><button class="btn btn-outline-danger" @click="deleteRequest(request.id)">Decline</button></td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="display-6 text-center" v-else>
          <br><br><br>
          No Requests made by the employees right now...
        </div>
      </div>
    </div>
    <div v-else>
      <div class="requests" v-if="signupRequest">
        <div class="requests-body" v-if="!EmptyRequests">
          <br>
          <div class="display-5 text-center">Pending Store Manager Signup Requests</div>
          <br><br>
          <table class="table">
            <thead>
              <tr class="table-success">
                <th scope="col" style="text-align:center">First Name</th>
                <th scope="col" style="text-align:center">Last Name</th>
                <th scope="col" style="text-align:center">Username</th>
                <th scope="col" style="text-align:center">Email</th>
                <th scope="col" style="text-align:center">Date of Birth</th>
                <th colspan="2" scope="col" style="text-align:center">Action</th>
              </tr>
            </thead>
            <tbody v-for="request in signupresults" :key="request.id">
              <tr>
                <td scope="col" style="text-align:center">{{ request.first_name }}</td>
                <td scope="col" style="text-align:center">{{ request.last_name }}</td>
                <td scope="col" style="text-align:center">{{ request.username }}</td>
                <td scope="col" style="text-align:center">{{ request.email }}</td>
                <td scope="col" style="text-align:center">{{ request.dob }}</td>
                <td scope="col" style="text-align:center"><button class="btn btn-outline-success" @click="ApproveSignupRequest(request.id)">Approve</button></td>
                <td scope="col" style="text-align:center"><button class="btn btn-outline-danger" @click="DeleteSignUpRequest(request.id)">Decline</button></td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="display-6 text-center" v-else>
          <br><br><br>
          No Sign Up Requests made right now...
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AdminNavbar from '@/components/AdminNavbar.vue'
export default {
  name: 'AdminHome',
  data () {
    return {
      requestsVisible: true,
      signupRequest: true,
      EmptyStore: false,
      results: [],
      name: '',
      viewRequest: true,
      EmptyRequests: false,
      signupresults: []
    }
  },
  components: {
    AdminNavbar
  },
  methods: {
    getManRequests () {
      const token = sessionStorage.getItem('access_token')
      fetch('http://127.0.0.1:5000/api/Requests/', {
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
            this.EmptyStore = false
            this.results = data.result
            this.name = data.user
            console.log('Request Setup Successful')
          } else {
            this.EmptyStore = true
            this.name = data.user
            console.log('Request Setup Unsuccessful')
          }
        })
        .catch(error => {
          console.error('Error : ', error)
        })
    },
    approveRequest (value, type, name) {
      if (type === 'ADD') {
        this.addCategory(value)
      } else if (type === 'UPDATE') {
        this.updateCategory(value)
      } else if (type === 'DELETE') {
        this.deleteCategory(value, name)
      }
    },
    updateCategory (value) {
      const token = sessionStorage.getItem('access_token')
      fetch(`http://127.0.0.1:5000/api/Request/${value}/`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          Authorization: 'Bearer ' + token
        }
      })
        .then(response => response.json())
        .then(data => {
          if (data.msg === 'Successful') {
            console.log('Request Update Successful')
            this.$router.push('/AdminHome')
          } else {
            console.error('Request Update Unsuccessful')
          }
        })
        .catch(error => {
          console.error('Error : ', error)
        })
    },
    addCategory (value) {
      const token = sessionStorage.getItem('access_token')
      fetch(`http://127.0.0.1:5000/api/Request/${value}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          Authorization: 'Bearer ' + token
        }
      })
        .then(response => response.json())
        .then(data => {
          if (data.msg === 'Successful') {
            console.log('Request Addition Successful')
            this.$router.push('/AdminHome')
          } else {
            console.error('Request Addition Unsuccessful')
          }
        })
        .catch(error => {
          console.error('Error : ', error)
        })
    },
    deleteCategory (value, name) {
      const token = sessionStorage.getItem('access_token')
      fetch(`http://127.0.0.1:5000/api/Category/${name}/`, {
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
            console.log('Request Deletion Successful')
            this.deleteRequest(value)
            this.$router.push('/AdminHome')
          } else {
            console.error('Request Deletion Unsuccessful')
          }
        })
        .catch(error => {
          console.error('Error : ', error)
        })
    },
    deleteRequest (value) {
      const token = sessionStorage.getItem('access_token')
      fetch(`http://127.0.0.1:5000/api/Request/${value}/`, {
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
            console.log('Request Deletion Successful')
            this.$router.push('/AdminHome')
          } else {
            console.error('Request Deletion Unsuccessful')
          }
        })
        .catch(error => {
          console.error('Error : ', error)
        })
    },
    ViewRequest (e) {
      if (e) {
        this.viewRequest = true
        this.getManRequests()
      } else {
        this.viewRequest = false
        this.getPeople()
      }
    },
    ApproveSignupRequest (value) {
      const token = sessionStorage.getItem('access_token')
      fetch(`http://127.0.0.1:5000/api/SignUpRequest/${value}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          Authorization: 'Bearer ' + token
        }
      })
        .then(response => response.json())
        .then(data => {
          if (data.msg === 'Successful') {
            console.log('Request Addition Successful')
            this.$router.push('/AdminHome')
          } else {
            console.error('Request Addition Unsuccessful')
          }
        })
        .catch(error => {
          console.error('Error : ', error)
        })
    },
    DeleteSignUpRequest (value) {
      const token = sessionStorage.getItem('access_token')
      fetch(`http://127.0.0.1:5000/api/SignUpRequest/${value}/`, {
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
            console.log('Request Deletion Successful')
            this.$router.push('/AdminHome')
          } else {
            console.error('Request Deletion Unsuccessful')
          }
        })
        .catch(error => {
          console.error('Error : ', error)
        })
    },
    getPeople () {
      const token = sessionStorage.getItem('access_token')
      fetch('http://127.0.0.1:5000/api/SignUpRequests/', {
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
            this.EmptyRequests = false
            this.signupresults = data.result
            this.name = data.user
            console.log('Request Setup Successful')
          } else {
            this.EmptyRequests = true
            this.name = data.user
            console.log('Request Setup Unsuccessful')
          }
        })
        .catch(error => {
          console.error('Error : ', error)
        })
    }
  },
  mounted () {
    this.getManRequests()
  }
}
</script>

<style>

</style>
