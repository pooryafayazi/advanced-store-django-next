// frontend\src\components\HomeView.jsx
'use client'
/** @jsxImportSource @emotion/react */
import { css } from '@emotion/react'
import Container from './Container'
import { Button } from './Ui'

export default function HomeView() {
  return (
    <Container>
      <section
        css={css`
          margin-top: 18px;
          display: grid;
          grid-template-columns: 1.2fr 0.8fr;
          gap: 16px;
          align-items: stretch;

          @media (max-width: 860px) {
            grid-template-columns: 1fr;
          }
        `}
      >
        <div
          css={css`
            background: #fff;
            border: 1px solid rgba(0, 0, 0, 0.08);
            border-radius: 18px;
            padding: 18px;
          `}
        >
          <h1
            css={css`
              margin: 0 0 10px;
              font-size: 24px;
            `}
          >
            فروشگاه Advanced Store
          </h1>

          <p
            css={css`
              margin: 0 0 14px;
              opacity: 0.8;
              line-height: 1.9;
            `}
          >
            تمرین اول Next: صفحات اصلی + اتصال به API جنگو + طراحی responsive.
          </p>

          <div
            css={css`
              display: flex;
              gap: 10px;
              flex-wrap: wrap;
            `}
          >
            <Button href="/products">رفتن به فروشگاه</Button>
            <Button href="/about" variant="ghost">
              درباره ما
            </Button>
          </div>
        </div>

        <div
          css={css`
            border-radius: 18px;
            border: 1px solid rgba(0, 0, 0, 0.08);
            background:
              radial-gradient(
                circle at 30% 30%,
                rgba(17, 24, 39, 0.18),
                transparent 55%
              ),
              radial-gradient(
                circle at 70% 70%,
                rgba(17, 24, 39, 0.1),
                transparent 55%
              ),
              #fff;

            @media (max-width: 860px) {
              height: 180px;
            }
          `}
        />
      </section>

      <section
        css={css`
          margin-top: 16px;
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 12px;

          @media (max-width: 860px) {
            grid-template-columns: 1fr;
          }
        `}
      >
        {[
          'کامپوننت‌ها دست‌نویس',
          'CSS-in-JS با Emotion',
          'Docker + Django API',
        ].map((t) => (
          <div
            key={t}
            css={css`
              background: #fff;
              border: 1px solid rgba(0, 0, 0, 0.08);
              border-radius: 16px;
              padding: 14px;
              opacity: 0.9;
            `}
          >
            {t}
          </div>
        ))}
      </section>
    </Container>
  )
}
