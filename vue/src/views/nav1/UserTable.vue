<template>
	<section>
		<!--工具条-->
		<el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
			<el-form :inline="true" :model="filters" :rules="rules2">
				<el-form-item>
					<el-input v-model="filters.name" placeholder="姓名/账号"></el-input>
				</el-form-item>
				<el-form-item>
					<el-button type="primary" v-on:click="getUsers">查询</el-button>
				</el-form-item>
			</el-form>
		</el-col>

		<!--列表-->
		<el-table :data="users"  highlight-current-row  @selection-change="selsChange" v-loading="listLoading" style="width: 100%;" >
			<el-table-column type="selection" width="65">
			</el-table-column>
			<el-table-column prop="id" label="账号" width="170" sortable>
			</el-table-column>
      <el-table-column prop="name" label="姓名" width="170" sortable>
			</el-table-column>
			<el-table-column prop="phone" label="电话" width="170" sortable>
			</el-table-column>
			<el-table-column prop="email" label="邮箱" width="190" sortable>
			</el-table-column>
			<el-table-column prop="role" label="权限" width="170">
        <template slot-scope="scope">
        <span>{{scope.row.role === 0 ? '普通用户' : '管理员'}}</span>
        </template>
			</el-table-column>
			<el-table-column label="操作" width="280">
				<template scope="scope">
					<el-button size="small" @click="$router.push(`/admin/dataGraph/${scope.row.id}`)">详情</el-button>
					<el-button type="danger" size="small" @click="handleDel(scope.$index, scope.row)">删除</el-button>
          <el-button type='primary' size="small" @click="handleUpdate(scope.$index, scope.row.id)">
            设为{{1 === users[scope.$index].role ? '普通用户' : '管理员'}}
          </el-button>
				</template>
			</el-table-column>
		</el-table>

		<!--工具条-->
		<el-col :span="24" class="toolbar">
			<el-button type="danger" @click="batchRemove" :disabled="this.sels.length===0">批量删除</el-button>
			<el-pagination layout="prev, pager, next" @current-change="handleCurrentChange" :page-size="page_size" :total="total" style="float:right;">
			</el-pagination>
		</el-col>

	</section>
</template>

<script>
import util from "../../common/js/util";
import { getUserList, removeUser, batchRemoveUser ,setUserPermit} from "../../api/api";

export default {
  data() {
    return {
      filters: {
        name: ""
      },
      users: [],
      page_size: 10,
      total: 0,
      page: 1,
      listLoading: false,
      sels: [], //列表选中列
    };
  },
  methods: {
    handleCurrentChange(val) {
      this.page = val;
      this.getUsers();
    },
    //获取用户列表
    getUsers() {
      let para = {
        page: this.page,
        name: this.filters.name
      };
      this.listLoading = true;
      //NProgress.start();
      getUserList(para).then(res => {
        this.total = res.data.total;
        this.page_size = res.data.page_size;
        this.users = res.data.infos;
        console.log(res)
        this.listLoading = false;
      });
    },
    //删除
    handleDel: function(index, row) {
      this.$confirm("确认删除该用户吗?", "提示", {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: "warning"
      })
        .then(() => {
          this.listLoading = true;
          //NProgress.start();
          removeUser({id: row.id}).then(res => {
            this.listLoading = false;
            if (res.data.code == 200) {
              this.$message.success("删除成功");
              this.getUsers();
            } else {
              this.$message.error(res.data.msg);
            }

          });
        })
        .catch(() => {
          this.$message({
            type:"info",
            message:"取消删除",
          })
        });
    },
    //修改用户权限
    handleUpdate: function(index, id){
      this.$confirm("确认修改该用户权限吗?","提示",{
        type:"commit"
      })
      .then(() => {
        this.listLoading = true;
        let para = { id : id };
        setUserPermit(para).then(res => {
            this.listLoading = false;
            if (res.data.code == 200) {
              this.$message.success("修改成功");
              this.getUsers();
            } else {
              this.$message.error(res.data.msg);
            }
          });
      })
      .catch(() => {
        this.$message({
            type:"info",
            message:"取消修改",
          })
      });
    },
    selsChange: function(sels) {
      this.sels = sels;
    },
    //批量删除
    batchRemove: function() {
      let ids = this.sels.map(item => item.id).toString();
      this.$confirm("确认删除选中用户吗？", "提示", {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: "warning"
      })
        .then(() => {
          this.listLoading = true;
          let para = { ids: ids };
          batchRemoveUser(para).then(res => {
            this.listLoading = false;
            if (res.data.code == 200) {
              this.$message.success("删除成功");
              this.getUsers();
            } else {
              this.$message.error(res.data.msg);
            }
          });
        })
        .catch(() => {
          this.$message({
            type:"info",
            message:"取消删除",
          })
        });
    }
  },
  mounted() {
    this.getUsers();
  }
};
</script>

<style scoped>

</style>