let startSession = document.getElementById("loginMe");

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

		const response = await fetch("http://127.0.0.1:8007/login/access-token", {
			method: 'POST',
			headers: {
				'Accept': 'application/json',
				'Content-Type': 'application/x-www-form-urlencoded'
			},
			body: formBody
		}).then(response => response.json()).then(data => {
			console.log(data["access_token"])
		});

}

startSession.addEventListener("click", async (event) => {
  event.preventDefault();
  let username = document.getElementById("usernameInput").value
  let password = document.getElementById("passwordInput").value
  let data = await LoginMe(username, password)

});