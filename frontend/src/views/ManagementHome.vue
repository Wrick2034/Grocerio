<template>
    <div>
      <ManNavbar :name="uname" @view-home="ViewHome" />
      <br>
      <div class="row" v-if="viewHome">
          <div class="col" style="display:flex;flex-direction:column;flex-wrap:wrap;justify-content:space-around;">
            <div class="categories" v-for="item in results" :key="item.name">
              <div class="card" style="display:flex;flex-direction:column;flex-wrap:wrap;justify-content:space-around;overflow-x:auto;overflow-y:hidden;width:auto">
                <div class="card-header text-center" style="background-color: rgb(239, 244, 175);height: 130px;"><router-link to="/ManagementHome" @click="exportCSV(item.name)"><h1 style="float:left"><i class="bi bi-file-text-fill"></i></h1></router-link><p class="display-3">{{ item.name }}</p><h6 style="float:right"><router-link to="/ManagementHome" @click="UpdateCategory(item.name)">UPDATE</router-link>    |   <router-link to="/ManagementHome" @click="DeleteCategory(item.name)">DELETE</router-link></h6></div>
                <div class="body" style="display:flex;flex-direction:row;flex-wrap:wrap;justify-content:space-around;overflow-x:auto;overflow-y:hidden;">
                  <div class="card-body" v-for="product in item.products" :key="product.name" style="display:flex;flex-direction:row;flex-wrap:wrap;justify-content:space-around;overflow-x:auto;overflow-y:hidden;background-color: rgb(233, 233, 233);">
                    <ItemCard :item="product"/>
                  </div>
                </div>
                <div style="justify-content:space-around;display: flex">
                    <router-link to="/ManagementHome" @click="AddProduct(item.name)">
                        <i class="bi bi-plus-circle-fill custom-icon"></i>
                    </router-link>
                </div>
              </div>
            </div>
          </div>
      </div>
      <div class="row" v-else>
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
                <th scope="col" style="text-align:center">Date</th>
              </tr>
            </thead>
            <tbody v-for="request in requests" :key="request.id">
              <tr>
                <td scope="col" style="text-align:center">{{ request.type }}</td>
                <td scope="col" style="text-align:center">{{ request.old_name }}</td>
                <td scope="col" style="text-align:center">{{ request.new_name }}</td>
                <td scope="col" style="text-align:center">{{ request.date }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="display-6 text-center" v-else>
          <br><br><br>
          You have made no requests...
        </div>
      </div>
      <div class="float" v-if="viewHome">
        <router-link to="/ManagementHome" @click="AddCategory"><i class="bi bi-plus-circle-fill my-float"></i></router-link>
      </div>
    </div>
  </template>

<script>
import ManNavbar from '@/components/ManNavbar.vue'
import ItemCard from '@/components/man_card.vue'
export default {
  name: 'ManagementHome',
  components: {
    ManNavbar,
    ItemCard
  },
  data () {
    return {
      results: [],
      uname: '',
      viewHome: true,
      requests: [],
      EmptyStore: false
    }
  },
  methods: {
    ViewHome (e) {
      if (e) {
        this.viewHome = true
        this.getManHome()
      } else {
        this.viewHome = false
        this.getRequests()
      }
    },
    AddCategory () {
      this.$router.push(`/AddCategory/${this.uname}`)
    },
    UpdateCategory (value) {
      this.$router.push(`/UpdateCategory/${this.uname}/${value}`)
    },
    AddProduct (value) {
      this.$router.push(`/AddProduct/${this.uname}/${value}`)
    },
    DeleteCategory (value) {
      const token = sessionStorage.getItem('access_token')
      fetch('http://127.0.0.1:5000/api/Requests/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          Authorization: 'Bearer ' + token
        },
        body: JSON.stringify({
          type: 'DELETE',
          old_name: value
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
    },
    getManHome () {
      const token = sessionStorage.getItem('access_token')
      fetch('http://127.0.0.1:5000/api/ManHome/', {
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
    getRequests () {
      const token = sessionStorage.getItem('access_token')
      fetch('http://127.0.0.1:5000/api/ManRequest/', {
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
            this.requests = data.result
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
    exportCSV (name) {
      const token = sessionStorage.getItem('access_token')
      fetch(`http://127.0.0.1:5000/api/Trigger/${name}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          Authorization: 'Bearer ' + token
        }
      })
        .then(response => response.json())
        .then(data => {
          setTimeout(() => { window.open('http://127.0.0.1:5000/api/Download') }, 6000)
        })
        .catch(error => {
          console.error('Error : ', error)
          window.alert('Failed to export CSV file')
        })
    }
  },
  mounted () {
    this.getManHome()
  }
}
</script>

<style>
  .float
  {
    position:fixed;
    width:60px;
    height:60px;
    bottom:40px;
    right:40px;
    color:#33CC66;
    border-radius:50px;
    text-align:center;
  }
  .my-float
  {
    margin-top:10px;
    font-size: 50px;
  }
  .custom-icon{
    width:40px;
    height:40px;
    display: inline-block;
    font-size: 35px;
    margin-bottom: 13px;
    color: peru;
  }
</style>
