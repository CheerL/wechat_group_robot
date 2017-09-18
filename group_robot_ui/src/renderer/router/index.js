import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  mode: 'hash',
  routes: [{
    path: '*',
    redirect: '/'
  },
  {
    path: '/',
    alias: '/login/',
    name: 'login',
    component: require('@/components/Login')
  },
  {
    path: '/info/',
    name: 'info',
    component: require('@/components/Info')
  },
  {
    path: '/group/',
    name: 'group',
    component: require('@/components/Group')
  },
  {
    path: '/test/',
    name: 'test',
    component: require('@/components/Test')
  }
  ]
})
