<template>
  <el-form :model="ruleForm2" :rules="rules2" ref="ruleForm2" label-position="left" label-width="0px" class="demo-ruleForm login-container">
    <h3 class="title">论文管理系统（后台）登录</h3>
    <el-form-item prop="account">
      <el-input type="text" v-model="ruleForm2.account" auto-complete="off" placeholder="用户名"></el-input>
    </el-form-item>
    <el-form-item prop="checkPass">
      <el-input type="password" v-model="ruleForm2.checkPass" auto-complete="off" placeholder="密码"></el-input>
    </el-form-item>
    <el-checkbox v-model="checked" checked class="remember">记住密码</el-checkbox>
    <el-form-item style="width:100%;">
      <el-button type="primary" style="width:100%;" @click.native.prevent="handleSubmit2" :loading="logining">登录</el-button>
    </el-form-item>
    <p class="form-footer">By 数据库实践，第三小组</p>
  </el-form>
</template>

<script>
import {requestAdminLogin} from '../api/api';

export default {
    data() {
      return {
        logining: false,
        ruleForm2: {
          account: 'yz',
          checkPass: '123456'
        },
        rules2: {
          account: [
            { required: true, message: '请输入用户名', trigger: 'blur' },
          ],
          checkPass: [
            { required: true, message: '请输入密码', trigger: 'blur' },
          ]
        },
        checked: true
      };
    },
    mounted() {
      const token = sessionStorage.getItem('token');
      if (token) {
        sessionStorage.setItem('token', token);
        this.$router.push({ path: '/admin/userTable' });
      }
    },
    methods: {
      handleSubmit2() {
        this.$refs.ruleForm2.validate((valid) => {
          if (valid) {
            this.logining = true;
            const loginParams = {username: this.ruleForm2.account, password: this.ruleForm2.checkPass};
            requestAdminLogin(loginParams).then(data => {
              this.logining = false;
              let { code, token, name } = data;
              if (code !== 200) {
                window.alert('登录失败');
              } else {
                window.alert('登录成功');
                sessionStorage.setItem('adminToken', JSON.stringify(token));
                sessionStorage.setItem('name', JSON.stringify(name));
                this.$router.push({ path: '/admin/usertable' });
              }
            });
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      }
    }
  }

</script>

<style lang="scss" scoped>
  .login-container {
    -webkit-border-radius: 5px;
    border-radius: 5px;
    -moz-border-radius: 5px;
    background-clip: padding-box;
    margin: 180px auto;
    width: 420px;
    padding: 35px 35px 15px 35px;
    background: #fff;
    border: 1px solid #eaeaea;
    box-shadow: 0 0 25px #cac6c6;
    font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
    .title {
      margin: 0 auto 40px auto;
      text-align: center;
      color: #505458;
    }
    .form-footer{
      text-align: center;
      font-size: small;
      color: #505458;
    }
    .remember {
      margin: 0 0 15px 0;
    }
    .link{
      margin: 0 0 15px 0;
      font-size: small;
      color: #409EFF;
      text-decoration: none;
    }
    .form-options{
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
  }
</style>