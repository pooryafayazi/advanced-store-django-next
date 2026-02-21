// frontend\src\components\ProductDetailView.jsx
'use client'
/** @jsxImportSource @emotion/react */
import { css } from '@emotion/react'
import Container from './Container'
import { Button } from './Ui'

export default function ProductDetailView({ p }) {
  const title = p?.title ?? p?.name ?? 'محصول'
  const price = p?.price ?? p?.unit_price

  return (
    <Container>
      <div
        css={css`
          margin-top: 16px;
          display: grid;
          grid-template-columns: 0.9fr 1.1fr;
          gap: 14px;
          align-items: start;

          @media (max-width: 860px) {
            grid-template-columns: 1fr;
          }
        `}
      >
        <div
          css={css`
            height: 320px;
            border-radius: 18px;
            border: 1px solid rgba(0, 0, 0, 0.08);
            background: linear-gradient(
              135deg,
              rgba(17, 24, 39, 0.18),
              rgba(17, 24, 39, 0.03)
            );

            @media (max-width: 860px) {
              height: 220px;
            }
          `}
        />

        <div
          css={css`
            background: #fff;
            border: 1px solid rgba(0, 0, 0, 0.08);
            border-radius: 18px;
            padding: 16px;
          `}
        >
          <h1
            css={css`
              margin: 0;
              font-size: 22px;
            `}
          >
            {title}
          </h1>

          <p
            css={css`
              margin: 10px 0 0;
              font-weight: 800;
            `}
          >
            {price != null
              ? `${Number(price).toLocaleString('fa-IR')} تومان`
              : '—'}
          </p>

          <p
            css={css`
              margin: 12px 0 0;
              opacity: 0.8;
              line-height: 2;
            `}
          >
            {p?.description ??
              'توضیحات این محصول بعداً از API نمایش داده می‌شود.'}
          </p>

          <div
            css={css`
              margin-top: 14px;
              display: flex;
              gap: 10px;
              flex-wrap: wrap;
            `}
          >
            <Button disabled>افزودن به سبد خرید</Button>
            <Button variant="ghost" disabled>
              افزودن به علاقه‌مندی
            </Button>
          </div>
        </div>
      </div>
    </Container>
  )
}
