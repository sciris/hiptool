// index.js -- vue-router path configuration code
//
// Last update: 2/21/18 (gchadder3)

import Vue from 'vue'
import Router from 'vue-router'
import DashboardLayout from '@/components/app/DashboardLayout.vue'
// GeneralViews
import NotFound from '@/components/generic/NotFoundPage.vue'

// Admin pages
import Overview from '@/components/app/Overview.vue'
import Notifications from '@/components/app/Notifications.vue'
import ProjectsPage from '@/components/app/ProjectsPage'
import DiseaseBurdenPage from '@/components/app/DiseaseBurdenPage'
import InterventionsPage from '@/components/app/InterventionsPage'
import HealthPackagesPage from '@/components/app/HealthPackagesPage'
import LoginPage from '@/components/app/LoginPage'
import MainAdminPage from '@/components/app/MainAdminPage'
import RegisterPage from '@/components/app/RegisterPage'
import UserChangeInfoPage from '@/components/app/UserChangeInfoPage'
import ChangePasswordPage from '@/components/app/ChangePasswordPage'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      component: DashboardLayout,
      redirect: '/admin/projects'
    },
    {
      path: '/login',
      name: 'LoginPage',
      component: LoginPage
    },
    {
      path: '/admin',
      component: DashboardLayout,
      redirect: '/admin/stats',
      children: [
        {
          path: 'projects',
          name: 'ProjectsPage',
          component: ProjectsPage
        },
        {
          path: 'bod',
          name: 'DiseaseBurdenPage',
          component: DiseaseBurdenPage
        },
        {
          path: 'interventions',
          name: 'InterventionsPage',
          component: InterventionsPage
        },
        {
          path: 'healthpackages',
          name: 'HealthPackagesPage',
          component: HealthPackagesPage
        },
        {
          path: 'mypage',
          name: 'MyPage',
          component: MyPage
        },
        {
          path: 'mainadmin',
          name: 'MainAdminPage',
          component: MainAdminPage
        },
        {
          path: 'register',
          name: 'RegisterPage',
          component: RegisterPage
        },
        {
          path: 'changeinfo',
          name: 'UserChangeInfoPage',
          component: UserChangeInfoPage
        },
        {
          path: 'changepassword',
          name: 'ChangePasswordPage',
          component: ChangePasswordPage
        },
    ]
  },
    { path: '*', component: NotFound }
  ]
})

/**
 * Asynchronously load view (Webpack Lazy loading compatible)
 * The specified component must be inside the Views folder
 * @param  {string} name  the filename (basename) of the view to load.
function view(name) {
   var res= require('../components/app/' + name + '.vue');
   return res;
};**/

// export default routes
