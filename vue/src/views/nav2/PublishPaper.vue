<template>
	<section>
		<!--工具条-->
		<el-col :span="24" class="toolbar" style="padding-bottom: 0px; background-color: light-grey;">
      <el-form>
			<el-form-item class="sub-header">发布新的论文</el-form-item>
      </el-form>
		</el-col>

		<!--表单-->
		<el-form ref="form" :model="form" label-width="106px" >
      <el-form-item label="论文标题" required>
        <el-input v-model="form.title" ></el-input>
      </el-form-item>
      <el-row>
        <el-col :span="11">
        <el-form-item label="第一作者" required>
          <el-input v-model="form.paper_first_author"></el-input>
        </el-form-item>
        </el-col>
        <el-col :span="11" style="float:right;">
        <el-form-item label="第一作者邮箱">
          <el-input v-model="form.first_author_email"></el-input>
        </el-form-item>
        </el-col>
      </el-row>
      <el-row>
      <el-col :span="11">
      <el-form-item label="第二作者">
        <el-input v-model="form.paper_second_author"></el-input>
      </el-form-item>
      </el-col>
      <el-col :span="11" style="float:right;">
      <el-form-item label="第二作者邮箱" >
        <el-input v-model="form.second_author_email"></el-input>
      </el-form-item>
      </el-col>
      </el-row>
      <el-row>
      <el-col :span="11">
      <el-form-item label="第三作者">
        <el-input v-model="form.paper_third_author"></el-input>
      </el-form-item>
      </el-col>
      <el-col :span="11" style="float:right;">
      <el-form-item label="第三作者邮箱" >
        <el-input v-model="form.third_author_email"></el-input>
      </el-form-item>
      </el-col>
      </el-row>
      <el-form-item label="摘要">
        <el-input type="textarea" v-model="form.abstract"></el-input>
      </el-form-item>
      <el-form-item label="论文类型" required>
        <el-select v-model="form.paper_type" placeholder="请选择论文类型" :clearable="true">
          <el-option label="理论证明型" value="1"></el-option>
          <el-option label="综述型" value="2"></el-option>
          <el-option label="实验型" value="3"></el-option>
          <el-option label="工具型" value="4"></el-option>
          <el-option label="数据集型" value="5"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="研究方向" required>
      <el-cascader ref="domain" v-model="form.domain_name" :options="domains" :show-all-levels="false" :clearable="true" props. checkStrictly="true" :popper-append-to-body="false" value-key="label" :emitPath="false" @change="handleDomainChange"></el-cascader>
      </el-form-item>
      <el-form-item label="相关会议">
        <el-input v-model="form.meeting"></el-input>
      </el-form-item>
      <el-form-item label="引用文献">

        <el-col :span="18" v-for="(item, index) in counter" :key="index">
          <el-input v-model="form.cited_paper[index]"></el-input>
          <el-button icon="el-icon-minus" @click="deleteRow(index)"></el-button>
        </el-col>
        <el-col :span="2">
          <el-button icon="el-icon-plus" @click="addRow"></el-button>
        </el-col>
      </el-form-item>
      <el-form-item label="发表日期">
        <el-col :span="11">
          <el-date-picker type="datetime" placeholder="选择日期"  v-model="form.date1" style="width: 100%;"></el-date-picker>
        </el-col>

      </el-form-item>
      <el-form-item label="上传正文文件" required>
        <el-upload
            class="upload-demo"
            ref="upload"
            action=""
            :limit="1"
            :file-list="fileList"
            accept=".pdf,.doc,.docx"
            :auto-upload="false"
            :on-exceed="handleExceed"
            :on-preview="handlePreview"
            :on-change="handleChange1"
            :on-remove="handleRemove2"
            >
            <el-button slot="trigger" size="medium" type="primary">选取文件</el-button>
          </el-upload>
      </el-form-item>

      <el-col class="toolbar">
      <el-form-item style="text-align:center;">
        <el-button type="primary" @click="onSubmit">发布论文</el-button>
        <el-button type="info" @click="Cancel">取消</el-button>
      </el-form-item>
      </el-col>
    </el-form>
	</section>
</template>

<script>
import { publishPaper,getDomainList,uploadFile} from "../../api/api";

export default {
  data() {
    return {
      counter:[],
      domains:[],
      //listLoading: false,
      //sels: [], //列表选中列
      fileList: [],
      extraFileList:[],
      //user_id: 21,
      form: {
          title: '',
          paper_first_author:'',
          first_author_email:'',
          paper_second_author:'',
          second_author_email:'',
          paper_third_author:'',
          third_author_email:'',
          abstract:'',
          paper_type: '',
          domain_name:'',
          meeting:'',
          cited_paper:[],
          date1: '',
          note:'',
        },
      paper_file: null,
      paper_file_name:'',
      body_url:'',
      extra_file: null,
      extra_file_name:'',
      extra_file_url:'',
    };
  },
  methods: {
    Cancel:function(){
      this.$router.go(-1);
    },
    //动态表单
    addRow(){
      this.counter.push('');

    },
    deleteRow(index){
      if(index !== -1){
        this.form.cited_paper.splice(index,1);
        this.counter.splice(index,1);
      }
    },
    //获取级联选择器的domain数据
    getDomains(){
      getDomainList().then(res => {
        this.domains = this.getTreeDomain(res.data.tree);
      });
    },
    //递归解决空级联造成的bug
    getTreeDomain(data){
      //循环遍历Json数据
      for(var i=0;i<data.length;i++){
        data[i].value = data[i].label;
        if(data[i].children.length<1){
          //children若为空数组 则将children设为undefined
          data[i].children = undefined;

        } else {
          this.getTreeDomain(data[i].children);
        }
      }
      return data;
    },
    handleDomainChange:function(){
      const node = this.$refs['domain'].getCheckedNodes();
      this.form.domain_name=node[0].data.label;
      //window.alert(this.form.domain_name);
    },
    handleCurrentChange(val) {
      this.page = val;
      this.getMyPaper();
    },
    //获取用户列表
    getMyPaper() {
      //let user_id = id;
      let para = {
        page: this.page,

      };
      //this.listLoading = true;
      //NProgress.start();
      getMyPaperList(para).then(res => {
        this.total = res.data.total;
        this.total_page = res.data.total_page;
        this.page_size = res.data.page_size;
        this.papers = res.data.paperInfos;
       // this.listLoading = false;
      });
    },

    // 超过文件上传最大个数
    handleExceed (files, fileList) {
      this.$message.warning('很抱歉当前支持最大上传文件个数为 1 个！')
    },
    //处理提交
    onSubmit:function(){
      let param = new FormData(); //创建form对象
      let file = this.paper_file;
      let file_name = this.paper_file_name;
      param.append('only_one_file', file);
      param.append('file_name', file_name)

      uploadFile(param).then(res => {
        //window.alert(res.data.file_url);
        this.body_url = res.data.file_url;
        //window.alert(this.body_url)

      //提交附加文件
      if(this.extra_file){
      let param2 = new FormData(); //创建form对象
      let file2 = this.extra_file;
      let file2_name = this.extra_file_name;
      param2.append('only_one_file', file2);
      param2.append('file_name', file2_name)

      uploadFile(param2).then(res => {
        console.log(res.data.file_url);
        this.extra_file_url = res.data.file_url;

      //window.alert(this.body_url)
      //window.alert(this.extra_file_url)
      var time = new Date()
      let send_time = time.toLocaleDateString(); //获取当前日期
      let para = {

        paper_title: this.form.title,
        paper_first_author: this.form.paper_first_author,
        first_author_email: this.form.first_author_email,
        paper_second_author: this.form.paper_second_author,
        second_author_email: this.form.second_author_email,
        paper_third_author: this.form.paper_third_author,
        third_author_email: this.form.third_author_email,
        paper_abstract: this.form.abstract,
        paper_type: this.form.paper_type,
        paper_publish_time: this.form.date1,
        paper_send_time: send_time,
        meeting: this.form.meeting,
        cited_paper: JSON.stringify(this.form.cited_paper),
        body_url: this.body_url,
        note: this.form.note,
        domain_name: this.form.domain_name,
        document_url: this.extra_file_url
      };
      publishPaper(para).then(res => {
        if(res.data.code == 200){
          this.$message.success("发布成功");
          this.$router.go(-1);
        } else {
          this.$message.error(res.data.msg);
        }
      })
      })}
      else{
      this.extra_file_url = '';
        //window.alert(this.body_url)
      //window.alert(this.extra_file_url)
      var time = new Date()
      let send_time = time.toLocaleDateString(); //获取当前日期
      let para = {

        paper_title: this.form.title,
        paper_first_author: this.form.paper_first_author,
        first_author_email: this.form.first_author_email,
        paper_second_author: this.form.paper_second_author,
        second_author_email: this.form.second_author_email,
        paper_third_author: this.form.paper_third_author,
        third_author_email: this.form.third_author_email,
        paper_abstract: this.form.abstract,
        paper_type: this.form.paper_type,
        paper_publish_time: this.form.date1,
        paper_send_time: send_time,
        meeting: this.form.meeting,
        cited_paper: JSON.stringify(this.form.cited_paper),
        body_url: this.body_url,
        note: this.form.note,
        domain_name: this.form.domain_name,
        document_url: this.extra_file_url
      };
      publishPaper(para).then(res => {
        if(res.data.code == 200){
          this.$message.success("发布成功");
          this.$router.go(-1);
        } else {
          this.$message.error(res.data.msg);
        }
      })
      }
      })
    },
    // 文件状态改变
    handleChange1 (file, fileList) {
      if (file) {
        const extension = file.name.substring(file.name.lastIndexOf('.') + 1)
        const size = file.size / 1024 / 1024
        if (extension !== 'doc' && extension !=='pdf' && extension !=='docx') { // 校验文件格式
          this.$message.warning('只支持上传后缀名为.doc或.docx或.pdf的文件')
         }
        if (size > 20) { // 校验文件大小
          this.$message.warning('文件大小不能超过20MB')
        }

        this.paper_file = file.raw;
        this.paper_file_name = file.name;

      }
    },
    handleChange2 (file, extraFileList) {
      if (file) {
        const extension = file.name.substring(file.name.lastIndexOf('.') + 1)
        const size = file.size / 1024 / 1024
        if (extension !=='pdf') { // 校验文件格式
          this.$message.warning('只支持上传后缀名为.doc或.docx或.pdf的文件')
         }
        if (size > 20) { // 校验文件大小
          this.$message.warning('文件大小不能超过20MB')
        }

        this.extra_file = file.raw;
        this.extra_file_name = file.name;
      }
    },
    // 文件删除时
    handleRemove1 (file, fileList) {
      console.log(file, fileList)
      this.fileList = [] // 文件列表置空
    },
    handleRemove2 (file, extraFileList) {
      this.extraFileList = [] // 文件列表置空
    },
    // 点击文件列表中已上传的文件时的钩子
    handlePreview (file) {
      console.log(file)
    },
  },
  mounted() {
    this.getDomains();
  }
};
</script>

<style scoped>
.sub-header{
  float:left;
  font-family: "Microsoft Yahei";
  font-weight: bold;
  font-size: 20px;
}
.text {
    font-size: 13px;
    font-family: "Hiragino Sans GB";
}
.item {
    margin-bottom: 3px;
}
.clearfix:before,
.clearfix:after {
    display: table;
    content: "";
}
.clearfix:after {
    clear: both
}
.box-card{
  margin-top:10px;
  background-color: rgb(246, 248, 248);
}
.list_title{
  font-family: "Hiragino Sans GB";
  font-size:16px;
}




</style>