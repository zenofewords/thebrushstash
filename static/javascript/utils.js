import {
  addProduct,
  applyPromoCode,
  continueToPaymentRequest,
  processOrder,
  removeProduct,
  setPaymentMethod,
  submitReviewRequest,
  subscribeToNewsletter,
  updateProduct,
  updateShippingAddress,
  updateShippingCost,
} from './requests'
import {
  bag,
  bagBuyLink,
  bagContent,
  bagItemCount,
  bagTotal,
  cashOnDeliveryRadio,
  cashOnDeliverySubmitWrapper,
  cashOnDeliveryWrapper,
  checkoutAddressTitle,
  checkoutAddressWrapper,
  checkoutIpgWrapper,
  checkoutPaymentTitle,
  checkoutPaymentWrapper,
  codOrderNumber,
  continueToPaymentButton,
  creditCardRadio,
  differentShippingAddressInput,
  imageWrappers,
  invoiceFormShippingCountryInput,
  ipgAmount,
  ipgCardholderAddress,
  ipgCardholderCity,
  ipgCardholderCountry,
  ipgCardholderEmail,
  ipgCardholderName,
  ipgCardholderSurname,
  ipgCardholderZipCode,
  ipgCart,
  ipgFormSubmitButton,
  ipgLanguage,
  ipgOrderNumber,
  ipgPaymentMaestro,
  ipgPaymentMaster,
  ipgPaymentVisa,
  ipgSignature,
  joinNewsletterMessage,
  mainWrapper,
  navigationWrapper,
  newSummaryGrandTotal,
  newSummaryGrandTotalHrk,
  newSummaryTax,
  newSummaryTotal,
  newSummaryWrapper,
  nonFieldError,
  promoCodeMessage,
  promoCodeMessageCloseIcon,
  productRatingCount,
  productRatingGauge,
  productReviewsWrapper,
  promoCodeInput,
  reviewBagLink,
  shippingAddressChoice,
  shippingAddressWrapper,
  summaryCheckoutButton,
  summaryGrandTotal,
  summaryGrandTotalHrk,
  summaryRowFees,
  summaryRowFeesValue,
  summaryShippingCost,
  summaryTax,
  summaryTotal,
  thumbnailWrappers,
} from './selectors'

export const currencySymbolMapping = {
  hrk: 'kn',
  eur: '€',
  gbp: '£',
  usd: '$',
}

export const formatPrice = (price, exchangeRate, currency) => {
  const displayPrice = (price * 1) / (exchangeRate * 1)

  if (currency === 'hrk') {
    return `${displayPrice.toFixed(2)} ${currencySymbolMapping[currency]}`
  }
  return `${currencySymbolMapping[currency]}${displayPrice.toFixed(2)}`
}

export const getCookie = (name) => {
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

export const toggleStickyNav = (scrollPosition) => {
  if (scrollPosition > 159) {
    navigationWrapper.classList.add('sticky-nav')
    mainWrapper.classList.add('sticky-nav-margin')
  } else {
    navigationWrapper.classList.remove('sticky-nav')
    mainWrapper.classList.remove('sticky-nav-margin')
  }
}

export const updatePaymentMethod = (paymentMethod) => {
  setPaymentMethod(paymentMethod).then(
    (data) => data.json()
  ).then((response) => {
    if (response.payment_method === 'cash-on-delivery') {
      summaryRowFees.classList.remove('hidden')
      summaryRowFeesValue.innerHTML = formatPrice(
        `${response.bag['fees']}`, response.exchange_rate, response.currency
      )

      ipgFormSubmitButton.classList.add('hidden')
      cashOnDeliverySubmitWrapper.classList.remove('hidden')
    } else {
      summaryRowFees.classList.add('hidden')
      summaryRowFeesValue.innerHTML = null

      cashOnDeliverySubmitWrapper.classList.add('hidden')
      ipgFormSubmitButton.classList.remove('hidden')
    }
    ipgAmount.value = response.bag.grand_total

    if (summaryShippingCost) {
      summaryShippingCost.innerHTML = formatPrice(
        `${response.bag['shipping_cost']}`, response.exchange_rate, response.currency
      )
    }
    if (summaryGrandTotal) {
      summaryGrandTotal.innerHTML = formatPrice(
        `${response.bag['grand_total']}`, response.exchange_rate, response.currency
      )
    }
    if (newSummaryGrandTotal) {
      newSummaryGrandTotal.innerHTML = formatPrice(
        `${response.bag['new_grand_total']}`, response.exchange_rate, response.currency
      )
    }
    if (summaryGrandTotalHrk) {
      summaryGrandTotalHrk.innerHTML = `${response.bag.grand_total} kn`
    }
  })
}

const updateIPGInputs = (response) => {
  ipgOrderNumber.value = response.order_number
  ipgAmount.value = response.grand_total
  ipgCart.value = response.cart
  ipgLanguage.value = response.language
  ipgSignature.value = response.signature
  ipgCardholderEmail.value = response.user_information.email
  ipgCardholderName.value = response.user_information.first_name
  ipgCardholderSurname.value = response.user_information.last_name
  ipgCardholderAddress.value = response.user_information.address
  ipgCardholderCity.value = response.user_information.city
  ipgCardholderZipCode.value = response.user_information.zip_code
  ipgCardholderCountry.value = response.user_information.country
  ipgPaymentMaestro.value = response.payment_maestro
  ipgPaymentMaster.value = response.payment_master
  ipgPaymentVisa.value = response.payment_visa
}

const moveToPaymentForm = () => {
  continueToPaymentButton.disabled = false

  checkoutAddressTitle.classList.add('inactive')
  checkoutAddressWrapper.classList.add('inactive')
  checkoutPaymentTitle.classList.remove('inactive')
  checkoutPaymentWrapper.classList.remove('inactive')
  checkoutIpgWrapper.classList.remove('inactive')
}

export const continueToPayment = (country) => {
  continueToPaymentRequest(country).then(
    (data) => data.json()
  ).then((response) => {
    if (response.show_cod) {
      cashOnDeliveryWrapper.hidden = false
      cashOnDeliverySubmitWrapper.hidden = false
      cashOnDeliveryRadio.checked = true

      shippingAddressChoice.hidden = true
      shippingAddressWrapper.hidden = true

      updatePaymentMethod(cashOnDeliveryRadio.value)
    } else {
      creditCardRadio.checked = true
      shippingAddressChoice.hidden = false

      cashOnDeliveryWrapper.hidden = true
      cashOnDeliverySubmitWrapper.hidden = true

      if (creditCardRadio.checked && differentShippingAddressInput.checked) {
        shippingAddressWrapper.hidden = false
        updateShippingCostForCountry(invoiceFormShippingCountryInput.value)
      }

      updatePaymentMethod(creditCardRadio.value)
    }
  }).then(
    () => moveToPaymentForm()
  ).then(() => {
    checkoutAddressTitle.scrollIntoView(false)
  })
}

export const processPaymentAddressData = (checkoutAddressForm, callback) => {
  const formData = new FormData(checkoutAddressForm)
  const data = {}
  for (const [key, value] of formData.entries()) {
    data[key] = value
  }

  processOrder(data).then(
    (data) => data.json()
  ).then((response) => {
    if (response.non_field_errors) {
      throw response.non_field_errors
    }
    codOrderNumber.value = response.order_number
    updateIPGInputs(response)
  }).then(() => {
    callback()
  }).catch((error) => {
    nonFieldError.innerHTML = error
    nonFieldError.hidden = false
    nonFieldError.scrollIntoView(false)
  })
}

export const updateShippingAddressData = (form) => {
  const formData = new FormData(form)

  const data = {}
  for (const [key, value] of formData.entries()) {
    data[key] = value
  }

  updateShippingAddress(data).then((data) => data.json().then((response) => {
    ipgAmount.value = response.grand_total
    ipgSignature.value = response.signature
    form.submit()
  }))
}

export const switchActiveImage = (event) => {
  const id = event.currentTarget.dataset.id
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
  }
}

export const subToNewsletter = (emailData) => {
  return subscribeToNewsletter(emailData).then(
    (data) => data.json()
  ).then((response) => {
    if (response.email0) {
      throw response.email0
    } else {
      joinNewsletterMessage.hidden = false
      joinNewsletterMessage.classList.remove('error')
      joinNewsletterMessage.innerHTML = response.message
      return true
    }
  }).catch((error) => {
    joinNewsletterMessage.classList.add('error')
    joinNewsletterMessage.hidden = false
    joinNewsletterMessage.innerHTML = error
    return false
  })
}

export const hideBagMobile = () => {
  bag.classList.remove('bag-show')
}

export const hideBag = () => {
  bag.classList.remove('bag-show')
  bag.classList.remove('bag-desktop-show')
}

export const toggleBag = (event) => {
  event.preventDefault()
  clearTimeout(hideBagTimer)
  bag.classList.toggle('bag-show')
  navigationWrapper.classList.remove('nav-mobile-open')
  document.body.classList.remove('lock-scroll')
}

let hideBagTimer
bag.addEventListener('mouseover', (event) => {
  clearTimeout(hideBagTimer)
})

bag.addEventListener('mouseout', (event) => {
  hideBagTimer = setTimeout(hideBag, 300)
})

export const refreshBag = (response) => {
  clearTimeout(hideBagTimer)

  bagTotal.innerHTML = formatPrice(
    `${response.bag['total']}`, response.exchange_rate, response.currency
  )
  bagContent.innerHTML = ''

  for (const [key, values] of Object.entries(response.bag.products)) {
    bagContent.appendChild(createProductNode(key, values, response))
  }
  bagItemCount.innerHTML = response.bag.total_quantity

  if (window.location.pathname !== '/review-bag/') {
    bag.classList.add('bag-desktop-show')
    hideBagTimer = setTimeout(hideBag, 2000)
  }
  if (Object.keys(response.bag.products).length < 1) {
    reviewBagLink.classList.add('hidden')
    bagBuyLink.classList.remove('hidden')
    setTimeout(hideBagMobile, 300)
  } else {
    reviewBagLink.classList.remove('hidden')
    bagBuyLink.classList.add('hidden')
  }
}

const refreshReviewBag = (response, slug) => {
  const product = document.getElementById(slug)

  if (!product) {
    return
  }

  if (product && !response.bag['products'][slug]) {
    product.classList.add('hidden')
  } else {
    const itemCount = document.getElementById(`${slug}-item-count`)
    const itemSubtotal = document.getElementById(`${slug}-item-subtotal`)
    const itemDecrement = document.getElementById(`${slug}-item-decrement`)
    const quantity = response.bag['products'][slug]['quantity']

    itemCount.innerHTML = quantity
    itemSubtotal.innerHTML = formatPrice(
      response.bag['products'][slug]['subtotal'], response.exchange_rate, response.currency
    )

    if (quantity < 2) {
      itemDecrement.classList.add('disabled')
    } else {
      itemDecrement.classList.remove('disabled')
    }
  }
  summaryShippingCost.innerHTML = formatPrice(
    `${response.bag['shipping_cost']}`, response.exchange_rate, response.currency
  )
  summaryTotal.innerHTML = formatPrice(
    `${response.bag['total']}`, response.exchange_rate, response.currency
  )
  summaryGrandTotal.innerHTML = formatPrice(
    `${response.bag['grand_total']}`, response.exchange_rate, response.currency
  )
  summaryTax.innerHTML = formatPrice(
    response.bag['tax'], response.exchange_rate, response.currency
  )

  if (summaryGrandTotalHrk) {
    summaryGrandTotalHrk.innerHTML = `${response.bag.grand_total} kn`
  }

  const products = response.bag.products
  if (Object.keys(products).length === 0 && products.constructor === Object) {
    summaryCheckoutButton.classList.add('disabled')
  }
}

const createProductNode = (key, values, response) => {
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
  productRemove.classList.add('bag-product-remove')
  productRemove.addEventListener('click', () => removeFromBag(key))
  bagProductHeader.appendChild(productRemove)

  const bagProductStats = document.createElement('div')
  bagProductStats.classList.add('bag-product-stats')
  const productQuantity = document.createElement('span')
  productQuantity.classList.add('bag-product-quantity')
  const productSubtotal = document.createElement('span')
  productQuantity.innerHTML = `Quantity: ${values.quantity}`
  productSubtotal.innerHTML = `Subtotal: ${formatPrice(
    `${values['subtotal']}`, response.exchange_rate, response.currency
  )}`
  bagProductStats.appendChild(productQuantity)
  bagProductStats.appendChild(productSubtotal)

  bagProductContent.appendChild(bagProductHeader)
  bagProductContent.appendChild(bagProductStats)
  bagProduct.appendChild(bagProductImage)
  bagProduct.appendChild(bagProductContent)

  return bagProduct
}

export const removeFromBag = (slug) => {
  removeProduct(slug).then((data) => data.json().then((response) => {
    refreshBag(response)
    refreshReviewBag(response, slug)

    if (ipgAmount && ipgCart) {
      ipgAmount.value = response.bag.grand_total
      ipgCart.value = response.cart
    }
  }))
}

export const addToBag = (dataset) => {
  addProduct(dataset).then((data) => data.json().then((response) => {
    refreshBag(response)
  }))
}

export const addOneToBag = (slug) => {
  updateProduct(slug, 'increment').then((data) => data.json().then((response) => {
    refreshBag(response)
    refreshReviewBag(response, slug)
  }))
}

export const removeOneFromBag = (slug) => {
  updateProduct(slug, 'decrement').then((data) => data.json().then((response) => {
    refreshBag(response)
    refreshReviewBag(response, slug)
  }))
}

export const showErrorMessage = (target) => {
  target.focus()
  const errorLabel = document.getElementById(`${target.id}-error`)
  errorLabel.hidden = false
}

export const clearErrorMessages = () => {
  const errorLabels = document.getElementsByClassName('error')
  for (let i = 0; i < errorLabels.length; i++) {
    errorLabels[i].hidden = true
  }
}

export const updateShippingCostForCountry = (countryName, callback = null, inPersonPickup = false) => {
  const shippingCostData = inPersonPickup ? {
    in_person_pickup: true,
  } : {
    country_name: countryName,
  }
  updateShippingCost(shippingCostData).then((data) => data.json().then((response) => {
    summaryShippingCost.innerHTML = formatPrice(
      response.bag['shipping_cost'], response.exchange_rate, response.currency
    )
    summaryGrandTotal.innerHTML = formatPrice(
      response.bag['grand_total'], response.exchange_rate, response.currency
    )

    if (newSummaryGrandTotal) {
      newSummaryGrandTotal.innerHTML = formatPrice(
        response.bag['new_grand_total'], response.exchange_rate, response.currency
      )
    }

    if (summaryGrandTotalHrk) {
      summaryGrandTotalHrk.innerHTML = `${response.bag.grand_total} kn`

      if (newSummaryGrandTotalHrk) {
        newSummaryGrandTotalHrk.innerHTML = `${response.bag.new_grand_total} kn`
      }
    }
  }).then(() => {
    if (callback) {
      callback()
    }
  }))
}

export const scrollToElement = (element, offset = 60) => {
  const bodyRect = document.body.getBoundingClientRect().top
  const elementRect = element.getBoundingClientRect().top
  window.scrollTo(
    {top: elementRect - bodyRect - offset}
  )
}

export const submitReview = (productReviewForm) => {
  const formData = new FormData(productReviewForm)
  const data = {}
  for (const [key, value] of formData.entries()) {
    data[key] = value
  }

  submitReviewRequest(data).then(
    (data) => data.json()
  ).then((response) => {
    productReviewForm.hidden = true

    const title = document.createElement('h3')
    title.innerHTML = `${response.user_name}`
    title.classList.add(`stars-${response.score}`)
    const content = document.createElement('p')
    content.innerHTML = response.content.replace(/(?:\r\n|\r|\n)/g, '<br>')

    const ratings = response.ratings
    let percentage = 0
    if (ratings > 0) {
      percentage = Math.round(response.total_score / ratings / 5 * 100)
    }

    productRatingCount.innerHTML = `(${response.ratings})`
    productRatingGauge.style = `width: ${percentage}%`

    if (productReviewsWrapper.children) {
      productReviewsWrapper.insertBefore(content, productReviewsWrapper.childNodes[0])
      productReviewsWrapper.insertBefore(title, productReviewsWrapper.childNodes[0])
    } else {
      productReviewsWrapper.appendChild(content)
      productReviewsWrapper.appendChild(title)
    }
  })
}

export const processPromoCode = (code) => {
  applyPromoCode({'code': code}).then(
    (data) => data.json()
  ).then((response) => {
    if (response.bag && response.bag.promo_code) {
      newSummaryWrapper.classList.remove('hidden')

      newSummaryTax.innerHTML = formatPrice(
        response.bag['new_tax'], response.exchange_rate, response.currency
      )
      newSummaryTotal.innerHTML = formatPrice(
        response.bag['new_total'], response.exchange_rate, response.currency
      )
      newSummaryGrandTotal.innerHTML = formatPrice(
        response.bag['new_grand_total'], response.exchange_rate, response.currency
      )

      if (newSummaryGrandTotalHrk) {
        newSummaryGrandTotalHrk.innerHTML = `${response.bag.new_grand_total} kn`
      }
    } else {
      newSummaryWrapper.classList.add('hidden')
    }

    if (response.code) {
      promoCodeMessage.innerHTML = ''
      promoCodeMessage.innerHTML = response.code
      promoCodeMessage.appendChild(promoCodeMessageCloseIcon)
      promoCodeMessage.classList.remove('hidden')
    }
  }).catch((error) => {
    console.log(error)
  })
}
