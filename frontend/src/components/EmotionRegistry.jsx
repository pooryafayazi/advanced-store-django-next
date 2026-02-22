// frontend\src\components\EmotionRegistry.jsx
'use client'

import * as React from 'react'
import { CacheProvider } from '@emotion/react'
import createCache from '@emotion/cache'
import { useServerInsertedHTML } from 'next/navigation'

function createEmotionCache() {
  const cache = createCache({ key: 'css', prepend: true })
  cache.compat = true
  return cache
}

export default function EmotionRegistry({ children }) {
  // The cache is created only once and remains immutable
  const cache = React.useMemo(() => createEmotionCache(), [])

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
