import{_ as d,B as p,I as g,D as L,e as m,H as f,J as D,K as h,f as i,w as a,F as c,g as l,o as _,N as v,y as w}from"./vendor.27671223.js";const x={name:"InsertLink",props:["editor"],components:{Button:p,Input:g,Dialog:L},data(){return{setLinkDialog:{url:"",show:!1}}},methods:{openDialog(){let t=this.editor.getAttributes("link").href;t&&(this.setLinkDialog.url=t),this.setLinkDialog.show=!0},setLink(t){t===""?this.editor.chain().focus().extendMarkRange("link").unsetLink().run():this.editor.chain().focus().extendMarkRange("link").setLink({href:t}).run(),this.setLinkDialog.show=!1,this.setLinkDialog.url=""},reset(){this.setLinkDialog=this.$options.data().setLinkDialog}}},V=w(" Save ");function y(t,e,B,I,o,s){const r=l("Input"),u=l("Button"),k=l("Dialog");return _(),m(c,null,[f(t.$slots,"default",D(h({onClick:s.openDialog}))),i(k,{options:{title:"Set Link"},modelValue:o.setLinkDialog.show,"onUpdate:modelValue":e[3]||(e[3]=n=>o.setLinkDialog.show=n),onAfterLeave:s.reset},{"body-content":a(()=>[i(r,{type:"text",label:"URL",modelValue:o.setLinkDialog.url,"onUpdate:modelValue":e[0]||(e[0]=n=>o.setLinkDialog.url=n),onKeydown:e[1]||(e[1]=v(n=>s.setLink(n.target.value),["enter"]))},null,8,["modelValue"])]),actions:a(()=>[i(u,{appearance:"primary",onClick:e[2]||(e[2]=n=>s.setLink(o.setLinkDialog.url))},{default:a(()=>[V]),_:1})]),_:1},8,["modelValue","onAfterLeave"])],64)}var C=d(x,[["render",y]]);export{C as default};
