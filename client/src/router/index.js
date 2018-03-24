// index.js -- vue-router path configuration code
//
// Last update: 2/21/18 (gchadder3)

// Import main things
import Vue from 'vue'
import Router from 'vue-router'
import DashboardLayout from '@/components/app/DashboardLayout.vue'

// App views
import NotFound from '@/components/generic/NotFoundPage.vue'
import ProjectsPage from '@/components/app/ProjectsPage'
import DiseaseBurdenPage from '@/components/app/DiseaseBurdenPage'
import InterventionsPage from '@/components/app/InterventionsPage'
import HealthPackagesPage from '@/components/app/HealthPackagesPage'
import LoginPage from '@/components/app/LoginPage'
import MainAdminPage from '@/components/app/MainAdminPage'
import RegisterPage from '@/components/app/RegisterPage'
import UserChangeInfoPage from '@/components/app/UserChangeInfoPage'
import ChangePasswordPage from '@/components/app/ChangePasswordPage'
import Help from '@/components/app/Help'
import Contact from '@/components/app/Contact'
import About from '@/components/app/About'


Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/register',
      name: 'RegisterPage',
      component: RegisterPage
    },
    {
      path: '/login',
      name: 'LoginPage',
      component: LoginPage
    },
    {
      path: '/',
      component: DashboardLayout,
      redirect: '/projects',
      children: [
        {
          path: 'projects',
          name: 'Manage projects',
          component: ProjectsPage
        },
        {
          path: 'projects',
          name: 'Manage projects',
          component: ProjectsPage
        },
        {
          path: 'bod',
          name: 'Disease burden',
          component: DiseaseBurdenPage
        },
        {
          path: 'interventions',
          name: 'Interventions',
          component: InterventionsPage
        },
        {
          path: 'healthpackages',
          name: 'Define health packages',
          component: HealthPackagesPage
        },
        {
          path: 'mainadmin',
          name: 'Admin',
          component: MainAdminPage
        },
        {
          path: 'changeinfo',
          name: 'Edit account',
          component: UserChangeInfoPage
        },
        {
          path: 'changepassword',
          name: 'Change password',
          component: ChangePasswordPage
        },
        {
          path: 'help',
          name: 'Help',
          component: Help
        },
        {
          path: 'contact',
          name: 'Contact',
          component: Contact
        },
        {
          path: 'about',
          name: 'About',
          component: About
        },
      ]
    },
    { path: '*', component: NotFound }
  ]
})
