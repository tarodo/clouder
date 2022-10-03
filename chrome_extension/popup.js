let startSession = document.getElementById("start_session");

startSession.addEventListener("click", async () => {
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: testLogin,
  });
});

async function testLogin() {
	let details = {
		'username': 'odmin@main.god',
		'password': 'kurit'
	};
	console.log("We start")
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
	});

	response.json().then(data => {
		console.log(data);
	});
}

function readAllReleases() {
	function handleRelease(release) {
		let new_release = {}
		new_release["id"] = release.getAttribute("data-ec-id")
		new_release["title"] = release.getAttribute("data-ec-name")
		new_release["r_link"] = release.getElementsByClassName("horz-release-artwork-parent")[0].getElementsByTagName("a")[0].getAttribute("href")
		new_release["session_position"] = release.getAttribute("data-ec-position")

		let raw_artists = release.getElementsByClassName("buk-horz-release-artists")[0].getElementsByTagName("a")
		let artists = {}
		for (const art of raw_artists) {
			let art_id = art.getAttribute("data-artist")
			artists[art_id] = {
				art_link: art.getAttribute("href"),
				art_title: art.innerText
			}
		}
		new_release["artists"] = artists
		
		let raw_labels = release.getElementsByClassName("buk-horz-release-labels")[0].getElementsByTagName("a")
		let labels = {}
		for (const label of raw_labels) {
			let label_id = label.getAttribute("data-label")
			labels[label_id] = {
				label_link: label.getAttribute("href"),
				label_title: label.innerText
			}
		}
		new_release["labels"] = labels
		
		new_release["date"] = release.getElementsByClassName("buk-horz-release-released")[0].innerText
		
		return new_release
	}
	
	const cur_url = new URL(window.location.href)
	if (cur_url.hostname !== "www.beatport.com") {
		return
	}
	if (!(cur_url.pathname > "/genre/")) {
		return
	}
	
	const style_name = cur_url.pathname.split("/")[2]
	const page = cur_url.searchParams.get('page')
	const start_date = cur_url.searchParams.get('start-date')
	const end_date = cur_url.searchParams.get('end-date')
	
	let new_releases = document.getElementsByClassName("bucket-item");
	let releases = {}
	for (const work_element of new_releases) {
		let release = handleRelease(work_element)
		if (release){
			releases[release.id] = release
		}
	}
	
	let session_page = {
		style_name: style_name,
		page: page,
		start_date: start_date,
		end_date: end_date,
		releases: releases
	}
	console.log(session_page)
}