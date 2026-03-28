const API_URL = 'http://localhost:5000'

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