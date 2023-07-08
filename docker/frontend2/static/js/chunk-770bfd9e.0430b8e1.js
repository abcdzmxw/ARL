(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-770bfd9e"],{c430b:function(e,t,a){"use strict";a.r(t);var n=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"app-container calendar-list-container"},[a("basic-container",[a("avue-crud",{ref:"crud",attrs:{option:e.tableOption,page:e.page,data:e.list,search:e.search,"table-loading":e.listLoading,"before-open":e.beforeOpen,permission:e.permissionList},on:{"update:page":function(t){e.page=t},"update:search":function(t){e.search=t},"on-load":e.getPage,"selection-change":e.selectionChange,"search-change":e.searchChange,"refresh-change":e.refreshChange,"row-save":e.handleSave,"row-del":e.handleDelete},scopedSlots:e._u([{key:"statistic",fn:function(t){var n=t.row;return[n.statistic?a("div",[a("span",[e._v("站点："+e._s(n.statistic.site_cnt))]),a("br"),a("span",[e._v("域名："+e._s(n.statistic.domain_cnt))])]):a("div",[e._v("-")])]}},{key:"options",fn:function(t){t.row;return[e._v(" options ")]}},{key:"functionForm",fn:function(t){return[a("el-checkbox-group",{model:{value:e.checkedFuction,callback:function(t){e.checkedFuction=t},expression:"checkedFuction"}},e._l(e.functionOptions,(function(t){return a("el-checkbox",{key:t.key,attrs:{label:t.key}},[e._v(e._s(t.value))])})),1)]}},{key:"status",fn:function(t){var n=t.row;return["done"==n.status?a("el-tag",{attrs:{size:"mini",type:"success"}},[e._v(e._s(n.status))]):e._e(),"error"==n.status?a("el-tag",{attrs:{size:"mini",type:"info"}},[e._v(e._s(n.status))]):e._e()]}},{key:"menu",fn:function(t){var n=t.row;return[a("el-button",{attrs:{size:"small",type:"text",icon:"el-icon-refresh"}},[e._v("同步")]),a("el-button",{attrs:{size:"small",type:"text",icon:"el-icon-download"},on:{click:function(t){return e.handleExport(n)}}},[e._v("导出")]),a("el-button",{attrs:{size:"small",type:"text",icon:"el-icon-turn-off"},on:{click:function(t){return e.handleStop(n)}}},[e._v("停止")]),a("el-button",{attrs:{size:"small",type:"text",icon:"el-icon-open"},on:{click:function(t){return e.handleRestart(n)}}},[e._v("重启")])]}}]),model:{value:e.form,callback:function(t){e.form=t},expression:"form"}},[a("template",{slot:"menuLeft"},[a("el-button",{attrs:{size:"small",icon:"el-icon-delete",disabled:!e.selectedRows.length},on:{click:e.handleDelete}},[e._v("批量删除")]),a("el-button",{attrs:{size:"small",icon:"el-icon-delete",disabled:!e.selectedRows.length},on:{click:e.handleStop}},[e._v("批量停止")]),a("el-select",{staticStyle:{width:"140px !important"},attrs:{disabled:!e.selectedRows.length,clearable:"",size:"small",placeholder:"批量导出"},on:{change:e.handleExport},model:{value:e.exportValue,callback:function(t){e.exportValue=t},expression:"exportValue"}},e._l(e.exportOptions,(function(e){return a("el-option",{key:e.value,attrs:{label:e.label,value:e.value,disabled:e.disabled}})})),1)],1)],2)],1)],1)},s=[],o=a("c7eb"),i=a("1da1"),r=(a("d3b7"),a("d81d"),a("3ca3"),a("ddb0"),a("2b3d"),a("9861"),a("b0c0"),a("159b"),a("caad"),a("2532"),a("b775"));function c(e){return Object(r["a"])({url:"/task/",method:"GET",params:e,isReturnNativeResponse:!0})}function l(e){return Object(r["a"])({url:"/task/",method:"post",data:e})}function u(e){return Object(r["a"])({url:"/task/delete/",method:"post",data:e})}function p(e){return Object(r["a"])({url:"/task/batch_stop/",method:"post",data:e})}function d(e){return Object(r["a"])({url:"/task/stop/".concat(e),method:"get"})}function h(e){return Object(r["a"])({url:"/task/restart/",method:"post",data:e})}function g(){return Object(r["a"])({url:"/task/get_domain_brute_type",method:"get"})}function m(){return Object(r["a"])({url:"/task/get_function",method:"get"})}function f(){return Object(r["a"])({url:"/task/get_port_scan_type",method:"get"})}function b(e,t){return Object(r["a"])({url:"/batch_export/".concat(e,"/"),method:"get",data:t,isNoCodeResponse:!0,responseType:"blob"})}var _={dialogDrag:!1,dialogWidth:540,labelWidth:76,border:!0,index:!0,indexLabel:"序号",stripe:!0,menuAlign:"center",menuWidth:290,menu:!0,align:"center",viewBtn:!1,excelBtn:!1,addBtn:!0,addBtnText:"添加任务",delBtn:!0,editBtn:!1,columnBtn:!1,printBtn:!1,menuType:"text",searchMenuSpan:6,searchShow:!0,searchIndex:3,searchIcon:!0,labelSuffix:" ",selection:!0,size:"mini",column:[{label:"任务名",prop:"name",search:!0,span:24,width:130,rules:[{required:!0,message:"请填写任务名",trigger:"blur"}]},{label:"目标",prop:"target",search:!0,type:"textarea",maxRows:2,minRows:2,span:24,width:120,searchPlaceholder:"目标",placeholder:"请输入目标，支持IP、IP段、域名",rules:[{required:!0,message:"请填写目标",trigger:"blur"}]},{label:"统计",prop:"statistic",span:12,display:!1},{label:"配置项",prop:"options",span:12,display:!1},{label:"任务类型",prop:"task_tag",search:!0,searchType:"select",dicData:[{label:"资产侦查任务",value:"task"},{label:"资产监控任务",value:"monitor"},{label:"风险巡航任务",value:"risk_cruising"},{label:"资产站点更新",value:"asset_site_update"}],span:12,hide:!0,display:!1},{label:"状态",prop:"status",search:!0,span:12,display:!1},{label:"开始时间",prop:"start_time",span:12,display:!1},{label:"结束时间",prop:"end_time",span:12,display:!1},{label:"Task_Id",prop:"_id",search:!0,span:12,width:180,display:!1},{label:"域名爆破类型",prop:"domain_brute_type",type:"select",labelWidth:140,dicData:[],props:{label:"value",value:"key"},span:24,hide:!0,rules:[{required:!0,message:"请选择",trigger:"blur"}]},{label:"端口扫描类型",prop:"port_scan_type",type:"select",labelWidth:140,dicData:[],props:{label:"value",value:"key"},span:24,hide:!0,rules:[{required:!0,message:"请选择",trigger:"blur"}]},{label:"",prop:"function",slot:!0,hide:!0}]},v={name:"MenuList",components:{},data:function(){return{search:{},tableOption:_,page:{total:0,currentPage:1,pageSize:10,ascs:[],descs:[]},paramsSearch:{},list:[],listLoading:!1,form:{},selectedRows:[],exportOptions:[{label:"C段批量导出",value:"cip"},{label:"域名批量导出",value:"domain"},{label:"IP批量导出",value:"ip"},{label:"IP端口批量导出",value:"ip_port"},{label:"站点批量导出",value:"site"},{label:"URL批量导出",value:"url"}],exportValue:"",checkedFuction:[],functionOptions:[],domainBruteOptions:[],portScanOptions:[]}},computed:{permissionList:function(){return{}}},watch:{},created:function(){this.getDic()},methods:{getDic:function(){var e=this;return Object(i["a"])(Object(o["a"])().mark((function t(){var a,n,s;return Object(o["a"])().wrap((function(t){while(1)switch(t.prev=t.next){case 0:return t.next=2,g();case 2:return a=t.sent,t.next=5,f();case 5:return n=t.sent,t.next=8,m();case 8:s=t.sent,e.domainBruteOptions=a.data.data,e.portScanOptions=n.data,e.functionOptions=s.data;case 12:case"end":return t.stop()}}),t)})))()},selectionChange:function(e){this.selectedRows=e},getPage:function(e,t){var a=this;this.listLoading=!0,c(Object.assign({page:e.currentPage,size:e.pageSize,descs:this.page.descs,ascs:this.page.ascs},t)).then((function(e){console.log("res",e),200==e.code&&(a.list=e.items,a.page.total=e.total,a.page.currentPage=e.page,a.page.pageSize=e.size)})).catch((function(e){console.log("err",e)})).finally((function(){a.listLoading=!1}))},refreshChange:function(e){this.getPage(this.page)},searchChange:function(e,t){this.page.currentPage=1,this.getPage(this.page,this.filterForm(e)),t()},beforeOpen:function(e,t){var a=this.tableOption.column;a[9].dicData=this.domainBruteOptions,a[10].dicData=this.portScanOptions,e()},handleRestart:function(e){var t=this;this.$confirm("是否重启选择的记录","提示",{confirmButtonText:"确定",cancelButtonText:"取消",type:"warning"}).then((function(){var a={task_id:[e._id]};h(a).then((function(e){200==e.code?(t.$message({showClose:!0,message:e.message,type:"success"}),t.getPage(t.page)):t.$message({showClose:!0,message:e.message,type:"error"})}))}))},handleStop:function(e){var t=this;this.$confirm("是否确认停止选择的记录","提示",{confirmButtonText:"确定",cancelButtonText:"取消",type:"warning"}).then((function(){var a=e._id?e._id:{task_id:t.selectedRows.map((function(e){return e._id}))},n=e._id?d:p;n(a).then((function(e){200==e.code?(t.$message({showClose:!0,message:e.message,type:"success"}),t.getPage(t.page)):t.$message({showClose:!0,message:e.message,type:"error"})}))}))},handleDelete:function(e){var t=this;this.$confirm("是否确认删除选择的记录","提示",{confirmButtonText:"确定",cancelButtonText:"取消",type:"warning"}).then((function(){var a={task_id:e._id?[e._id]:t.selectedRows.map((function(e){return e._id}))};u(a).then((function(e){200==e.code?(t.$message({showClose:!0,message:e.message,type:"success"}),t.getPage(t.page)):t.$message({showClose:!0,message:e.message,type:"error"})}))}))},handleExport:function(e){var t=this;this.$confirm("是否导出?","提示",{confirmButtonText:"确定",cancelButtonText:"取消",type:"warning"}).then((function(){var a=e._id?"":t.exportValue,n={task_id:e._id?[e._id]:t.selectedRows.map((function(e){return e._id}))};console.log("type",a,"data:",n),b(a,n).then((function(e){if(window.navigator.msSaveBlob)try{var t=new Blob([e.data]);window.navigator.msSaveBlob(t,"导出文件.txt")}catch(s){console.log(s)}else{var a=window.URL.createObjectURL(e.data),n=document.createElement("a");n.style.display="none",n.href=a,n.setAttribute("download","导出文件.txt"),document.body.appendChild(n),n.click(),document.body.removeChild(n),window.URL.revokeObjectURL(n.href)}})).catch((function(e){console.log("err",e)})).finally((function(){t.listLoading=!1}))}))},handleSave:function(e,t,a){var n=this,s=this,o=e.name,i=e.target,r=e.domain_brute_type,c=e.port_scan_type,u={name:o,target:i,domain_brute_type:r,port_scan_type:c},p={};s.functionOptions.forEach((function(e){p[e.key]=s.checkedFuction.includes(e.key)})),console.log("params2",p);var d=Object.assign(u,p);console.log("params",d),l(d).then((function(e){200==e.code?(s.$message({showClose:!0,message:e.message,type:"success"}),s.getPage(n.page)):(s.$message({showClose:!0,message:e.message,type:"error"}),s.getPage(n.page))})).catch((function(e){console.log("err",e)})).finally((function(){t(),a()}))}}},y=v,w=a("2877"),k=Object(w["a"])(y,n,s,!1,null,null,null);t["default"]=k.exports}}]);