(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-0d19f148"],{"1e6a":function(e,n,t){"use strict";t.r(n);var a=function(){var e=this,n=e.$createElement,t=e._self._c||n;return t("div",{staticClass:"u-crud",staticStyle:{"padding-top":"15px"}},[t("avue-crud",{ref:"crud",attrs:{page:e.page,option:e.tableOption,data:e.list,search:e.search,"table-loading":e.listLoading,"before-open":e.beforeOpen,permission:e.permissionList},on:{"update:page":function(n){e.page=n},"update:search":function(n){e.search=n},"on-load":e.getPage,"search-change":e.searchChange,"refresh-change":e.refreshChange},scopedSlots:e._u([{key:"record",fn:function(n){var a=n.row;return e._l(a.record,(function(n){return t("p",{key:n},[e._v(e._s(n))])}))}},{key:"ips",fn:function(n){var a=n.row;return e._l(a.ips,(function(n){return t("p",{key:n},[e._v(e._s(n))])}))}}]),model:{value:e.form,callback:function(n){e.form=n},expression:"form"}},[t("template",{slot:"menuLeft"},[t("el-button",{attrs:{size:"mini",type:"primary",icon:"el-icon-download"},on:{click:e.handleExport}},[e._v("导出站点")])],1)],2)],1)},o=[],i=(t("d3b7"),t("3ca3"),t("ddb0"),t("2b3d"),t("9861"),t("b775"));function s(e){return Object(i["a"])({url:"/domain/",method:"GET",params:e})}function r(e){return Object(i["a"])({url:"/domain/export/",method:"get",data:e,isNoCodeResponse:!0,responseType:"blob"})}var c={dialogDrag:!1,dialogWidth:420,labelWidth:76,border:!0,index:!0,indexLabel:"序号",stripe:!0,menuAlign:"center",menuWidth:0,menu:!1,align:"left",viewBtn:!1,excelBtn:!1,addBtn:!1,delBtn:!1,editBtn:!1,columnBtn:!1,printBtn:!1,menuType:"text",searchMenuSpan:6,searchShow:!0,searchIndex:3,searchIcon:!0,selection:!1,size:"mini",column:[{label:"域名",prop:"domain",search:!0,span:24,rules:[{required:!0,message:"请填写名称",trigger:"blur"}]},{label:"解析类型",prop:"type",search:!0,span:12},{label:"记录值",prop:"record",search:!0,span:24},{label:"关联IP",prop:"ips",search:!0,span:12},{label:"来源",prop:"source",search:!0,span:12}]},l={name:"MenuList",components:{},data:function(){return{search:{},tableOption:c,page:{total:0,currentPage:1,pageSize:10,ascs:[],descs:[]},paramsSearch:{},list:[],listLoading:!1,form:{},inputIdVisible:"",inputValue:""}},computed:{permissionList:function(){return{}}},watch:{},created:function(){},methods:{getPage:function(e,n){var t=this;this.listLoading=!0,s(Object.assign({page:e.currentPage,size:e.pageSize,descs:this.page.descs,ascs:this.page.ascs},n)).then((function(e){t.list=e.items,t.page.total=e.total,t.page.currentPage=e.page,t.page.pageSize=e.size,t.listLoading=!1})).catch((function(){t.listLoading=!1}))},refreshChange:function(e){console.log("refreshChange",e),this.getPage(this.page)},searchChange:function(e,n){console.log("searchChange",e),this.page.currentPage=1,this.getPage(this.page,this.filterForm(e)),n()},beforeOpen:function(e,n){e()},handleDel:function(e,n){var t=this;this.$confirm("是否确认删除?","警告",{confirmButtonText:"确定",cancelButtonText:"取消",type:"warning"}).then((function(){var n={menu_id:e.id};delObj(n).then((function(e){200==e.code?(t.$message({showClose:!0,message:e.message,type:"success"}),t.getPage(t.page)):t.$message({showClose:!0,message:e.message,type:"error"})}))})).catch((function(e){console.log("err",e)}))},handleCloseTag:function(e,n){var t=this;console.log("row",e,n);var a={_id:e._id,tag:n};(void 0)(a).then((function(e){console.log("del tag res",e),t.getPage(t.page)}))},showInput:function(e){var n=this;this.inputIdVisible="inp_"+e._id,this.$nextTick((function(e){n.$refs.saveTagInput.$refs.input.focus()}))},handleInputConfirm:function(e){var n=this;console.log("handleInputConfirm",e);var t=this.inputValue;if(console.log("inputValue",t),t){console.log("if",t);var a={_id:e._id,tag:t};(void 0)(a).then((function(e){console.log("add tag res",e),n.getPage(n.page),n.inputIdVisible="",n.inputValue=""}))}},handleExport:function(){var e=this;this.$confirm("是否导出站点?","提示",{confirmButtonText:"确定",cancelButtonText:"取消",type:"warning"}).then((function(){r(e.page).then((function(e){if(window.navigator.msSaveBlob)try{var n=new Blob([e.data]);window.navigator.msSaveBlob(n,"domain.txt")}catch(o){console.log(o)}else{var t=window.URL.createObjectURL(e.data),a=document.createElement("a");a.style.display="none",a.href=t,a.setAttribute("download","domain.txt"),document.body.appendChild(a),a.click(),document.body.removeChild(a),window.URL.revokeObjectURL(a.href)}})).catch((function(e){console.log("err",e)})).finally((function(){e.listLoading=!1}))}))}}},u=l,d=(t("7e71"),t("2877")),p=Object(d["a"])(u,a,o,!1,null,"99afba9c",null);n["default"]=p.exports},"7e71":function(e,n,t){"use strict";t("db51")},db51:function(e,n,t){}}]);