<template>
	<section>
		<!--工具条-->
		<el-col :span="24" class="toolbar" style="padding-bottom: 0; background-color: light-grey;">
      <el-form>
			<el-form-item class="sub-header">已发布的论文</el-form-item>
      <el-form-item style="float:right;">按照时间顺序（最新）</el-form-item>
      </el-form>
		</el-col>

		<!--卡片-论文-->
		<el-card class="box-card" v-for="(item, index) in papers" :key="index">
      <div slot="header" class="clearfix">
        <span class="list_title">Title: {{item.paper_title}}</span>
        <el-button style="float: right; width:80px; padding: 3px 0" type="text" @click="$router.push(`/user/updatePaper/${item.paper_id}`)">修改论文</el-button>
        <el-button style="float: right; width:80px; padding: 3px 0" type="text" @click="$router.push(`/user/paperDetails/${item.paper_id}`)">论文详情</el-button>
        <el-button style="float: right; width:80px; padding: 3px 0" type="text" @click="handleDel(item.paper_id)">删除论文</el-button>
      </div>
      <div class="text item">
        <i class="el-icon-date"></i>
        &nbsp;{{item.paper_send_time }}
        <span style="margin-left:40px;">
          论文类型：{{item.paper_type}}
        </span>
      </div>
    </el-card>

		<!--工具条-->
		<el-col :span="24" class="toolbar">
			<el-button type="primary" @click="$router.push(`/user/publishPaper`)" style="font-size:16px;">发布新论文</el-button>
			<el-pagination layout="prev, pager, next" @current-change="handleCurrentChange" :page-size="page_size" :total="total" style="float:right;">
			</el-pagination>
		</el-col>

	</section>
</template>

<script>
import { getMyPaperList, updatePaper, deletePaper } from "../../api/api";

export default {
  data() {
    return {
      papers: [],
      page_size: 6,
      total: 0,
      total_page: 0,
      page: 1
    };
  },
  methods: {
    handleCurrentChange(val) {
      this.page = val;
      this.getMyPaper();
    },
    //获取论文列表
    getMyPaper() {
      let para = {
        page: this.page,

      };
      getMyPaperList(para).then(res => {
        this.total = res.data.total;
        this.total_page = res.data.total_page;
        this.page_size = res.data.page_size;
        this.papers = res.data.paperInfos;
      });
    },
    handleDel:function(paper_id){
      this.$confirm("确认删除该论文吗?", "提示", {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: "commit"
      }).then(()=>{
        let para = {paper_id: paper_id};
        deletePaper(para).then(res => {
          if(res.data.code === 200){
            this.$message({
              type:'success',
              message:'删除成功'
            })
            this.getMyPaper()
          } else {
            this.$message({
              type:'error',
              message: res.data.msg
            })
          }
        })
      })
    }
  },
  mounted() {
    this.getMyPaper();
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