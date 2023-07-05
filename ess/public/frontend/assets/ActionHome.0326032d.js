import{r as k,E as w,q as _,a as C,e as m,m as a,f as l,w as i,u as o,C as A,D as h,g as y,o as p,F as N,x as B,y as f,t as D,I as g}from"./vendor.27671223.js";const L={class:"mx-20"},j={class:"flex flex-row items-center justify-between"},G=a("h2",{class:"text-5xl font-black text-gray-900"},"Lists",-1),S=f("New List"),T={class:"mt-2"},U=f("New Action"),$={class:"space-y-2"},I={setup(q){const s=k({title:"",category:"General"}),d=w(!1),n=_({doctype:"Action",fields:["name","title","status","description","date","due_date"],filters:{status:"ToDo"},limit:100});n.reload();const r=_({doctype:"Category",fields:["name"],transform(c){return c.map(t=>t.name)},cache:"actions"});r.reload();const v=C(()=>r.list.loading||!r.data?[]:r.data),x=c=>{n.setValue.submit({name:c,status:"Completed",onSuccess(){n.reload()}})},V=()=>{console.log(s),n.insert.submit(s)};return(c,t)=>{const u=y("Button"),b=y("router-link");return p(),m("div",L,[a("div",j,[G,l(u,{"icon-left":"plus"},{default:i(()=>[S]),_:1})]),a("div",T,[l(o(A),{title:"General"},{default:i(()=>[a("div",null,[a("ul",null,[(p(!0),m(N,null,B(o(n).data,e=>(p(),m("li",{class:"flex flex-row space-y-2 items-center justify-between",key:e.title},[l(b,{to:`/actions/${e.name}`},{default:i(()=>[f(D(e.title),1)]),_:2},1032,["to"]),l(u,{onClick:E=>x(e.name),icon:"check"},null,8,["onClick"])]))),128))]),l(u,{onClick:t[0]||(t[0]=e=>d.value=!0),"icon-left":"plus"},{default:i(()=>[U]),_:1})])]),_:1})]),l(o(h),{options:{title:"Add New Action",actions:[{label:"Add Action",appearance:"primary",handler:({close:e})=>{V(),e()}},{label:"Cancel"}]},modelValue:d.value,"onUpdate:modelValue":t[3]||(t[3]=e=>d.value=e)},{"body-content":i(()=>[a("div",$,[l(o(g),{modelValue:o(s).title,"onUpdate:modelValue":t[1]||(t[1]=e=>o(s).title=e),type:"text",required:"",placeholder:"Give your action a title...",label:"Title"},null,8,["modelValue"]),l(o(g),{modelValue:o(s).category,"onUpdate:modelValue":t[2]||(t[2]=e=>o(s).category=e),label:"List",type:"select",options:o(v)},null,8,["modelValue","options"])])]),_:1},8,["options","modelValue"])])}}};export{I as default};
