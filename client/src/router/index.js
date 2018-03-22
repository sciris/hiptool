// index.js -- vue-router path configuration code
//
// Last update: 2/21/18 (gchadder3)

import Vue from 'vue'
import Router from 'vue-router'
import DashboardLayout from '@/components/Dashboard/Layout/DashboardLayout.vue'
// GeneralViews
import NotFound from '@/components/GeneralViews/NotFoundPage.vue'

// Admin pages
import Overview from '@/components/Dashboard/Views/Overview.vue'
import UserProfile from '@/components/Dashboard/Views/UserProfile.vue'
import Notifications from '@/components/Dashboard/Views/Notifications.vue'
import Icons from '@/components/Dashboard/Views/Icons.vue'
import Maps from '@/components/Dashboard/Views/Maps.vue'
import Typography from '@/components/Dashboard/Views/Typography.vue'
import TableList from '@/components/Dashboard/Views/TableList.vue'
import ProjectsPage from '@/components/Dashboard/Views/ProjectsPage'

// 
import DiseaseBurdenPage from '@/components/Dashboard/Views/DiseaseBurdenPage'
import InterventionsPage from '@/components/Dashboard/Views/InterventionsPage'
import HealthPackagesPage from '@/components/Dashboard/Views/HealthPackagesPage'
import MyPage from '@/components/Dashboard/Views/MyPage'
import LoginPage from '@/components/Dashboard/Views/LoginPage'
import MainAdminPage from '@/components/Dashboard/Views/MainAdminPage'
import RegisterPage from '@/components/Dashboard/Views/RegisterPage'
import UserChangeInfoPage from '@/components/Dashboard/Views/UserChangeInfoPage'
import ChangePasswordPage from '@/components/Dashboard/Views/ChangePasswordPage'

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
