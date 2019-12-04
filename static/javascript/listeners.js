import {
  setCookieInfo,
} from './requests'
import {
  addToBagButtons,
  bagLink,
  bagMobile,
  bagMobileOpenButton,
  bagProductDecrement,
  bagProductIncrement,
  cashOnDeliveryRadio,
  cashOnDeliverySubmitButton,
  cashOnDeliveryWrapper,
  checkoutAddressForm,
  checkoutAddressTitle,
  checkoutAddressWrapper,
  checkoutPaymentTitle,
  checkoutPaymentWrapper,
  checkoutR1CompanyAddress,
  checkoutR1CompanyName,
  checkoutR1CompanyUIN,
  checkoutR1FieldsWrapper,
  closeModalButtons,
  continueToPaymentButton,
  cookieInfo,
  cookieWrapper,
  creditCardRadio,
  creditCardSecureLogos,
  creditCardSecureModals,
  creditCardWrapper,
  emailInputs,
  fieldInfo,
  fieldInfoIcon,
  invoiceFormAddressInput,
  invoiceFormAgreeToTermsInput,
  invoiceFormCityInput,
  invoiceFormCountryInput,
  invoiceFormEmailInput,
  invoiceFormFirstNameInput,
  invoiceFormLastNameInput,
  invoiceFormZipCodeInput,
  languageOptions,
  navigationWrapper,
  navMobileCloseButton,
  navMobileOpenButton,
  phoneNumberInput,
  previousStepLink,
  r1ReceiptCheckbox,
  registerButton,
  registerForm,
  removeProductButtons,
  shipToMenu,
  subscribeToNewsletterButton,
  thumbnailWrappers,
} from './selectors'
import {
  addOneToBag,
  addToBag,
  hideErrorMessages,
  processPaymentAddressData,
  removeFromBag,
  removeOneFromBag,
  showErrorMessage,
  subToNewsletter,
  switchActiveImage,
  toggleBag,
  toggleStickyNav,
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

    continueToPaymentButton.disabled = true
    hideErrorMessages()
    const valid = checkoutAddressForm.reportValidity()

    if (valid) {
      processPaymentAddressData(checkoutAddressForm)
    } else {
      continueToPaymentButton.disabled = false
    }
  })

  cashOnDeliverySubmitButton && cashOnDeliverySubmitButton.addEventListener('click', (event) => {
    event.preventDefault()

    cashOnDeliverySubmitButton.disabled = true
    hideErrorMessages()
    previousStepLink.style.pointerEvents = 'none'
    const valid = checkoutAddressForm.reportValidity()

    if (valid) {
      checkoutAddressForm.submit()
    } else {
      cashOnDeliverySubmitButton.disabled = false
      previousStepLink.style.pointerEvents = 'auto'
    }
  })

  subscribeToNewsletterButton && subscribeToNewsletterButton.addEventListener('click', (event) => {
    subscribeToNewsletterButton.disabled = true

    const emailData = {
      email0: '',
      email1: '',
    }
    for (let i = 0; i < emailInputs.length; i++) {
      emailData[`email${i}`] = emailInputs[i].value
    }
    subToNewsletter(emailData).then(() => {
      subscribeToNewsletterButton.disabled = false
    })
  })

  for (let i = 0; i < bagProductDecrement.length; i++) {
    bagProductDecrement[i].addEventListener('click', (event) => {
      removeOneFromBag(bagProductDecrement[i].dataset.slug)
    })
  }

  for (let i = 0; i < bagProductIncrement.length; i++) {
    bagProductIncrement[i].addEventListener('click', (event) => {
      addOneToBag(bagProductDecrement[i].dataset.slug)
    })
  }

  for (let i = 0; i < removeProductButtons.length; i++) {
    const button = removeProductButtons[i]
    button.addEventListener('click', () => removeFromBag(button.dataset.slug))
  }

  for (let i = 0; i < addToBagButtons.length; i++) {
    const button = addToBagButtons[i]
    button.addEventListener('click', () => addToBag(button.dataset))
  }

  registerButton && registerButton.addEventListener('click', (event) => {
    registerButton.classList.add('disabled')

    const valid = registerForm.reportValidity()
    if (!valid) {
      registerButton.classList.remove('disabled')
    }
  })

  invoiceFormAgreeToTermsInput && invoiceFormAgreeToTermsInput.addEventListener('invalid', (event) => {
    if (!event.target.checked) {
      event.target.setCustomValidity('Potrebno je pristati na uvjete korištenja prije nastavka kupnje.')
    } else {
      event.target.setCustomValidity('')
      const valid = checkoutAddressForm.reportValidity()

      if (valid) {
        hideErrorMessages()
        processPaymentAddressData(checkoutAddressForm)
      }
    }
  })

  invoiceFormFirstNameInput && invoiceFormFirstNameInput.addEventListener('invalid', (event) => {
    event.preventDefault()
    showErrorMessage(event.target.id)
  })

  invoiceFormLastNameInput && invoiceFormLastNameInput.addEventListener('invalid', (event) => {
    event.preventDefault()
    showErrorMessage(event.target.id)
  })

  invoiceFormCountryInput && invoiceFormCountryInput.addEventListener('invalid', (event) => {
    event.preventDefault()
    showErrorMessage(event.target.id, 'Odaberite državu.')
  })

  invoiceFormAddressInput && invoiceFormAddressInput.addEventListener('invalid', (event) => {
    event.preventDefault()
    showErrorMessage(event.target.id)
  })

  invoiceFormCityInput && invoiceFormCityInput.addEventListener('invalid', (event) => {
    event.preventDefault()
    showErrorMessage(event.target.id)
  })

  invoiceFormZipCodeInput && invoiceFormZipCodeInput.addEventListener('invalid', (event) => {
    event.preventDefault()
    showErrorMessage(event.target.id)
  })

  invoiceFormEmailInput && invoiceFormEmailInput.addEventListener('invalid', (event) => {
    event.preventDefault()
    showErrorMessage(event.target.id, 'Unesite ispravnu e-mail adresu.')
  })

  phoneNumberInput && phoneNumberInput.addEventListener('invalid', (event) => {
    console.log('phone invalid')
    event.preventDefault()
    showErrorMessage(event.target.id, 'Ovo polje je obavezno.')
  })
})
