import '../sass/shop.sass'

const ready = (runGeneral) => {
  if (document.attachEvent ? document.readyState === 'complete' : document.readyState !== 'loading') {
    runGeneral()
  } else {
    document.addEventListener('DOMContentLoaded', runGeneral)
  }
}

ready(() => {
  document.querySelector('.close-cookie-info').addEventListener('click', () => {
    document.querySelector('.cookie-wrappper').hidden = true
  })

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
})
