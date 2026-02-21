// frontend\src\components\SiteFooter.jsx
'use client'
/** @jsxImportSource @emotion/react */
import { css } from '@emotion/react'
import Container from './Container'

export default function SiteFooter() {
  return (
    <footer
      css={css`
        border-top: 1px solid rgba(0, 0, 0, 0.08);
        margin-top: 32px;
      `}
    >
      <Container>
        <div
          css={css`
            display: flex;
            justify-content: space-between;
            gap: 12px;
            padding: 18px 0;
            flex-wrap: wrap;
          `}
        >
          <small>© {new Date().getFullYear()} Advanced Store</small>
          <small
            css={css`
              opacity: 0.7;
            `}
          >
            Next + Django • App Router
          </small>
        </div>
      </Container>
    </footer>
  )
}
