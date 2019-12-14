import {
  setCookieInfo,
  setRegion,
} from './requests'
import {
  addToBagButtons,
  bag,
  bagLink,
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
  differentShippingAddressInput,
  differentShippingAddressInputWrapper,
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
  invoiceFormShippingAddressInput,
  invoiceFormShippingCityInput,
  invoiceFormShippingCountryInput,
  invoiceFormShippingFirstNameInput,
  invoiceFormShippingLastNameInput,
  invoiceFormShippingZipCodeInput,
  invoiceFormZipCodeInput,
  ipgCheckoutForm,
  ipgFormSubmitButton,
  joinNewsletterMessage,
  languageFormsMobile,
  languageInputsMobile,
  languageOptions,
  logingFormPasswordInput,
  logingFormPasswordInput1,
  logingFormPasswordInput2,
  logingFormUsernameInput,
  navigationWrapper,
  navMobileCloseButton,
  navMobileOpenButton,
  phoneNumberInput,
  previousStepLink,
  r1ReceiptCheckbox,
  registerButton,
  registerForm,
  removeProductButtons,
  sameShippingAddressInput,
  sameShippingAddressInputWrapper,
  shippingAddressChoice,
  shippingAddressWrapper,
  shipToMenu,
  subscribeToNewsletterButton,
  thumbnailWrappers,
  termsCheckboxErrorMessage,
} from './selectors'
import {
  addOneToBag,
  addToBag,
  clearErrorMessages,
  processPaymentAddressData,
  refreshBag,
  removeFromBag,
  removeOneFromBag,
  showErrorMessage,
  subToNewsletter,
  switchActiveImage,
  toggleBag,
  toggleStickyNav,
  updatePaymentMethod,
  updateShippingAddressData,
  updateShippingCostForCountry,
} from './utils'

const ready = (runScript) => {
  if (document.attachEvent ? document.readyState === 'complete' : document.readyState !== 'loading') {
    runScript()
  } else {
    document.addEventListener('DOMContentLoaded', runScript)
  }
}

ready(() => {
  navMobileOpenButton && navMobileOpenButton.addEventListener('click', (event) => {
    navigationWrapper.classList.add('nav-mobile-open')
    bag.classList.remove('bag-show')
    document.body.classList.add('lock-scroll')
  })

  navMobileCloseButton && navMobileCloseButton.addEventListener('click', (event) => {
    navigationWrapper.classList.remove('nav-mobile-open')
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

  fieldInfo && fieldInfo.addEventListener('click', (event) => {
    fieldInfo.hidden = true
  })

  previousStepLink && previousStepLink.addEventListener('click', (event) => {
    event.preventDefault()
    phoneNumberInput.required = false

    checkoutAddressTitle.classList.remove('inactive')
    checkoutAddressWrapper.classList.remove('inactive')
    checkoutPaymentTitle.classList.add('inactive')
    checkoutPaymentWrapper.classList.add('inactive')
    updateShippingCostForCountry(invoiceFormCountryInput.value)

    creditCardRadio.checked = false
    shippingAddressChoice.hidden = true
    shippingAddressWrapper.hidden = true
    invoiceFormShippingFirstNameInput.required = false
    invoiceFormShippingLastNameInput.required = false
    invoiceFormShippingCountryInput.required = false
    invoiceFormShippingAddressInput.required = false
    invoiceFormShippingCityInput.required = false
    invoiceFormShippingZipCodeInput.required = false
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
      updateShippingCostForCountry(
        invoiceFormCountryInput.value, () => updatePaymentMethod(cashOnDeliveryRadio.value)
      )

      shippingAddressChoice.hidden = true
      shippingAddressWrapper.hidden = true
      invoiceFormShippingFirstNameInput.required = false
      invoiceFormShippingLastNameInput.required = false
      invoiceFormShippingCountryInput.required = false
      invoiceFormShippingAddressInput.required = false
      invoiceFormShippingCityInput.required = false
      invoiceFormShippingZipCodeInput.required = false
    }
  })

  creditCardWrapper && creditCardWrapper.addEventListener('click', (event) => {
    if (!creditCardRadio.checked) {
      creditCardRadio.checked = true
      phoneNumberInput.required = false

      shippingAddressChoice.hidden = false
      sameShippingAddressInput.checked = true
      updatePaymentMethod(creditCardRadio.value)

      differentShippingAddressInputWrapper.scrollIntoView(false)
    }
  })

  differentShippingAddressInputWrapper && differentShippingAddressInputWrapper.addEventListener('click', (event) => {
    if (!differentShippingAddressInput.checked) {
      differentShippingAddressInput.checked = true
      shippingAddressWrapper.hidden = false

      if (invoiceFormShippingCountryInput.value) {
        updateShippingCostForCountry(invoiceFormShippingCountryInput.value)
      }

      invoiceFormShippingFirstNameInput.required = true
      invoiceFormShippingLastNameInput.required = true
      invoiceFormShippingCountryInput.required = true
      invoiceFormShippingAddressInput.required = true
      invoiceFormShippingCityInput.required = true
      invoiceFormShippingZipCodeInput.required = true

      differentShippingAddressInput.scrollIntoView()
    }
  })

  sameShippingAddressInputWrapper && sameShippingAddressInputWrapper.addEventListener('click', (event) => {
    if (!sameShippingAddressInput.checked) {
      sameShippingAddressInput.checked = true
      shippingAddressWrapper.hidden = true
      updateShippingCostForCountry(invoiceFormCountryInput.value)

      invoiceFormShippingFirstNameInput.required = false
      invoiceFormShippingLastNameInput.required = false
      invoiceFormShippingCountryInput.required = false
      invoiceFormShippingAddressInput.required = false
      invoiceFormShippingCityInput.required = false
      invoiceFormShippingZipCodeInput.required = false
    }
  })

  ipgFormSubmitButton && ipgFormSubmitButton.addEventListener('click', (event) => {
    event.preventDefault()
    const valid = ipgCheckoutForm.reportValidity()

    if (valid) {
      if (differentShippingAddressInput.checked) {
        updateShippingAddressData(ipgCheckoutForm)
      } else {
        ipgCheckoutForm.submit()
      }
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
    clearErrorMessages()
    const valid = checkoutAddressForm.reportValidity()

    if (valid) {
      processPaymentAddressData(checkoutAddressForm)

      if (creditCardRadio.checked) {
        shippingAddressChoice.hidden = false
      }
      if (creditCardRadio.checked && differentShippingAddressInput.checked) {
        shippingAddressWrapper.hidden = false
        updateShippingCostForCountry(invoiceFormShippingCountryInput.value)
      }
    } else {
      continueToPaymentButton.disabled = false
    }
  })

  cashOnDeliverySubmitButton && cashOnDeliverySubmitButton.addEventListener('click', (event) => {
    event.preventDefault()

    cashOnDeliverySubmitButton.disabled = true
    clearErrorMessages()
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
    joinNewsletterMessage.classList.add('error')

    const emailData = {
      email0: '',
      email1: '',
    }
    for (let i = 0; i < emailInputs.length; i++) {
      emailData[`email${i}`] = emailInputs[i].value
    }
    subToNewsletter(emailData).then((success) => {
      subscribeToNewsletterButton.disabled = success
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
    clearErrorMessages()
    registerButton.classList.add('disabled')

    const valid = registerForm.reportValidity()
    if (!valid) {
      registerButton.classList.remove('disabled')
    }
  })

  invoiceFormAgreeToTermsInput && invoiceFormAgreeToTermsInput.addEventListener('invalid', (event) => {
    event.target.setCustomValidity('')

    if (!event.target.checked) {
      const errorMessage = termsCheckboxErrorMessage.innerHTML
      event.target.setCustomValidity(errorMessage)
    } else {
      const valid = checkoutAddressForm.reportValidity()

      if (valid) {
        clearErrorMessages()

        if (creditCardRadio.checked) {
          shippingAddressChoice.hidden = false
        }
        if (creditCardRadio.checked && differentShippingAddressInput.checked) {
          shippingAddressWrapper.hidden = false
          updateShippingCostForCountry(invoiceFormShippingCountryInput.value)
        }
        processPaymentAddressData(checkoutAddressForm)
      }
    }
  })

  invoiceFormCountryInput && invoiceFormCountryInput.addEventListener('change', (event) => {
    const selected = event.target.value
    if (selected && invoiceFormShippingCountryInput && !invoiceFormShippingCountryInput.value) {
      updateShippingCostForCountry(selected)
    }
  })

  invoiceFormShippingCountryInput && invoiceFormShippingCountryInput.addEventListener('change', (event) => {
    const selected = event.target.value
    if (selected) {
      updateShippingCostForCountry(selected)
    }
  })

  invoiceFormFirstNameInput && invoiceFormFirstNameInput.addEventListener('invalid', (event) => {
    event.preventDefault()
    showErrorMessage(event.target)
  })

  invoiceFormLastNameInput && invoiceFormLastNameInput.addEventListener('invalid', (event) => {
    event.preventDefault()
    showErrorMessage(event.target)
  })

  invoiceFormCountryInput && invoiceFormCountryInput.addEventListener('invalid', (event) => {
    event.preventDefault()
    showErrorMessage(event.target)
  })

  invoiceFormAddressInput && invoiceFormAddressInput.addEventListener('invalid', (event) => {
    event.preventDefault()
    showErrorMessage(event.target)
  })

  invoiceFormCityInput && invoiceFormCityInput.addEventListener('invalid', (event) => {
    event.preventDefault()
    showErrorMessage(event.target)
  })

  invoiceFormZipCodeInput && invoiceFormZipCodeInput.addEventListener('invalid', (event) => {
    event.preventDefault()
    showErrorMessage(event.target)
  })

  invoiceFormShippingFirstNameInput && invoiceFormShippingFirstNameInput.addEventListener('invalid', (event) => {
    event.preventDefault()
    showErrorMessage(event.target)
  })

  invoiceFormShippingLastNameInput && invoiceFormShippingLastNameInput.addEventListener('invalid', (event) => {
    event.preventDefault()
    showErrorMessage(event.target)
  })

  invoiceFormShippingCountryInput && invoiceFormShippingCountryInput.addEventListener('invalid', (event) => {
    event.preventDefault()
    showErrorMessage(event.target)
  })

  invoiceFormShippingAddressInput && invoiceFormShippingAddressInput.addEventListener('invalid', (event) => {
    event.preventDefault()
    showErrorMessage(event.target)
  })

  invoiceFormShippingCityInput && invoiceFormShippingCityInput.addEventListener('invalid', (event) => {
    event.preventDefault()
    showErrorMessage(event.target)
  })

  invoiceFormShippingZipCodeInput && invoiceFormShippingZipCodeInput.addEventListener('invalid', (event) => {
    event.preventDefault()
    showErrorMessage(event.target)
  })

  invoiceFormEmailInput && invoiceFormEmailInput.addEventListener('invalid', (event) => {
    event.preventDefault()
    showErrorMessage(event.target)
  })

  phoneNumberInput && phoneNumberInput.addEventListener('invalid', (event) => {
    event.preventDefault()
    fieldInfo.hidden = false
    showErrorMessage(event.target)
  })

  logingFormUsernameInput && logingFormUsernameInput.addEventListener('invalid', (event) => {
    event.preventDefault()
    showErrorMessage(event.target)
  })

  logingFormPasswordInput && logingFormPasswordInput.addEventListener('invalid', (event) => {
    event.preventDefault()
    showErrorMessage(event.target)
  })

  logingFormPasswordInput1 && logingFormPasswordInput1.addEventListener('invalid', (event) => {
    event.preventDefault()
    showErrorMessage(event.target)
  })

  logingFormPasswordInput2 && logingFormPasswordInput2.addEventListener('invalid', (event) => {
    event.preventDefault()
    showErrorMessage(event.target)
  })

  checkoutR1CompanyAddress && checkoutR1CompanyAddress.addEventListener('invalid', (event) => {
    event.preventDefault()
    showErrorMessage(event.target)
  })

  checkoutR1CompanyName && checkoutR1CompanyName.addEventListener('invalid', (event) => {
    event.preventDefault()
    showErrorMessage(event.target)
  })

  checkoutR1CompanyUIN && checkoutR1CompanyUIN.addEventListener('invalid', (event) => {
    event.preventDefault()
    showErrorMessage(event.target)
  })

  for (let i = languageFormsMobile.length - 1; i >= 0; i--) {
    languageFormsMobile[i].addEventListener('change', (event) => {
      languageInputsMobile[i].value = event.target.value === 'hr' ? 'hr' : 'en'

      setRegion(event.target.value).then((data) => data.json().then((response) => {
        refreshBag(response)
        languageFormsMobile[i].submit()
      }))
    })
  }
})
