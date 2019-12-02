import {
  addProduct,
  processOrder,
  removeProduct,
  setPaymentMethod,
  subscribeToNewsletter,
  updateProduct,
} from './requests'
import {
  bag,
  bagBuyLink,
  bagBuyMobileLink,
  bagContent,
  bagContentMobile,
  bagItemCount,
  bagItemCountMobile,
  bagMobile,
  bagTotal,
  bagTotalMobile,
  cashOnDeliveryRadio,
  cashOnDeliverySubmitWrapper,
  checkoutAddressTitle,
  checkoutAddressWrapper,
  checkoutHelpText,
  checkoutPaymentTitle,
  checkoutPaymentWrapper,
  continueToPaymentButton,
  creditCardRadio,
  imageWrappers,
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
  ipgSignature,
  joinNewsletterMessage,
  mainWrapper,
  navigationWrapper,
  phoneNumberInput,
  reviewBagLink,
  reviewBagLinkMobile,
  summaryCheckoutButton,
  summaryGrandTotal,
  summaryGrandTotalHrk,
  summaryRowFees,
  summaryRowFeesValue,
  summaryShippingCost,
  summaryTotal,
  thumbnailWrappers,
} from './selectors'

export const currencySymbolMapping = {
  hrk: 'kn',
  eur: '€',
  gbp: '£',
  usd: '$',
}

export const formatPrice = (price, currency) => {
  if (currency === 'hrk') {
    return `${price} ${currencySymbolMapping[currency]}`
  }
  return `${currencySymbolMapping[currency]}${price}`
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

export const toggleBag = (event) => {
  event.preventDefault()
  bag.classList.toggle('bag-hide')
}

export const updatePaymentMethod = (paymentMethod) => {
  setPaymentMethod(paymentMethod).then((data) => data.json().then((response) => {
    if (parseInt(response.bag.fees)) {
      summaryRowFees.classList.remove('hidden')
      summaryRowFeesValue.innerHTML = `${response.bag.fees} kn` // must be in hrk
      ipgFormSubmitButton.classList.add('hidden')
      cashOnDeliverySubmitWrapper.classList.remove('hidden')
    } else {
      summaryRowFees.classList.add('hidden')
      ipgFormSubmitButton.classList.remove('hidden')
      cashOnDeliverySubmitWrapper.classList.add('hidden')
      summaryRowFeesValue.innerHTML = null
    }
    ipgAmount.value = response.bag.grand_total_hrk // must be in hrk

    if (summaryShippingCost) {
      summaryShippingCost.innerHTML = formatPrice(
        `${response.bag[`shipping_cost_${response.currency}`]}`, response.currency
      )
    }
    if (summaryGrandTotal) {
      summaryGrandTotal.innerHTML = formatPrice(
        `${response.bag[`grand_total_${response.currency}`]}`, response.currency
      )
    }
  }))
}

const updateIPGInputs = (response) => {
  ipgOrderNumber.value = response.order_number
  ipgAmount.value = response.grand_total_hrk // must be in hrk
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
}

const moveToPaymentForm = () => {
  continueToPaymentButton.disabled = false
  checkoutAddressTitle.classList.add('inactive')
  checkoutAddressWrapper.classList.add('inactive')
  checkoutPaymentTitle.classList.remove('inactive')
  checkoutPaymentWrapper.classList.remove('inactive')
}

export const processPaymentAddressData = (checkoutAddressForm) => {
  phoneNumberInput.required = true

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
    updateIPGInputs(response)

    if (response.region === 'hr') {
      cashOnDeliveryRadio.checked = true
      phoneNumberInput.required = true
      updatePaymentMethod(cashOnDeliveryRadio.value)
    } else {
      updatePaymentMethod(creditCardRadio.value)
    }
  }).then(
    () => moveToPaymentForm()
  ).catch((error) => {
    checkoutHelpText.innerHTML = error
    checkoutHelpText.classList.add('error')
  })
  checkoutAddressTitle.scrollIntoView(false)
}

export const switchActiveImage = (event) => {
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

    // history.pushState({mediaObject: id}, '', `?gallery-item=${id}`)
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
    }
  }).catch((error) => {
    joinNewsletterMessage.classList.add('error')
    joinNewsletterMessage.hidden = false
    joinNewsletterMessage.innerHTML = error
  })
}

export const hideBagMobile = () => {
  bagMobile.classList.add('bag-hide')
}

export const hideBag = () => {
  bag.classList.add('bag-hide')
}

let hideBagTimer
bag.addEventListener('mouseover', (event) => {
  clearTimeout(hideBagTimer)
})

bag.addEventListener('mouseout', (event) => {
  hideBagTimer = setTimeout(hideBag, 500)
})

export const refreshBag = (response) => {
  clearTimeout(hideBagTimer)

  bagTotal.innerHTML = formatPrice(
    `${response.bag[`total_${response.currency}`]}`, response.currency
  )
  bagTotalMobile.innerHTML = formatPrice(
    `${response.bag[`total_${response.currency}`]}`, response.currency
  )
  bagContent.innerHTML = ''
  bagContentMobile.innerHTML = ''

  for (const [key, values] of Object.entries(response.bag.products)) {
    bagContent.appendChild(createProductNode(key, values, response))
    bagContentMobile.appendChild(createProductNode(key, values, response))
  }
  bagItemCount.innerHTML = response.bag.total_quantity
  bagItemCountMobile.innerHTML = response.bag.total_quantity

  if (window.location.pathname !== '/review-bag/') {
    bag.classList.remove('bag-hide')
    hideBagTimer = setTimeout(hideBag, 3000)
  }
  if (Object.keys(response.bag.products).length < 1) {
    reviewBagLink.classList.add('hidden')
    reviewBagLinkMobile.classList.add('hidden')
    bagBuyLink.classList.remove('hidden')
    bagBuyMobileLink.classList.remove('hidden')
    setTimeout(hideBagMobile, 1000)
  } else {
    reviewBagLink.classList.remove('hidden')
    reviewBagLinkMobile.classList.remove('hidden')
    bagBuyLink.classList.add('hidden')
    bagBuyMobileLink.classList.add('hidden')
  }
}

const refreshReviewBag = (response, slug) => {
  const product = document.getElementById(slug)

  if (product) {
    product.remove()

    summaryShippingCost.innerHTML = formatPrice(
      `${response.bag[`shipping_cost_${response.currency}`]}`, response.currency
    )
    summaryTotal.innerHTML = formatPrice(
      `${response.bag[`total_${response.currency}`]}`, response.currency
    )
    summaryGrandTotal.innerHTML = formatPrice(
      `${response.bag[`grand_total_${response.currency}`]}`, response.currency
    )
  }

  if (summaryGrandTotalHrk) {
    summaryGrandTotalHrk.innerHTML = `${response.bag.grand_total_hrk} kn`
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
    `${values[`subtotal_${response.currency}`]}`, response.currency
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
      ipgAmount.value = response.bag.grand_total_hrk // must be in hrk
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
  updateProduct(slug, 'increment')
}

export const removeOneFromBag = (slug) => {
  updateProduct(slug, 'decrement')
}
