/**
 * API client wrapper with authentication support
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export class ApiClient {
  private baseURL: string
  private token: string | null = null

  constructor(baseURL: string = API_URL) {
    this.baseURL = baseURL

    // Load token from cookies if available
    if (typeof window !== 'undefined') {
      this.token = this.getTokenFromCookie()
    }
  }

  /**
   * Get token from cookie
   */
  private getTokenFromCookie(): string | null {
    if (typeof document === 'undefined') return null

    const cookies = document.cookie.split(';')
    const authCookie = cookies.find((cookie) => cookie.trim().startsWith('auth_token='))

    if (authCookie) {
      return authCookie.split('=')[1]
    }

    return null
  }

  /**
   * Set token in cookie (httpOnly=false for client-side access, secure in production)
   */
  setToken(token: string | null) {
    this.token = token
    if (typeof window !== 'undefined') {
      if (token) {
        // Set cookie with 24 hour expiration (matching JWT expiration from backend)
        const maxAge = 60 * 60 * 24 // 24 hours in seconds
        document.cookie = `auth_token=${token}; path=/; max-age=${maxAge}; SameSite=Lax${
          process.env.NODE_ENV === 'production' ? '; Secure' : ''
        }`
      } else {
        // Clear cookie
        document.cookie = 'auth_token=; path=/; max-age=0'
      }
    }
  }

  getToken(): string | null {
    return this.token
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`

    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    }

    // Add authentication header if token exists
    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`
    }

    const response = await fetch(url, {
      ...options,
      headers,
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({
        detail: 'An error occurred',
      }))
      throw new Error(
        typeof error.detail === 'string'
          ? error.detail
          : 'Validation error'
      )
    }

    // Handle 204 No Content
    if (response.status === 204) {
      return {} as T
    }

    return response.json()
  }

  async get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'GET' })
  }

  async post<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    })
  }

  async patch<T>(endpoint: string, data: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PATCH',
      body: JSON.stringify(data),
    })
  }

  async delete<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'DELETE' })
  }
}

// Export singleton instance
export const api = new ApiClient()
