(function(root){
 'use strict';const key='weiter-bilden-demo.course-progress.v1',statuses=['registered','completed'],legacy={started:'registered'};
 // Older saves used "started" (von mir begonnen); it is read as "registered" (angemeldet).
 function validate(value,allowedIds){if(!value||typeof value!=='object'||Array.isArray(value))throw new Error('Die Kursmarkierungen sind ungültig.');const allowed=allowedIds?new Set(allowedIds):null,clean={};for(const [id,raw] of Object.entries(value)){const status=legacy[raw]||raw;if(!/^\d{1,12}$/.test(id)||!statuses.includes(status)||(allowed&&!allowed.has(id)))throw new Error('Die Datei enthält eine unbekannte Kursmarkierung.');clean[id]=status;}return clean;}
 function read(storage,allowedIds){const text=storage.getItem(key);return text?validate(JSON.parse(text),allowedIds):{};}
 function write(storage,value,allowedIds){const clean=validate(value,allowedIds);storage.setItem(key,JSON.stringify(clean));return clean;}
 function matches(status,filter){return !filter||(filter==='unmarked'?!status:status===filter);}
 const date=iso=>iso?iso.slice(8,10)+'.'+iso.slice(5,7)+'.'+iso.slice(0,4):'';
 // Where a registered course stands today, derived from its dates. Courses without fixed dates are marked as done by hand.
 function phase(status,timing,today){
  if(status==='completed')return {key:'completed',label:'Absolviert (eigene Angabe)'};
  if(status!=='registered')return null;
  const t=timing||{status:'unknown'};
  if(t.status==='future')return {key:'upcoming',label:'Angemeldet · Start am '+date(t.start)};
  if(t.status==='ongoing'||t.status==='unknown')return {key:'selfpaced',label:'Angemeldet · jederzeit machbar – nach Abschluss als absolviert markieren'};
  const over=t.status==='ended'||(!t.end&&t.start<today);
  if(over)return {key:'finished',label:'Angemeldet · Kurs ist vorbei – als absolviert markieren?'};
  return {key:'running',label:'Angemeldet · läuft gerade'+(t.end?' bis '+date(t.end):'')};
 }
 const api={key,statuses,validate,read,write,matches,phase};root.WbaCourseProgress=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
