function handleClick(event) {
  let parent = event.target.closest('.sc-cdd38545-6.ZuJgX')
  let statusSpan = document.querySelector('.clouder-status')
  if (parent) {
    let artwork = parent.querySelector('.artwork')

    if (artwork) {
      console.log('Release ID: ', artwork.getAttribute('href').split('/').pop().trim())
      statusSpan ? statusSpan.textContent = '' : ''
    } else {
      console.log('Artwork element not found.')
    }
  } else {
    console.log('Parent element not found.')
  }
}

function addEventListenersToButtons() {
  let buttons = document.querySelectorAll('button.sc-a89217b5-0.fJWJNw')
  buttons.forEach(function(button) {
    button.addEventListener('click', handleClick)
  });
}

addEventListenersToButtons()

let observer = new MutationObserver(function(mutations) {
  mutations.forEach(function(mutation) {
    if (mutation.addedNodes.length) {
      addEventListenersToButtons()
    }
  })
})

let config = { childList: true, subtree: true }

observer.observe(document.body, config)
