// frontend\src\app\products\[id]\page.jsx
import ProductDetailView from '../../../components/ProductDetailView'
import { getProductById } from '../../../lib/api'
import { notFound } from 'next/navigation'

export default async function ProductDetailPage({ params }) {
  const { id } = await params

  let p = null
  try {
    p = await getProductById(id)
  } catch {
    notFound()
  }

  return <ProductDetailView p={p} />
}
