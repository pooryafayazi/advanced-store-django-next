// frontend\src\components\AboutView.jsx
'use client'
/** @jsxImportSource @emotion/react */
import { css } from '@emotion/react'
import Container from './Container'

export default function AboutView() {
  return (
    <Container>
      <div
        css={css`
          margin-top: 16px;
          background: #fff;
          border: 1px solid rgba(0, 0, 0, 0.08);
          border-radius: 18px;
          padding: 16px;
        `}
      >
        <h2
          css={css`
            margin: 0 0 8px;
          `}
        >
          درباره ما
        </h2>

        <p
          css={css`
            margin: 0;
            opacity: 0.8;
            line-height: 2;
          `}
        >
          این پروژه برای تمرین NextJS (App Router) روی بک‌اند Django ساخته شده.
          تمرکز: ساخت کامپوننت‌های reusable و طراحی تمیز.
        </p>
      </div>
    </Container>
  )
}
