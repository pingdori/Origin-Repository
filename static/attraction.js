async function attraction(endpoint, url) {
    //連接
    await fetch(`${endpoint}/${url}`, {
            method: "get",
            mode: "cors",
            headers: {
                "Content-Type": "application/json"
            }
        },)
        .then(res => {
            return res.json();
        })
        .then(jsonData => {
            let titleText=document.querySelector(".titleText");
            let bookingText=document.querySelectorAll(".bookingText");
            let introduceText=document.querySelectorAll(".introduceText");
            let category=bookingText[0];
            let Mrt=bookingText[2];
            let description=introduceText[0];
            let address = introduceText[1];
            let transport = introduceText[2];
            let tab = document.querySelector("#tab");
            let lunboButton=document.querySelector(".lunboButton");
            let nameData = jsonData.data.name;
            let categories=jsonData.data.category;
            let mrtData =jsonData.data.mrt;
            let descriptionData = jsonData.data.description;
            let addressData = jsonData.data.address;
            let transportData = jsonData.data.transport;
            let test = transportData.split('&nbsp;');
            let imagesLength = jsonData.data.images.length;
            for(let i=0;i<imagesLength;i++){
                imagesData = jsonData.data.images[i];
                let imgEle = document.createElement('img');
                imgEle.setAttribute('src', imagesData);
                imgEle.setAttribute("class","tabImg");
                tab.appendChild(imgEle);
            }
            for(let i=1;i<imagesLength;i++){
                let span = document.createElement('span');
                span.setAttribute("class","tabBtn");
                span.setAttribute("num",[i]);
                lunboButton.appendChild(span);
            }
            titleText.textContent= nameData;
            category.textContent =categories;
            Mrt.textContent=mrtData;
            description.textContent=descriptionData;
            address.textContent=addressData;
            transport.textContent=test;
        })
    }
let getUrlString= location.pathname;
let url=getUrlString.split("/");
let endpoint="http://54.243.128.73:3000/api/attractions"
attraction(endpoint,url[2]);
    //輪播
    let pages=0;
    let time = setInterval(runFn,6000);
    function runFn(){      
        let imgNum = document.getElementsByClassName('tabImg').length;
        pages = ++pages == imgNum ? 0 : pages;
        slideTo(pages);
     }
     //圓點
     window.onclick = function  () {
        let imgNum = document.getElementsByClassName('tabImg').length;
        let tbs = document.getElementsByClassName("tabBtn");
        for(let i=0;i<imgNum;i++){
            tbs[i].onclick = function  () {
                clearInterval(time);
                slideTo(this.attributes['num'].value);
                pages = this.attributes['num'].value;
                time = setInterval(runFn,6000);
            }
        }
    }
    let morning = document.getElementById("radioinput");
    let afternoon = document.getElementById("radioinput1");
    let bookingmoney1 =  document.querySelector(".bookingmoney1");
    let bookingmoney2 =  document.querySelector(".bookingmoney2");
    morning.onclick = function(){
            bookingmoney1.setAttribute("class","hover");
            bookingmoney2.setAttribute("class","bookingmoney2");
        }
    afternoon.onclick = function(){
            bookingmoney2.setAttribute("class","hover");
            bookingmoney1.setAttribute("class","bookingmoney1");
        }
    //上一張切換
    let prve = document.getElementsByClassName("prve");
    prve[0].onclick = function () {
        let imgNum = document.getElementsByClassName('tabImg').length;
        clearInterval(time);
        pages--;
        if(pages == -1){
            pages = imgNum-1;
        }
        slideTo(pages);
        time = setInterval(runFn,6000);
    }
    //下一張切換
    let next = document.getElementsByClassName("next");
    next[0].onclick = function () {
        let imgNum = document.getElementsByClassName('tabImg').length;
        clearInterval(time);
        pages++;
        if(pages == imgNum){
            pages =0;
        }
        slideTo(pages);
        time = setInterval(runFn,6000);
    }
    //輪播處理
    function slideTo(index){
        index = parseInt(index);
        let images = document.getElementsByClassName('tabImg');
        for(let i=0;i<images.length;i++){
            if( i == index ){
                images[i].style.display = 'inline';         
            }else{
                images[i].style.display = 'none';
            }
        }
        let tabBtn = document.getElementsByClassName('tabBtn');
        for(let j=0;j<tabBtn.length;j++){
            if( j == index ){
                tabBtn[j].classList.add("hover");
                pages=j;
            }else{
                tabBtn[j].classList.remove("hover");
            }
        }
        
    }