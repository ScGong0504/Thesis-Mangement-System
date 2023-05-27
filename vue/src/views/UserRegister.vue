<template>
  <el-form :model="ruleForm2" :rules="rules2" ref="ruleForm2" label-position="left" label-width="0px" class="demo-ruleForm login-container">
    <h3 class="title">论文管理系统注册</h3>
    <el-form-item prop="account">
      <el-input type="text" v-model="ruleForm2.account" placeholder="用户名"></el-input>
    </el-form-item>
    <el-form-item prop="checkPass">
      <el-input type="password" v-model="ruleForm2.checkPass" auto-complete="off" placeholder="密码">
      </el-input>
    </el-form-item>
    <el-form-item prop="checkTwicePass">
      <el-input type="password" v-model="ruleForm2.checkTwicePass" auto-complete="off" placeholder="请重复输入密码" >
      </el-input>
    </el-form-item>
    <el-form-item prop="email">
      <el-row>
        <el-col :span="16" >
          <el-input type="text" v-model="ruleForm2.email" auto-complete="off" placeholder="邮箱地址" ></el-input>
        </el-col>
        <el-col :span="6" offset="1">
          <el-button type="primary" style="width: 100px" @click="getVerify" :disabled="!showVerifyCode">
            <span v-show="showVerifyCode">{{ verifyCodeButtonContent }}</span>
            <span v-show="!showVerifyCode">{{ wait_time }} s</span>
          </el-button>
        </el-col>
      </el-row>
    </el-form-item>
    <el-form-item prop="verifyCode">
      <el-input type="password" v-model="ruleForm2.verifyCode" auto-complete="off" placeholder="请输入您邮箱收到的验证码" >
      </el-input>
    </el-form-item>
    <el-form-item style="width:100%;">
      <el-button type="primary" style="width:100%;" @click.native.prevent="handleSubmit2" :loading="registering">注册</el-button>
    </el-form-item>
    <p class="form-footer">By 数据库实践，第三小组</p>
  </el-form>
</template>

<script>
import {requestRegister, nameNoRepeat, getVerifyCode} from '../api/api';
  export default {
    data() {
      const validateEmail = (rule, value, callback) => {
        if (!/^([a-zA-Z\d_-])+@([a-zA-Z\d_-])+((.[a-zA-Z\d_-]{2,3}){1,2})$/.test(value)) {
          callback(new Error('邮箱格式错误'))
        } else {
          callback()
        }
      };
      const twicePassSame = (rule, value, callback) => {
        if (value === '') {
          return callback(new Error('请输入密码'));
        } else if (value !== this.ruleForm2.checkPass) {
          return callback(new Error('您的两次密码输入不一致'));
        } else {
          return callback()
        }
      };
      const accountRule = (rule, value, callback) => {
        if (value === '') {
          return callback(new Error('请输入用户名'));
        }
        nameNoRepeat({username: value}).then(res => {
          if (res.data['code'] === 500){
            return callback(new Error('该用户名已存在'));
          }
          else{
            return callback();
          }
        })
      }
      return {
        verifyCodeButtonContent: '发送验证码',
        showVerifyCode: true,
        wait_time: 60,
        registering: false,
        ruleForm2: {
          account: '',
          checkPass: '',
          checkTwicePass: '',
          email: '',
          verifyCode: ''
        },
        rules2: {
          account: [
            {required: true, validator: accountRule, trigger: 'change'},
          ],
          checkPass: [
            {required: true, message: '请输入密码', trigger: 'change'},
          ],
          checkTwicePass: [
            {required: true, validator: twicePassSame, trigger: 'change'},
          ],
          email: [
            {required: true, validator: validateEmail, trigger: 'change'},
          ],
        }
      };
    },
    mounted() {
      const token = sessionStorage.getItem('token');
      if (token) {
        sessionStorage.setItem('token', token);
        this.$router.push({path: '/user/paperTable'});
      }
    },
    methods: {
      getVerify(){
        if (!/^([a-zA-Z\d_-])+@([a-zA-Z\d_-])+((.[a-zA-Z\d_-]{2,3}){1,2})$/.test(this.ruleForm2.email)){
          window.alert('您的邮箱有误，请重新输入')
          return
        }
        this.showVerifyCode = false
        this.wait_time = 60
        let clock = window.setInterval(() => {
          this.wait_time--
          if (this.wait_time < 0) {
            window.clearInterval(clock)
            this.wait_time = 60
            this.showVerifyCode = true
            this.verifyCodeButtonContent = '重新发送'
            }
        },1000);
        let param = {
          'email': this.ruleForm2.email
        }
        getVerifyCode(param).then(res => {
          if(res.status === 200){
            sessionStorage.setItem('verifyCode', res.data['verify_code'])
          }
          window.alert(res.data.msg)
        })
      },
      handleSubmit2() {
        this.$refs.ruleForm2.validate((valid) => {
          if (valid) {
            this.registering = true;
            const RegisterParams = {username: this.ruleForm2.account, password: this.ruleForm2.checkPass,
              twicePassword: this.ruleForm2.checkTwicePass, email: this.ruleForm2.email};
            if(this.ruleForm2.verifyCode !== sessionStorage.getItem('verifyCode')){
              window.alert('邮箱验证码错误，请重新输入')
              this.registering = false
              return
            }
            requestRegister(RegisterParams).then(res => {
              this.registering = false;
              let msg = res.data['msg'];
              let code = res.data['code'];
              window.alert(msg)
              this.$router.push({path: '/user/login'});
            });
          } else {
            window.alert('您的表单验证失败，请确认填写正确后重试')
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
    margin: 120px auto;
    width: 420px;
    padding: 35px 35px 15px 35px;
    background: #fff;
    border: 1px solid #eaeaea;
    box-shadow: 0 0 25px #cac6c6;
    .title {
      margin: 0 auto 40px auto;
      text-align: center;
      color: #505458;
    }
    .remember {
      margin: 0 0 35px 0;
    }
    .form-footer{
      text-align: center;
      font-size: small;
      color: #505458;
    }
  }
</style>