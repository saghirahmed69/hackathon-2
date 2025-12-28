/**
 * Authentication utilities
 */

import { api } from './api'
import type { AuthResponse, SignupRequest, SigninRequest } from './types'

export const auth = {
  /**
   * Sign up a new user (auto-login with token)
   */
  async signup(data: SignupRequest): Promise<AuthResponse> {
    const response = await api.post<AuthResponse>('/api/auth/signup', data)

    // Store token (auto-login after signup)
    if (response.access_token) {
      api.setToken(response.access_token)
    }

    return response
  },

  /**
   * Sign in an existing user
   */
  async signin(data: SigninRequest): Promise<AuthResponse> {
    const response = await api.post<AuthResponse>('/api/auth/signin', data)

    // Store token
    if (response.access_token) {
      api.setToken(response.access_token)
    }

    return response
  },

  /**
   * Sign out the current user
   */
  async signout(): Promise<void> {
    // Clear token
    api.setToken(null)

    // Call API endpoint (optional, mainly for logging)
    try {
      await api.post('/api/auth/logout')
    } catch (error) {
      // Ignore errors, we've already cleared the token
      console.error('Logout error:', error)
    }
  },

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    return !!api.getToken()
  },

  /**
   * Get current auth token
   */
  getToken(): string | null {
    return api.getToken()
  },
}
