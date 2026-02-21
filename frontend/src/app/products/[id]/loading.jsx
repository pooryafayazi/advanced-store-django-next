// frontend\src\app\products\[id]\loading.jsx
import Container from '../../../components/Container'

export default function Loading() {
  return (
    <Container>
      <div style={{ marginTop: 16 }}>
        <div
          style={{
            height: 18,
            width: 220,
            borderRadius: 10,
            background: 'rgba(0,0,0,0.08)',
          }}
        />
        <div
          style={{
            marginTop: 14,
            display: 'grid',
            gridTemplateColumns: 'repeat(3, 1fr)',
            gap: 12,
          }}
        >
          {Array.from({ length: 6 }).map((_, i) => (
            <div
              key={i}
              style={{
                height: 120,
                borderRadius: 16,
                background: 'rgba(0,0,0,0.06)',
              }}
            />
          ))}
        </div>
      </div>
    </Container>
  )
}
