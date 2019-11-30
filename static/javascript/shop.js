import '../sass/shop.sass'
import './listeners'
import {
  addProduct,
  removeProduct,
  setRegion,
} from './requests'
import {
  addToBagButtons,
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
  ipgAmount,
  ipgCart,
  languageForm,
  languageInput,
  navigationWrapper,
  removeProductButtons,
  reviewBagLink,
  reviewBagLinkMobile,
  shipToMenu,
  shipToSelects,
  summaryCheckoutButton,
  summaryGrandTotal,
  summaryGrandTotalHrk,
  summaryShippingCost,
  summaryTotal,
  videoWrappers,
} from './selectors'

import {
  formatPrice,
} from './utils'

const ready = (runScript) => {
  if (document.attachEvent ? document.readyState === 'complete' : document.readyState !== 'loading') {
    runScript()
  } else {
    document.addEventListener('DOMContentLoaded', runScript)
  }
}

ready(() => {
  for (let i = 0; i < addToBagButtons.length; i++) {
    const button = addToBagButtons[i]
    button.addEventListener('click', () => addToBag(button.dataset))
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

  for (let i = 0; i < removeProductButtons.length; i++) {
    const button = removeProductButtons[i]
    button.addEventListener('click', () => removeFromBag(button.dataset.slug))
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
    productRemove.innerHTML = '&times;'
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

  let hideBagTimer
  const hideBag = () => {
    bag.classList.add('bag-hide')
  }
  const hideBagMobile = () => {
    bagMobile.classList.add('bag-hide')
  }

  bag.addEventListener('mouseover', (event) => {
    clearTimeout(hideBagTimer)
  })
  bag.addEventListener('mouseout', (event) => {
    hideBagTimer = setTimeout(hideBag, 500)
  })

  const refreshBag = (response) => {
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

  const addToBag = (dataset) => {
    addProduct(dataset).then((data) => data.json().then((response) => {
      refreshBag(response)
    }))
  }

  const removeFromBag = (slug) => {
    removeProduct(slug).then((data) => data.json().then((response) => {
      refreshBag(response)
      refreshReviewBag(response, slug)

      if (ipgAmount && ipgCart) {
        ipgAmount.value = response.bag.grand_total_hrk // must be in hrk
        ipgCart.value = response.cart
      }
    }))
  }
})
