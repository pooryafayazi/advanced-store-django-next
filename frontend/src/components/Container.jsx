// frontend\src\components\Container.jsx
'use client'
/** @jsxImportSource @emotion/react */
import { css } from '@emotion/react'

export default function Container({ children }) {
  return (
    <div
      css={css`
        width: 100%;
        max-width: 1100px;
        margin: 0 auto;
        padding: 16px;
      `}
    >
      {children}
    </div>
  )
}
