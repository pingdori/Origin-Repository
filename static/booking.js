function enter(event) {
	if (event.keyCode == 13) {
		searchKeyword();
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
let apiUserUrl = "http://54.243.128.73:3000/api/user";
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
	fetch(apiUserUrl, {
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
			signupError.setAttribute("id", "hide");
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
async function bookingUserCheck() {
	let loginClick = document.querySelector(".loginClick");
	let logoutClick = document.querySelector(".logoutClick");
	let userName = document.querySelector("#userName");
	let nameinfor = document.querySelector("#nameinfor");
	let mailinfor = document.querySelector("#mailinfor");
	let url = "http://54.243.128.73:3000/api/user";
	let fetchApi = await fetch(url);
	let jsonData = await fetchApi.json();
	if (jsonData.data == "null") {
		document.location.href = "http://54.243.128.73:3000/";
	} else {
		loginClick.setAttribute("id", "hide");
		logoutClick.setAttribute("id", "logoutClick");
		userName.textContent = jsonData.data.name
		nameinfor.value = jsonData.data.name
		mailinfor.value = jsonData.data.email
		getBookingApi();
	}
}
let apiBookingUrl = "http://54.243.128.73:3000/api/booking"
async function getBookingApi() {
	let fetchApi = await fetch(apiBookingUrl);
	let jsonData = await fetchApi.json();
	if (jsonData.data) {
		let titleText = document.querySelector(".inforAttractions");
		let bookingDate = document.querySelector("#bookingDate");
		let bookingTime = document.querySelector("#bookingTime");
		let bookingFee = document.querySelector("#bookingFee");
		let bookingAddress = document.querySelector("#bookingAddress");
		let bookingimg = document.querySelector("#img");
		titleText.textContent = jsonData.data.attraction.name
		bookingDate.textContent = jsonData.data.date
		bookingAddress.textContent = jsonData.data.attraction.address
		bookingimg.innerHTML = `<img src="${jsonData.data.attraction.image}"></img>`
		if (jsonData.data.time == "morning") {
			bookingTime.textContent = "早上9點至中午12點"
		} else {
			bookingTime.textContent = "下午1點至下午4點"
		}
		if (jsonData.data.price == "2000") {
			bookingFee.textContent = "新台幣 2000元"
		} else {
			bookingFee.textContent = "新台幣 2500元"
		}
	} else if (jsonData.error) {
		let main = document.querySelector("#main");
		let inforTexthHide = document.querySelector(".inforTextHide");
		let headline = document.querySelector("#headline");
		main.setAttribute("id", "hide");
		inforTexthHide.setAttribute("id", "inforTexthHide");
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
		location.reload("http://54.243.128.73:3000/attraction/");
	}
	reload()
}
async function deleteBooking() {
	let request = {
		method: "DELETE",
	}
	let fetchApi = await fetch(apiBookingUrl, request);
	let jsonData = await fetchApi.json();
	if (jsonData.ok) {
		reload();
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

function input_onchange(me) {
	if (me.value.length < me.getAttribute('maxlength') - 1) {
		return;
	}
	var i;
	var elements = me.form.elements;
	for (i = 0, numElements = elements.length; i < numElements; i++) {
		if (elements[i] == me) {
			break;
		}
	}
	elements[i + 1].focus();
}
async function bookingAttraction() {
	let url = "http://54.243.128.73:3000/api/user";
	let fetchApi = await fetch(url);
	let jsonData = await fetchApi.json();
	if (jsonData.data.email) {
		document.location.href = "http://54.243.128.73:3000/booking";
	} else if (jsonData.data == "null") {
		loginClock();
	}
}


let _APPKEY_='app_kc2JI7ljN1SH0OU6EDNMRKHZkp0n3wIGXK1G7gCh5v4dPnPX1wEtL0nRy4dA';
    TPDirect.setupSDK(124033,_APPKEY_, 'sandbox');
    let fields = {
        number: {
            element: '#card-number',
            placeholder: '**** **** **** ****'
        },
        expirationDate: {
            element: document.getElementById('card-expiration-date'),
            placeholder: 'MM / YY'
        },
        ccv: {
            element: '#card-ccv',
            placeholder: 'ccv'
        }
    }

    let argument = {
        fields: fields,
        styles: {
            'input': {
                'color': 'black',
                'font-family': 'Noto Sans TC',
                'font-style': 'normal',
                'font-size': '16px',
                'line-height': '21px',
                'font-weight': 'normal',
            },
            ':focus': {
                'color': 'black'
            },
            '.valid': {
                'color': 'green'
            },
            '.invalid': {
                'color': 'red'
            },
            '@media screen and (max-width: 400px)': {
                'input': {
                    'color': 'orange'
                }
            }
        }
    };
    TPDirect.card.setup(argument);

    function onSubmit(event) {
    // event.preventDefault()

    // 取得 TapPay Fields 的 status
    const tappayStatus = TPDirect.card.getTappayFieldsStatus()

    // 確認是否可以 getPrime
    if (tappayStatus.canGetPrime === false) {
        console.log('can not get prime')
        return
    }
    // Get prime
    TPDirect.card.getPrime((result) => {
        if (result.status !== 0) {
            console.log('get prime error ' + result.msg)
            return
        }
        else{
			fetchOrderPostAPi();
			console.log('get prime 成功')
		}

        // send prime to your server, to pay with Pay by Prime API .
        // Pay By Prime Docs: https://docs.tappaysdk.com/tutorial/zh/back.html#pay-by-prime-api
    })
}

async function fetchOrderPostAPi() {
	let fetchApi = await fetch(apiBookingUrl);
	let jsonData = await fetchApi.json();
	if (jsonData.data) {
		let price=jsonData.data.price;
		let id=jsonData.data.attraction.id;
		let name =jsonData.data.attraction.name;
		let address=jsonData.data.attraction.address;
		let image =jsonData.data.attraction.image;
		let date =jsonData.data.date;
		let time =jsonData.data.time;
		let userName=document.forms["bookingForm"]["nameinfor"].value;
		let email=document.forms["bookingForm"]["mailinfor"].value;
		let phone= document.forms["bookingForm"]["phoneinfor"].value;
		let data = {
			"prime": null,
			"order": {
			  "price":price,
			  "trip": {
				"attraction": {
				  "id":id,
				  "name":name,
				  "address":address,
				  "image":image
				},
				"date": date,
				"time": time
			  },
			  "contact": {
				"name": userName,
				"email": email,
				"phone": phone
			  }
			}
		  }
		fetchOrderPost(data);
	}
	
}


let fetchOrderUrl="http://54.243.128.73:3000/api/orders"
async function fetchOrderPost(data){
	
	TPDirect.card.getPrime(async(result)=>{
		if(result.status===0){
			let tappayPrime=result.card.prime;
			data.prime=tappayPrime;
			console.log(data);
			
			let newHeaders=new Headers({
				"Content-Type": "application/json"
				});
			let fetchDetail={
				method: "POST",
				body:JSON.stringify(data),
				headers:newHeaders
				}
			let fetchData=await fetch(fetchOrderUrl,fetchDetail);
			let fetchJson=await fetchData.json();
			let fetchJsonData=fetchJson.data.number;
			console.log(fetchJson.data.number);
			deleteBooking();
			document.location.href=`http://54.243.128.73:3000/thankyou?number=${fetchJsonData}`;
		// fetch(apiUserUrl, {
		// 	method: "POST",
		// 	body: JSON.stringify(data),
		// 	headers: new Headers({
		// 		"Content-Type": "application/json"
		// 	})
	// })

}
	})
}

setTimeout(function () {
        
	document.getElementById("loader").style.display = "none";
	document.getElementById("loaderCon").style.display = "none";

}, 500);
