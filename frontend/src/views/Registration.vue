<template>
    <div class="signup">
        <br><br>
        <div class="container-fluid shadow p-3 mb-5 bg-body-tertiary rounded"
            style="border:1px solid;border-radius:30px;background-color:aliceblue;width:73%">
            <div class="header-contents">
                New User Registration
            </div>
            <hr><br>
            <div>
                <form @submit.prevent>
                    <div id="fname" class="form-outline mb-4">
                        <input type="text" v-model="fname" placeholder="Enter First Name" align="middle" class="form-control"
                            required>
                    </div>
                    <br>
                    <div id="lname" class="form-outline mb-4">
                        <input type="text" v-model="lname" placeholder="Enter Last Name" align="middle" class="form-control">
                    </div>
                    <br>
                    <div id="email" class="form-outline mb-4">
                        <input type="email" v-model="email" placeholder="Enter Email ID" align="middle" class="form-control"
                            required>
                    </div>
                    <br>
                    <div id="uname" class="form-outline mb-4">
                        <input type="text" v-model="uname" placeholder="Enter Username" align="middle" class="form-control"
                            required>
                    </div>
                    <br>
                    <div id="pass" class="form-outline mb-4">
                        <input type="password" v-model="pass" placeholder="Enter Password" align="middle" class="form-control"
                            required>
                    </div>
                    <br>
                    <div id="dob" class="form-outline mb-4">
                        <input type="date" v-model="dob" placeholder="Enter Date of Birth" align="middle" class="form-control"
                            required>
                    </div>
                    <div id="submit-button" class="d-grid gap-2 d-md-flex justify-content-md-center">
                        <button @:click="SignUp" class="btn btn-outline-success" type="submit" value="sign up">Sign up</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>

export default {
  name: 'SignUp',
  data () {
    return {
      fname: '',
      lname: '',
      uname: '',
      email: '',
      pass: '',
      dob: ''
    }
  },
  methods: {
    SignUp () {
      if (!this.uname || !this.pass || !this.fname || !this.email || !this.dob) {
        alert('Please enter all the details !!')
        return
      }
      const token = sessionStorage.getItem('access_token')
      fetch('http://127.0.0.1:5000/api/Registration/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          Authorization: 'Bearer ' + token
        },
        body: JSON.stringify({
          first_name: this.fname,
          last_name: this.lname,
          username: this.uname,
          password: this.pass,
          email: this.email,
          dob: this.dob
        })
      })
        .then(response => response.json())
        .then(data => {
          if (data.SignUp === 'Successful') {
            console.log('SignUp successful')
            this.$router.push('/User')
          } else {
            console.error('SignUp failed')
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
.signup {
    background-image: url("@/assets/background.jpeg");
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-size: cover;
    height: 200vh;
}

.header-contents {
    font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
    font-size: 40px;
    text-align: center;
}
</style>
