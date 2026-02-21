// frontend\src\components\EmotionRegistry.jsx
'use client'

import * as React from 'react'
import { CacheProvider } from '@emotion/react'
import createCache from '@emotion/cache'
import { useServerInsertedHTML } from 'next/navigation'

function createEmotionCache() {
  return createCache({ key: 'css', prepend: true })
}

export default function EmotionRegistry({ children }) {
  const [cache] = React.useState(() => {
    const c = createEmotionCache()
    c.compat = true
    return c
  })

  useServerInsertedHTML(() => {
    const inserted = cache.inserted
    let styles = ''
    const names = []

    for (const name in inserted) {
      const value = inserted[name]
      if (typeof value === 'string') {
        styles += value
        names.push(name)
      }
    }

    // ✅ خیلی مهم: جلوگیری از دوباره-insert شدن در رندرهای بعدی
    cache.inserted = {}

    if (!styles) return null

    return (
      <style
        data-emotion={`${cache.key} ${names.join(' ')}`}
        dangerouslySetInnerHTML={{ __html: styles }}
      />
    )
  })

  return <CacheProvider value={cache}>{children}</CacheProvider>
}
