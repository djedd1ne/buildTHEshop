const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

export function loginWith42() {
  window.location.href = `${API_URL}/auth/42/login`
}

export function loginWithLearningHub() {
  window.location.href = `${API_URL}/auth/learninghub/login`
}

export async function fetchMe(token) {
  const res = await fetch(`${API_URL}/me`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })

  if (!res.ok) {
    throw new Error('Unauthorized')
  }

  return await res.json()
}

export async function purchaseProduct(token, product) {
  const res = await fetch(`${API_URL}/api/purchase`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({
      name: product.name,
      price: product.price,
      emoji: product.emoji
    })
  })

  const data = await res.json()

  if (!res.ok) {
    throw new Error(data.error || 'Purchase failed')
  }

  return data
}

export async function fetchOrders(token) {
  const res = await fetch(`${API_URL}/api/orders`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })

  if (!res.ok) {
    throw new Error('Failed to fetch orders')
  }

  return await res.json()
}