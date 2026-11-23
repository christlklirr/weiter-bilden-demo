(function(root){
 'use strict';
 const S=root.WbaSearch,C=root.WbaCourseProgress;
 function el(tag,className,text){const n=document.createElement(tag);if(className)n.className=className;if(text!=null)n.textContent=text;return n;}
 function link(label,url){const a=el('a','',label);try{const u=new URL(url);if(!['https:','http:'].includes(u.protocol))return el('span','',label);a.href=u.href;a.target='_blank';a.rel='noopener noreferrer';}catch{return el('span','',label);}return a;}
 function heart(c,saved){const b=el('button','fav-button',saved?'♥':'♡');b.type='button';b.dataset.favorite=c.id;b.setAttribute('aria-pressed',String(saved));b.setAttribute('aria-label',(saved?'Von der Kursliste entfernen: ':'Auf die Kursliste setzen: ')+c.title);b.title=saved?'Gemerkt – zum Entfernen antippen':'Merken';return b;}
 function statusButtons(c,current){const box=el('div','status-buttons');box.setAttribute('role','group');box.setAttribute('aria-label','Meine Teilnahme: '+c.title);for(const [value,label] of [['registered','Angemeldet'],['completed','Absolviert']]){const b=el('button','status-button '+value,(current===value?'✓ ':'')+label);b.type='button';b.dataset.status=value;b.dataset.course=c.id;b.setAttribute('aria-pressed',String(current===value));box.append(b);}return box;}
 function phaseBadge(c,status){const p=C.phase(status,S.timing(c),S.viennaToday());return p?el('span','phase-badge phase-'+p.key,p.label):null;}
 function timingBadge(c){const t=S.timing(c),from=S.displayDate(t.start),labels={started:'⚠ Bereits gestartet am '+from+' · Einstieg beim Anbieter prüfen',ended:'Termin bereits beendet',today:'⚠ Startet heute · zählt als bereits gestartet',future:'Start am '+from,ongoing:'Kein Termin eingetragen · beim Anbieter prüfen',unknown:'Termin unklar · Quelle prüfen'};return el('span','date-status '+t.status,labels[t.status]);}
 // Info buttons: a small (i) next to a label opens its explanation; Escape or a click elsewhere closes it.
 function initInfo(){
  const closeAll=except=>{for(const b of document.querySelectorAll('.info-btn[aria-expanded="true"]'))if(b!==except){b.setAttribute('aria-expanded','false');document.getElementById(b.getAttribute('aria-controls')).hidden=true;}};
  document.addEventListener('click',e=>{const b=e.target.closest('.info-btn');if(!b){if(!e.target.closest('.info-pop'))closeAll();return;}e.preventDefault();const pop=document.getElementById(b.getAttribute('aria-controls')),open=b.getAttribute('aria-expanded')!=='true';closeAll(b);b.setAttribute('aria-expanded',String(open));pop.hidden=!open;if(open)place(b,pop);});
  // Fixed positioning keeps the box inside the screen on phones; it opens below the button, or above it if there is no room.
  function place(b,pop){const vw=document.documentElement.clientWidth,vh=window.innerHeight,r=b.getBoundingClientRect();pop.style.position='fixed';pop.style.transform='';pop.style.right='auto';pop.style.left='0px';pop.style.top='0px';const w=pop.offsetWidth,h=pop.offsetHeight;pop.style.left=Math.max(12,Math.min(r.left-10,vw-w-12))+'px';pop.style.top=(r.bottom+8+h>vh-8&&r.top-8-h>8?r.top-8-h:r.bottom+8)+'px';}
  window.addEventListener('scroll',()=>closeAll(),{passive:true});window.addEventListener('resize',()=>closeAll());
  document.addEventListener('keydown',e=>{if(e.key!=='Escape')return;const open=document.querySelector('.info-btn[aria-expanded="true"]');if(open){closeAll();open.focus();}});
 }
 function navCount(store){const n=store.ids().length;for(const badge of document.querySelectorAll('[data-list-count]'))badge.textContent=n?String(n):'';}
 const api={el,link,heart,statusButtons,phaseBadge,timingBadge,initInfo,navCount};root.WbaUI=api;
})(window);
