/**
 * Priority Selector Component
 *
 * Dropdown component for selecting task priority level (high, medium, low).
 * Part of User Story 1: Task Priority Management (FR-005)
 */

import { PriorityLevel } from '@/lib/types'

interface PrioritySelectorProps {
  value: PriorityLevel
  onChange: (priority: PriorityLevel) => void
  required?: boolean
  className?: string
}

export default function PrioritySelector({
  value,
  onChange,
  required = false,
  className = '',
}: PrioritySelectorProps) {
  return (
    <div className={className}>
      <label htmlFor="priority" className="block text-sm font-medium text-gray-700 mb-1">
        Priority {required && <span className="text-red-500">*</span>}
      </label>
      <select
        id="priority"
        value={value}
        onChange={(e) => onChange(e.target.value as PriorityLevel)}
        required={required}
        className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
      >
        <option value="high">High</option>
        <option value="medium">Medium</option>
        <option value="low">Low</option>
      </select>
    </div>
  )
}
