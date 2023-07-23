let startSession = document.getElementById("start_session")

startSession.addEventListener("click", async () => {
  let [tab] = await chrome.tabs.query({active: true, currentWindow: true})
  let bp_token = document.getElementById("bpToken").value
  chrome.scripting.executeScript({
    target: {tabId: tab.id},
    func: readAllReleases,
    args: [bp_token]
  });
});


async function readAllReleases(bp_token) {

  function getToken() {
    return new Promise((resolve, reject) => {
        chrome.storage.sync.get('access_token', function(result) {
            if (chrome.runtime.lastError) {
                reject(chrome.runtime.lastError);
            } else {
                resolve(result.access_token);
            }
        });
    });
}

  let token = await getToken()
  // chrome.storage.sync.get('access_token', function (result) {
  //   token = result.access_token
  // });

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

  function regRelease(token, release) {
    console.log(token)
    console.log(release)
    const response = fetch(`http://127.0.0.1:8006/releases/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        name: release["title"],
        url: release["uri"],
        bp_id: release["id"]
      })
    }).then(response => response.json()).then(data => {
      console.log(data)
    });

  }

  function addYellowDot(release_row) {
    const clouderInfo = document.createElement('div')
    clouderInfo.className = 'sc-e751ecad-0 cNVqXt'
    const newSpan = document.createElement('span')

    newSpan.className = 'fade'

    const yellowDot = document.createElement('div')
    yellowDot.style.width = '10px'
    yellowDot.style.height = '10px'
    yellowDot.classList.add('dot--audited')
    yellowDot.style.borderRadius = '50%'

    newSpan.appendChild(yellowDot)
    clouderInfo.appendChild(newSpan)
    release_row.prepend(clouderInfo)
  }

  function handleRelease(release, idx, token) {
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

    addYellowDot(release)
    regRelease(token, new_release)

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
    let release = handleRelease(work_element, idx, token)
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

  async function postData(url = '', data = {}) {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + bp_token
      },
      body: JSON.stringify(data)
    })
    return response
  }

  function addPlaylistControl() {
    let parentDiv = document.querySelector('.sc-347751ec-8.gSeLef')

    let newDiv = document.createElement('div')
    newDiv.className = 'sc-347751ec-7 cveLdp'
    newDiv.style.height = '30px'
    newDiv.style.justifyContent = 'center'
    let playlistIds = {
      'Melodic': 1600521,
      'Party': 1597656,
      'Hard': 1597645,
      'Melan': 1597650,
      'ReDrum': 1597654,
      'Exper': 1597917
    }
    let spanNames = Object.keys(playlistIds)

    let statusSpan = document.createElement('span')
    statusSpan.className = 'sc-347751ec-5 hcrYxg clouder-status'
    statusSpan.style.padding = '8px'
    statusSpan.style.paddingLeft = '35px'
    statusSpan.style.display = 'block'
    statusSpan.style.width = '500px'
    statusSpan.style.textAlign = 'left'
    newDiv.appendChild(statusSpan)

    spanNames.forEach(function(name) {
        const newSpan = document.createElement('span')
        newSpan.className = 'sc-cdd38545-4 erNSOX'
        newSpan.textContent = name
        newSpan.style.padding = '8px'
        newSpan.addEventListener('click', async function() {
          let playlistName = this.textContent
          let playlistId = playlistIds[playlistName]
          console.log('Playlist: ' + playlistName + ' :: ID: ' + playlistId)
          let trackID = document.querySelector('.sc-347751ec-6.jtjvJw > a').getAttribute('href').split('/').pop()
          let trackElement = document.querySelector('.sc-347751ec-6.jtjvJw > a > .sc-347751ec-5.hcrYxg')
          let trackTitle = trackElement.textContent.trim();
          let response = await postData(`https://api.beatport.com/v4/my/playlists/${playlistId}/tracks/bulk/`, {track_ids:[trackID]})

          if (!response.ok) {
            console.error('HTTP error', response.status)
            statusSpan.textContent = `Some problem with Track '${trackTitle}' :: ID ${trackID} and '${this.textContent}' playlist`
          } else {
            console.log('Track added successfully')
            statusSpan.textContent = `Track '${trackTitle}' loaded to '${this.textContent}' playlist`
            console.log(`Track '${trackTitle}' with ID ${trackID} loaded to '${this.textContent}' playlist`)
          }
        });

        const newAnchor = document.createElement('div')
        newAnchor.title = name
        newAnchor.style.cursor = "pointer"
        // newAnchor.href = '#'
        newAnchor.appendChild(newSpan)

        newDiv.appendChild(newAnchor)
    })

    let pseudoStatusSpan = document.createElement('span')
    pseudoStatusSpan.className = 'sc-347751ec-5 hcrYxg clouder-status'
    pseudoStatusSpan.style.width = '500px'
    newDiv.appendChild(pseudoStatusSpan)

    if (parentDiv.firstChild) {
        parentDiv.insertBefore(newDiv, parentDiv.firstChild.nextSibling)
    } else {
        parentDiv.appendChild(newDiv)
    }
  }

  addPlaylistControl()
}