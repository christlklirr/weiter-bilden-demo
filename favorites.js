(function(root){
 'use strict';const key='weiter-bilden-demo.favorites.v1';
 // Saved courses are kept in the order they were added. Ids that no longer exist in the data are dropped, so a data refresh never breaks the list.
 function clean(value,allowedIds){if(!Array.isArray(value))throw new Error('Die Merkliste ist ungültig.');const allowed=allowedIds?new Set(allowedIds):null,seen=new Set();for(const id of value){if(typeof id!=='string'||!/^\d{1,12}$/.test(id))throw new Error('Die Merkliste enthält einen ungültigen Eintrag.');if((!allowed||allowed.has(id))&&!seen.has(id))seen.add(id);}return [...seen];}
 function read(storage,allowedIds){const text=storage.getItem(key);return text?clean(JSON.parse(text),allowedIds):[];}
 function write(storage,list,allowedIds){const value=clean(list,allowedIds);storage.setItem(key,JSON.stringify(value));return value;}
 function toggle(list,id){return list.includes(id)?list.filter(x=>x!==id):[...list,id];}
 function bookingUrl(course){return course.links&&course.links.length?course.links[0]:course.url;}
 function asText(list,courses){const byId=new Map(courses.map(c=>[c.id,c]));return list.map(id=>byId.get(id)).filter(Boolean).map((c,i)=>(i+1)+'. '+c.title+'\n   '+[c.provider,c.term].filter(Boolean).join(' · ')+'\n   '+bookingUrl(c)).join('\n\n');}
 const api={key,clean,read,write,toggle,bookingUrl,asText};root.WbaFavorites=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
