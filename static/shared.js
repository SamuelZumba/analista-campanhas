const $=(s,root=document)=>root.querySelector(s),$$=(s,root=document)=>[...root.querySelectorAll(s)];
const money=v=>new Intl.NumberFormat('pt-BR',{style:'currency',currency:'BRL'}).format(Number(v)||0);
const fmt=n=>new Intl.NumberFormat('pt-BR').format(Number(n)||0);
let toastTimer;function toast(message){const el=$('#toast');el.textContent=message;el.hidden=false;clearTimeout(toastTimer);toastTimer=setTimeout(()=>el.hidden=true,3600)}
async function api(url,opts={}){const r=await fetch(url,{...opts,headers:{'Content-Type':'application/json',...(opts.headers||{})}});const data=await r.json().catch(()=>({}));if(!r.ok){const detail=data.detail;throw new Error(typeof detail==='string'?detail:Array.isArray(detail)?detail.map(x=>x.msg).join('; '):'Erro '+r.status)}return data}
function addText(parent,tag,text,cls){let el=document.createElement(tag);if(cls)el.className=cls;el.textContent=text;parent.appendChild(el);return el}
async function copyText(text){try{await navigator.clipboard.writeText(text);toast('Texto copiado.')}catch(e){toast('Não foi possível copiar automaticamente.')}}
