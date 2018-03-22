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
import ProjectsPage from '@/components/ProjectsPage'
import DiseaseBurdenPage from '@/components/DiseaseBurdenPage'
import InterventionsPage from '@/components/InterventionsPage'
import HealthPackagesPage from '@/components/HealthPackagesPage'
import MyPage from '@/components/MyPage'
import LoginPage from '@/components/LoginPage'
import MainAdminPage from '@/components/MainAdminPage'
import RegisterPage from '@/components/RegisterPage'
import UserChangeInfoPage from '@/components/UserChangeInfoPage'
import ChangePasswordPage from '@/components/ChangePasswordPage'

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
          path: '/bod',
          name: 'DiseaseBurdenPage',
          component: DiseaseBurdenPage
        },
        {
          path: '/interventions',
          name: 'InterventionsPage',
          component: InterventionsPage
        },
        {
          path: '/healthpackages',
          name: 'HealthPackagesPage',
          component: HealthPackagesPage
        },
        {
          path: '/mypage',
          name: 'MyPage',
          component: MyPage
        },
        {
          path: '/login',
          name: 'LoginPage',
          component: LoginPage
        },
        {
          path: '/mainadmin',
          name: 'MainAdminPage',
          component: MainAdminPage
        },
        {
          path: '/register',
          name: 'RegisterPage',
          component: RegisterPage
        },
        {
          path: '/changeinfo',
          name: 'UserChangeInfoPage',
          component: UserChangeInfoPage
        },
        {
          path: '/changepassword',
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
