(function(root){
 'use strict';
 const fold=value=>String(value??'').toLocaleLowerCase('de-AT');
 const viennaToday=()=>new Intl.DateTimeFormat('sv-SE',{timeZone:'Europe/Vienna'}).format(new Date());
 function timing(course,today=viennaToday()){
  if(fold(course.term).trim()==='wird laufend angeboten')return {status:'ongoing',started:false,start:null,end:null};
  const dates=[...String(course.term||'').matchAll(/(\d{2})\.(\d{2})\.(\d{4})/g)];
  function parse(m){if(!m)return null;const [,d,month,y]=m;if(+y<2000||+y>2100)return null;const date=new Date(Date.UTC(+y,+month-1,+d));return date.getUTCFullYear()===+y&&date.getUTCMonth()+1===+month&&date.getUTCDate()===+d?y+'-'+month+'-'+d:null;}
  const start=parse(dates[0]),end=dates.length>1?parse(dates[dates.length-1]):null;
  if(!start||(dates.length>1&&!end)||(end&&end<start))return {status:'unknown',started:false,start:null,end:null};
  return {status:end&&end<today?'ended':start<today?'started':start===today?'today':'future',started:start<today,start,end};
 }
 // Date groups for the start-date chips. A start today counts as already started: live courses cannot be joined any more.
 const dateGroups=['future','ongoing','unknown','started','ended'],defaultDateGroups=['future','ongoing','unknown'];
 function dateGroup(course,today){const s=timing(course,today).status;return s==='today'?'started':s;}
 function timingMatches(course,groups,today){return !Array.isArray(groups)||groups.includes(dateGroup(course,today));}
 // One place filter: "online", "nationwide" or "state:<Bundesland>", all read from the wba place field.
 function placeMatches(course,place){if(place==='online')return course.online===true;if(place==='nationwide')return course.nationwide===true;if(place.startsWith('state:'))return course.states.includes(place.slice(6));return true;}
 const displayDate=iso=>/^\d{4}-\d{2}-\d{2}$/.test(iso||'')?iso.slice(8,10)+'.'+iso.slice(5,7)+'.'+iso.slice(0,4):'';
 // Lernformat: the original classification wins. If it is "unklar", the course texts are searched for clear cues.
 // Exactly one kind of cue → that format (marked as derived, with the text passage); none or conflicting cues → stays "unklar".
 // "Wird laufend angeboten" alone says nothing about the format (it usually just means no date was entered).
 const formatCues=[
  // Only phrases that describe how the course itself runs. Words such as "vor Ort", "Seminarraum", "Webinar" or
  // "Selbststudium" also appear in site menus or as one part of a mixed course and caused wrong results.
  ['Blended',/auch online|tlw\. module|teilweise online|modul \d+ "?live-online|präsenz und (?:einige[n]? )?online|präsenz- und online|online und (?:in )?präsenz|online- und präsenz|hybrid|blended/i],
  ['asynchrones E-Learning',/selbstlernkurs|im eigenen tempo|in ihrem eigenen tempo|zeit- und ortsunabhängig|ohne zeitliche bindung|on[- ]demand/i],
  ['Live-Webinar',/live-online|online-live|liveonline|(?:via|per) (?:zoom|ms teams|microsoft teams)|kursort:? online|videokonferenz/i],
  ['Präsenz',/präsenzunterricht|präsenzveranstaltung|präsenztermine?\b|präsenzseminar|in präsenz statt|findet in präsenz|als präsenz/i]];
 // A passage naming three or more formats side by side is a filter menu of the provider site, not a course statement.
 const formatWords=/präsenz|live-online|online-live|e-learning|blended|webinar|selbststudium/gi;
 const isMenu=text=>new Set((text.match(formatWords)||[]).map(w=>w.toLowerCase())).size>=3;
 function cueIn(text,re){const g=new RegExp(re.source,'gi');let m;while((m=g.exec(text))){const a=Math.max(0,m.index-45),b=Math.min(text.length,m.index+m[0].length+45),win=text.slice(a,b);if(!isMenu(win))return (a?'…':'')+win.replace(/\s+/g,' ').trim()+(b<text.length?'…':'');}return null;}
 function cuesIn(sources){const found=[];for(const [format,re] of formatCues)for(const s of sources){const evidence=cueIn(s.text,re);if(evidence){found.push({format,evidence,source:s.label});break;}}
  // A mixed statement ("Präsenz und Online-Live") explains the single cues it contains.
  return found.some(f=>f.format==='Blended')?found.filter(f=>f.format==='Blended'):found;}
 const formatCache=new WeakMap();
 function formatInfo(course){
  if(course.format&&course.format!=='unklar')return {format:course.format,inferred:false};
  if(formatCache.has(course))return formatCache.get(course);
  // Only the wba entry (first source) counts. Provider pages contain menus, teasers for other courses and topic texts,
  // e.g. every BFI Wien page advertises some other course as "Live-Online", which led to wrong results.
  const found=cuesIn((course.sources||[]).slice(0,1));
  const result=found.length===1?{format:found[0].format,inferred:true,evidence:found[0].evidence,source:found[0].source}:{format:'unklar',inferred:false,conflict:found.length>1?found.map(f=>f.format):null};
  formatCache.set(course,result);return result;}
 const profileOrder=['wba-Zertifikat','wba-Basisbildungszertifikat','wba-Diplom Lehren/Gruppenleitung/Training','wba-Diplom Beratung','wba-Diplom Bildungsmanagement','wba-Diplom Bibliothekswesen','Diplomübergreifend'];
 function competencyGroups(courses,profile=''){
  const groups=new Map();
  for(const course of courses)for(const c of course.competencies){if(profile&&c.profile!==profile)continue;const key=c.profile;if(!groups.has(key))groups.set(key,new Set());groups.get(key).add(c.name);}
  return [...groups].sort(([a],[b])=>(profileOrder.indexOf(a)<0?99:profileOrder.indexOf(a))-(profileOrder.indexOf(b)<0?99:profileOrder.indexOf(b))||a.localeCompare(b,'de')).map(([profile,names])=>({profile,names:[...names].sort((a,b)=>a.localeCompare(b,'de'))}));
 }
 function assignmentMatches(c,filters){return(!filters.profile||c.profile===filters.profile)&&(!filters.competency||c.name===filters.competency)&&(!filters.competencyProfile||c.profile===filters.competencyProfile);}
 // Search terms: separate words must all occur (anywhere); text in quotes stays one fixed phrase. No synonyms, no stemming.
 function terms(query){const text=String(query??'').replace(/[„“”«»]/g,'"'),out=[],re=/"([^"]*)"?|(\S+)/g;let m;while((m=re.exec(text))){const t=fold((m[1]??m[2]??'').trim());if(t&&!out.includes(t))out.push(t);}return out;}
 const escape=s=>s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&'),wordCache=new Map();
 // Whole words: the term must not touch another letter or digit, so punctuation and text start/end count as boundaries.
 function wordRe(term){if(!wordCache.has(term))wordCache.set(term,new RegExp('(?<![\\p{L}\\p{N}])'+escape(term)+'(?![\\p{L}\\p{N}])','gu'));const re=wordCache.get(term);re.lastIndex=0;return re;}
 function ranges(text,list,whole=false){const t=fold(text),found=[];for(const term of list){if(whole){const re=wordRe(term);let m;while((m=re.exec(t)))found.push([m.index,m.index+m[0].length]);}else{let i=t.indexOf(term);while(i!==-1){found.push([i,i+term.length]);i=t.indexOf(term,i+term.length);}}}found.sort((a,b)=>a[0]-b[0]||b[1]-a[1]);const merged=[];for(const r of found){const last=merged[merged.length-1];if(last&&r[0]<=last[1])last[1]=Math.max(last[1],r[1]);else merged.push([...r]);}return merged;}
 function hits(text,term,whole){return whole?wordRe(term).test(fold(text)):fold(text).includes(term);}
 function matchingSources(course,query,whole=false){const list=terms(query);return list.length?course.sources.filter(s=>list.some(term=>hits(s.text,term,whole))):[];}
 function matches(course,filters){
  const list=terms(filters.query);if(list.length&&!list.every(term=>course.sources.some(s=>hits(s.text,term,filters.whole))))return false;
  if(filters.profile||filters.competency){if(!course.competencies.some(c=>assignmentMatches(c,filters)))return false;}
  if(filters.type&&course.type!==filters.type)return false;
  if(filters.format&&formatInfo(course).format!==filters.format)return false;
  if(!timingMatches(course,filters.dates,filters.today))return false;
  if(filters.place&&!placeMatches(course,filters.place))return false;
  if(filters.state&&!course.states.includes(filters.state))return false;
  for(const key of ['online','nationwide'])if(filters[key]&&course[key]!== (filters[key]==='yes'))return false;
  return true;
 }
 function compare(sort){return(a,b)=>{
  let n=0;
  if(sort==='title')return a.title.localeCompare(b.title,'de');
  const [field,direction]=sort.split('-');const key=field==='span'?'span':field;
  const av=a[key],bv=b[key];
  if(av==null&&bv!=null)return 1;if(bv==null&&av!=null)return -1;
  if(av!=null&&bv!=null)n=(av-bv)*(direction==='desc'?-1:1);
  return n||a.title.localeCompare(b.title,'de');
 };}
 const api={fold,terms,ranges,matchingSources,matches,compare,formatInfo,competencyGroups,assignmentMatches,profileOrder,timing,timingMatches,placeMatches,displayDate,dateGroup,dateGroups,defaultDateGroups,viennaToday};root.WbaSearch=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
