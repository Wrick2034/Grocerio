import { createRouter, createWebHistory } from 'vue-router'
import landingPage from '@/views/Landing.vue'
import UserLogin from '@/views/u_login.vue'
import SignUp from '@/views/Registration.vue'
import ManLogin from '@/views/m_login.vue'
import UserHome from '@/views/Home.vue'
import ManagementHome from '@/views/ManagementHome.vue'
import AdminHome from '@/views/AdminHome.vue'
import OrderConfirmation from '@/views/Confirmation.vue'
import SearchResults from '@/views/SearchResults.vue'
import ManReg from '@/views/m_registration.vue'
import UpdateProduct from '@/views/UpdateProduct.vue'
import AddCategory from '@/views/AddCategory.vue'
import UpdateCategory from '@/views/UpdateCategory.vue'
import AddProduct from '@/views/AddProduct.vue'

const routes = [
  {
    path: '/',
    name: 'Land',
    component: landingPage
  },
  {
    path: '/User',
    name: 'User Login',
    component: UserLogin
  },
  {
    path: '/Management',
    name: 'Management Login',
    component: ManLogin
  },
  {
    path: '/ManRegister',
    name: 'Management SignUp',
    component: ManReg
  },
  {
    path: '/Register',
    name: 'User SignUp',
    component: SignUp
  },
  {
    path: '/Home',
    name: 'User Home',
    component: UserHome
  },
  {
    path: '/AdminHome',
    name: 'Admin Home',
    component: AdminHome
  },
  {
    path: '/ManagementHome',
    name: 'Management Home',
    component: ManagementHome
  },
  {
    path: '/Confirm',
    name: 'Order Confirmation',
    component: OrderConfirmation
  },
  {
    path: '/Search/:value',
    name: 'Search Results',
    component: SearchResults
  },
  {
    path: '/UpdateProduct/:value',
    name: 'Update Product',
    component: UpdateProduct
  },
  {
    path: '/AddCategory/:value',
    name: 'Add Category',
    component: AddCategory
  },
  {
    path: '/UpdateCategory/:value/:category',
    name: 'Update Category',
    component: UpdateCategory
  },
  {
    path: '/AddProduct/:value/:category',
    name: 'Add Product',
    component: AddProduct
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
