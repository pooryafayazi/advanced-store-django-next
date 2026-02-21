// frontend\src\components\ProductsView.jsx
'use client'
/** @jsxImportSource @emotion/react */
import { css } from '@emotion/react'
import Container from './Container'
import ProductCard from './ProductCard'

export default function ProductsView({ items }) {
  return (
    <Container>
      <div
        css={css`
          margin-top: 12px;
        `}
      >
        <h2
          css={css`
            margin: 0;
            font-size: 20px;
          `}
        >
          فروشگاه
        </h2>
        <p
          css={css`
            margin: 8px 0 0;
            opacity: 0.75;
          `}
        >
          لیست محصولات
        </p>
      </div>

      <div
        css={css`
          margin-top: 14px;
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 12px;

          @media (max-width: 980px) {
            grid-template-columns: repeat(2, 1fr);
          }
          @media (max-width: 620px) {
            grid-template-columns: 1fr;
          }
        `}
      >
        {items.map((p) => (
          <ProductCard key={p.id ?? p.pk ?? p.slug} p={p} />
        ))}
      </div>
    </Container>
  )
}
