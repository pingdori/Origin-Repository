// function enter(event) {
// 	if (event.keyCode == 13) {
// 		searchKeyword();
// 	}
// }
//首頁代入瀑布流
async function index(endpoint, pages) {
	//連接
	await fetch(`${endpoint}?page=${pages}`, {
		method: "get",
		mode: "cors",
		headers: {
			"Content-Type": "application/json"
		}
	}, ).then(res => {
		return res.json();
	}).then(jsonData => {
		countData = jsonData.data.length;
		let items = document.querySelector("#item");
		for (i = 0; i < jsonData.data.length; i++) {
			id = jsonData.data[i].id;
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
        <p id="nametext"><a href="http://54.243.128.73:3000/attraction/${id}">${names}<a></p>
        <div class="texts">
        <p id="mrttext">${mrts}</p>
        <div class="textContainer"></div>
        <p id="text">${categories}</p>`;
			items.parentNode.appendChild(post);
		}
		nextPageData(jsonData);
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
		id = jsonData.data[i].id;
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
        <p id="nametext"><a href="http://54.243.128.73:3000/api/attractions/${id}">${names}<a></p>
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
let modalDialog = document.querySelector(".modal-dialog");
let bgcBlack = document.querySelector(".black");
let modalDialog1 = document.querySelector(".modal-dialog1");
let Xbutton = document.querySelector(".Xbutton");
let signInError = document.querySelector(".signInError");
let signupError = document.querySelector('.signupError');

function loginClock() {
	bgcBlack.setAttribute("id", "black");
	modalDialog.setAttribute("id", "modal-dialog");
}

function onclickBlack() {
	bgcBlack.setAttribute("id", "hide");
	modalDialog.setAttribute("id", "hide");
	modalDialog1.setAttribute("id", "hide");
	if (signInError.id == "signInError") {
		signInError.setAttribute("id", "hide");
	}
	if (signupError.id == "signupError") {
		signupError.setAttribute("id", "hide");
	}
}

function onclickXbutton() {
	bgcBlack.setAttribute("id", "hide");
	modalDialog.setAttribute("id", "hide");
	modalDialog1.setAttribute("id", "hide");
	if (signInError.id == "signInError") {
		signInError.setAttribute("id", "hide");
	}
	if (signupError.id == "signupError") {
		signupError.setAttribute("id", "hide");
	}
}

function onclickloginHelp() {
	modalDialog.setAttribute("id", "hide");
	modalDialog1.setAttribute("id", "modalDialog1");
}

function onclickloginHelp1() {
	modalDialog.setAttribute("id", "modalDialog");
	modalDialog1.setAttribute("id", "hide");
}
let url = "http://54.243.128.73:3000/api/user";
async function getSignupData() {
	let signupError2 = document.querySelector(".signupError2")
	let signupError = document.querySelector('.signupError');
	let signupOk = document.querySelector('.signupOk');
	let modalDialog1 = document.querySelector('.modal-dialog1');
	let nameElement = document.getElementById('username');
	let username = nameElement.value;
	let emailElement1 = document.getElementById('email1');
	let email1 = emailElement1.value;
	let passwordElement1 = document.getElementById('password1');
	let password1 = passwordElement1.value;
	let data = {
		"username": username,
		"email": email1,
		"password": password1
	};
	fetch(url, {
		method: "POST",
		body: JSON.stringify(data),
		headers: new Headers({
			"Content-Type": "application/json"
		})
	}).then(res => {
		return res.json()
	}).then(jsonData => {
		modalDialog1.style.height = '352px';
		if (jsonData.error) {
			signupError.setAttribute("id", "signupError");
			signupOk.setAttribute("id", "hide");
		} else if (jsonData.ok) {
			signupError.setAttribute("id", "hide0");
			signupOk.setAttribute("id", "signupOk");
		}
	}).catch(err => {})
}
async function getSignInData() {
	let loginClick = document.querySelector(".loginClick");
	let logoutClick = document.querySelector(".logoutClick");
	let signInError = document.querySelector(".signInError");
	let emailElement = document.getElementById('email');
	let email = emailElement.value;
	let passwordElement = document.getElementById('password');
	let password = passwordElement.value;
	let data = {
		"email": email,
		"password": password
	};
	let modalDialog = document.querySelector('#modal-dialog');
	await fetch(url, {
		method: "PATCH",
		body: JSON.stringify(data),
		headers: new Headers({
			"Content-Type": "application/json"
		})
	}).then(res => {
		return res.json()
	}).then(jsonData => {
		if (jsonData.error) {
			signInError.setAttribute("id", "signInError");
			modalDialog.style.height = '295px';
		} else if (jsonData.ok) {
			signInError.setAttribute("id", "hide");
			loginClick.setAttribute("id", "hide");
			logoutClick.setAttribute("id", "logoutClick");
			reload();
		}
	})
}
async function userCheck() {
	let loginClick = document.querySelector(".loginClick");
	let logoutClick = document.querySelector(".logoutClick");
	let fetchApi = await fetch(url);
	let jsonData = await fetchApi.json();
	if (jsonData.data.email) {
		loginClick.setAttribute("id", "hide");
		logoutClick.setAttribute("id", "logoutClick");
	} else if (jsonData.data == null) {
		loginClick.setAttribute("id", "loginClick");
		logoutClick.setAttribute("id", "hide");
	}
}
async function logoutClick() {
	let request = {
		method: "DELETE",
	}
	let loginClick = document.querySelector(".loginClick");
	let logoutClick = document.querySelector(".logoutClick");
	let fetchApi = await fetch(url, request);
	let jsonData = await fetchApi.json();
	if (jsonData.ok) {
		loginClick.setAttribute("id", "loginClick");
		logoutClick.setAttribute("id", "hide");
	}
	history.go(0);
}
async function bookingAttraction() {
	let url = "http://54.243.128.73:3000/api/user";
	let fetchApi = await fetch(url);
	let jsonData = await fetchApi.json();
	if (jsonData.data.email) {
		// document.location.href="/booking";
		document.location.href = "http://54.243.128.73:3000/booking";
	} else if (jsonData.data == "null") {
		console.log("hi");
		loginClock();
	}
}

function validateEmail() {
	let inputsValue = document.forms["loginForm"]["signinEmail"].value;
	let inputs = document.querySelector("#email")
	let atpos = inputsValue.indexOf("@");
	let dotpos = inputsValue.lastIndexOf(".");
	if (atpos < 1 || dotpos < atpos + 2 || dotpos + 2 >= inputsValue.length) {
		inputs.classList.add("invalid");
		inputs.classList.remove("valid");
		inputs.style.border = "#f5898f 2px solid";
	} else {
		inputs.classList.add("valid");
		inputs.classList.remove("invalid");
		inputs.style.border = "#337788 2px solid";
	}
}

function validateEmail1() {
	let inputsValue = document.forms["signupForm"]["signupEmail"].value;
	let inputs = document.querySelector("#email1")
	let atpos = inputsValue.indexOf("@");
	let dotpos = inputsValue.lastIndexOf(".");
	if (atpos < 1 || dotpos < atpos + 2 || dotpos + 2 >= inputsValue.length) {
		inputs.classList.add("invalid");
		inputs.classList.remove("valid");
		inputs.style.border = "#f5898f 2px solid";
	} else {
		inputs.classList.add("valid");
		inputs.classList.remove("invalid");
		inputs.style.border = "#337788 2px solid";
	}
}

function validateButton() {
	let x = document.forms["loginForm"]["signinPassword"].value;
	let loginbutton = document.querySelector("#loginbutton")
	if (x == null || x == "") {
		return false;
	} else {
		loginbutton.focus();
	}
}

function validateButton1() {
	let x = document.forms["signupForm"]["signupPassword"].value;
	let signupbutton = document.querySelector("#signupbutton")
	if (x == null || x == "") {
		return false;
	} else {
		signupbutton.focus();
	}
}

function validateButton2() {
	let x = document.forms["searchForm"]["searchData"].value;
	let submit = document.querySelector("#submit")
	if (x == null || x == "") {
		reload();
	} else {
		submit.focus();
	}
}

function reload() {
	history.go(0);
}
