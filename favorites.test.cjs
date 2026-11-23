const test=require('node:test'),assert=require('node:assert/strict'),F=require('./favorites.js');
function memory(){const m=new Map();return{getItem:k=>m.has(k)?m.get(k):null,setItem:(k,v)=>m.set(k,String(v))};}
const courses=[{id:'1',title:'Trainerin DaF',provider:'BFI OÖ',term:'01.03.2027',url:'https://login.wba.or.at/bildungsangebot/1',links:['https://www.bfi-ooe.at/kurs/1']},{id:'2',title:'Moderation',provider:'BFI Wien',term:'',url:'https://login.wba.or.at/bildungsangebot/2',links:[]}];

test('Herz setzt und entfernt Kurse in der Reihenfolge des Hinzufügens',()=>{let list=[];list=F.toggle(list,'2');list=F.toggle(list,'1');assert.deepEqual(list,['2','1']);assert.deepEqual(F.toggle(list,'2'),['1']);});
test('Merkliste wird gespeichert und wieder gelesen',()=>{const s=memory();F.write(s,['1','2'],['1','2']);assert.deepEqual(F.read(s,['1','2']),['1','2']);assert.deepEqual(F.read(memory(),['1']),[]);});
test('Nicht mehr vorhandene Kurse und Doppelte fallen still weg',()=>{const s=memory();s.setItem(F.key,JSON.stringify(['1','99','1']));assert.deepEqual(F.read(s,['1','2']),['1']);});
test('Ungültige Merkliste wird abgelehnt',()=>{assert.throws(()=>F.clean({a:1}));assert.throws(()=>F.clean(['<script>']));});
test('Anmeldelink bevorzugt die Anbieterseite, sonst wba',()=>{assert.equal(F.bookingUrl(courses[0]),'https://www.bfi-ooe.at/kurs/1');assert.equal(F.bookingUrl(courses[1]),'https://login.wba.or.at/bildungsangebot/2');});
test('Kopierte Liste enthält Titel, Anbieter und Link',()=>{assert.equal(F.asText(['2','1'],courses),'1. Moderation\n   BFI Wien\n   https://login.wba.or.at/bildungsangebot/2\n\n2. Trainerin DaF\n   BFI OÖ · 01.03.2027\n   https://www.bfi-ooe.at/kurs/1');});
