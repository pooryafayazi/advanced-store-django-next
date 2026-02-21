// frontend\src\app\layout.jsx
import './globals.css'
import EmotionRegistry from '../components/EmotionRegistry'
import SiteHeader from '../components/SiteHeader'
import SiteFooter from '../components/SiteFooter'

export default function RootLayout({ children }) {
  return (
    <html lang="fa" dir="rtl">
      <body>
        <EmotionRegistry>
          <SiteHeader />
          <main className="main">{children}</main>
          <SiteFooter />
        </EmotionRegistry>
      </body>
    </html>
  )
}
