import '../sass/shop.sass'
import './listeners'
import {
  setRegion,
} from './requests'
import {
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

        setRegion(event).then((data) => data.json().then((response) => {
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
        history.pushState({mediaObject: event.target.id}, '', `?gallery-item=${event.target.id}`)
        loadVideo(videoWrappers[i])
      }
    })
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
