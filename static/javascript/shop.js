import '../sass/shop.sass'
import './listeners'
import {
  setRegion,
} from './requests'
import {
  imagesWithPreview,
  languageForm,
  languageInput,
  navigationWrapper,
  shipToMenu,
  shipToSelects,
  videoWrappers,
} from './selectors'
import {
  refreshBag,
} from './utils'

const ready = (runScript) => {
  if (document.attachEvent ? document.readyState === 'complete' : document.readyState !== 'loading') {
    runScript()
  } else {
    document.addEventListener('DOMContentLoaded', runScript)
  }
}

ready(() => {
  window.history.pushState({page: 1}, '', '')
  window.onpopstate = (event) => {
    const location = event.target.location
    const search = new URLSearchParams(location.search)

    if (search.get('next')) {
      window.location = search.get('next')
      return
    }
    if (!location.hash) {
      window.location = event.target.location.origin
    }
  }

  const onSelectFocus = (event) => {
    for (let i = 0; i < shipToMenu.length; i++) {
      shipToMenu[i].hidden = false
    }

    const menuItemClick = (event) => {
      event.preventDefault()

      if (!event.target.firstElementChild || !event.target.firstElementChild.classList.contains('flag-icon')) {
        for (let i = 0; i < shipToMenu.length; i++) {
          shipToMenu[i].hidden = true
        }
        removeClickListener(event)
      } else if (event.target.classList.contains('language-option')) {
        languageInput.value = event.target.dataset.language

        setRegion(event.target.dataset.region).then((data) => data.json().then((response) => {
          refreshBag(response)
          languageForm.submit()
        }))
      }
    }

    const removeClickListener = () => {
      document.removeEventListener('click', menuItemClick)
    }
    document.addEventListener('click', menuItemClick)
  }

  for (let i = 0; i < shipToSelects.length; i++) {
    shipToSelects[i].addEventListener('blur', (event) => {
      if (!event.relatedTarget || !event.relatedTarget.classList.contains('language-option')) {
        shipToMenu[i].hidden = true
      }
    })
    shipToSelects[i].addEventListener('focus', onSelectFocus)
    shipToSelects[i].addEventListener('click', (event) => {
      event.preventDefault()

      if (shipToMenu[i].hidden) {
        onSelectFocus(event)
      }
    })
  }

  let currentModal
  for (let i = 0; i < videoWrappers.length; i++) {
    videoWrappers[i].addEventListener('click', (event) => {
      event.preventDefault()

      if (currentModal) {
        document.body.classList.remove('lock-scroll')
        navigationWrapper.hidden = false
        videoWrappers[i].removeChild(currentModal)
        videoWrappers[i].classList.remove('fade')
        currentModal = undefined
      } else {
        document.body.classList.add('lock-scroll')
        navigationWrapper.hidden = true
        loadVideo(videoWrappers[i])
      }
    })
  }
  const previewImageWrapper = document.createElement('div')
  previewImageWrapper.classList.add('image-preview')

  for (var i = 0; i < imagesWithPreview.length; i++) {
    imagesWithPreview[i].addEventListener('click', (event) => {
      event.preventDefault()

      while (previewImageWrapper.firstChild) {
        previewImageWrapper.removeChild(previewImageWrapper.firstChild)
      }
      document.body.classList.add('lock-scroll')
      navigationWrapper.hidden = true

      const picture = document.querySelector('.selected')
      const size = window.innerWidth > window.innerHeight ? window.innerHeight * 0.9 : window.innerWidth * 0.9
      const imagePreview = new Image(size, size)
      const image = picture.getElementsByTagName('img')[0].currentSrc
      imagePreview.src = image

      previewImageWrapper.appendChild(imagePreview)
      document.body.appendChild(previewImageWrapper)

      currentModal = previewImageWrapper
    })
  }
  previewImageWrapper.addEventListener('click', (event) => {
    if (currentModal) {
      document.body.classList.remove('lock-scroll')
      document.body.removeChild(previewImageWrapper)
      navigationWrapper.hidden = false
      currentModal = undefined
    }
  })

  const loadVideo = (videoWrapper) => {
    const id = videoWrapper.dataset.youtubeVideoId
    const html = `<iframe
      width="100%" height="100%"
      src="https://www.youtube-nocookie.com/embed/${id}?rel=0&amp;autoplay=1"
      frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
      allowfullscreen>
    </iframe>`
    const iframe = document.createElement('iframe')

    videoWrapper.classList.add('fade')
    videoWrapper.hidden = false
    videoWrapper.appendChild(iframe)
    iframe.contentWindow.document.open()
    iframe.contentWindow.document.write(html)
    iframe.contentWindow.document.close()

    currentModal = iframe
  }
})
