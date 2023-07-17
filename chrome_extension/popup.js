let startSession = document.getElementById("start_session")

startSession.addEventListener("click", async () => {
  let [tab] = await chrome.tabs.query({active: true, currentWindow: true})
  chrome.scripting.executeScript({
    target: {tabId: tab.id},
    func: readAllReleases,
  });
});

function readAllReleases() {
  chrome.storage.sync.get('access_token', function (result) {
    let token = result.access_token
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

  function addYellowDot() {
    const insertPlaces = document.querySelectorAll('div.sc-e751ecad-1.gSaMFX.row')
    console.log(insertPlaces)
    insertPlaces.forEach(function (place) {
      const clouderInfo = document.createElement('div')
      clouderInfo.className = 'sc-e751ecad-0 cNVqXt'
      const newSpan = document.createElement('span')

      newSpan.className = 'fade'

      const yellowDot = document.createElement('div')
      yellowDot.style.width = '10px'
      yellowDot.style.height = '10px'
      yellowDot.classList.add('dot--yellow')
      yellowDot.style.borderRadius = '50%'

      newSpan.appendChild(yellowDot)
      clouderInfo.appendChild(newSpan)
      place.prepend(clouderInfo)
    })
  }

  async function postData(url = '', data = {}) {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer AIEUyWlvOWSEvx5Sq5kL7fB4l86xkE'
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

        const newAnchor = document.createElement('a')
        newAnchor.title = name
        newAnchor.href = '#'
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


  addYellowDot()
  addPlaylistControl()
}