import {
  addToBagSelect
} from './selectors'
import {
  getCookie,
} from './utils'

export const setRegion = (event) => fetch(
  '/api/region/',
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
)

export const setCookieInfo = () => fetch(
  '/api/cookie/',
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
)

export const setPaymentMethod = (paymentMethod) => fetch(
  '/api/update-payment-method/',
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
)

export const processOrder = (data) => fetch(
  '/api/process-order/',
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
)

export const removeProduct = (slug) => fetch(
  '/api/remove-from-bag/',
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
)

export const addProduct = (dataset) => fetch(
  '/api/add-to-bag/',
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
      price_hrk: parseFloat(dataset.priceHrk.replace(',', '.')),
      price_eur: parseFloat(dataset.priceEur.replace(',', '.')),
      price_gbp: parseFloat(dataset.priceGbp.replace(',', '.')),
      price_usd: parseFloat(dataset.priceUsd.replace(',', '.')),
      image_url: dataset.imageUrl,
    }),
  }
)

export const subscribeToNewsletter = (emailData) => fetch(
  '/api/subscribe-to-newsletter/',
  {
    method: 'POST',
    cache: 'no-cache',
    credentials: 'same-origin',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    body: JSON.stringify({
      email0: emailData['email0'],
      email1: emailData['email1'],
    }),
  }
)
