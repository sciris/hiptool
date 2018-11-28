import Vue from 'vue';
import Router from 'vue-router';
import DashboardLayout from './app/DashboardLayout.vue'
import ProjectsPage from './app/ProjectsPage.vue';
import AboutPage from './app/AboutPage.vue';
import HelpPage from './app/HelpPage.vue';
import ContactPage from './app/ContactPage.vue';
import NotFoundPage from './app/NotFoundPage.vue';
import { views } from 'sciris-uikit';

import HealthPackagesPage from './app/HealthPackagesPage.vue';
import InterventionsPage from './app/InterventionsPage.vue';
import DiseaseBurdenPage from './app/DiseaseBurdenPage.vue';

Vue.use(Router);

const appProps = {
  favicon: "static/favicon-96x96.png",
  logo: "static/img/healthpriorlogo-inverse.png",
  verboseToolName: "Health Services Prioritization Tool",
  authBackgroundColour: "#212120"
}

let router = new Router({
  routes: [
    {
      path: '/mainadmin',
      name: 'Admin',
      component: views.MainAdminPage,
    },
    {
      path: '/login',
      name: 'Login',
      component: views.LoginPage,
      props: appProps 
    },
    {
      path: '/register',
      name: 'Registration',
      component: views.RegisterPage,
      props: appProps 
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
        {
          path: 'healthpackages',
          name: 'Define health packages',
          component: HealthPackagesPage
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
          path: '/changepassword',
          name: 'Change password',
          component: views.ChangePasswordPage,
        }, {
          path: '/changeinfo',
          name: 'Edit account',
          component: views.UserChangeInfoPage,
        },
        {
          path: 'help',
          name: 'Help',
          component: HelpPage
        },
        {
          path: 'contact',
          name: 'Contact',
          component: ContactPage
        },
        {
          path: 'about',
          name: 'About',
          component: AboutPage
        },
      ] 
    },
    { path: '*', component: NotFoundPage }
  ]
});

export default router
