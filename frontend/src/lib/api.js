// frontend\src\lib\api.js
const DJANGO_INTERNAL =
  process.env.DJANGO_INTERNAL_URL ||
  process.env.DJANGO_BASE_URL ||
  "http://localhost:8000";

async function safeFetch(url, options) {
  const res = await fetch(url, options);
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`API error ${res.status} for ${url}\n${text}`);
  }
  return res.json();
}

export async function getProducts() {
  return safeFetch(`${DJANGO_INTERNAL}/api/shop/products/`, {
    cache: "no-store",
  });
}

export async function getProductById(id) {
  return safeFetch(`${DJANGO_INTERNAL}/api/shop/products/${id}/`, {
    cache: "no-store",
  });
}
