import {
  addToBagSelect
} from './selectors'
import {
  getCookie,
} from './utils'

const fetchRequest = (url, payload) => fetch(
  url,
  {
    method: 'POST',
    cache: 'no-cache',
    credentials: 'same-origin',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    body: JSON.stringify(payload),
  }
)

export const setRegion = (region) => fetchRequest(
  '/api/region/',
  {
    region: region,
  }
)

export const setCookieInfo = () => fetchRequest(
  '/api/cookie/',
  {
    accepted: true,
  }
)

export const setPaymentMethod = (paymentMethod) => fetchRequest(
  '/api/update-payment-method/',
  {
    payment_method: paymentMethod,
  }
)

export const continueToPaymentRequest = (countryName) => fetchRequest(
  '/api/continue-to-payment/',
  {
    country_name: countryName,
  }
)

export const processOrder = (data) => fetchRequest(
  '/api/process-order/',
  data,
)

export const removeProduct = (slug) => fetchRequest(
  '/api/remove-from-bag/',
  {
    slug: slug,
  }
)

export const addProduct = (dataset) => fetchRequest(
  '/api/add-to-bag/',
  {
    pk: dataset.id,
    slug: dataset.slug,
    name: dataset.name,
    quantity: parseInt(dataset.multiple ? addToBagSelect.value : 1),
    price_hrk: parseFloat(dataset.priceHrk.replace(',', '.')),
    price_eur: parseFloat(dataset.priceEur.replace(',', '.')),
    price_gbp: parseFloat(dataset.priceGbp.replace(',', '.')),
    price_usd: parseFloat(dataset.priceUsd.replace(',', '.')),
    tax: parseFloat(dataset.tax.replace(',', '.')),
    image_url: dataset.imageUrl,
  }
)

export const updateProduct = (slug, action) => fetchRequest(
  '/api/update-bag/',
  {
    slug: slug,
    action: action,
  }
)

export const updateShippingAddress = (data) => fetchRequest(
  '/api/update-shipping-address/',
  data,
)

export const updateShippingCost = (countryName) => fetchRequest(
  '/api/update-shipping-cost/',
  {
    country_name: countryName,
  }
)

export const subscribeToNewsletter = (emailData) => fetchRequest(
  '/api/subscribe-to-newsletter/',
  {
    email0: emailData['email0'],
    email1: emailData['email1'],
  }
)
