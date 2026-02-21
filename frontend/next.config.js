// frontend/next.config.js
const path = require('path')

/** @type {import('next').NextConfig} */
const nextConfig = {
  turbopack: {
    root: path.join(__dirname),
  },
  async rewrites() {
    const backend = process.env.DJANGO_BASE_URL || 'http://localhost:8000'
    return [
      { source: '/api/:path*', destination: `${backend}/api/:path*` },
      { source: '/media/:path*', destination: `${backend}/media/:path*` },
    ]
  },
}

module.exports = nextConfig
