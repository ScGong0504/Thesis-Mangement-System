<template>
	<section>
		<!--工具条-->
		<el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
			<el-form :inline="true" :model="father" :rules="rules2">
				<el-form-item>
					<el-input v-model="father.name" placeholder="输入新的根方向名称"></el-input>
				</el-form-item>
				<el-form-item>
					<el-button type="primary" @click="addFather">添加根方向</el-button>
				</el-form-item>
			</el-form>
		</el-col>

		<!--树结构-->
    <el-col>
		<el-tree
        ref="tree"
        node-key="label"
        :data="domains"
        :props="defaultProps"
        :expand-on-click-node="false"
        default-expand-all
        style="position: relative; top: 50%; "
        overflow:auto >
      <span slot-scope="{ node, data }">
        <span>{{ node.label }}</span>
        <span style="margin-left:60px;">
            <i class="el-icon-plus" @click="append(data)"></i>
            <el-button type="text" justify="end" size="small" @click="append(data)" >添加</el-button>
            <i class="el-icon-delete" @click="remove(node, data)"></i>
            <el-button type="text" justify="end" size="small" @click="remove(node, data)">删除</el-button>
            <i class="el-icon-edit" @click="handleEdit(node, data)"></i>
            <el-button type="text" justify="end" size="small" @click="handleEdit(node, data)">修改</el-button>
        </span>
      </span>
    </el-tree>
    </el-col>
	</section>
</template>

<script>
let id = 1000;
import util from "../../common/js/util";
import { getDomainList, deleteDomainList, addDomainList, updateDomain } from "../../api/api";

export default {
  data() {
    return {
      father:{
        name:""
      },
      domains: [],
      defaultProps: {
          children: 'children',
          label: 'label'
      }
    };
  },
  methods: {
    //获取研究方向列表
    getDomains(){
      //this.listLoading = true;
      //NProgress.start();
      getDomainList().then(res => {
        this.domains = res.data.tree;
        //this.listLoading = false;
      });
    },
    //添加根方向
    addFather:function(){
      let para = {
        domain_name: this.father.name,
        parent_domain: "grandfather"
      };
      //this.listLoading = true;
      const newFather = { label:this.father.name, children:[]};
      this.domains.push(newFather)
      //this.listLoading = false;
      addDomainList(para).then(res => {
        if(res.data.code==200){
          this.$message.success("添加成功");
          this.getDomains();
        } else {
              this.$message.error(res.data.msg);
            }
      })
    },
    //添加子方向
    append(data) {
      this.$prompt("研究方向名称","添加子方向",{
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputPattern: /^[\a-\z\A-\Z0-9\u4e00-\u9fe5]+$/,//允许输入英文/中文/数字
      }).then(({value})=>{
        const newChild = { label: value, children: [] };

        if (!data.children) {
          this.$set(data, 'children', []);
        }
        let para = {
          domain_name : value,
          parent_domain : data.label
        }
        //window.alert(data.label)
        addDomainList(para).then(res=>{
          if(res.data.code == 200){
            this.$message({
              type:'success',
              message:'添加成功'
            })
            this.getDomains()
          } else {
            this.$message({
              type:'error',
              message: res.data.msg
            })
          }
          data.children.push(newChild);
        })
      })
      },
    //删除
    remove(node, data) {
        let test = node.parent.label?node.parent.label:"grandfather";
        let para = {
          domain_name : node.label,
          parent_domain : test
        };

        this.$confirm("确认删除该方向吗?", "提示", {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: "commit"
        }).then(()=>{
          //window.alert(node.parent.label)
        deleteDomainList(para).then(res=>{
          if(res.data.code == 200){
            this.$message({
              type:'success',
              message:'删除成功'
            })
            this.getDomains()
          } else {
            this.$message({
              type:'error',
              message: res.data.msg
            })
          }
          const parent = node.parent;
          const children = parent.data.children || parent.data;
          const index = children.findIndex(d => d.label === data.label);
          children.splice(index, 1);
        })
        })
      },
    //修改研究方向
    handleEdit(node, data) {
      this.$prompt("请输入新的研究方向名称" ,"修改研究方向名称",{
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputPattern: /^[\a-\z\A-\Z0-9\u4e00-\u9fe5]+$/,//允许输入英文/中文/数字
      }).then(({value})=>{
        let para = {
          domain_name : node.label,
          new_name : value
        }
        //window.alert(data.label)
        updateDomain(para).then(res=>{
          if(res.data.code == 200){
            this.$message({
              type:'success',
              message:'修改成功'
            })
            this.getDomains()
          } else {
            this.$message({
              type:'error',
              message: res.data.msg
            })
          }
        })
      })
    },
  },
  mounted() {
    this.getDomains();
  }
};
</script>

<style >
.el-tree-node{
  position:relative;
  padding-left:16px;
}
.el-tree-node__children{
  padding-left:16px;
}
.el-tree-node:before {
     border-left: 1px dashed #1389BC;
     bottom: 0px;
     height: 100%;
     top: -26px;
     width: 1px;
}
.el-tree-node:after {
     border-top: 1px dashed #1389BC;
     height: 20px;
     top: 12px;
     width: 18px;
}
.el-tree .el-tree-node__expand-icon.expanded {
      -webkit-transform: rotate(0deg);
      transform: rotate(90deg);
}
.el-tree .el-icon-caret-right:before {
      content: "\e723";
      font-size: 16px;
      color: #1389BC;
      position: absolute;
      left: -20px;
      top: -8px;
}
.el-tree .el-tree-node__expand-icon.expanded.el-icon-caret-right:before{
      content: "\e723";
      font-size: 16px;
      color: #1389BC;
      position: absolute;
      left: -20px;
      top: -8px;
}
.el-tree-node__content>.el-tree-node__expand-icon {
     padding: 0;
}

</style>