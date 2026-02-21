// frontend\src\app\products\[id]\not-found.jsx
import Container from '../../../components/Container'

export default function NotFound() {
  return (
    <Container>
      <h2>محصول پیدا نشد</h2>
      <p style={{ opacity: 0.75 }}>
        یا id اشتباه است یا endpoint جزئیات فرق دارد.
      </p>
    </Container>
  )
}
