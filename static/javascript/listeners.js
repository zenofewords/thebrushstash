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
  checkoutIpgWrapper,
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
  invoiceFormNote,
  invoiceFormShippingAddressInput,
  invoiceFormShippingCityInput,
  invoiceFormShippingCountryInput,
  invoiceFormShippingFirstNameInput,
  invoiceFormShippingLastNameInput,
  invoiceFormShippingZipCodeInput,
  invoiceFormStateCountyInput,
  invoiceFormZipCodeInput,
  ipgCheckoutForm,
  ipgFormSubmitButton,
  joinNewsletterMessage,
  languageFormsMobile,
  languageInputsMobile,
  languageOptions,
  loginButton,
  logingFormPasswordInput,
  logingFormPasswordInput1,
  logingFormPasswordInput2,
  logingFormUsernameInput,
  navigationWrapper,
  navMobileCloseButton,
  navMobileOpenButton,
  phoneNumberInput,
  previousStepLink,
  productDescription,
  productAboutTab,
  productReviewContent,
  productReviewContentErrorMessage,
  productReviewRatingErrorMessage,
  productReviewTab,
  productReview,
  productReviewForm,
  promoCodeInput,
  promoCodeSubmitButton,
  r1ReceiptCheckbox,
  ratingLink,
  registerButton,
  registerForm,
  removeProductButtons,
  sameShippingAddressInput,
  sameShippingAddressInputWrapper,
  shippingAddressChoice,
  shippingAddressWrapper,
  shipToMenu,
  starScoreInputs,
  submitReviewButton,
  subscribeToNewsletterButton,
  termsCheckboxErrorMessage,
  thumbnailWrappers,
} from './selectors'
import {
  addOneToBag,
  addToBag,
  continueToPayment,
  clearErrorMessages,
  processPaymentAddressData,
  processPromoCode,
  refreshBag,
  removeFromBag,
  removeOneFromBag,
  scrollToElement,
  showErrorMessage,
  submitReview,
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

    checkoutAddressTitle.classList.remove('inactive')
    checkoutAddressWrapper.classList.remove('inactive')
    checkoutPaymentTitle.classList.add('inactive')
    checkoutPaymentWrapper.classList.add('inactive')
    checkoutIpgWrapper.classList.add('inactive')
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

  if (invoiceFormCountryInput && invoiceFormCountryInput.value) {
    updateShippingCostForCountry(invoiceFormCountryInput.value)
  }

  cashOnDeliveryWrapper && cashOnDeliveryWrapper.addEventListener('click', (event) => {
    if (!cashOnDeliveryRadio.checked) {
      cashOnDeliveryRadio.checked = true
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

      shippingAddressChoice.hidden = false
      sameShippingAddressInput.checked = true
      updatePaymentMethod(creditCardRadio.value)

      scrollToElement(differentShippingAddressInputWrapper, 240)
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

      scrollToElement(differentShippingAddressInput)
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

    ipgFormSubmitButton.disabled = true
    clearErrorMessages()
    const valid = ipgCheckoutForm.reportValidity()

    if (valid) {
      if (differentShippingAddressInput.checked) {
        processPaymentAddressData(checkoutAddressForm, () => updateShippingAddressData(ipgCheckoutForm))
      } else {
        processPaymentAddressData(checkoutAddressForm, () => ipgCheckoutForm.submit())
      }
    } else {
      ipgFormSubmitButton.disabled = false
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
      continueToPayment(invoiceFormCountryInput.value)
    } else {
      continueToPaymentButton.disabled = false
    }
  })

  cashOnDeliverySubmitButton && cashOnDeliverySubmitButton.addEventListener('click', (event) => {
    event.preventDefault()

    cashOnDeliverySubmitButton.disabled = true
    clearErrorMessages()
    const valid = checkoutAddressForm.reportValidity()

    if (valid) {
      processPaymentAddressData(checkoutAddressForm, () => checkoutAddressForm.submit())
    } else {
      cashOnDeliverySubmitButton.disabled = false
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
      event.target.setCustomValidity(termsCheckboxErrorMessage.innerHTML)
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
        continueToPayment(invoiceFormCountryInput.value)
      }
    }
  })

  const showInputLabel = (input) => {
    const label = input.closest('div').querySelector('.field-label')

    if (input.value.length > 0) {
      input.classList.add('show-label')
      label.classList.add('show-label')
    } else {
      input.classList.remove('show-label')
      label.classList.remove('show-label')
    }
  }

  const formInputs = [
    invoiceFormFirstNameInput,
    invoiceFormLastNameInput,
    invoiceFormCountryInput,
    invoiceFormAddressInput,
    invoiceFormCityInput,
    invoiceFormZipCodeInput,
    invoiceFormStateCountyInput,
    invoiceFormShippingFirstNameInput,
    invoiceFormShippingLastNameInput,
    invoiceFormShippingAddressInput,
    invoiceFormShippingCityInput,
    invoiceFormShippingZipCodeInput,
    invoiceFormEmailInput,
    phoneNumberInput,
    logingFormUsernameInput,
    logingFormPasswordInput,
    logingFormPasswordInput1,
    logingFormPasswordInput2,
    checkoutR1CompanyAddress,
    checkoutR1CompanyName,
    checkoutR1CompanyUIN,
    invoiceFormCountryInput,
    invoiceFormNote,
  ]

  for (let i = 0; i < formInputs.length; i++) {
    if (formInputs[i]) {
      showInputLabel(formInputs[i])

      formInputs[i].addEventListener('input', (event) => {
        showInputLabel(formInputs[i])
      })

      formInputs[i].addEventListener('invalid', (event) => {
        event.preventDefault()
        showErrorMessage(event.target)

        if (formInputs[i] === phoneNumberInput) {
          fieldInfo.hidden = false
        }
      })
    }
  }

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

  for (let i = languageFormsMobile.length - 1; i >= 0; i--) {
    languageFormsMobile[i].addEventListener('change', (event) => {
      languageInputsMobile[i].value = event.target.value === 'hr' ? 'hr' : 'en'

      setRegion(event.target.value).then((data) => data.json().then((response) => {
        refreshBag(response)
        languageFormsMobile[i].submit()
      }))
    })
  }

  ratingLink && ratingLink.addEventListener('click', (event) => {
    event.preventDefault()

    productDescription.hidden = true
    productReview.hidden = false
    productAboutTab.classList.remove('active')
    productReviewTab.classList.add('active')

    scrollToElement(productReviewTab)
  })

  submitReviewButton && submitReviewButton.addEventListener('click', (event) => {
    event.preventDefault()
    starScoreInputs[0].setCustomValidity('')
    productReviewContent.setCustomValidity('')

    submitReviewButton.disabled = true
    clearErrorMessages()

    const valid = productReviewForm.reportValidity()
    if (valid) {
      submitReview(productReviewForm)
    } else {
      starScoreInputs[0].setCustomValidity(productReviewRatingErrorMessage.innerHTML)
      productReviewContent.setCustomValidity(productReviewContentErrorMessage.innerHTML)
      submitReviewButton.disabled = false
    }
  })

  productAboutTab && productAboutTab.addEventListener('click', (event) => {
    event.preventDefault()

    productDescription.hidden = false
    productReview.hidden = true
    productAboutTab.classList.add('active')
    productReviewTab.classList.remove('active')
  })

  productReviewTab && productReviewTab.addEventListener('click', (event) => {
    event.preventDefault()

    productDescription.hidden = true
    productReview.hidden = false
    productAboutTab.classList.remove('active')
    productReviewTab.classList.add('active')
  })

  for (let i = 0; i < starScoreInputs.length; i++) {
    starScoreInputs[i].addEventListener('click', (event) => {
      const score = parseInt(event.target.value)

      const starIcons = document.getElementsByClassName('star-icon')
      for (var s = 0; s < starIcons.length; s++) {
        starIcons[s].hidden = false
      }
      const starFillIcons = document.getElementsByClassName('star-fill-icon')
      for (let f = 0; f < starFillIcons.length; f++) {
        starFillIcons[f].hidden = true
      }

      for (let j = 0; j < score; j++) {
        const starFillIcon = starFillIcons[j]
        starFillIcon.hidden = false

        const starIcon = starIcons[j]
        starIcon.hidden = true
      }
    })
  }

  promoCodeSubmitButton && promoCodeSubmitButton.addEventListener('click', (event) => {
    promoCodeInput.classList.remove('promo-code-error')

    if (!promoCodeInput.value) {
      promoCodeInput.classList.add('promo-code-error')
    } else {
      processPromoCode(promoCodeInput.value)
    }
  })

  loginButton && loginButton.addEventListener('click', (event) => {
    const redirect = () => {
      const search = new URLSearchParams(window.location.search)
      window.location.replace(search.get('next') ? search.get('next') : '/')
    }
    setTimeout(redirect, 5000)
  })
})
