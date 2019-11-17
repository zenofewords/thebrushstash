import '../sass/shop.sass'

const ready = (runScript) => {
  if (document.attachEvent ? document.readyState === 'complete' : document.readyState !== 'loading') {
    runScript()
  } else {
    document.addEventListener('DOMContentLoaded', runScript)
  }
}

ready(() => {
  const navigationWrapper = document.querySelector('.navigation-wrapper')
  const mainWrapper = document.querySelector('.main-wrapper')
  const cookieInfo = document.querySelector('.accept-cookie')
  const shipToSelect = document.querySelector('.ship-to-select')
  const shipToMenu = document.querySelector('.ship-to-menu')
  const languageOptions = document.getElementsByClassName('language-option')
  const languageInput = document.getElementById('language-input')
  const languageForm = document.getElementById('language-form')
  const imageWrappers = document.getElementsByClassName('image-wrapper portrait')
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

  const continueToPaymentButton = document.getElementById('continue-to-payment')
  const checkoutAddressForm = document.getElementById('checkout-address-form')
  const checkoutAddressTitle = document.querySelector('.checkout-address-title')
  const checkoutPaymentTitle = document.querySelector('.checkout-payment-title')
  const checkoutAddressWrapper = document.querySelector('.checkout-address-wrapper')
  const checkoutPaymentWrapper = document.querySelector('.checkout-payment-wrapper')
  const previousStepLink = document.querySelector('.previous-step-link')

  const cashOnDeliveryWrapper = document.querySelector('.cash-on-delivery-wrapper')
  const cashOnDeliveryRadio = document.getElementById('cash-on-delivery')
  const creditCardWrapper = document.querySelector('.credit-card-wrapper')
  const creditCardRadio = document.getElementById('credit-card')
  const summaryRowFees = document.getElementById('summary-row-fees')
  const summaryRowFeesValue = document.getElementById('summary-value-fees')
  const phoneNumberInput = document.getElementById('id_phone_number')

  const corvusOrderNumber = document.getElementById('order_number')
  const corvusAmount = document.getElementById('amount')
  const corvusCart = document.getElementById('cart')
  const corvusSignature = document.getElementById('signature')
  const corvusCardholderName = document.getElementById('cardholder_name')
  const corvusCardholderSurname = document.getElementById('cardholder_surname')
  const corvusCardholderEmail = document.getElementById('cardholder_email')

  const corvusFormSubmitButton = document.getElementById('corvus-form-submit-button')
  const cashOnDeliverySubmitWrapper = document.getElementById('cash-on-delivery-submit-wrapper')

  cashOnDeliveryWrapper && cashOnDeliveryWrapper.addEventListener('click', (event) => {
    if (!cashOnDeliveryRadio.checked) {
      cashOnDeliveryRadio.checked = true
      updatePaymentMethod(cashOnDeliveryRadio.value)
    }
  })

  creditCardWrapper && creditCardWrapper.addEventListener('click', (event) => {
    if (!creditCardRadio.checked) {
      creditCardWrapper.checked = true
      updatePaymentMethod(creditCardRadio.value)
    }
  })

  const updatePaymentMethod = (paymentMethod) => {
    fetch('/api/update-payment-method/',
      {
        method: 'POST',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
          payment_method: paymentMethod,
        }),
      }
    ).then((data) => data.json().then((response) => {
      if (response.bag.fees) {
        summaryRowFees.classList.remove('hidden')
        summaryRowFeesValue.innerHTML = `${response.bag.fees} kn`
        corvusFormSubmitButton.classList.add('hidden')
        cashOnDeliverySubmitWrapper.classList.remove('hidden')
      } else {
        summaryRowFees.classList.add('hidden')
        corvusFormSubmitButton.classList.remove('hidden')
        cashOnDeliverySubmitWrapper.classList.add('hidden')
        summaryRowFeesValue.innerHTML = null
      }
      corvusAmount.value = response.bag.grand_total
      summaryGrandTotal.innerHTML = response.bag.grand_total
    }))
  }

  creditCardWrapper && creditCardWrapper.addEventListener('click', (event) => {
    creditCardRadio.checked = true
  })

  continueToPaymentButton && continueToPaymentButton.addEventListener('click', (event) => {
    event.preventDefault()
    const valid = checkoutAddressForm.reportValidity()

    if (valid) {
      phoneNumberInput.required = true

      const formData = new FormData(checkoutAddressForm)
      const data = {}
      for (const [key, value] of formData.entries()) {
        data[key] = value
      }

      fetch('/api/process-order/',
        {
          method: 'POST',
          cache: 'no-cache',
          credentials: 'same-origin',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
          },
          body: JSON.stringify(data),
        }
      ).then((data) => data.json().then((response) => {
        corvusOrderNumber.value = response.order_number
        corvusAmount.value = response.grand_total
        corvusCart.value = response.cart
        corvusSignature.value = response.signature
        corvusCardholderEmail.value = response.user_information.email
        corvusCardholderName.value = response.user_information.first_name
        corvusCardholderSurname.value = response.user_information.last_name

        if (response.region === 'hr') {
          updatePaymentMethod(cashOnDeliveryRadio.value)
        } else {
          updatePaymentMethod(creditCardRadio.value)
        }
      }))

      checkoutAddressTitle.classList.add('inactive')
      checkoutAddressWrapper.classList.add('inactive')
      checkoutPaymentTitle.classList.remove('inactive')
      checkoutPaymentWrapper.classList.remove('inactive')

      checkoutAddressTitle.scrollIntoView(false)
    }
  })
  previousStepLink && previousStepLink.addEventListener('click', (event) => {
    event.preventDefault()
    phoneNumberInput.required = false

    checkoutAddressTitle.classList.remove('inactive')
    checkoutAddressWrapper.classList.remove('inactive')
    checkoutPaymentTitle.classList.add('inactive')
    checkoutPaymentWrapper.classList.add('inactive')
  })

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
    const bagProduct = document.createElement('div')
    bagProduct.classList.add('bag-product')
    bagProduct.slug = key

    const bagProductImage = document.createElement('div')
    bagProductImage.classList.add('bag-product-image')
    const imageWrapper = document.createElement('div')
    imageWrapper.classList.add('image-wrapper')
    const image = document.createElement('img')
    image.classList.add('picture')
    image.src = `${values.image_url}`
    image.alt = `${values.name}`
    imageWrapper.appendChild(image)
    bagProductImage.appendChild(imageWrapper)

    const bagProductContent = document.createElement('div')
    bagProductContent.classList.add('bag-product-content')
    const bagProductHeader = document.createElement('div')
    bagProductHeader.classList.add('bag-product-header')
    const productName = document.createElement('span')
    productName.classList.add('bag-product-name')
    productName.innerHTML = `${values.name}`
    bagProductHeader.appendChild(productName)

    const productRemove = document.createElement('span')
    productRemove.innerHTML = '&times;'
    productRemove.classList.add('bag-product-remove')
    productRemove.addEventListener('click', () => removeProduct(key))
    bagProductHeader.appendChild(productRemove)

    const bagProductStats = document.createElement('div')
    bagProductStats.classList.add('bag-product-stats')
    const productQuantity = document.createElement('span')
    productQuantity.classList.add('bag-product-quantity')
    const productSubtotal = document.createElement('span')
    productQuantity.innerHTML = `Quantity: ${values.quantity}`
    productSubtotal.innerHTML = `Subtotal: ${values.subtotal} kn`
    bagProductStats.appendChild(productQuantity)
    bagProductStats.appendChild(productSubtotal)

    bagProductContent.appendChild(bagProductHeader)
    bagProductContent.appendChild(bagProductStats)
    bagProduct.appendChild(bagProductImage)
    bagProduct.appendChild(bagProductContent)

    return bagProduct
  }

  let hideBagTimer
  const hideBag = () => {
    bag.classList.add('bag-hide')
  }

  bag.addEventListener('mouseover', (event) => {
    clearTimeout(hideBagTimer)
  })
  bag.addEventListener('mouseout', (event) => {
    hideBagTimer = setTimeout(hideBag, 500)
  })

  const refreshBag = (response) => {
    clearTimeout(hideBagTimer)
    bagTotal.innerHTML = `${response.bag.total} kn`
    bagContent.innerHTML = ''

    for (const [key, values] of Object.entries(response.bag.products)) {
      bagContent.appendChild(createProductNode(key, values))
    }
    bagItemCount.innerHTML = response.bag.total_quantity

    if (window.location.pathname !== '/review-bag/') {
      bag.classList.remove('bag-hide')
      hideBagTimer = setTimeout(hideBag, 3000)
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
          image_url: dataset.imageUrl,
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
