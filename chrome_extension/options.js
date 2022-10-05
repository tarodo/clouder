const api_url = "http://127.0.0.1:8007"

let startSession = document.getElementById("loginMe");

async function LoginMe(username, password) {
	let details = {
		'username': username,
		'password': password
	};

	chrome.storage.sync.get('access_token', function(result) {
		console.log('Value currently is ' + result.access_token);
	});

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

}

startSession.addEventListener("click", async (event) => {
  event.preventDefault();
  let username = document.getElementById("usernameInput").value
  let password = document.getElementById("passwordInput").value
  let data = await LoginMe(username, password)

});