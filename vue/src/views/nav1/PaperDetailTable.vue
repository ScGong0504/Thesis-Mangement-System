<template>
	<section>
  <div class="paper_container" >
	<div class="title">{{paperInfo.title}}</div>

  <p class="author"><span>作者：</span> {{paperInfo.author.join(' / ')}}</p>
  <p><span>摘要：</span>{{paperInfo.abstract}}</p>
  <p><span>类型：</span>{{paperInfo.paper_type}}</p>
  <p><span>研究方向：</span> {{paperInfo.paper_domain_name.join(', ')}}</p>
  <p>
    <span>发表日期：</span> {{paperInfo.paper_publish_time}}
    <span style="float:right; margin-right:30%;">
      <span>发布时间：</span><span class="p">{{paperInfo.paper_send_time}}</span>
    </span>
  </p>
  <p><span>发表的会议：</span>{{paperInfo.paper_meeting_name}}</p>
  <div style="text-align:center; margin-left:0px; height:50px;">
    <el-button type="primary" @click="handlePaper">查看论文</el-button>
    <el-button type="info" @click="handleNote">查看笔记</el-button>
  </div>
  <hr style="border:1px dashed #ccc;" />
  <div class="reference">
    <p><span>参考文献：</span></p>
    <p v-for="(item,index) in paperInfo.cited_paper" :key="index" style="margin-left:35px; ">
      <a @click="findRefer(item.paper_id)">
      [{{index+1}}]:&nbsp;{{item.title}}</a>
    </p>
  </div>
  </div>
  </section>
</template>

<script>
import { paperView, getFile } from "../../api/api";

export default {
  data() {
    return {
      paperInfo:{
        title:'',
        author:[],
        abstract:"",
        paper_type:"",
        paper_domain_name:[],
        paper_publish_time:"",
        paper_send_time:"",
        paper_meeting_name:"",
        paper_note_id: 0,
        paper_body_issue:"",
        cited_paper:[],
        paper_document:""
      }
    };
  },
  methods: {
    getPaperInfo(){
      let id = this.$route.params.id;
      let para = {paper_id : id};
      paperView(para).then(res => {
        this.paperInfo = res.data.paperInfos;
      })
    },
    findRefer:function(paper_id){
      this.$router.push({path:`/user/paperDetails/${paper_id}`})
      this.getPaperInfo();
    },
    handlePaper:function(){
      let url = {file_name: this.paperInfo.paper_body_url};
      if(this.paperInfo.paper_body_url){
        getFile(url).then((res)=>{
        const blob = new Blob([res.data], {'type': 'application/pdf'})
        const link = document.createElement('a')
        link.download = '正文文件'
        link.style.display = 'none'
        link.href = URL.createObjectURL(blob)
        document.body.appendChild(link)
        link.click()//执行下载
        URL.revokeObjectURL(link.href)//释放blob对象
        document.body.removeChild(link) //下载完成移除元素
      }).catch(function(error){
        console.log(error)
      })
      }
      else{
        window.alert('当前论文未上传正文文件')
      }
    },
    handleNote(){
      this.$router.push(`/user/paperNote/${this.$route.params.id}`)
    }
  },
  mounted() {
    this.getPaperInfo();
  }
};
</script>

<style scoped>
.paper_container{
    overflow: hidden;
    margin-top:10px;
    margin-left:20px;
    margin-right:20px;
    background-color: rgb(246, 250, 249);

}
.title{
  font-family:"宋体",sans-serif;
  font-size: 25px;
  font-weight:bold;
  line-height:2.5em;
  text-align: center;
  margin-top:10px;
}
.author{
  text-align: center;
}
.p{
  vertical-align: middle;
  font-family: "宋体",'Times New Roman', Times, serif;
  font-size: 15px;
  font-weight: lighter;
  margin-left:20px;
  margin-right:20px;
  line-height: 1.5em;
}
p{
  vertical-align: middle;
  font-family: "宋体",'Times New Roman', Times, serif;
  font-size: 15px;
  margin-left:20px;
  margin-right:20px;
  line-height: 1.5em;
}
span{
  font-family: "Microsoft Yahei", Helvetica, sans-serif;
  font-weight: bold;
}
.el-button{
  padding: 10px 15px;
  margin-left: 0px;
  margin-right: 20px;
  width: 130px;
  height: 40px;
  font-size: 15px;
}
.el-button--primary{
  background-color: #93cdb5;
  border-color: #93cdb5;
}
.el-button--primary:hover{
  background-color: #abe3cc;
  border-color: #abe3cc;
}
.el-button--info{
  background-color: #84bee0;
  border-color: #84bee0;
}
.el-button--info:hover{
  background-color: rgb(115,204,255);
  border-color: rgb(115,204,255);
}

.el-button--success{
  background-color: #13ce66;
  border-color: #13ce66;
}
.el-button--success:hover{
  background-color: rgb(66,216,133);
  border-color: rgb(66,216,133);
}
.el-button--danger{
  background-color: #ff4949;
  border-color: #ff4949;
}
.el-button--danger:hover{
  background-color: rgb(255,109,109);
  border-color: rgb(255,109,109);
}
.el-button--warning{
  background-color: #f7ba2a;
  border-color: #f7ba2a;
}
.el-button--warning:hover{
  background-color: rgb(249,200,85);
  border-color: rgb(249,200,85);
}
a:hover{
  text-decoration: underline;
  cursor: pointer;
  color: rgb(48, 115, 154);
}
</style>