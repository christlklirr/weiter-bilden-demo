(function(root){
 'use strict';
 // Personal course list: hearts (gemerkt) and participation status (angemeldet/absolviert), kept in this browser only.
 // The course list shows every course that is hearted or has a status.
 function create(storage,courseIds,C=root.WbaCourseProgress,F=root.WbaFavorites){
  let progress={},favorites=[],ok=true;const listeners=[];
  function load(){ok=true;try{progress=C.read(storage,courseIds);}catch{progress={};ok=false;}try{favorites=F.read(storage,courseIds);}catch{favorites=[];ok=false;}}
  // Ask the browser once to keep this site's storage instead of clearing it automatically (e.g. when space runs low).
  // Asked on the first change, not on page load, because Firefox shows a permission prompt for it.
  let persistAsked=false;
  function keep(){if(persistAsked)return;persistAsked=true;const s=typeof navigator!=='undefined'&&navigator.storage;if(s&&s.persist&&s.persisted)s.persisted().then(p=>p||s.persist()).catch(()=>{});}
  function save(){try{C.write(storage,progress,courseIds);F.write(storage,favorites,courseIds);}catch{ok=false;}keep();}
  const emit=()=>{for(const fn of listeners)fn();};
  load();
  return {
   get ok(){return ok;},
   status:id=>progress[id]||'',
   isSaved:id=>favorites.includes(id),
   favorites:()=>[...favorites],
   progress:()=>({...progress}),
   ids(){return [...new Set([...favorites,...Object.keys(progress)])];},
   toggleSaved(id){favorites=F.toggle(favorites,id);save();emit();},
   setStatus(id,status){if(progress[id]===status)delete progress[id];else progress[id]=status;save();emit();},
   replace(nextFavorites,nextProgress){favorites=F.clean(nextFavorites,courseIds);progress=C.validate(nextProgress,courseIds);save();emit();},
   reload(){load();emit();},
   onChange(fn){listeners.push(fn);},
   keys:[C.key,F.key]
  };
 }
 // Backup file: current format plus the older course-progress and Kompetenzstand exports.
 function parseBackup(value,courseIds,C=root.WbaCourseProgress,F=root.WbaFavorites){
  if(!value||typeof value!=='object')throw new Error('Die Datei ist keine Kursliste dieser App.');
  if(value.type==='wba-kursliste')return {favorites:F.clean(value.favorites||[],courseIds),progress:C.validate(value.courses||{},courseIds)};
  if(value.type==='wba-course-progress')return {favorites:null,progress:C.validate(value.courses||{},courseIds)};
  if(value.courseProgress)return {favorites:null,progress:C.validate(value.courseProgress,courseIds)};
  throw new Error('Die Datei ist keine Kursliste dieser App.');
 }
 const api={create,parseBackup};root.WbaStore=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
