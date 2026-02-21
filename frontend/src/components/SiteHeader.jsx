// frontend\src\components\SiteHeader.jsx
'use client'
/** @jsxImportSource @emotion/react */
import { css } from '@emotion/react'
import Link from 'next/link'
import Container from './Container'

export default function SiteHeader() {
  return (
    <header
      css={css`
        border-bottom: 1px solid rgba(0, 0, 0, 0.08);
        position: sticky;
        top: 0;
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        z-index: 10;
      `}
    >
      <Container>
        <nav
          css={css`
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            padding: 14px 0;
          `}
        >
          <div
            css={css`
              font-weight: 800;
            `}
          >
            <Link
              href="/"
              css={css`
                text-decoration: none;
                color: #111827;
              `}
            >
              Advanced Store
            </Link>
          </div>

          <div
            css={css`
              display: flex;
              gap: 14px;
              flex-wrap: wrap;
            `}
          >
            {[
              { href: '/products', label: 'فروشگاه' },
              { href: '/about', label: 'درباره' },
              { href: '/contact', label: 'تماس' },
            ].map((x) => (
              <Link
                key={x.href}
                href={x.href}
                css={css`
                  text-decoration: none;
                  color: #111827;
                  padding: 8px 10px;
                  border-radius: 10px;
                `}
              >
                {x.label}
              </Link>
            ))}
          </div>
        </nav>
      </Container>
    </header>
  )
}
