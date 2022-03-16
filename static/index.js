function enter(event) {
    if (event.keyCode == 13) {
        searchKeyword();
    }
}
//首頁代入瀑布流
async function index(endpoint, pages) {
//連接
await fetch(`${endpoint}?page=${pages}`, {
        method: "get",
        mode: "cors",
        headers: {
            "Content-Type": "application/json"
        }
    }, )
    .then(res => {
        return res.json();
    })
    .then(jsonData => {
        countData = jsonData.data.length;
        let items = document.querySelector("#item");
        for (i = 0; i < jsonData.data.length; i++) {
            names = jsonData.data[i].name;
            mrts = jsonData.data[i].mrt;
            categories = jsonData.data[i].category;
            images = jsonData.data[i].images[0];
            let imgEle = document.createElement('img');
            imgEle.setAttribute('src', images);
            const post = document.createElement('div');
            post.setAttribute("id", "item0");
            post.innerHTML = `
        <div id="img"><img src="${images}"></div>
        <p id="nametext">${names}</p>
        <div class="texts">
        <p id="mrttext">${mrts}</p>
        <div class="textContainer"></div>
        <p id="text">${categories}</p>`;
            items.parentNode.appendChild(post);
        }
        nextPageData(jsonData);
    })
    .catch(err => {  
    })
}
//傳入首頁瀑布流
const endpoint = "http://54.243.128.73:3000/api/attractions";
index(endpoint, 0);

//尋找資料>給定初次搜尋某關鍵字的頁數
function searchKeyword() {
let keywordValue = document.querySelector("#searchData").value;
let pages = 0;
if (document.querySelector("#item2")) {
    let item2 = document.querySelectorAll("#item2");
    let main = document.querySelector("#searchResult");
    let footer = document.querySelector("footer");
    let count = searchResult.childElementCount;
    for (let i = 0; i < count - 1; i++) {
        if (document.querySelectorAll("#item2")) {
            searchResult.removeChild(item2[i]);
        }
    }
}
getError(pages, keywordValue);
}
//判斷是否為error，否則dataPrint尋找資料>獲取資訊
async function getError(pages, searchValue) {
let keywordValue = document.querySelector("#searchData").value;
let fetchApi = await fetch(`http://54.243.128.73:3000/api/attractions?page=${pages}&keyword=${keywordValue}`);
let jsonData = await fetchApi.json();
if (jsonData.error == "true") {
    if (document.querySelector("#error")) {
        let error = document.querySelector("#error");
    }
    showError();
} else {
    if (document.querySelector("#error")) {
        let error = document.querySelector("#error");
        error.setAttribute("id", "hide0");
    }
    if (document.querySelector("#hide")) {
        let searchResult = document.querySelector("#hide");
        searchResult.setAttribute("id", "searchResult");
    }
    dataPrint(jsonData);
}
}
//error頁面調整
function showError() {
if (document.querySelector("main")) {
    let main = document.querySelector("main");
    main.setAttribute("id", "hide")
}
let hide = document.querySelector("#hide0");
hide.setAttribute("id", "error");
}

function dataPrint(jsonData) {
if (document.querySelector("#main")) {
    let mains = document.querySelector("#main");
    mains.remove();
}
let searchResult = document.querySelector("#searchResult");
let items = document.querySelector("#item1");
countData = jsonData.data.length;
for (i = 0; i < jsonData.data.length; i++) {
    names = jsonData.data[i].name;
    mrts = jsonData.data[i].mrt;
    categories = jsonData.data[i].category;
    images = jsonData.data[i].images[0];
    let imgEle = document.createElement('img');
    imgEle.setAttribute('src', images);
    const post = document.createElement('div');
    post.setAttribute("id", "item2");
    post.innerHTML = `
        <div id="img"><img src="${images}"></div>
        <p id="nametext">${names}</p>
        <div class="texts">
        <p id="mrttext">${mrts}</p>
        <div class="textContainer"></div>
        <p id="text">${categories}</p>`;
    items.parentNode.appendChild(post);
}
nextdata(jsonData);
}
function nextdata(jsonData) {
const pages = jsonData.nextpage;
if (pages != "null") {
    searchInfiniteScroll(pages);
}
}
///下一頁資訊
function nextPageData(jsonData) {
const pages = jsonData.nextpage;
if (pages != "null") {
    infiniteScroll(pages);
}
}
//首頁瀑布流
function infiniteScroll(pages) {
let keywordValue = document.querySelector("#searchData").value;
const root = document.querySelector('#root');
const rootObserve = document.querySelector('#rootContainer')
const callback = ([entry]) => {
    if (entry.isIntersecting) {
        let ready = false;

        if (pages) {
            index("http://54.243.128.73:3000/api/attractions", pages);
            pages = false;
        } else if (document.querySelector("#hide")) {
            observer.unobserve(rootObserve);
        }
    }
}
const options = {
    root: root,
    rootMargin: "-40px",
    threshold: 1
}
const observer = new IntersectionObserver(callback, options);
observer.observe(rootObserve);
}
//搜尋系統瀑布流
function searchInfiniteScroll(pages) {
let keywordValue = document.querySelector("#searchData").value;
const root = document.querySelector('#root0');
const rootObserve = document.querySelector('#rootContainer0')
const callback = ([entry]) => {
    if (entry.isIntersecting) {
        let ready = false;
        if (pages) {
            getError(pages, keywordValue);
            pages = false;
        }
    } else if (pages == null) {
        observer.unobserve(rootObserve);
        ready = false;
    }
}
const options = {
    root: root,
    rootMargin: "-40px",
    threshold: 1
}
const observer = new IntersectionObserver(callback, options);
observer.observe(rootObserve);
}
