<template>
	<el-row class="container">
		<el-col :span="24" class="header">
			<el-col :span="10" class="logo" :class="collapsed?'logo-collapse-width':'logo-width'">
				{{collapsed?'':sysName}}
			</el-col>
			<el-col :span="10">
<!--				<div class="tools" @click.prevent="collapse">-->
<!--					<i class="fa fa-align-justify"></i>-->
<!--				</div>-->
			</el-col>
			<el-col :span="4" class="userinfo">
				<el-dropdown trigger="hover">
					<span class="el-dropdown-link userinfo-inner"><img src="https://s1.ax1x.com/2018/02/08/93yKtU.jpg" /> {{sysUserName}}</span>
					<el-dropdown-menu slot="dropdown">
            <el-dropdown-item @click.native="settings">修改密码</el-dropdown-item>
						<el-dropdown-item divided @click.native="logout">退出登录</el-dropdown-item>
					</el-dropdown-menu>
				</el-dropdown>
			</el-col>
		</el-col>
		<el-col :span="24" class="main">
			<aside :class="collapsed?'menu-collapsed':'menu-expanded'">

        <!--导航菜单-->
				<el-menu :default-active="$route.path" class="el-menu-vertical-demo el-menu-expand" @open="handleopen" @close="handleclose" @select="handleselect"
					 unique-opened router v-if="!collapsed">
					<template v-for="(item,index) in $router.options.routes" v-if="!item.hiddenUser">
						<el-submenu :index="index+''" v-if="!item.leaf">
							<template slot="title"><i :class="item.iconCls"></i>{{item.name}}</template>
							<el-menu-item v-for="child in item.children" :index="child.path" :key="child.path" v-if="!child.hiddenUser">{{child.name}}</el-menu-item>
						</el-submenu>
						<el-menu-item v-if="item.leaf&&item.children.length>0" :index="item.children[0].path"><i :class="item.iconCls"></i>{{item.children[0].name}}</el-menu-item>
					</template>
				</el-menu>

        <!--导航菜单-折叠后-->
				<ul class="el-menu el-menu-vertical-demo collapsed" v-if="collapsed" ref="menuCollapsed">
					<li v-for="(item,index) in $router.options.routes" v-if="!item.hiddenUser" class="el-submenu item">
						<template v-if="!item.leaf">
							<div class="el-submenu__title" style="padding-left: 20px;" @mouseover="showMenu(index,true)" @mouseout="showMenu(index,false)"><i :class="item.iconCls"></i></div>
							<ul class="el-menu submenu" :class="'submenu-hook-'+index" @mouseover="showMenu(index,true)" @mouseout="showMenu(index,false)">
								<li v-for="child in item.children" v-if="!child.hiddenUser" :key="child.path" class="el-menu-item" style="padding-left: 40px;" :class="$route.path==child.path?'is-active':''" @click="$router.push(child.path)">{{child.name}}</li>
							</ul>
						</template>
						<template v-else>
							<li class="el-submenu">
								<div class="el-submenu__title el-menu-item" style="padding-left: 20px;height: 56px;line-height: 56px;padding: 0 20px;" :class="$route.path==item.children[0].path?'is-active':''" @click="$router.push(item.children[0].path)"><i :class="item.iconCls"></i></div>
							</li>
						</template>
					</li>
				</ul>
			</aside>

      <section class="content-container">
				<div class="grid-content bg-purple-light">
					<el-col :span="24" class="breadcrumb-container">
						<strong class="title">{{$route.name}}</strong>
						<el-breadcrumb separator="/" class="breadcrumb-inner">
							<el-breadcrumb-item v-for="item in $route.matched" :key="item.path">
								{{ item.name }}
							</el-breadcrumb-item>
						</el-breadcrumb>
					</el-col>
					<el-col :span="24" class="content-wrapper">
						<transition name="fade" mode="out-in">
							<router-view></router-view>
						</transition>
					</el-col>
				</div>
			</section>

    <!--修改密码界面-->
		<el-dialog title="修改密码" v-model="setpwdFormVisible" :close-on-click-modal="false">
			<el-form :model="setpwdForm" label-width="80px" :rules="setpwdFormRules" ref="setpwdForm">
				<el-row>
  						<el-form-item label="原密码" prop="oldpass">
							<el-input type = "password" v-model="setpwdForm.oldpass" auto-complete="off"></el-input>
						</el-form-item>
  						<el-form-item label="新密码" prop="newpass">
							<el-input type = "password" v-model="setpwdForm.newpass" auto-complete="off"></el-input>
						</el-form-item>
            <el-form-item label="确认密码" prop="confirpass">
							<el-input type = "password" v-model="setpwdForm.confirpass" auto-complete="off"></el-input>
						</el-form-item>
				</el-row>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click.native="setpwdFormVisible = false">取消</el-button>
        <el-button type="primary" @click.native="editSubmit" :loading="editLoading">提交</el-button>
			</div>
		</el-dialog>
		</el-col>
	</el-row>
</template>

<script>
import { setpwd } from "../api/api";
export default {
  data() {
    const validatePass = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入新密码"));
      } else if (value.length < 8) {
        callback(new Error("密码长度请大于8"));
      } else {
        if (this.setpwdForm.confirpass !== "") {
          this.$refs.setpwdForm.validateField("confirpass");
        }
        callback();
      }
    };
    const validatePass2 = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请再次输入新密码"));
      } else if (value !== this.setpwdForm.newpass) {
        callback(new Error("两次输入密码不一致!"));
      } else {
        callback();
      }
    };
    return {
      sysName: "论文管理系统",
      collapsed: false,
      sysUserName: "",
      form: {
        name: "",
        region: "",
        date1: "",
        date2: "",
        delivery: false,
        type: [],
        resource: "",
        desc: ""
      },

      setpwdFormVisible: false,
      editLoading: false,
      setpwdFormRules: {
        oldpass: [{ required: true, message: "请输入旧密码", trigger: "blur" }],
        newpass: [{ validator: validatePass, trigger: "blur" }],
        confirpass: [{ validator: validatePass2, trigger: "blur" }]
      },
      setpwdForm: {
        oldpass: "",
        newpass: "",
        confirpass: ""
      }
    };
  },
  methods: {
    onSubmit() {
      console.log("submit!");
    },
    handleopen() {
      //console.log('handleopen');
    },
    handleclose() {
      //console.log('handleclose');
    },
    handleselect: function(a, b) {},
    //退出登录
    logout: function() {
      var _this = this;
      this.$confirm("确认退出吗?", "提示", {
        //type: 'warning'
      })
        .then(() => {
          sessionStorage.removeItem("userToken");
          _this.$router.push("/user/login");
        })
        .catch(() => {});
    },
    //修改密码
    settings: function() {
      this.setpwdFormVisible = true;
    },
    editSubmit: function() {
      this.$refs.setpwdForm.validate(valid => {
        if (valid) {
          this.$confirm("确认修改吗？", "提示", {}).then(() => {
            this.editLoading = true;
            let para = Object.assign({}, this.setpwdForm);
            setpwd(para).then(res => {
              this.editLoading = false;
              let { code, msg } = res.data;
              if (code !== 200) {
                this.$message({
                  message: msg,
                  type: 'error'
                });
              } else {
                this.$message({
                  message: msg,
                  type: 'success'
                });
              }
              this.$refs["setpwdForm"].resetFields();
              this.setpwdFormVisible = false;
            });
          });
        }
      });
    },
    //折叠导航栏
    collapse: function() {
      this.collapsed = !this.collapsed;
    },
    showMenu(i, status) {
      this.$refs.menuCollapsed.getElementsByClassName(
        "submenu-hook-" + i
      )[0].style.display = status ? "block" : "none";
    }
  },
  mounted() {
    const token = sessionStorage.getItem("token");
    let user = sessionStorage.getItem("name");
    if (token && user) {
      user = JSON.parse(user);
      this.sysUserName = user || "";
    } else {
      sessionStorage.removeItem("token");
      this.$router.push("/user/login");
    }
  }
};
</script>

<style scoped lang="scss">
@import "~scss_vars";

.container {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 100%;
  .header {
    height: 60px;
    line-height: 60px;
    background: $color-primary;
    color: #fff;
    .userinfo {
      text-align: right;
      padding-right: 35px;
      float: right;
      .userinfo-inner {
        cursor: pointer;
        color: #fff;
        img {
          width: 40px;
          height: 40px;
          border-radius: 20px;
          margin: 10px 0px 10px 10px;
          float: right;
        }
      }
    }
    .logo {
      //width:230px;
      height: 60px;
      font-size: 22px;
      padding-left: 20px;
      padding-right: 20px;
      border-color: rgba(238, 241, 146, 0.3);
      border-right-width: 1px;
      border-right-style: solid;
      img {
        width: 40px;
        float: left;
        margin: 10px 10px 10px 18px;
      }
      .txt {
        color: #fff;
      }
    }
    .logo-width {
      width: 230px;
    }
    .logo-collapse-width {
      width: 60px;
    }
    .tools {
      padding: 0 23px;
      width: 14px;
      height: 60px;
      line-height: 60px;
      cursor: pointer;
    }
  }
  .main {
    display: flex;
    // background: #324057;
    position: absolute;
    top: 60px;
    bottom: 0;
    overflow: hidden;
    aside {
      flex: 0 0 230px;
      width: 230px;
      // position: absolute;
      // top: 0px;
      // bottom: 0px;
      .el-menu {
        height: 100%;
      }
      .collapsed {
        width: 60px;
        .item {
          position: relative;
        }
        .submenu {
          position: absolute;
          top: 0;
          left: 60px;
          z-index: 99999;
          height: auto;
          display: none;
        }
      }
    }
    .menu-collapsed {
      flex: 0 0 60px;
      width: 60px;
    }
    .menu-expanded {
      flex: 0 0 230px;
      width: 230px;
    }
    .el-menu-expand {
      width: 100% !important;
    }
    .el-menu-item {
      min-width: 60px;
      &.is-active {
        background-color: #cdc9c9 !important;
        border-right: 4px solid $color-primary;
        color: $color-primary;
      }
    }
    .content-container {
      flex: 1;
      overflow-y: scroll;
      padding: 20px;
      .breadcrumb-container {
        .title {
          width: 200px;
          float: left;
          color: #475669;
        }
        .breadcrumb-inner {
          float: right;
        }
      }
      .content-wrapper {
        background-color: #fff;
        box-sizing: border-box;
      }
    }
  }
}
</style>