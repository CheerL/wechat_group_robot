// import Vue from 'vue'
// import axios from 'axios'

// import App from './App'
// import router from './router'
// import store from './store'

// if (!process.env.IS_WEB) Vue.use(require('vue-electron'))
// Vue.http = Vue.prototype.$http = axios
// Vue.config.productionTip = false

// /* eslint-disable no-new */
// new Vue({
//   components: { App },
//   router,
//   store,
//   template: '<App/>'
// }).$mount('#app')

import Vue from 'vue'
import axios from 'axios'

import App from './App'
import router from './router'
import store from './store'
import "./theme/theme.less"

import { Row, Col } from 'iview/src/components/grid'
import Collapse from 'iview/src/components/collapse'
import Switch from 'iview/src/components/switch'
import { Select, Option } from 'iview/src/components/select'
import Icon from 'iview/src/components/icon'
import Input from 'iview/src/components/input'
import Menu from 'iview/src/components/menu'
import Button from 'iview/src/components/button'
import Spin from 'iview/src/components/spin'
import Avatar from 'iview/src/components/avatar'
import Card from 'iview/src/components/card'
import Tag from 'iview/src/components/tag'
import Badge from 'iview/src/components/badge'
import Modal from 'iview/src/components/modal'
const MenuItem = Menu.Item
const MenuGroup = Menu.Group
const ButtonGroup = Button.Group
const Panel = Collapse.Panel

if (!process.env.IS_WEB) Vue.use(require('vue-electron'))
Vue.http = Vue.prototype.$http = axios
Vue.config.productionTip = false
import iView from 'iview'
Vue.use(iView)

// const iView_list = [
//     Row,
//     Collapse,
//     Icon,
//     Menu,
//     Button,
//     ButtonGroup,
//     MenuGroup,
//     MenuItem,
//     Panel,
//     Spin,
//     Avatar,
//     Card,
//     Input,
//     Tag,
//     Badge,
//     Modal
// ]
// for (let each of iView_list) {
//     Vue.component(each.name, each)
// }
// Vue.component('i-switch', Switch)
// Vue.component('Col', Col)
// Vue.component('Option', Option)
// Vue.component('Select', Select)


/* eslint-disable no-new */
new Vue({
    components: { App },
    router,
    store,
    template: '<App/>'
}).$mount('#app')