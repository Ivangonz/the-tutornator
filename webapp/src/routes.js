import Login from './components/public/Login.vue'
import Home from './components/secure/Home.vue'
import Profile from './components/secure/Profile.vue'
import Warning from './components/public/Warning.vue'

import Admin from './components/secure/Admin.vue'
import Member from './components/secure/Member.vue'
import Agent from './components/secure/Agent.vue'

import Users from './components/secure/admin/Users.vue'
import UserEditCreate from './components/secure/admin/UserEditCreate.vue'

import Roles from './components/secure/admin/Roles.vue'
import RoleEditCreate from './components/secure/admin/RoleEditCreate.vue'
import Calendar from "@/components/public/Calendar";
import AdminTools from "@/components/public/AdminTools";
import Tutors from "@/components/public/Tutors";
import ManageAccount from "@/components/public/ManageAccount";


export const routes = [
  {
    path: '/', component: Home, name: 'home', meta: {
      breadcrumb: [
        { name: 'Home' }
      ]
    }
  },
  { path: '/login', component: Login, name: 'login' },
  {
    path: '/profile', component: Profile, name: 'profile', meta: {
      breadcrumb: [
        { name: 'Home', link: '/' },
        { name: 'Profile' }
      ]
    }
  },

  {
    path: '/admin', component: Admin, name: 'admin', meta: {
      breadcrumb: [
        { name: 'Home', link: '/' },
        { name: 'Admin' }
      ],
      requiredRoles: ['admin']
    },
    redirect: {
      name: 'users'
    },
    children:[
      {
        path: 'users', component: Users, name: 'users', meta: {
          breadcrumb: [
            { name: 'Home', link: '/' },
            { name: 'Admin', link: '/admin' },
            { name: 'Users' }
          ],
          requiredRoles: ['admin']
        }
      },
      {
        path: 'users/edit/:id', component: UserEditCreate, name: 'usereditcreate', meta: { 
          breadcrumb: [
            { name: 'Home', link: '/' },
            { name: 'Admin', link: '/admin' },
            { name: 'Users', link: '/admin/users' },
            { name: 'Edit'},
          ],
          requiredRoles: ['admin']
        }
      },
      {
        path: 'roles', component: Roles, name: 'roles', meta: {
          breadcrumb: [
            { name: 'Home', link: '/' },
            { name: 'Admin', link: '/admin' },
            { name: 'Roles' }
          ],
          requiredRoles: ['admin']
        }
      },
      {
        path: 'roles/edit/:id', component: RoleEditCreate, name: 'roleeditcreate', meta: { 
          breadcrumb: [
            { name: 'Home', link: '/' },
            { name: 'Admin', link: '/admin' },
            { name: 'Roles', link: '/admin/roles' },
            { name: 'Edit'},
          ],
          requiredRoles: ['admin']
        }
      }


    ]

  },
  { path: '/calendar', component: Calendar, name: 'calendar'  },
  { path: '/adminTools', component: AdminTools, name: 'admintools'  },
  { path: '/tutors', component: Tutors, name: 'tutors'  },
  { path: '/manageAccount', component: ManageAccount, name: 'manageaccount'},
  { path: '/member', component: Member, name: 'member' },
  { path: '/agent', component: Agent, name: 'agent' },

  { path: '/unauthorized', component: Warning, name: 'warning' },

];


