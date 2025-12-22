/**
 * Next.js middleware for route protection
 */

import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

// Protected routes that require authentication
const protectedRoutes = ['/dashboard']

// Public routes (don't redirect if authenticated)
const publicRoutes = ['/', '/signin', '/signup']

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl

  // Get token from cookie or header
  const token = request.cookies.get('auth_token')?.value

  // Check if route is protected
  const isProtectedRoute = protectedRoutes.some((route) =>
    pathname.startsWith(route)
  )

  // Redirect to signin if accessing protected route without token
  if (isProtectedRoute && !token) {
    const signinUrl = new URL('/signin', request.url)
    signinUrl.searchParams.set('redirect', pathname)
    return NextResponse.redirect(signinUrl)
  }

  return NextResponse.next()
}

export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - api routes
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
}
