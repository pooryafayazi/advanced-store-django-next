// frontend\src\components\ProductCard.jsx
'use client'
/** @jsxImportSource @emotion/react */
import { css } from '@emotion/react'
import { Button } from './Ui'

export default function ProductCard({ p }) {
  const id = p?.id ?? p?.pk ?? p?.uuid
  const title = p?.title ?? p?.name ?? 'بدون عنوان'
  const price = p?.price ?? p?.unit_price

  return (
    <div
      css={css`
        border: 1px solid rgba(0, 0, 0, 0.08);
        border-radius: 16px;
        padding: 14px;
        display: flex;
        flex-direction: column;
        gap: 12px;
        background: #fff;
      `}
    >
      <div
        css={css`
          display: flex;
          gap: 12px;
          align-items: center;
        `}
      >
        <div
          css={css`
            width: 64px;
            height: 64px;
            border-radius: 14px;
            background: linear-gradient(
              135deg,
              rgba(17, 24, 39, 0.15),
              rgba(17, 24, 39, 0.03)
            );
            flex: 0 0 auto;
          `}
        />
        <div>
          <h3
            title={title}
            css={css`
              margin: 0;
              font-size: 16px;
              line-height: 1.6;
              overflow: hidden;
              text-overflow: ellipsis;
              white-space: nowrap;
            `}
          >
            {title}
          </h3>
          <p
            css={css`
              margin: 6px 0 0;
              opacity: 0.75;
            `}
          >
            {price != null
              ? `${Number(price).toLocaleString('fa-IR')} تومان`
              : '—'}
          </p>
        </div>
      </div>

      <div
        css={css`
          display: flex;
          justify-content: space-between;
          gap: 10px;
        `}
      >
        <Button href={`/products/${id}`} variant="ghost">
          جزئیات
        </Button>
        <Button disabled title="بعداً به cart وصل می‌کنیم">
          افزودن
        </Button>
      </div>
    </div>
  )
}
