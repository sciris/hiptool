// index.js -- vue-router path configuration code
//
// Last update: 2018-09-09

// Import main things
import Vue from 'vue'
import Router from 'vue-router'
import DashboardLayout from '@/app/DashboardLayout.vue'

// App views
import NotFound from '@/app/NotFoundPage.vue'
import ProjectsPage from '@/app/ProjectsPage'
import DiseaseBurdenPage from '@/app/DiseaseBurdenPage'
import InterventionsPage from '@/app/InterventionsPage'
import EquityPage from '@/app/EquityPage'
import FinancialRiskPage from '@/app/FinancialRiskPage'
import HealthPackagesPage from '@/app/HealthPackagesPage'
import LoginPage from '@/app/LoginPage'
import MainAdminPage from '@/app/MainAdminPage'
import RegisterPage from '@/app/RegisterPage'
import UserChangeInfoPage from '@/app/UserChangeInfoPage'
import ChangePasswordPage from '@/app/ChangePasswordPage'
import Help from '@/app/Help'
import Contact from '@/app/Contact'
import About from '@/app/About'


Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/register',
      name: 'Registration',
      component: RegisterPage
    },
    {
      path: '/login',
      name: 'Login',
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
          path: 'bod',
          name: 'Define burden of disease',
          component: DiseaseBurdenPage
        },
        {
          path: 'interventions',
          name: 'Define interventions',
          component: InterventionsPage
        },
        // {
        //   path: 'equity',
        //   name: 'Define equity',
        //   component: EquityPage
        // },
        // {
        //   path: 'financialrisk',
        //   name: 'Define financial risk protection',
        //   component: FinancialRiskPage
        // },
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
