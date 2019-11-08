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
  const imageWrappers = document.getElementsByClassName('image-wrapper small')
  const thumbnailWrappers = document.getElementsByClassName('image-wrapper thumbnail')
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

  const switchActiveImage = (event) => {
    const id = event.currentTarget.id
    const reveal = [...imageWrappers].find(x => x.id === id)
    const hide = [...imageWrappers].find(x => x.classList.contains('selected'))

    if (reveal.id !== hide.id) {
      reveal.classList.add('selected')
      reveal.hidden = false
      hide.classList.remove('selected')
      hide.hidden = true

      const unselect = [...thumbnailWrappers].find(x => x.classList.contains('selected'))
      event.currentTarget.classList.add('selected')
      unselect.classList.remove('selected')

      history.pushState({mediaObject: id}, '', `?gallery-item=${id}`)
    }
  }

  for (var i = 0; i < thumbnailWrappers.length; i++) {
    thumbnailWrappers[i].addEventListener('click', (event) => {
      event.preventDefault()

      switchActiveImage(event)
    })
  }

  for (let i = 0; i < videoWrappers.length; i++) {
    videoWrappers[i].addEventListener('click', (event) => {
      event.preventDefault()

      if (currentModal) {
        document.body.classList.remove('lock-scroll')
        videoWrappers[i].removeChild(currentModal)
        videoWrappers[i].classList.remove('fade')
        currentModal = undefined
      } else {
        document.body.classList.add('lock-scroll')
        history.pushState({mediaObject: event.target.id}, '', `?gallery-item=${event.target.id}`)
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
  const bagLink = document.querySelector('.bag-link')
  const bag = document.querySelector('.bag')
  const bagContent = document.querySelector('.bag-content')
  const addToBagSelect = document.getElementById('add-to-bag-select')
  const addToBagButtons = document.getElementsByClassName('add-to-bag-button')
  const bagTotal = document.querySelector('.bag-total')
  const bagItemCount = document.querySelector('.bag-item-count')

  const reviewBagLink = document.querySelector('.review-bag-link')
  const summaryTotal = document.getElementById('summary-total')
  const summaryGrandTotal = document.getElementById('summary-grand-total')

  const toggleBag = (event) => {
    event.preventDefault()
    bag.classList.toggle('bag-hide')
  }

  bagLink.addEventListener('click', toggleBag)

  const removeProductButtons = document.getElementsByClassName('bag-product-remove')
  for (let i = 0; i < removeProductButtons.length; i++) {
    const button = removeProductButtons[i]
    button.addEventListener('click', () => removeProduct(button.dataset.slug))
  }

  const createProductNode = (key, values) => {
    const product = document.createElement('div')
    const productHeader = document.createElement('div')
    const productInfo = document.createElement('div')
    const productRemove = document.createElement('span')
    productHeader.classList.add('bag-product-header')

    const name = document.createElement('span')
    name.classList.add('bag-product-name')
    name.innerHTML = `${values.name}`
    productHeader.appendChild(name)
    productRemove.innerHTML = '&times;'
    productRemove.classList.add('bag-product-remove')
    productRemove.addEventListener('click', () => removeProduct(key))
    productHeader.appendChild(productRemove)

    const quantity = document.createElement('span')
    const subtotal = document.createElement('span')
    quantity.innerHTML = `Quantity: ${values.quantity}`
    subtotal.innerHTML = `Subtotal: ${values.subtotal} kn`
    productInfo.classList.add('bag-product-content')
    productInfo.appendChild(quantity)
    productInfo.appendChild(subtotal)

    product.slug = key
    product.appendChild(productHeader)
    product.appendChild(productInfo)

    return product
  }

  const refreshBag = (response) => {
    bagTotal.innerHTML = `${response.bag.total} kn`
    bagContent.innerHTML = ''

    for (const [key, values] of Object.entries(response.bag.products)) {
      bagContent.appendChild(createProductNode(key, values))
    }
    bagItemCount.innerHTML = response.bag.total_quantity

    if (window.location.pathname !== '/review-bag/') {
      bag.classList.remove('bag-hide')
    }
    reviewBagLink.hidden = Object.keys(response.bag.products).length < 1
  }

  const refreshReviewBag = (response, slug) => {
    const product = document.getElementById(slug)
    product.remove()

    summaryTotal.innerHTML = response.bag.total
    summaryGrandTotal.innerHTML = response.bag.grand_total
  }

  const removeProduct = (slug) => {
    fetch('/api/remove-from-bag/',
      {
        method: 'POST',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
          slug: slug,
        }),
      }
    ).then((data) => data.json().then((response) => {
      refreshBag(response)

      if (window.location.pathname === '/review-bag/') {
        refreshReviewBag(response, slug)
      }
    }))
  }

  const addProduct = (dataset) => {
    fetch('/api/add-to-bag/',
      {
        method: 'POST',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
          pk: dataset.id,
          slug: dataset.slug,
          name: dataset.name,
          quantity: parseInt(dataset.multiple ? addToBagSelect.value : 1),
          price: parseFloat(dataset.price),
        }),
      }
    ).then((data) => data.json().then((response) => {
      refreshBag(response)
    }))
  }

  for (let i = 0; i < addToBagButtons.length; i++) {
    const button = addToBagButtons[i]
    button.addEventListener('click', () => addProduct(button.dataset))
  }

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

  const navigationWrapper = document.querySelector('.navigation-wrapper')
  const mainWrapper = document.querySelector('.main-wrapper')

  const toggleStickyNav = (scrollPosition) => {
    if (scrollPosition > 190) {
      navigationWrapper.classList.add('sticky-nav')
      mainWrapper.classList.add('sticky-nav-margin')
    } else {
      navigationWrapper.classList.remove('sticky-nav')
      mainWrapper.classList.remove('sticky-nav-margin')
    }
  }

  let ticking = false
  window.addEventListener('scroll', (event) => {
    if (!ticking) {
      window.requestAnimationFrame(() => {
        toggleStickyNav(window.scrollY)
        ticking = false
      })
      ticking = true
    }
  })
})
