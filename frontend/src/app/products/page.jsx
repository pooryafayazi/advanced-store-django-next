// frontend\src\app\products\page.jsx
import ProductsView from '../../components/ProductsView'
import { getProducts } from '../../lib/api'

export default async function ProductsPage() {
  const data = await getProducts()
  const items = Array.isArray(data) ? data : (data?.results ?? [])
  return <ProductsView items={items} />
}
