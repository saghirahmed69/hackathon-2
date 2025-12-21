'use client'

/**
 * Signup form component with client-side validation
 */

import { useState, FormEvent } from 'react'
import { useRouter } from 'next/navigation'
import { auth } from '@/lib/auth'
import type { SignupRequest } from '@/lib/types'

export default function SignupForm() {
  const router = useRouter()
  const [formData, setFormData] = useState<SignupRequest>({
    email: '',
    password: '',
  })
  const [confirmPassword, setConfirmPassword] = useState('')
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [isLoading, setIsLoading] = useState(false)
  const [successMessage, setSuccessMessage] = useState('')

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

    // Password validation (min 8 characters)
    if (!formData.password) {
      newErrors.password = 'Password is required'
    } else if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters long'
    }

    // Confirm password validation
    if (formData.password !== confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match'
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
    setSuccessMessage('')

    // Client-side validation
    if (!validateForm()) {
      return
    }

    setIsLoading(true)

    try {
      // Call signup API
      await auth.signup(formData)

      // Show success message
      setSuccessMessage('Account created successfully! Redirecting to sign in...')

      // Redirect to signin after 2 seconds
      setTimeout(() => {
        router.push('/signin')
      }, 2000)
    } catch (error: any) {
      // Handle API errors
      if (error.status === 409) {
        setErrors({ email: 'Email already registered' })
      } else if (error.detail) {
        setErrors({ general: error.detail })
      } else {
        setErrors({ general: 'Failed to create account. Please try again.' })
      }
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6 w-full max-w-md">
      <h2 className="text-2xl font-bold text-center">Create Account</h2>

      {/* Success message */}
      {successMessage && (
        <div className="p-4 bg-green-50 border border-green-200 rounded-md text-green-800">
          {successMessage}
        </div>
      )}

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
          placeholder="At least 8 characters"
        />
        {errors.password && <p className="mt-1 text-sm text-red-600">{errors.password}</p>}
      </div>

      {/* Confirm password field */}
      <div>
        <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-1">
          Confirm Password
        </label>
        <input
          id="confirmPassword"
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          disabled={isLoading}
          className={`w-full px-4 py-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
            errors.confirmPassword ? 'border-red-500' : 'border-gray-300'
          }`}
          placeholder="Re-enter password"
        />
        {errors.confirmPassword && (
          <p className="mt-1 text-sm text-red-600">{errors.confirmPassword}</p>
        )}
      </div>

      {/* Submit button */}
      <button
        type="submit"
        disabled={isLoading}
        className="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        {isLoading ? 'Creating account...' : 'Sign Up'}
      </button>

      {/* Sign in link */}
      <p className="text-center text-sm text-gray-600">
        Already have an account?{' '}
        <a href="/signin" className="text-blue-600 hover:text-blue-700 font-medium">
          Sign in
        </a>
      </p>
    </form>
  )
}
