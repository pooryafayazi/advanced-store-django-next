// frontend\src\app\products\error.jsx
'use client'

import Container from '../../components/Container'
import { Button } from '../../components/Ui'

export default function Error({ error, reset }) {
  return (
    <Container>
      <h2>خطا در دریافت محصولات</h2>
      <pre style={{ whiteSpace: 'pre-wrap', opacity: 0.8 }}>
        {String(error?.message || error)}
      </pre>
      <Button onClick={reset}>تلاش دوباره</Button>
    </Container>
  )
}
