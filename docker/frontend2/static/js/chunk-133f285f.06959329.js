(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-133f285f"],{"6c35":function(e,t,n){"use strict";n.r(t);var a=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"app-container calendar-list-container"},[n("basic-container",[n("avue-crud",{ref:"crud",attrs:{option:e.tableOption,data:e.list,page:e.page,search:e.search,"table-loading":e.listLoading,"before-open":e.beforeOpen,permission:e.permissionList},on:{"update:page":function(t){e.page=t},"update:search":function(t){e.search=t},"on-load":e.getPage,"search-change":e.searchChange,"refresh-change":e.refreshChange,"row-update":e.handleUpdate,"row-save":e.handleSave,"row-del":e.handleDel},scopedSlots:e._u([{key:"menu",fn:function(t){var a=t.row;return[n("el-button",{attrs:{type:"text",size:"small",icon:"el-icon-suitcase"},on:{click:function(t){return e.showDialog(a,"assign")}}},[e._v("分配菜单")])]}}]),model:{value:e.form,callback:function(t){e.form=t},expression:"form"}})],1),n("el-dialog",{staticClass:"avue-dialog avue-dialog--top",attrs:{size:"small",title:e.mDialog.title,visible:e.mDialog.visible,width:e.mDialog.width,top:0,"close-on-click-modal":e.fasle,destroyOnClose:""},on:{"update:visible":function(t){return e.$set(e.mDialog,"visible",t)},opened:e.beforeOpen2}},[n("div",["assign"==e.mDialog.sign?[n("avue-form",{ref:"assign",attrs:{option:e.assignOption},scopedSlots:e._u([{key:"menu_id",fn:function(t){return[n("el-tree",{ref:"tree",attrs:{props:e.defaultProps,data:e.treeData,"show-checkbox":"","node-key":"id",defaultExpandAll:""},on:{check:e.handleTreeCheck}})]}}],null,!1,3645095404),model:{value:e.assignForm,callback:function(t){e.assignForm=t},expression:"assignForm"}})]:e._e()],2),e.mDialog.hasFoot?n("div",{staticClass:"avue-dialog__footer"},[n("el-button",{attrs:{size:"small"},on:{click:function(t){e.mDialog.visible=!1}}},[e._v("取 消")]),n("el-button",{attrs:{size:"small",type:"primary"},on:{click:e.handleDialogSubmit}},[e._v("确 定")])],1):e._e()])],1)},s=[],o=n("5530"),i=n("2909"),r=n("c7eb"),c=n("1da1"),l=(n("d81d"),n("d3b7"),n("159b"),n("a15b"),n("fe15")),u=n("82b1"),d={dialogDrag:!1,dialogHeight:560,labelWidth:"130",border:!0,index:!0,indexLabel:"序号",stripe:!0,menuAlign:"center",menuWidth:360,align:"center",viewBtn:!1,excelBtn:!1,addBtn:!0,delBtn:!0,editBtn:!0,columnBtn:!1,printBtn:!1,menuType:"text",searchMenuSpan:6,searchShow:!0,searchIndex:3,searchIcon:!0,labelSuffix:" ",column:[{label:"角色名称",prop:"role_name",span:12,search:!0,rules:[{required:!0,message:"请填写",trigger:"blur"}]},{label:"角色编码",prop:"role_code",span:12,search:!0,rules:[{required:!0,message:"请填写",trigger:"blur"}]}]},g={name:"RoleList",components:{},data:function(){return{search:{},tableOption:d,page:{total:0,currentPage:1,pageSize:10,ascs:[],descs:[]},paramsSearch:{},list:[],listLoading:!1,form:{},firstLevelMenuList:[],mDialog:{title:"提示",visible:!1,width:"40%",hasFoot:!0,sign:""},assignOption:{labelWidth:120,menuBtn:!1,column:[{label:"菜单",type:"tree",prop:"menu_id",slot:!0,rules:[{required:!1,message:"请选择",trigger:"blur"}]}]},assignForm:{},curr_role_id:"",treeData:[],defaultCheckedKeys:[],defaultProps:{label:"menu_name",children:"childrens"},checkedMenuId:[]}},computed:{permissionList:function(){return{}}},watch:{},created:function(){this.getAllMenuList()},methods:{getAllMenuList:function(){var e=this;return Object(c["a"])(Object(r["a"])().mark((function t(){return Object(r["a"])().wrap((function(t){while(1)switch(t.prev=t.next){case 0:return console.log("1"),t.next=3,Object(u["e"])().then((function(t){console.log("allMenu",t),e.treeData=t.data}));case 3:case"end":return t.stop()}}),t)})))()},getPage:function(e,t){var n=this;this.listLoading=!0,Object(l["c"])(Object.assign({page:e.currentPage,size:e.pageSize,descs:this.page.descs,ascs:this.page.ascs},t)).then((function(e){var t=e.data;n.list=t.items,n.page.total=t.total,n.page.currentPage=t.page,n.page.pageSize=t.size,n.listLoading=!1})).catch((function(){n.listLoading=!1}))},refreshChange:function(e){console.log("refreshChange",e),this.getPage(this.page)},searchChange:function(e,t){console.log("searchChange",e),this.page.currentPage=1,this.getPage(this.page,this.filterForm(e)),t()},beforeOpen:function(e,t){e()},beforeOpen2:function(){this.getHadMenu()},getHadMenu:function(){var e=this;Object(u["c"])(this.curr_role_id).then((function(t){e.defaultCheckedKeys=t.data.map((function(e){return e.id})),e.checkedMenuId=Object(i["a"])(e.defaultCheckedKeys);var n=setInterval((function(){e.defaultCheckedKeys.forEach((function(t){var n=e.$refs.tree.getNode(t);n.isLeaf&&e.$refs.tree.setChecked(n,!0)})),clearInterval(n)}),200)}))},handleDel:function(e,t){var n=this;this.$confirm("是否确认删除?","警告",{confirmButtonText:"确定",cancelButtonText:"取消",type:"warning"}).then((function(){var t={id:e.id};Object(l["b"])(t).then((function(e){200==e.code?(n.$message({showClose:!0,message:e.message,type:"success"}),n.getPage(n.page)):n.$message({showClose:!0,message:e.message,type:"error"})}))})).catch((function(e){console.log("err",e)}))},handleSave:function(e,t,n){var a=this,s=this,i=Object(o["a"])({},e);Object(l["a"])(i).then((function(e){200==e.code?(s.$message({showClose:!0,message:e.message,type:"success"}),s.getPage(a.page)):(s.$message({showClose:!0,message:e.message,type:"error"}),s.getPage(a.page))})).catch((function(e){console.log("err",e)})).finally((function(){t(),n()}))},handleUpdate:function(e,t,n,a){var s=this,i=this,r=Object(o["a"])({},e);Object(l["f"])(r).then((function(e){200==e.code?(i.$message({showClose:!0,message:e.message,type:"success"}),i.getPage(s.page)):(i.$message({showClose:!0,message:e.message,type:"error"}),i.getPage(s.page),i.getFirstLevelMenuList())})).catch((function(e){console.log("err",e)})).finally((function(){n(),a()}))},showDialog:function(e,t){console.log("show",e,t),this.mDialog.sign=t,this.mDialog.visible=!0,"assign"==t&&(this.mDialog.title="分配菜单",this.mDialog.width="680px",this.curr_role_id=e.id)},handleDialogSubmit:function(e){var t=this;console.log("handleSubmit_assign",this.curr_role_id);var n={menu_id:this.checkedMenuId.join(",")};Object(u["b"])(this.curr_role_id,n).then((function(e){t.$message({showClose:!0,message:e.message,type:"success"}),t.closeDialog()})).catch((function(e){t.$message({showClose:!0,message:res.message,type:"error"})})).finally((function(){e(),t.closeDialog()}))},closeDialog:function(){this.mDialog.visible=!1},handleTreeCheck:function(e,t,n,a){var s=this.$refs.tree.getCheckedNodes(!1,!0).map((function(e){return e.id}));console.log("nodes",s),this.checkedMenuId=s,console.log("checkedMenuId",this.checkedMenuId)}}},h=g,f=n("2877"),m=Object(f["a"])(h,a,s,!1,null,null,null);t["default"]=m.exports},"82b1":function(e,t,n){"use strict";n.d(t,"g",(function(){return s})),n.d(t,"e",(function(){return o})),n.d(t,"f",(function(){return i})),n.d(t,"c",(function(){return r})),n.d(t,"b",(function(){return c})),n.d(t,"a",(function(){return l})),n.d(t,"h",(function(){return u})),n.d(t,"d",(function(){return d}));var a=n("b775");function s(e){return Object(a["a"])({url:"/menu/pageList",method:"GET",params:e})}function o(e){return Object(a["a"])({url:"/menu/list",method:"GET",params:e})}function i(){return Object(a["a"])({url:"/menu/getAllFirstLevelMenuList",method:"GET"})}function r(e){return Object(a["a"])({url:"/menu/assignMenu/".concat(e),method:"GET"})}function c(e,t){return Object(a["a"])({url:"/menu/assignMenu/".concat(e),method:"PATCH",data:t})}function l(e){return Object(a["a"])({url:"/menu/",method:"POST",data:e})}function u(e){return Object(a["a"])({url:"/menu/",method:"PATCH",data:e})}function d(e){return Object(a["a"])({url:"/menu/",method:"DELETE",data:e})}},fe15:function(e,t,n){"use strict";n.d(t,"c",(function(){return s})),n.d(t,"e",(function(){return o})),n.d(t,"d",(function(){return i})),n.d(t,"a",(function(){return r})),n.d(t,"f",(function(){return c})),n.d(t,"b",(function(){return l}));var a=n("b775");function s(e){return Object(a["a"])({url:"/role/pageList",method:"get",params:e})}function o(e){return Object(a["a"])({url:"/role/assignRoleList",method:"get",params:e})}function i(){return Object(a["a"])({url:"/role/list",method:"get"})}function r(e){return Object(a["a"])({url:"/role/",method:"post",data:e})}function c(e){return Object(a["a"])({url:"/role/",method:"patch",data:e})}function l(e){return Object(a["a"])({url:"/role/",method:"delete",data:e})}}}]);