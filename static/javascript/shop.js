import '../sass/shop.sass'

const ready = (runScript) => {
  if (document.attachEvent ? document.readyState === 'complete' : document.readyState !== 'loading') {
    runScript()
  } else {
    document.addEventListener('DOMContentLoaded', runScript)
  }
}

ready(() => {
  const cookieInfo = document.querySelector('.accept-cookie')
  const shipToSelect = document.querySelector('.ship-to-select')
  const shipToMenu = document.querySelector('.ship-to-menu')
  const languageOptions = document.getElementsByClassName('language-option')
  const languageInput = document.getElementById('language-input')
  const languageForm = document.getElementById('language-form')
  const galleryThumbnailLinks = document.getElementsByClassName('gallery-thumbnail-link')
  const videoWrappers = document.getElementsByClassName('video-wrapper')

  const onSelectFocus = (event) => {
    shipToMenu.hidden = false

    const menuItemClick = (event) => {
      event.preventDefault()

      if (!event.target.firstElementChild || !event.target.firstElementChild.classList.contains('flag-icon')) {
        shipToMenu.hidden = true
        removeClickListener(event)
      } else if (event.target.classList.contains('language-option')) {
        languageInput.value = event.target.dataset.language

        fetch('/api/region/',
          {
            method: 'POST',
            cache: 'no-cache',
            credentials: 'same-origin',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
              region: event.target.dataset.region,
            }),
          }
        ).then((data) => languageForm.submit())
      }
    }

    const removeClickListener = () => {
      document.removeEventListener('click', menuItemClick)
    }
    document.addEventListener('click', menuItemClick)
  }

  let currentModal
  const loadVideo = (videoWrapper) => {
    const id = videoWrapper.dataset.youtubeVideoId
    const size = videoWrapper.dataset.size

    const html = `<iframe width="100%" height="100%" src="https://www.youtube-nocookie.com/embed/${id}?rel=0&amp;autoplay=1" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>`
    const iframe = document.createElement('iframe')

    videoWrapper.classList.add('fade')
    videoWrapper.hidden = false
    videoWrapper.appendChild(iframe)
    iframe.contentWindow.document.open()
    iframe.contentWindow.document.write(html)
    iframe.contentWindow.document.close()

    currentModal = iframe
  }

  for (let i = 0; i < videoWrappers.length; i++) {
    videoWrappers[i].addEventListener('click', (event) => {
      if (currentModal) {
        document.body.classList.remove('lock-scroll')
        videoWrappers[i].removeChild(currentModal)
        videoWrappers[i].classList.remove('fade')
        currentModal = undefined
      } else {
        document.body.classList.add('lock-scroll')
        loadVideo(videoWrappers[i])
      }
    })
  }

  shipToSelect.addEventListener('blur', (event) => {
    if (!event.relatedTarget || !event.relatedTarget.classList.contains('language-option')) {
      shipToMenu.hidden = true
    }
  })
  shipToSelect.addEventListener('focus', onSelectFocus)
  shipToSelect.addEventListener('click', (event) => {
    event.preventDefault()

    if (shipToMenu.hidden) {
      onSelectFocus(event)
    }
  })

  for (let i = 0; i < languageOptions.length; i++) {
    languageOptions[i].addEventListener('blur', (event) => {
      if (!event.relatedTarget || !event.relatedTarget.classList.contains('language-option')) {
        shipToMenu.hidden = true
      }
    })
  }

  cookieInfo && cookieInfo.addEventListener('click', () => {
    fetch('/api/cookie/',
      {
        method: 'POST',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
          accepted: true,
        }),
      }
    ).then(() => {
      document.querySelector('.cookie-wrappper').hidden = true
    })
  })

  const getCookie = (name) => {
    let cookieValue = null

    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';')

      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim()

        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
          break
        }
      }
    }
    return cookieValue
  }

  const creditCardSecureLogos = document.getElementsByClassName('credit-card-secure-logo')
  const creditCardSecureModals = document.getElementsByClassName('credit-card-secure-modal')
  const closeModalButtons = document.getElementsByClassName('close-modal-button')

  for (let i = 0; i < creditCardSecureLogos.length; i++) {
    creditCardSecureLogos[i].addEventListener('click', (event) => {
      const clickedModalId = event.target.id + '-modal'

      for (let i = 0; i < creditCardSecureModals.length; i++) {
        if (creditCardSecureModals[i].id !== clickedModalId) {
          creditCardSecureModals[i].hidden = true
        }
      }

      const modal = document.getElementById(clickedModalId)
      modal.hidden = !modal.hidden
    })
  }

  for (let i = 0; i < closeModalButtons.length; i++) {
    closeModalButtons[i].addEventListener('click', (event) => {
      for (let i = 0; i < creditCardSecureModals.length; i++) {
        creditCardSecureModals[i].hidden = true
      }
    })
  }
})
