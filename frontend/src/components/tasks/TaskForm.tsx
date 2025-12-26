/**
 * TaskForm component - Form for creating new tasks
 */

'use client'

import { useState } from 'react'
import { TaskCreateRequest, PriorityLevel, RecurrencePattern } from '@/lib/types'
import PrioritySelector from './PrioritySelector'
import DateTimePicker from './DateTimePicker'

interface TaskFormProps {
  onSubmit: (data: TaskCreateRequest) => Promise<void>
  isLoading?: boolean
}

export default function TaskForm({ onSubmit, isLoading = false }: TaskFormProps) {
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [priority, setPriority] = useState<PriorityLevel>('medium')
  const [dueDate, setDueDate] = useState<string | null>(null)
  const [isRecurring, setIsRecurring] = useState(false)
  const [recurrencePattern, setRecurrencePattern] = useState<RecurrencePattern | null>(null)
  const [reminderTime, setReminderTime] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)

    // Validate title
    if (!title.trim()) {
      setError('Title is required')
      return
    }

    if (title.length > 1000) {
      setError('Title must be less than 1000 characters')
      return
    }

    if (description.length > 10000) {
      setError('Description must be less than 10,000 characters')
      return
    }

    try {
      await onSubmit({
        title: title.trim(),
        description: description.trim() || undefined,
        priority,
        due_date: dueDate,
        is_recurring: isRecurring,
        recurrence_pattern: recurrencePattern,
        reminder_time: reminderTime,
      })

      // Clear form on success
      setTitle('')
      setDescription('')
      setPriority('medium')
      setDueDate(null)
      setIsRecurring(false)
      setRecurrencePattern(null)
      setReminderTime(null)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create task')
    }
  }

  return (
    <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
      <h2 className="text-xl font-semibold text-gray-900 mb-4">Create New Task</h2>

      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-md">
          <p className="text-sm text-red-800">{error}</p>
        </div>
      )}

      <div className="space-y-4">
        <div>
          <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
            Title <span className="text-red-500">*</span>
          </label>
          <input
            id="title"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="What needs to be done?"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            maxLength={1000}
            disabled={isLoading}
            required
          />
          <p className="mt-1 text-xs text-gray-500">
            {title.length}/1000 characters
          </p>
        </div>

        <div>
          <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
            Description <span className="text-gray-400">(optional)</span>
          </label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Add more details about this task..."
            rows={4}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            maxLength={10000}
            disabled={isLoading}
          />
          <p className="mt-1 text-xs text-gray-500">
            {description.length}/10,000 characters
          </p>
        </div>

        {/* Phase III: Priority Selector */}
        <PrioritySelector
          value={priority}
          onChange={setPriority}
          required={true}
        />

        {/* Phase III: Due Date Picker */}
        <DateTimePicker
          label="Due Date"
          value={dueDate}
          onChange={setDueDate}
          required={false}
          includeTime={true}
        />

        {/* Phase III: Recurring Task Options */}
        <div className="space-y-2">
          <div className="flex items-center">
            <input
              id="is_recurring"
              type="checkbox"
              checked={isRecurring}
              onChange={(e) => {
                setIsRecurring(e.target.checked)
                if (!e.target.checked) setRecurrencePattern(null)
              }}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label htmlFor="is_recurring" className="ml-2 text-sm text-gray-700">
              Recurring task
            </label>
          </div>
          {isRecurring && (
            <select
              value={recurrencePattern || ''}
              onChange={(e) => setRecurrencePattern((e.target.value || null) as RecurrencePattern | null)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select pattern</option>
              <option value="daily">Daily</option>
              <option value="weekly">Weekly</option>
              <option value="monthly">Monthly</option>
            </select>
          )}
        </div>

        {/* Phase III: Reminder Time */}
        <DateTimePicker
          label="Reminder"
          value={reminderTime}
          onChange={setReminderTime}
          required={false}
          includeTime={true}
        />

        <button
          type="submit"
          disabled={isLoading || !title.trim()}
          className="w-full px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          {isLoading ? (
            <span className="flex items-center justify-center">
              <svg
                className="animate-spin -ml-1 mr-2 h-5 w-5 text-white"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                />
              </svg>
              Creating...
            </span>
          ) : (
            'Create Task'
          )}
        </button>
      </div>
    </form>
  )
}
