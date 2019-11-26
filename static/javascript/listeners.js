import {
  setCookieInfo,
} from './requests'
import {
  bagLink,
  cashOnDeliveryRadio,
  cashOnDeliveryWrapper,
  cookieInfo,
  cookieWrapper,
  bagMobile,
  bagMobileOpenButton,
  checkoutR1CompanyAddress,
  checkoutR1CompanyName,
  checkoutR1CompanyUIN,
  checkoutR1FieldsWrapper,
  creditCardRadio,
  creditCardWrapper,
  fieldInfo,
  fieldInfoIcon,
  navigationWrapper,
  navMobileCloseButton,
  navMobileOpenButton,
  r1ReceiptCheckbox,
  previousStepLink,
  phoneNumberInput,
  checkoutAddressTitle,
  checkoutAddressWrapper,
  checkoutPaymentTitle,
  checkoutPaymentWrapper,
  creditCardSecureLogos,
  creditCardSecureModals,
  closeModalButtons,
  languageOptions,
  shipToMenu,
  thumbnailWrappers,
  continueToPaymentButton,
  checkoutAddressForm,
} from './selectors'
import {
  switchActiveImage,
  toggleBag,
  toggleStickyNav,
  processPaymentAddressData,
  updatePaymentMethod,
} from './utils'

const ready = (runScript) => {
  if (document.attachEvent ? document.readyState === 'complete' : document.readyState !== 'loading') {
    runScript()
  } else {
    document.addEventListener('DOMContentLoaded', runScript)
  }
}

ready(() => {
  bagMobileOpenButton && bagMobileOpenButton.addEventListener('click', (event) => {
    bagMobile.classList.toggle('bag-hide')
  })

  navMobileOpenButton && navMobileOpenButton.addEventListener('click', (event) => {
    navigationWrapper.classList.remove('nav-mobile-close')
    document.body.classList.add('lock-scroll')
  })

  navMobileCloseButton && navMobileCloseButton.addEventListener('click', (event) => {
    navigationWrapper.classList.add('nav-mobile-close')
    document.body.classList.remove('lock-scroll')
  })

  r1ReceiptCheckbox && r1ReceiptCheckbox.addEventListener('change', (event) => {
    const checked = r1ReceiptCheckbox.checked
    checkoutR1FieldsWrapper.hidden = !checked
    checkoutR1CompanyName.required = checked
    checkoutR1CompanyAddress.required = checked
    checkoutR1CompanyUIN.required = checked
  })

  fieldInfoIcon && fieldInfoIcon.addEventListener('click', (event) => {
    fieldInfo.hidden = !fieldInfo.hidden
  })

  creditCardWrapper && creditCardWrapper.addEventListener('click', (event) => {
    creditCardRadio.checked = true
  })

  previousStepLink && previousStepLink.addEventListener('click', (event) => {
    event.preventDefault()
    phoneNumberInput.required = false

    checkoutAddressTitle.classList.remove('inactive')
    checkoutAddressWrapper.classList.remove('inactive')
    checkoutPaymentTitle.classList.add('inactive')
    checkoutPaymentWrapper.classList.add('inactive')
  })

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

  for (let i = 0; i < languageOptions.length; i++) {
    languageOptions[i].addEventListener('blur', (event) => {
      if (!event.relatedTarget || !event.relatedTarget.classList.contains('language-option')) {
        shipToMenu.hidden = true
      }
    })
  }

  cookieInfo && cookieInfo.addEventListener('click', () => {
    setCookieInfo().then(() => {
      cookieWrapper.hidden = true
    })
  })

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

  bagLink && bagLink.addEventListener('click', toggleBag)

  cashOnDeliveryWrapper && cashOnDeliveryWrapper.addEventListener('click', (event) => {
    if (!cashOnDeliveryRadio.checked) {
      cashOnDeliveryRadio.checked = true
      phoneNumberInput.required = true
      updatePaymentMethod(cashOnDeliveryRadio.value)
    }
  })

  creditCardWrapper && creditCardWrapper.addEventListener('click', (event) => {
    if (!creditCardRadio.checked) {
      creditCardRadio.checked = true
      phoneNumberInput.required = false
      updatePaymentMethod(creditCardRadio.value)
    }
  })

  for (var i = 0; i < thumbnailWrappers.length; i++) {
    thumbnailWrappers[i].addEventListener('click', (event) => {
      event.preventDefault()

      switchActiveImage(event)
    })
  }

  continueToPaymentButton && continueToPaymentButton.addEventListener('click', (event) => {
    event.preventDefault()
    const valid = checkoutAddressForm.reportValidity()

    if (valid) {
      processPaymentAddressData(checkoutAddressForm)
    }
  })
})
