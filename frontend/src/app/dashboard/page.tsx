'use client'

/**
 * Dashboard page (protected route)
 */

import { useRouter } from 'next/navigation'
import { auth } from '@/lib/auth'
import { useState } from 'react'

export default function DashboardPage() {
  const router = useRouter()
  const [isLoggingOut, setIsLoggingOut] = useState(false)

  /**
   * Handle logout
   */
  const handleLogout = async () => {
    setIsLoggingOut(true)
    try {
      await auth.signout()
      // Redirect to signin page
      router.push('/signin')
    } catch (error) {
      console.error('Logout error:', error)
      // Even if API call fails, token is cleared client-side
      router.push('/signin')
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header with logout */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">Todo Dashboard</h1>
          <button
            onClick={handleLogout}
            disabled={isLoggingOut}
            className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white font-medium rounded-md focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isLoggingOut ? 'Logging out...' : 'Logout'}
          </button>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Welcome to your Dashboard!</h2>
          <p className="text-gray-600 mb-4">
            You are successfully authenticated. Task management features will be available here.
          </p>
          <div className="bg-blue-50 border border-blue-200 rounded-md p-4">
            <p className="text-blue-800 text-sm">
              <strong>Authentication Status:</strong> You are logged in and this route is protected
              by JWT authentication middleware.
            </p>
          </div>
        </div>
      </main>
    </div>
  )
}
