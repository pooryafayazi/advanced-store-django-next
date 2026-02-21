// frontend\src\components\Ui.jsx
'use client'
/** @jsxImportSource @emotion/react */
import { css } from '@emotion/react'
import Link from 'next/link'

const baseBtn = css`
  border: 0;
  border-radius: 12px;
  padding: 10px 14px;
  cursor: pointer;
  font-weight: 600;
  transition:
    transform 0.08s ease,
    opacity 0.2s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;

  &:active {
    transform: scale(0.98);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
`

const variants = {
  primary: css`
    background: #111827;
    color: #fff;
  `,
  ghost: css`
    background: transparent;
    color: #111827;
    border: 1px solid rgba(17, 24, 39, 0.2);
  `,
}

export function Button({ children, variant = 'primary', href, ...props }) {
  const styles = [baseBtn, variants[variant]]

  if (href) {
    return (
      <Link href={href} css={styles}>
        {children}
      </Link>
    )
  }

  return (
    <button css={styles} {...props}>
      {children}
    </button>
  )
}

export function Input(props) {
  return (
    <input
      css={css`
        width: 100%;
        padding: 10px 12px;
        border-radius: 12px;
        border: 1px solid rgba(17, 24, 39, 0.2);
        outline: none;

        &:focus {
          border-color: rgba(17, 24, 39, 0.45);
        }
      `}
      {...props}
    />
  )
}
