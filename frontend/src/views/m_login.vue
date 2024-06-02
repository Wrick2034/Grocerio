
<template>
    <div class="m_login">
        <br><br><br>
        <div class="container-fluid shadow p-3 mb-5 bg-body-tertiary rounded"
            style="border:1px solid;border-radius:30px;background-color:aliceblue;width:45%;height:75%">
            <div class="header-contents">
                Management Login
            </div>
            <hr><br>
            <div>
                <form>
                    <div id="uname" class="form-outline mb-4">
                        <input type="text" v-model="username" placeholder="Enter Username" class="form-control">
                    </div>
                    <br>
                    <div id="pass" class="form-outline mb-4">
                        <input type="password" v-model="password" placeholder="Enter Password" class="form-control">
                    </div>
                    <br>
                    <div id="submit-button" class="d-grid gap-2 d-md-flex justify-content-md-center">
                        <button type="submit" class="btn btn-outline-success" @:click.prevent="login">Sign in</button>
                        <router-link to="/ManRegister"><button type="submit" class="btn btn-outline-danger">Sign up</button></router-link>
                    </div>
                </form>
                <br>
                <div align="center">Are you a user? Login <router-link to="/User">Here</router-link>...</div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ManLogin',
  data () {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    login () {
      if (!this.username || !this.password) {
        alert('Please enter both the username and the password !!')
        return
      }
      const userData = {
        username: this.username,
        password: this.password
      }
      axios
        .post('http://127.0.0.1:5000/api/managementLogin/', userData)
        .then((response) => {
          const data = response.data
          if (data.SignIn === 'Successful') {
            sessionStorage.setItem('access_token', data.access_token)
            console.log('Login successful')
            if (data.role === 'admin') {
              this.$router.push('/AdminHome')
            } else if (data.role === 'management') {
              this.$router.push('/ManagementHome')
            }
          } else {
            console.error('Login failed')
            alert('Invalid Credentials!!!')
          }
        })
        .catch((error) => {
          console.error('Error: ', error)
        })
    }
  },
  components: {}
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
    color: rgb(46, 55, 235);
    text-decoration: none;
}

a:visited {
    color: rgb(46, 55, 235);
    text-decoration: none;
}

a:active {
    color: rgb(46, 55, 235);
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
