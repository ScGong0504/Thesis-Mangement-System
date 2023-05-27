<template>
	<section>
		<el-col :span="24" style="padding-bottom: 0;display: flex;justify-content: center">
			<Card v-for="note in notes" style="width:350px;height: 350px;margin: 30px">
        <p slot="title" style="font-family: 田氏颜体大字库">
          {{ note.note_title }}
        </p>
        <div slot="extra" style="display: flex;">
          <a style="font-family: 田氏颜体大字库; margin-right: 10px" @click.stop="deleteNote_(note.note_id)" v-if="iCanAdd && note.note_content!=='该笔记已删除'">删除</a>
          <a style="font-family: 田氏颜体大字库" @click.stop="openComment(note.note_id)">评论区</a>
        </div>
        <p style="font-family: fangsong;font-size:16px" :style="note.note_content==='该笔记已删除' ? 'text-decoration:line-through;' : ''">
          {{ note.note_content }}
        </p>
      </Card>
		</el-col>
    <!--分页-->
		<el-col :span="24" class="toolbar" style="margin-top: 50px">
      <el-button @click="modal2=true" type="primary" :disabled="!iCanAdd">新增笔记</el-button>
			<el-pagination layout="prev, pager, next" @current-change="changePage" :page-size="page_size" :total="total" style="float:right;">
			</el-pagination>
		</el-col>
    <!--评论-->
    <Modal
        v-model="modal1"
        title="评论区"
        :styles="{width: '700px'}"
    >
      <template v-if="comments.length===0">
        <div style="display: flex;justify-content: center;flex-direction: column;align-items: center">
          <el-empty description=" " v-if="comments.length===0" style="width: 200px;height: 200px;padding: 30px;"></el-empty>
          <p>暂时没有评论噢！</p>
        </div>
      </template>
      <template v-else>
        <Scroll>
          <template v-for="comment in comments">
            <Card style="margin: 10px;">
              <!--评论-->
              <p>
                <strong>{{ comment.comment_username }}</strong>
                <strong style="color: #5e7382">{{ comment.comment_time }}</strong>
              </p>
              <p style="padding-top: 10px;font-family: 宋体;" :style="comment.comment_content==='该评论已删除' ? 'text-decoration:line-through;' : ''">{{comment.comment_content}}</p>
              <!--评论操作栏-->
              <div style="display: flex;padding-top: 10px;padding-bottom: 10px">
                <a style="padding-right: 10px;font-family: 宋体" @click="openCommentInput(comment.comment_id)">回复</a>
                <a style="padding-right: 10px;font-family: 宋体" @click="deleteComment_(comment.comment_id)">删除</a>
                <a style="padding-right: 10px;font-family: 宋体" @click="reply_show===0 ? reply_show=comment.comment_id :reply_show=0" v-if="comment.replys.length!=0">展开/收起回复</a>
              </div>
              <!--对于评论的回复-->
              <div style="display: flex;margin-bottom: 10px" v-if="commentInputVisable && commentInputIndex === comment.comment_id">
                <Input style="margin-right: 10px" v-model="commentInputContent" autofocus></Input>
                <Button type="success" :loading="modal_loading" @click="submitReply(comment.comment_id, '', commentInputContent)" :disabled="!Boolean(commentInputContent.length)">回复</Button>
               </div>
              <!--回复-->
              <div style="padding: 10px;background-color: #eaeaea;width: 95%;margin-left: 5%;" v-if="reply_show===comment.comment_id" v-for="reply in comment.replys">
               <p>
                 <strong> {{reply.username2}} </strong>
                 <strong> {{reply.username1 !== '' ? '回复了' + reply.username1 : ''}}</strong>
                 <strong style="color: #5e7382">{{reply.reply_time}}</strong>
               </p>
               <p style="padding-top: 10px;font-family: 宋体;" :style="reply.reply_content==='该回复已删除'?'text-decoration:line-through;':''">{{reply.reply_content}}</p>
               <div style="display: flex;padding-top: 10px">
                 <a style="padding-right: 10px;font-family: 宋体" @click.stop="openReplyInput(reply.reply_id)">回复</a>
                 <a style="padding-right: 10px;font-family: 宋体" v-if="reply.del_ok" @click="deleteReply_(reply.reply_id)">删除</a>
               </div>
               <div style="display: flex" v-if="replyInputVisable && replyInputIndex===reply.reply_id">
                <Input style="margin-right: 10px" v-model="replyInputContent" autofocus></Input>
                <Button type="success" :loading="modal_loading" @click="submitReply(comment.comment_id, reply.reply_id, replyInputContent)" :disabled="!Boolean(replyInputContent.length)">回复</Button>
               </div>
              </div>
            </Card>
          </template>
        </Scroll>
        <el-pagination layout="prev, pager, next" @current-change="changePageComment" :page-size="commentPageSize" :total="commentTotal">
        </el-pagination>
      </template>
      <div slot="footer" style="display: flex">
          <Input style="margin-right: 20px" v-model="commentValue" placeholder="请输入您的评论"></Input>
          <Button type="success" :loading="modal_loading"  @click="submitComment()" :disabled="!Boolean(commentValue.length)">评论</Button>
      </div>
    </Modal>
    <!--新增笔记-->
    <Modal
        v-model="modal2"
        title="新增笔记"
        @on-ok="submitNote"
    >
      <Input v-model="newNoteTitle" maxlength="12" show-word-limit placeholder="请输入笔记标题"></Input>
      <Input v-model="newNoteContent" maxlength="200" show-word-limit type="textarea"
             placeholder="笔记内容（字数上限为200字）" style="margin-top: 20px;" />
    </Modal>
	</section>
</template>

<script>
import {getNoteList, addNote, canIAddNote, getCommentList, addReply, addComment, deleteReply, deleteComment, deleteNote} from "../../api/api";
export default {
  data() {
    return {
      paper_id: 49, // 当前页面设置

      modal1: false, // 新增笔记弹窗
      modal2: false, // 评论区弹窗

      // 笔记列表
      notes: [],
      page_size: 3,
      total: 0,
      page: 1,
      listLoading: false,

      // 创建新的一篇笔记
      newNoteTitle: '',
      newNoteContent: '',
      iCanAdd: false,

      // 获取到的评论
      comments: [],
      commentTotal: 0,
      commentPage: 1,
      commentPageSize: 2,

      // 回复-评论（一级）
      commentInputIndex: 0,
      commentInputVisable: false,
      commentInputContent: '',

      // 回复-回复
      replyInputIndex: 0,
      replyInputVisable: false,
      replyInputContent: '',
      reply_show: 0,

      // 当前笔记弹窗
      commentValue: '',
      note_id: 0,
    }
  },
  methods: {
    submitNote(){
      let param = {
        'new_note_content':this.newNoteContent,
        'new_note_title':this.newNoteTitle,
        'paper_id':this.paper_id
      }
      addNote(param).then(res => {
        this.$Message.success(res.data.msg)
        if(res.status===200){
          this.getNotes()
        }
      })
    },
    cancel () {
      this.$Message.info('Clicked cancel');
    },
    changePage(e){
      this.page = e
      this.getNotes()
    },
    changePageComment(e){
      this.commentPage = e
      this.getComments()
    },
    getNotes(){
      let param = {
        page: this.page,
        paper_id: this.paper_id
      };
      this.listLoading = true
      getNoteList(param).then(res => {
        if (res.status === 200) {
          this.$Message.success(res.data.msg);
          this.total = res.data.total;
          this.page_size = res.data.page_size;
          this.notes = res.data.notes;
        } else {
          this.$Message.error(res.data.msg);
        }
        this.listLoading = false;
      })
    },
    getComments() {
      let param = {
        page: this.commentPage,
        note_id: this.note_id
      }
      getCommentList(param).then(res =>{
        this.commentPageSize = res.data.page_size
        this.comments = res.data.comments
        this.commentTotal = res.data.total
      })
    },
    openComment(note_id){
      this.modal1=true
      this.note_id = note_id
      this.getComments()
    },
    openCommentInput(comment_id){
      // 若为点击关闭则只关闭不删除，若点击变更则删除保存的输入内容
      this.commentInputContent = this.commentInputIndex === comment_id ? this.commentInputContent : ""
      this.commentInputIndex = comment_id
      this.commentInputVisable = !this.commentInputVisable
    },
    openReplyInput(reply_id){
      this.replyInputContent = this.replyInputIndex === reply_id ? this.replyInputContent : ""
      this.replyInputIndex = reply_id
      this.replyInputVisable = !this.replyInputVisable
    },
    submitComment(){
      let param = {
        note_id: this.note_id,
        comment_content: this.commentValue
      }
      addComment(param).then(res=>{
        if(res.status===200){
          this.$Message.success('新增评论成功')
        }
        else{
          this.$Message.error('新增评论失败')
        }
      })
      this.getComments()
    },
    submitReply(comment_id, reply2_id, reply_content){// reply2_id表示回复的回复，若回复的是评论则为’‘，comment_id表示回复的所在的评论
      let param = {
        comment_id: comment_id,
        reply2_id: reply2_id,
        reply_content: reply_content
      }
      addReply(param).then(res=>{
        if(res.status===200){
          this.$Message.success('新增评论成功')
        }
        else{
          this.$Message.error('新增评论失败')
        }
      })
    },
    deleteReply_(reply_id){
      let param = {
        reply_id: reply_id
      }
      deleteReply(param).then(res =>{
        if(res.status === 200){
          this.$Message.success(res.data.msg)
          this.getComments()
        }
        else{
          this.$Message.error(res.data.msg)
        }
      })
    },
    deleteComment_(comment_id){
      let param = {
        comment_id: comment_id
      }
      deleteComment(param).then(res =>{
        if(res.status === 200){
          this.$Message.success(res.data.msg)
          this.getComments()
        }
        else{
          this.$Message.error(res.data.msg)
        }
      })
    },
    deleteNote_(note_id){
      let param = {
        note_id: note_id,
        paper_id: this.paper_id
      }
      deleteNote(param).then(res =>{
        if(res.status === 200){
          this.$Message.success(res.data.msg)
          this.getNotes()
        }
        else{
          this.$Message.error(res.data.msg)
        }
      })
    }
  },
  mounted() {
    this.paper_id = this.$route.params.id
    canIAddNote({'paper_id': this.paper_id}).then(res=>{
      if(res.status===200){
        this.iCanAdd = true
      }
    })
    this.getNotes()
  }
};
</script>

<style scoped>

</style>