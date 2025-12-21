'use client'

/**
 * Signin form component with authentication
 */

import { useState, FormEvent } from 'react'
import { useRouter } from 'next/navigation'
import { auth } from '@/lib/auth'
import type { SigninRequest } from '@/lib/types'

export default function SigninForm() {
  const router = useRouter()
  const [formData, setFormData] = useState<SigninRequest>({
    email: '',
    password: '',
  })
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [isLoading, setIsLoading] = useState(false)

  /**
   * Client-side validation
   */
  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {}

    // Email validation
    if (!formData.email) {
      newErrors.email = 'Email is required'
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Please enter a valid email address'
    }

    // Password validation
    if (!formData.password) {
      newErrors.password = 'Password is required'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  /**
   * Handle form submission
   */
  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setErrors({})

    // Client-side validation
    if (!validateForm()) {
      return
    }

    setIsLoading(true)

    try {
      // Call signin API
      const response = await auth.signin(formData)

      // Token is automatically stored by auth.signin()
      // Redirect to dashboard
      router.push('/dashboard')
    } catch (error: any) {
      // Handle API errors
      if (error.status === 401) {
        setErrors({ general: 'Invalid email or password' })
      } else if (error.detail) {
        setErrors({ general: error.detail })
      } else {
        setErrors({ general: 'Failed to sign in. Please try again.' })
      }
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6 w-full max-w-md">
      <h2 className="text-2xl font-bold text-center">Sign In</h2>

      {/* General error message */}
      {errors.general && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-md text-red-800">
          {errors.general}
        </div>
      )}

      {/* Email field */}
      <div>
        <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
          Email
        </label>
        <input
          id="email"
          type="email"
          value={formData.email}
          onChange={(e) => setFormData({ ...formData, email: e.target.value })}
          disabled={isLoading}
          className={`w-full px-4 py-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
            errors.email ? 'border-red-500' : 'border-gray-300'
          }`}
          placeholder="you@example.com"
        />
        {errors.email && <p className="mt-1 text-sm text-red-600">{errors.email}</p>}
      </div>

      {/* Password field */}
      <div>
        <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
          Password
        </label>
        <input
          id="password"
          type="password"
          value={formData.password}
          onChange={(e) => setFormData({ ...formData, password: e.target.value })}
          disabled={isLoading}
          className={`w-full px-4 py-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
            errors.password ? 'border-red-500' : 'border-gray-300'
          }`}
          placeholder="Your password"
        />
        {errors.password && <p className="mt-1 text-sm text-red-600">{errors.password}</p>}
      </div>

      {/* Submit button */}
      <button
        type="submit"
        disabled={isLoading}
        className="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        {isLoading ? 'Signing in...' : 'Sign In'}
      </button>

      {/* Sign up link */}
      <p className="text-center text-sm text-gray-600">
        Don't have an account?{' '}
        <a href="/signup" className="text-blue-600 hover:text-blue-700 font-medium">
          Sign up
        </a>
      </p>
    </form>
  )
}
