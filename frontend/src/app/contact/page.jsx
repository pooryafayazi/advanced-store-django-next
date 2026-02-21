// frontend/src/app/contact/page.jsx
'use client'
/** @jsxImportSource @emotion/react */
import { css } from '@emotion/react'
import { useState } from 'react'
import Container from '../../components/Container'
import { Button, Input } from '../../components/Ui'

export default function ContactPage() {
  const [form, setForm] = useState({ name: '', email: '', message: '' })
  const [status, setStatus] = useState('idle')

  async function onSubmit(e) {
    e.preventDefault()
    setStatus('sending')

    try {
      // آماده اتصال واقعی:
      // await fetch("/api/communications/contact/", {
      //   method: "POST",
      //   headers: { "Content-Type": "application/json" },
      //   body: JSON.stringify(form),
      // });

      await new Promise((r) => setTimeout(r, 600))
      setStatus('sent')
    } catch {
      setStatus('error')
    }
  }

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
            margin: 0 0 12px;
          `}
        >
          تماس با ما
        </h2>

        <form
          onSubmit={onSubmit}
          css={css`
            display: grid;
            gap: 12px;
          `}
        >
          <label
            css={css`
              display: grid;
              gap: 8px;
              font-weight: 600;
            `}
          >
            نام
            <Input
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
            />
          </label>

          <label
            css={css`
              display: grid;
              gap: 8px;
              font-weight: 600;
            `}
          >
            ایمیل
            <Input
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
            />
          </label>

          <label
            css={css`
              display: grid;
              gap: 8px;
              font-weight: 600;
            `}
          >
            پیام
            <textarea
              value={form.message}
              onChange={(e) => setForm({ ...form, message: e.target.value })}
              css={css`
                width: 100%;
                min-height: 140px;
                padding: 10px 12px;
                border-radius: 12px;
                border: 1px solid rgba(17, 24, 39, 0.2);
                outline: none;
                resize: vertical;

                &:focus {
                  border-color: rgba(17, 24, 39, 0.45);
                }
              `}
            />
          </label>

          <div
            css={css`
              display: flex;
              align-items: center;
              gap: 10px;
              flex-wrap: wrap;
            `}
          >
            <Button disabled={status === 'sending'}>
              {status === 'sending' ? 'در حال ارسال...' : 'ارسال'}
            </Button>

            {status === 'sent' && (
              <span
                css={css`
                  color: #065f46;
                  font-weight: 700;
                `}
              >
                ارسال شد ✅
              </span>
            )}

            {status === 'error' && (
              <span
                css={css`
                  color: #991b1b;
                  font-weight: 700;
                `}
              >
                خطا ❌
              </span>
            )}
          </div>
        </form>
      </div>
    </Container>
  )
}
