import Vue from 'vue'
import App from './App'
import ElementUI from 'element-ui'
import { Message } from 'element-ui'
import './assets/theme/theme-#006a63/index.css'
import VueRouter from 'vue-router'
import store from './vuex/store'
import Vuex from 'vuex'
import routes from './routes'
//import Mock from './mock'
//Mock.bootstrap();
import 'font-awesome/css/font-awesome.min.css'
import axios from 'axios';
import ViewUI from 'view-design';
import 'view-design/dist/styles/iview.css';

Vue.use(ElementUI)
Vue.use(VueRouter)
Vue.use(Vuex)
Vue.use(ViewUI)


// 测试
const router = new VueRouter({
  mode: 'history',
  routes: routes
})

// http request 拦截器
axios.interceptors.request.use(
  config => {
    let token = sessionStorage.getItem('token');
    if (token) {  // 判断是否存在token，如果存在的话，则每个http header都加上token
      token =sessionStorage.getItem('token')+':';
      config.headers.Authorization = `Basic ${new Buffer(token).toString('base64')}`;
    }
    return config;
  },
  error => {
    Message({
      message: "登录状态信息过期,请重新登录",
      type: "error"
    });
    router.push({
      path: "/login"
    });
  });

// http response 拦截器
axios.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    if (error.response) {
      switch (error.response.status) {
        case 401:
          // 返回401，清除token信息并跳转到登录页面
          localStorage.removeItem('token');
          router.push({
             path: "/user/login"
          });
          Message({
            message: '请检查登录',
            type: 'error'
          });
      }
    }
  });


// 路由拦截器
router.beforeEach((to, from, next) => {
  // 两种不同的Token——管理员、用户
  let adminToken = sessionStorage.getItem('adminToken');
  let userToken = sessionStorage.getItem('userToken');
  // 保持两种Token与唯一Token的对齐
  if (!userToken && to.path.substring(0, 5) === '/user'){
    sessionStorage.removeItem('token');
  }
  else if (!adminToken && to.path.substring(0, 6) === '/admin'){
    sessionStorage.removeItem('token');
  }
  // 若跳转到登录页面，则去除Token（不再处于登录状态）
  if (to.path === '/user/login' || to.path === '/admin/login') {
    sessionStorage.removeItem('adminToken');
    sessionStorage.removeItem('userToken');
    sessionStorage.removeItem('token');
  }
  // 对页面为/user开头的（用户页面）进行的路由保护
  if (to.path.substring(0, 5) === '/user'){
    if (!userToken && to.path !== '/user/login' && to.path !== '/user/register'){
      sessionStorage.removeItem('token')
      next({ path: '/user/login' })
    }
    // 路由保护白名单（确认的，不需要保护的路由）
    else {
      // 对于user页面保护中，user不同权限能看到的页面的限制
      if (to.path !== '/user/register'){
        sessionStorage.setItem('token', userToken)
      }
      next()
    }
  }
  // 对页面为/admin开头的（管理员页面）进行的路由保护
  else if (to.path.substring(0, 6) === '/admin'){
    if (!adminToken && to.path !== '/admin/login'){
      sessionStorage.removeItem('token')
      next({ path: '/admin/login' })
    }
    else {
      sessionStorage.setItem('token', adminToken)
      next()
    }
  }
  // 其他未知情况处理
  else {
    next()
  }
})

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

