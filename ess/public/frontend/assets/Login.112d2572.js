import{z as m,e as p,f as e,w as n,g as o,o as d,m as u,u as f,A as _,y as w}from"./vendor.27671223.js";import{s as r}from"./index.cd572bec.js";const g={class:"m-3 flex flex-row items-center justify-center"},x=["onSubmit"],h=w("Login"),C=m({setup(b){function i(a){let t=new FormData(a.target);r.login.submit({email:t.get("email"),password:t.get("password")})}return(a,t)=>{const s=o("Input"),l=o("Button"),c=o("Card");return d(),p("div",g,[e(c,{title:"Login to your FrappeUI App!",class:"w-full max-w-md mt-4"},{default:n(()=>[u("form",{class:"flex flex-col space-y-2 w-full",onSubmit:_(i,["prevent"])},[e(s,{required:"",name:"email",type:"text",placeholder:"faris@main.com",label:"User ID"}),e(s,{required:"",name:"password",type:"password",placeholder:"\u2022\u2022\u2022\u2022\u2022\u2022",label:"Password"}),e(l,{loading:f(r).login.loading,appearance:"primary"},{default:n(()=>[h]),_:1},8,["loading"])],40,x)]),_:1})])}}});export{C as default};
