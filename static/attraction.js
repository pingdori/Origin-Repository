function enter(event) {
	if (event.keyCode == 13) {
		searchKeyword();
	}
}
async function attraction(endpoint, url) {
	//連接
	await fetch(`${endpoint}/${url}`, {
		method: "get",
		mode: "cors",
		headers: {
			"Content-Type": "application/json"
		}
	}, ).then(res => {
		return res.json();
	}).then(jsonData => {
		let titleText = document.querySelector(".titleText");
		let bookingText = document.querySelectorAll(".bookingText");
		let introduceText = document.querySelectorAll(".introduceText");
		let category = bookingText[0];
		let Mrt = bookingText[2];
		let description = introduceText[0];
		let address = introduceText[1];
		let transport = introduceText[2];
		let tab = document.querySelector("#tab");
		let lunboButton = document.querySelector(".lunboButton");
		let nameData = jsonData.data.name;
		let categories = jsonData.data.category;
		let mrtData = jsonData.data.mrt;
		let descriptionData = jsonData.data.description;
		let addressData = jsonData.data.address;
		let transportData = jsonData.data.transport;
		let test = transportData.split('&nbsp;');
		let imagesLength = jsonData.data.images.length;
		for (let i = 0; i < imagesLength; i++) {
			imagesData = jsonData.data.images[i];
			let imgEle = document.createElement('img');
			imgEle.setAttribute('src', imagesData);
			imgEle.setAttribute("class", "tabImg");
			tab.appendChild(imgEle);
		}
		for (let i = 1; i < imagesLength; i++) {
			let span = document.createElement('span');
			span.setAttribute("class", "tabBtn");
			span.setAttribute("num", [i]);
			lunboButton.appendChild(span);
		}
		titleText.textContent = nameData;
		category.textContent = categories;
		Mrt.textContent = mrtData;
		description.textContent = descriptionData;
		address.textContent = addressData;
		transport.textContent = test;
	})
}
let getUrlString = location.pathname;
let url = getUrlString.split("/");
let endpoint = "http://54.243.128.73:3000/api/attractions"
attraction(endpoint, url[2]);
//輪播
let pages = 0;
let time = setInterval(runFn, 6000);

function runFn() {
	let imgNum = document.getElementsByClassName('tabImg').length;
	pages = ++pages == imgNum ? 0 : pages;
	slideTo(pages);
}
//圓點
window.onclick = function() {
	let imgNum = document.getElementsByClassName('tabImg').length;
	let tbs = document.getElementsByClassName("tabBtn");
	for (let i = 0; i < imgNum; i++) {
		tbs[i].onclick = function() {
			clearInterval(time);
			slideTo(this.attributes['num'].value);
			pages = this.attributes['num'].value;
			time = setInterval(runFn, 6000);
		}
	}
}
let morning = document.getElementById("radioinput");
let afternoon = document.getElementById("radioinput1");
let bookingmoney1 = document.querySelector(".bookingmoney1");
let bookingmoney2 = document.querySelector(".bookingmoney2");
morning.onclick = function() {
	bookingmoney1.setAttribute("class", "hover");
	bookingmoney2.setAttribute("class", "bookingmoney2");
}
afternoon.onclick = function() {
	bookingmoney2.setAttribute("class", "hover");
	bookingmoney1.setAttribute("class", "bookingmoney1");
}
//上一張切換
let prve = document.getElementsByClassName("prve");
prve[0].onclick = function() {
	let imgNum = document.getElementsByClassName('tabImg').length;
	clearInterval(time);
	pages--;
	if (pages == -1) {
		pages = imgNum - 1;
	}
	slideTo(pages);
	time = setInterval(runFn, 6000);
}
//下一張切換
let next = document.getElementsByClassName("next");
next[0].onclick = function() {
	let imgNum = document.getElementsByClassName('tabImg').length;
	clearInterval(time);
	pages++;
	if (pages == imgNum) {
		pages = 0;
	}
	slideTo(pages);
	time = setInterval(runFn, 6000);
}
//輪播處理
function slideTo(index) {
	index = parseInt(index);
	let images = document.getElementsByClassName('tabImg');
	for (let i = 0; i < images.length; i++) {
		if (i == index) {
			images[i].style.display = 'inline';
		} else {
			images[i].style.display = 'none';
		}
	}
	let tabBtn = document.getElementsByClassName('tabBtn');
	for (let j = 0; j < tabBtn.length; j++) {
		if (j == index) {
			tabBtn[j].classList.add("hover");
			pages = j;
		} else {
			tabBtn[j].classList.remove("hover");
		}
	}
}
let modalDialog = document.querySelector(".modal-dialog");
let bgcBlack = document.querySelector(".black");
let modalDialog1 = document.querySelector(".modal-dialog1");
let Xbutton = document.querySelector(".Xbutton");

function loginClock() {
	bgcBlack.setAttribute("id", "black");
	modalDialog.setAttribute("id", "modal-dialog");
}

function onclickBlack() {
	bgcBlack.setAttribute("id", "hide");
	modalDialog.setAttribute("id", "hide");
	modalDialog1.setAttribute("id", "hide");
}

function onclickXbutton() {
	bgcBlack.setAttribute("id", "hide");
	modalDialog.setAttribute("id", "hide");
	modalDialog1.setAttribute("id", "hide");
}

function onclickloginHelp() {
	modalDialog.setAttribute("id", "hide");
	modalDialog1.setAttribute("id", "modalDialog1");
}

function onclickloginHelp1() {
	modalDialog.setAttribute("id", "modalDialog");
	modalDialog1.setAttribute("id", "hide");
}
let apiUserUrl = "http://54.243.128.73:3000/api/user";
async function getSignupData() {
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
	fetch(apiUserUrl, {
		method: "POST",
		body: JSON.stringify(data),
		headers: new Headers({
			"Content-Type": "application/json"
		})
	}).then(res => {
		return res.json()
	}).then(jsonData => {
		console.log(jsonData.ok);
		if (jsonData.error) {
			signupError.setAttribute("id", "signupError");
			signupOk.setAttribute("id", "hide");
			modalDialog1.style.height = '352px';
		} else if (jsonData.ok) {
			signupOk.setAttribute("id", "signupOk");
			signupError.setAttribute("id", "hide");
			modalDialog1.style.height = '352px';
		}
	})
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
	await fetch(apiUserUrl, {
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
			console.log(jsonData);
		} else if (jsonData.ok) {
			signInError.setAttribute("id", "hide");
			loginClick.setAttribute("id", "hide");
			logoutClick.setAttribute("id", "logoutClick");
			modalDialog.style.height = '275px';
			reload();
		}
	})
}
async function userCheck() {
	let url = "http://54.243.128.73:3000/api/user";
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
	let url = "http://54.243.128.73:3000/api/user";
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
		location.reload("http://54.243.128.73:3000/");
	}
	reload()
}

function reload() {
	history.go(0);
}