// const API_URL = "http://localhost:8000" this is for runing on the local maching 

const API_URL =
  window.__BASE_URL_BACKEND__ ||
  import.meta.env.VITE_BASE_URL_BACKEND ||
  "http://localhost:8000"; // fallback for local dev for doing test on my local machine 

export default API_URL;


export async function api(path, method = 'GET', body = null, token = null) {
  const headers = { 'Content-Type': 'application/json' }
  if (token) headers['Authorization'] = `Bearer ${token}`

  const res = await fetch(`${API_URL}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : null,
  })

  if (!res.ok) throw new Error(await res.text())
  return res.json()
}
