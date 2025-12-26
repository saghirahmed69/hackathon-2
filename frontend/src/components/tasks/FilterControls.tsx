/**
 * FilterControls Component
 *
 * UI controls for filtering tasks by status, priority, and due date (Phase III: FR-032)
 */

'use client'

import { PriorityLevel } from '@/lib/types'

interface FilterControlsProps {
  status: string
  onStatusChange: (status: '' | 'pending' | 'completed') => void
  priority: string
  onPriorityChange: (priority: '' | PriorityLevel) => void
  dueDate: string
  onDueDateChange: (dueDate: string) => void
  onClearFilters: () => void
  hasActiveFilters: boolean
}

export default function FilterControls({
  status,
  onStatusChange,
  priority,
  onPriorityChange,
  dueDate,
  onDueDateChange,
  onClearFilters,
  hasActiveFilters,
}: FilterControlsProps) {
  return (
    <div className="bg-white p-4 rounded-lg shadow border border-gray-200">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-medium text-gray-900">Filters</h3>
        {hasActiveFilters && (
          <button
            onClick={onClearFilters}
            className="text-sm text-blue-600 hover:text-blue-800"
          >
            Clear all
          </button>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Status Filter */}
        <div>
          <label className="block text-xs font-medium text-gray-700 mb-1">Status</label>
          <select
            value={status}
            onChange={(e) => onStatusChange(e.target.value as '' | 'pending' | 'completed')}
            className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All</option>
            <option value="pending">Pending</option>
            <option value="completed">Completed</option>
          </select>
        </div>

        {/* Priority Filter */}
        <div>
          <label className="block text-xs font-medium text-gray-700 mb-1">Priority</label>
          <select
            value={priority}
            onChange={(e) => onPriorityChange(e.target.value as '' | PriorityLevel)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>
        </div>

        {/* Due Date Filter */}
        <div>
          <label className="block text-xs font-medium text-gray-700 mb-1">Due Date</label>
          <select
            value={dueDate}
            onChange={(e) => onDueDateChange(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All</option>
            <option value={`on:${new Date().toISOString().split('T')[0]}`}>Due Today</option>
            <option value={`before:${new Date().toISOString().split('T')[0]}`}>Overdue</option>
            <option value={`after:${new Date().toISOString().split('T')[0]}`}>Upcoming</option>
          </select>
        </div>
      </div>
    </div>
  )
}
