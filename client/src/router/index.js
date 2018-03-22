// index.js -- vue-router path configuration code
//
// Last update: 2/21/18 (gchadder3)

import Vue from 'vue'
import Router from 'vue-router'
import DashboardLayout from '../components/Dashboard/Layout/DashboardLayout.vue'
// GeneralViews
import NotFound from '../components/GeneralViews/NotFoundPage.vue'

// Admin pages
import Overview from 'src/components/Dashboard/Views/Overview.vue'
import UserProfile from 'src/components/Dashboard/Views/UserProfile.vue'
import Notifications from 'src/components/Dashboard/Views/Notifications.vue'
import Icons from 'src/components/Dashboard/Views/Icons.vue'
import Maps from 'src/components/Dashboard/Views/Maps.vue'
import Typography from 'src/components/Dashboard/Views/Typography.vue'
import TableList from 'src/components/Dashboard/Views/TableList.vue'
import ProjectsPage from 'src/components/Dashboard/Views/ProjectsPage'

// 
import DiseaseBurdenPage from 'src/components/Dashboard/Views/DiseaseBurdenPage'
import InterventionsPage from 'src/components/Dashboard/Views/InterventionsPage'
import HealthPackagesPage from 'src/components/Dashboard/Views/HealthPackagesPage'
import MyPage from 'src/components/Dashboard/Views/MyPage'
import LoginPage from 'src/components/Dashboard/Views/LoginPage'
import MainAdminPage from 'src/components/Dashboard/Views/MainAdminPage'
import RegisterPage from 'src/components/Dashboard/Views/RegisterPage'
import UserChangeInfoPage from 'src/components/Dashboard/Views/UserChangeInfoPage'
import ChangePasswordPage from 'src/components/Dashboard/Views/ChangePasswordPage'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      component: DashboardLayout,
      redirect: '/admin/overview'
    },
    {
      path: '/admin',
      component: DashboardLayout,
      redirect: '/admin/stats',
      children: [
        {
          path: '/',
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
          path: 'login',
          name: 'LoginPage',
          component: LoginPage
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
        {
          path: 'overview',
          name: 'overview',
          component: Overview
        },
        {
          path: 'stats',
          name: 'stats',
          component: UserProfile
        },
        {
          path: 'notifications',
          name: 'notifications',
          component: Notifications
        },
        {
          path: 'icons',
          name: 'icons',
          component: Icons
        },
        {
          path: 'maps',
          name: 'maps',
          component: Maps
        },
        {
          path: 'typography',
          name: 'typography',
          component: Typography
        },
        {
          path: 'table-list',
          name: 'table-list',
          component: TableList
        }
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
   var res= require('../components/Dashboard/Views/' + name + '.vue');
   return res;
};**/

// export default routes
