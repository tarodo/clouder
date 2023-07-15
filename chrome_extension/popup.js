let startSession = document.getElementById("start_session");

startSession.addEventListener("click", async () => {
  let [tab] = await chrome.tabs.query({active: true, currentWindow: true});
  chrome.scripting.executeScript({
    target: {tabId: tab.id},
    func: readAllReleases,
  });
});

function readAllReleases() {
  chrome.storage.sync.get('access_token', function (result) {
    let token = result.access_token;
    console.log(token)
  });

  function handleReleaseArtists(raw_artists) {
    let artists = []
      raw_artists.forEach(function(artist) {
      let name = artist.textContent
      let id = artist.getAttribute('href').split('/').pop()
      let uri = artist.getAttribute('href')

      artists.push({
        name: name,
        id: id,
        uri: uri
      })
    })
    return artists
  }

  function handleReleaseLabels(raw_labels) {
      let labels = []
      raw_labels.forEach(function(label) {
      let name = label.textContent
      let id = label.getAttribute('href').split('/').pop()
      let uri = label.getAttribute('href')

      labels.push({
        name: name,
        id: id,
        uri: uri
      })
    })
    return labels
  }

  function handleRelease(release, idx) {
    let new_release = {}
    new_release["uri"] = release.querySelector('a.artwork').getAttribute('href')
    new_release["title"] = release.querySelector('span.erNSOX').textContent.trim()
    new_release["id"] = release.querySelector('a.artwork').getAttribute('href').split('/').pop()
    new_release["position"] = idx

    let raw_artists = release.querySelector('div.sc-d6bcf006-0.eOcWlw').querySelectorAll('a')
    new_release["artists"] = handleReleaseArtists(raw_artists)

    let raw_labels = release.querySelector('div.sc-e751ecad-0.cNVqXt.cell.label').querySelectorAll('a')
    new_release["labels"] = handleReleaseLabels(raw_labels)

    new_release["date"] = release.querySelector('div.sc-e751ecad-0.cNVqXt.cell.date').textContent.trim()

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

  const dateString = cur_url.searchParams.get('publish_date')
  const decodedString = decodeURIComponent(dateString);
  const [start_date, end_date] = decodedString.split(":");

  let new_releases = document.getElementsByClassName("gSaMFX");
  let releases = {}
  let idx = 0
  for (const work_element of new_releases) {
    idx = idx + 1
    let release = handleRelease(work_element, idx)
    if (release) {
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