<template>
	<section>
    <!--顶部搜索栏-->
		<el-col :span="24" style="padding-bottom: 0;display: flex;justify-content: center">
			<el-form :inline="true">
				<el-form-item>
					<el-input
              type="text"
              v-model="search.content"
              :placeholder="search.placeholder"
              style="width: 270px;"
              @keyup.enter.native="handleSearch"
              :disabled="search.searchDisable"
            >
             <i slot="prefix" class="el-input__icon el-icon-search" ></i>
          </el-input>
				</el-form-item>
				<el-form-item>
					<el-button type="primary" v-on:click="handleSearch" :disabled="search.searchDisable">查询</el-button>
          <el-button v-on:click="changeSearchMode" style="background-color: #ff6d6d;color: white">{{search.buttonContent}}</el-button>
				</el-form-item>
			</el-form>
		</el-col>
    <!--高级搜索-->
    <el-col :span="24" style="display: flex;justify-content: center;margin-bottom: 20px">
      <el-collapse v-model="activeNames" style="width: 68%;" @change="changeMore" accordion>
        <el-collapse-item title="高级搜索" name="1" style="font-size: 14px;">
          <RadioGroup v-model="mode" type="button" button-style="solid" style="margin-bottom: 10px">
              <Radio label="并模式"></Radio>
              <Radio label="或模式"></Radio>
          </RadioGroup>
          <div style="display: flex;align-items: center;margin-bottom: 10px">
            <p style="color: #395e46;margin-right: 10px;">论文标题</p>
            <el-input v-model="filters.title.content" style="width: 280px" size="small"></el-input>
            <p style="margin-left: 20px;color: #5e7382;margin-right: 5px">取反搜索</p>
            <el-checkbox v-model="filters.title.mode1"></el-checkbox>
            <p style="margin-left: 20px;color: #5e7382;margin-right: 5px">模糊搜索</p>
            <el-checkbox v-model="filters.title.mode2"></el-checkbox>
          </div>
          <div style="display: flex;align-items: center;margin-bottom: 10px">
            <p style="color: #395e46;margin-right: 10px;">论文作者</p>
            <el-input v-model="filters.author.content" style="width: 280px" size="small"></el-input>
            <p style="margin-left: 20px;color: #5e7382;margin-right: 5px">取反搜索</p>
            <el-checkbox v-model="filters.author.mode1"></el-checkbox>
            <p style="margin-left: 20px;color: #5e7382;margin-right: 5px">模糊搜索</p>
            <el-checkbox v-model="filters.author.mode2"></el-checkbox>
          </div>
          <div style="display: flex;align-items: center;margin-bottom: 10px">
            <p style="color: #395e46;margin-right: 10px">上传用户</p>
            <el-input v-model="filters.user.content" style="width: 280px" size="small"></el-input>
            <p style="margin-left: 20px;color: #5e7382;margin-right: 5px">取反搜索</p>
            <el-checkbox v-model="filters.user.mode1"></el-checkbox>
            <p style="margin-left: 20px;color: #5e7382;margin-right: 5px">模糊搜索</p>
            <el-checkbox v-model="filters.user.mode2"></el-checkbox>
          </div>
          <div style="display: flex;align-items: center;margin-bottom: 10px">
            <p style="color: #395e46;margin-right: 10px;">发布会议</p>
            <el-input v-model="filters.meeting.content" style="width: 280px" size="small"></el-input>
            <p style="margin-left: 20px;color: #5e7382;margin-right: 5px">取反搜索</p>
            <el-checkbox v-model="filters.meeting.mode1"></el-checkbox>
            <p style="margin-left: 20px;color: #5e7382;margin-right: 5px">模糊搜索</p>
            <el-checkbox v-model="filters.meeting.mode2"></el-checkbox>
          </div>
          <div style="display: flex;align-items: center;margin-bottom: 10px">
            <p style="color: #395e46;margin-right: 10px;">研究方向</p>
            <Cascader :data="domainOptions" trigger="hover" v-model="filters.domain.content" style="width: 280px"></Cascader>
            <p style="margin-left: 20px;color: #5e7382;margin-right: 5px">取反搜索</p>
            <el-checkbox v-model="filters.domain.mode1"></el-checkbox>
          </div>
          <div style="display: flex;align-items: center;margin-bottom: 10px">
            <p style="color: #395e46;margin-right: 10px;">论文类型</p>
            <Select v-model="filters.paper_type.content" style="width:280px">
              <Option v-for="item in paperTypeOptions" :value="item.value" :key="item.value">{{ item.label }}</Option>
            </Select>
            <p style="margin-left: 20px;color: #5e7382;margin-right: 5px">取反搜索</p>
            <el-checkbox v-model="filters.paper_type.mode1"></el-checkbox>
          </div>
          <div>
            <Button type="success" style="margin-right: 10px" @click="handleMoreSearch">提交搜索</Button>
            <Button @click="util1">取消</Button>
          </div>
        </el-collapse-item>
      </el-collapse>
    </el-col>
		<!--详情界面-->
    <el-col :span="24">
      <el-table :data="papers" highlight-current-row  @selection-change="selsChange" v-loading="listLoading" style="width: 100%;">
        <el-table-column prop="title" label="标题" width="" sortable>
        </el-table-column>
        <el-table-column prop="user" label="发布人" width="" sortable>
        </el-table-column>
        <el-table-column prop="authors" label="作者" width="" sortable>
        </el-table-column>
        <el-table-column prop="meeting" label="发布会议" width="" sortable>
        </el-table-column>
        <el-table-column prop="domains" label="研究方向" width="" sortable>
        </el-table-column>
        <el-table-column prop="type" label="论文类型" width="" sortable>
        </el-table-column>
        <el-table-column label="操作">
          <template scope="scope">
            <el-button size="small" type="success" @click="$router.push(`/user/paperDetails/${scope.row.id}`)">详情</el-button>
            <el-button size="small" type="primary" @click="handleDownload(scope.row.body_url)">下载</el-button>
          </template>
			  </el-table-column>
		</el-table>
    </el-col>
    <!--分页和批量下载-->
		<el-col :span="24" class="toolbar">
			<el-pagination layout="prev, pager, next" @current-change="changePage" :page-size="page_size" :total="total" style="float:right;">
			</el-pagination>
		</el-col>
	</section>
</template>

<script>
import {getPaperList, getPaperListByTitles, getFile, getDomainList} from "../../api/api";
export default {
  data() {
    return {
      mode: '并模式',
      filters: {
        title: {
          query: '',
          content: '',
          mode1: false,
          mode2: true,
        },
        author: {
          query: '',
          content: '',
          mode1: false,
          mode2: false,
        },
        user: {
          query: '',
          content: '',
          mode1: false,
          mode2: false,
        },
        meeting: {
          query: '',
          content: '',
          mode1: false,
          mode2: true,
        },
        abstract: {
          query: '',
          content: '',
          mode1: false,
          mode2: true,
        },
        paper_type: {
          query: '',
          content: '',
          mode1: false,
          mode2: false,
        },
        domain: {
          query: '',
          content: [],
          mode1: false,
          mode2: false
        }
      },
      search: {
        content: "",
        placeholder: "请输入论文标题查询",
        searchDisable: false,
        buttonContent: "复杂模式"
      },
      page_size: 20,
      total: 0,
      page: 1,
      listLoading: false,
      sels: [],
      select: '',
      activeNames: [],
      paperTypeOptions: [
        {
          'value': '理论证明型',
          'label': '理论证明型'
        //  ['理论证明型', '综述型', '实验型', '工具型', '数据集论文型']
        },
        {
          'value': '综述型',
          'label': '综述型'
        },
        {
          'value': '实验型',
          'label': '实验型'
        },
        {
          'value': '工具型',
          'label': '工具型'
        },
        {
          'value': '数据集论文型',
          'label': '数据集论文型'
        }
      ],
      domainOptions: [

      ],
      papers: []
    }
  },
  methods: {
    selsChange(sels) {
      this.sels = sels;
    },
    handleSearch:function() {
      this.clearFilter()
      if(this.search.buttonContent==='简单模式'){
        let param = {
          page: this.page,
          titles: this.search.content
        };
        this.listLoading = true
        getPaperListByTitles(param).then(res => {
          if (res.status === 200) {
            this.$Message.success(res.data.msg);
            this.total = res.data.total;
            this.page_size = res.data.page_size;
            this.papers = res.data.infos;
          } else {
            this.$Message.error(res.data.msg);
          }
          this.listLoading = false;
        })
      }
      else{
        this.filters.title.query = this.search.content + '|0|1'
        this.getPapers()
      }
    },
    handleDownload(paper_body_url){
      let url = {file_name: paper_body_url};
      if(paper_body_url){
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
    changeSearchMode(){
      this.search.searchDisable = false
      if(this.search.buttonContent === '复杂模式'){
        this.search.buttonContent = '简单模式'
        this.search.placeholder = '请输入多个论文名称以空格分隔'
      }
      else{
        this.util1()
      }
    },
    util1(){
      this.activeNames = []
      this.search.buttonContent = '复杂模式'
      this.search.placeholder = '请输入论文标题查询'
      this.search.searchDisable = false
    },
    changeMore(s){
      if(s==='1'){
        this.search.searchDisable = true
        this.search.buttonContent = '关闭高级搜索'
        this.search.placeholder = '处于高级搜索模式下，不可用'
      }
      else{
        this.search.searchDisable = false
        this.search.buttonContent = '复杂模式'
        this.search.placeholder = '请输入论文标题查询'
      }
    },
    getPapers(){
      let param = {
        page: this.page,
        condition_join: this.mode === '并模式' ? 'and' : 'or',
      };
      let key;
      for(key in this.filters){
        param[key] = this.filters[key].query
      }
      this.listLoading = true
      getPaperList(param).then(res => {
        if(res.status===200){
          this.total = res.data.total;
          this.page_size = res.data.page_size;
          this.papers = res.data.infos;
        }
        else{
          this.$Message.error(res.data.msg);
        }
        this.listLoading = false;
      })
    },
    clearFilter(){
      let key;
      for(key in this.filters){
        this.filters[key].query = ''
      }
    },
    handleMoreSearch(){
      this.clearFilter()
      let key;
      for(key in this.filters) {
        if(this.filters[key].content!=='') {
          if(key==='paper_type') {
            let values_ = ['理论证明型', '综述型', '实验型', '工具型', '数据集论文型']
            for (let i = 0; i < values_.length; i++) {
              if (values_[i] === this.filters[key].content) {
                this.filters[key].content = i + 1
                break
              }
            }
          }
          if(key!=='domain'){
            this.filters[key].query =
              this.filters[key].content +
              (this.filters[key].mode1 ? '|1' : '|0') +
              (this.filters[key].mode2 ? '|1' : '|0')
          }
          else if(key==='domain'&&this.filters[key].content.length!==0){
            this.filters[key].query =
              this.filters[key].content[this.filters[key].content.length-1] +
              (this.filters[key].mode1 ? '|1' : '|0') +
              (this.filters[key].mode2 ? '|1' : '|0')
          }
        }
      }
      this.getPapers()
      this.util1()
    },
    changePage(e){
      this.page = e
      this.getPapers()
    },
    getDomainOptions(){
      getDomainList({mode: 'user'}).then(res=>{
        this.domainOptions = res.data.tree
      })
    }
  },
  mounted() {
    this.getPapers()
    this.getDomainOptions()
  }
};
</script>

<style scoped>

</style>