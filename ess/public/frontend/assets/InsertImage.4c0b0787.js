import{_ as f,B as I,D,O as h,e as d,H as _,J as y,K as v,f as n,w as l,F as w,g as m,o as c,m as r,t as C,Q as B,y as u}from"./vendor.27671223.js";const b={name:"InsertImage",props:["editor"],expose:["openDialog"],data(){return{addImageDialog:{url:"",file:null,show:!1}}},components:{Button:I,Dialog:D},methods:{openDialog(){this.addImageDialog.show=!0},onImageSelect(t){let e=t.target.files[0];!e||(this.addImageDialog.file=e,h(e).then(i=>{this.addImageDialog.url=i}))},addImage(t){this.editor.chain().focus().setImage({src:t}).run(),this.reset()},reset(){this.addImageDialog=this.$options.data().addImageDialog}}},k={class:"relative cursor-pointer rounded-lg bg-gray-100 py-1 focus-within:bg-gray-200 hover:bg-gray-200"},x={class:"absolute inset-0 select-none px-2 py-1 text-base"},S=["src"],V=u(" Insert Image "),N=u(" Cancel ");function A(t,e,i,F,a,o){const g=m("Button"),p=m("Dialog");return c(),d(w,null,[_(t.$slots,"default",y(v({onClick:o.openDialog}))),n(p,{options:{title:"Add Image"},modelValue:a.addImageDialog.show,"onUpdate:modelValue":e[2]||(e[2]=s=>a.addImageDialog.show=s),onAfterLeave:o.reset},{"body-content":l(()=>[r("label",k,[r("input",{type:"file",class:"w-full opacity-0",onChange:e[0]||(e[0]=(...s)=>o.onImageSelect&&o.onImageSelect(...s)),accept:"image/*"},null,32),r("span",x,C(a.addImageDialog.file?"Select another image":"Select an image"),1)]),a.addImageDialog.url?(c(),d("img",{key:0,src:a.addImageDialog.url,class:"mt-2 w-full rounded-lg"},null,8,S)):B("",!0)]),actions:l(()=>[n(g,{appearance:"primary",onClick:e[1]||(e[1]=s=>o.addImage(a.addImageDialog.url))},{default:l(()=>[V]),_:1}),n(g,{onClick:o.reset},{default:l(()=>[N]),_:1},8,["onClick"])]),_:1},8,["modelValue","onAfterLeave"])],64)}var P=f(b,[["render",A]]);export{P as default};