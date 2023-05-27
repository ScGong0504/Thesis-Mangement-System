import UserLogin from './views/UserLogin.vue'
import NotFound from './views/404.vue'
import UserHome from './views/UserHome.vue'
import UserRegister from "./views/UserRegister.vue";
import AdminLogin from "./views/AdminLogin";
import AdminHome from "./views/AdminHome";
import UserTable from "./views/nav1/UserTable";
import PaperTable from "./views/nav1/PaperTable";
import DomainTable from "./views/nav1/DomainTable";
import paperDetailTable from "./views/nav1/paperDetailTable";
import UserPaper from "./views/nav2/UserPaper";
import PublishPaper from "./views/nav2/PublishPaper";
import noteTable from "./views/nav1/NoteTable";
import echart from "./views/nav1/echart";
import adminEcharts from "./views/nav1/adminEcharts";
import PaperUpdate from "./views/nav2/PaperUpdate";
import AdminPaperTable from "./views/nav1/AdminPaperTable";


let routes = [
    {
        path: '/user/login',
        component: UserLogin,
        name: '',
        hiddenUser: true,
        hiddenAdmin: true
    },
    {
        path: '/user/register',
        component: UserRegister,
        name: '',
        hiddenUser: true,
        hiddenAdmin: true
    },
    {
        path: '/404',
        component: NotFound,
        name: '',
        hiddenUser: true,
        hiddenAdmin: true
    },
    {
        path: '/',
        component: UserHome,
        name: '论文管理系统',
        leaf: true,//只有一个节点
        iconCls: 'fa fa-id-card-o',//图标样式class
        children: [
            { path: '/user/paperTable', component: PaperTable, name: '论文汇总' },
        ],
        hiddenAdmin: true
    },
    {
      path: '/',
      component: UserHome,
      name: '论文管理系统',
      leaf: true,//只有一个节点
      iconCls: 'fa fa-id-card-o',//图标样式class
      children: [
          { path: '/user/myPaperTable', component: UserPaper, name: '我的论文' },
      ],
      hiddenAdmin: true
    },
    {
      path: '/',
      component: UserHome,
      name: '论文管理系统',
      leaf: true,//只有一个节点
      iconCls: 'fa fa-id-card-o',//图标样式class
      children: [
          { path: '/user/dataGraph', component: echart, name: '统计数据' },
      ],
      hiddenAdmin: true
    },
    {
      path: '/',
      component: UserHome,
      name: '论文管理系统',
      leaf: true,//只有一个节点
      iconCls: 'fa fa-id-card-o',//图标样式class
      children: [
          { path: '/user/paperDetails/:id', component: paperDetailTable, name: '论文详情'},
      ],
      hiddenAdmin: true,
      hiddenUser: true
    },
    {
      path: '/',
      component: UserHome,
      name: '论文管理系统',
      leaf: true,//只有一个节点
      iconCls: 'fa fa-id-card-o',//图标样式class
      children: [
          { path: '/user/paperNote/:id', component: noteTable, name: '论文笔记'},
      ],
      hiddenAdmin: true,
      hiddenUser: true
    },
    {
      path: '/',
      component: UserHome,
      name: '论文管理系统',
      leaf: true,//只有一个节点
      iconCls: 'fa fa-id-card-o',//图标样式class
      children: [
          { path: '/user/publishPaper', component: PublishPaper, name: '发布论文' },

      ],
      hiddenAdmin: true,
      hiddenUser: true
    },
    {
      path: '/',
      component: UserHome,
      name: '论文管理系统',
      leaf: true,//只有一个节点
      iconCls: 'fa fa-id-card-o',//图标样式class
      children: [

          { path: '/user/updatePaper/:id', component: PaperUpdate, name: '修改论文' }
      ],
      hiddenAdmin: true,
      hiddenUser: true
    },
    {
        path: '*',
        hidden: true,
        redirect: { path: '/404' },
        hiddenAdmin: true,
        hiddenUser: true
    },
    {
        path: '/admin/login',
        component: AdminLogin,
        name: 'AdminLogin',
        hiddenUser: true,
        hiddenAdmin: true
    },
    {
        path: '/',
        component: AdminHome,
        name: 'Table',
        leaf: true,
        iconCls: 'fa fa-id-card-o',
        hiddenUser: true,
        children: [
            { path: '/admin/usertable', component: UserTable, name: '用户管理' },
        ]
    },
    {
      path: '/',
      component: AdminHome,
      name: 'Table',
      leaf: true,
      iconCls: 'fa fa-id-card-o',
      hiddenUser: true,
      children: [
          { path: '/admin/papertable', component:AdminPaperTable, name: '论文管理' },
      ]
  },
  {
    path: '/',
    component: AdminHome,
    name: 'Table',
    leaf: true,
    iconCls: 'fa fa-id-card-o',
    hiddenUser: true,
    children: [
        { path: '/admin/domaintable', component: DomainTable, name: '研究方向管理' },
    ]
  },
  {
    path: '/',
    component: AdminHome,
    name: 'Table',
    leaf: true,
    iconCls: 'fa fa-id-card-o',
    hiddenUser: true,
    hiddenAdmin:true,
    children: [
        { path: '/user/paperDetails/:id', component: paperDetailTable, name: '论文详情' },
    ]
  },
  {
    path: '/',
    component: AdminHome,
    name: '论文管理系统',
    leaf: true,//只有一个节点
    iconCls: 'fa fa-id-card-o',//图标样式class
    children: [
        { path: '/admin/dataGraph/:id', component: adminEcharts, name: '统计数据' },
    ],
    hiddenUser: true,
    hiddenAdmin:true
  },
];

export default routes;