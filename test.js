let XMLHttpRequest = require('xhr2');
let req=new XMLHttpRequest();

req.open("get","http://54.243.128.73:3000/api/attractions",true);
req.send();
req.onload=function(){
    // if(req.status == 200){
let str =JSON.parse(req.responseText);
for (i=0;i<12;i++){
names=str.data[i].name;
mrts=str.data[i].mrt;
categories=str.data[i].category;
images=str.data[i].images[0]
        // let nametextAll=document.querySelectorAll("#nametext");}
        // // for (i=0;i<12;i++){
        //         //文字
        //         name0=str.result.results[i].stitle
        //         n0[i].textContent =name0;
console.log(images)}
}