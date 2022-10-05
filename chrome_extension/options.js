const api_url = "http://127.0.0.1:8007"

let startSession = document.getElementById("loginMe");

showToken();

function showToken() {
	chrome.storage.sync.get('access_token', function(result) {
		let token =  result.access_token;
		document.getElementById("statusLogin").innerText = "Your Token:\n" + token;
	});
}

async function LoginMe(username, password) {
	let details = {
		'username': username,
		'password': password
	};

	let formBody = [];
	for (const property in details) {
		const encodedKey = encodeURIComponent(property);
		const encodedValue = encodeURIComponent(details[property]);
		formBody.push(encodedKey + "=" + encodedValue);
	}
	formBody = formBody.join("&");

	const response = await fetch(`${api_url}/login/access-token`, {
		method: 'POST',
		headers: {
			'Accept': 'application/json',
			'Content-Type': 'application/x-www-form-urlencoded'
		},
		body: formBody
	}).then(response => response.json()).then(data => {
		const token = data["access_token"]
		if (token) {
			chrome.storage.sync.set({ access_token: data["access_token"] });
		} else {
			console.log(data)
		}

	});
	showToken();
}

startSession.addEventListener("click", async (event) => {
  event.preventDefault();
  let username = document.getElementById("usernameInput").value
  let password = document.getElementById("passwordInput").value
  await LoginMe(username, password)

});