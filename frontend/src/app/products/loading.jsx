// frontend\src\app\products\loading.jsx
import Container from '../../components/Container'

export default function Loading() {
  return (
    <Container>
      <div className="sk">
        <div className="bar" />
        <div className="grid">
          {Array.from({ length: 6 }).map((_, i) => (
            <div className="card" key={i} />
          ))}
        </div>
      </div>
    </Container>
  )
}
