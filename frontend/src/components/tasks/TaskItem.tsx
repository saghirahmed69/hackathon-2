/**
 * TaskItem component - Renders individual task with edit/delete actions
 */

'use client'

import { Task, PriorityLevel } from '@/lib/types'
import { useState } from 'react'
import PrioritySelector from './PrioritySelector'
import DateTimePicker from './DateTimePicker'

// Priority badge styling (Phase III: FR-005)
const getPriorityBadgeStyles = (priority: PriorityLevel) => {
  switch (priority) {
    case 'high':
      return 'bg-red-100 text-red-800 border-red-200'
    case 'medium':
      return 'bg-yellow-100 text-yellow-800 border-yellow-200'
    case 'low':
      return 'bg-green-100 text-green-800 border-green-200'
  }
}

const getPriorityIcon = (priority: PriorityLevel) => {
  switch (priority) {
    case 'high':
      return '🔴'
    case 'medium':
      return '🟡'
    case 'low':
      return '🟢'
  }
}

// Due date indicator helpers (Phase III: FR-015, FR-016)
const isOverdue = (dueDate: string | null, completed: boolean): boolean => {
  if (!dueDate || completed) return false
  return new Date(dueDate) < new Date()
}

const isDueToday = (dueDate: string | null, completed: boolean): boolean => {
  if (!dueDate || completed) return false
  const due = new Date(dueDate)
  const today = new Date()
  return (
    due.getFullYear() === today.getFullYear() &&
    due.getMonth() === today.getMonth() &&
    due.getDate() === today.getDate()
  )
}

const formatDueDate = (dueDate: string | null): string | null => {
  if (!dueDate) return null
  const date = new Date(dueDate)
  const hasTime = dueDate.includes('T') && !dueDate.endsWith('T00:00:00')

  if (hasTime) {
    return date.toLocaleString(undefined, {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: 'numeric',
      minute: '2-digit',
    })
  } else {
    return date.toLocaleDateString(undefined, {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    })
  }
}

interface TaskItemProps {
  task: Task
  onUpdate: (updates: Partial<Task>) => void
  onDelete: () => void
}

export default function TaskItem({ task, onUpdate, onDelete }: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false)
  const [editTitle, setEditTitle] = useState(task.title)
  const [editDescription, setEditDescription] = useState(task.description || '')
  const [editPriority, setEditPriority] = useState<PriorityLevel>(task.priority)
  const [editDueDate, setEditDueDate] = useState<string | null>(task.due_date)
  const [editIsRecurring, setEditIsRecurring] = useState(task.is_recurring)
  const [editRecurrencePattern, setEditRecurrencePattern] = useState(task.recurrence_pattern)
  const [editReminderTime, setEditReminderTime] = useState<string | null>(task.reminder_time)
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false)

  // Phase III: Check due date status
  const taskIsOverdue = isOverdue(task.due_date, task.completed)
  const taskIsDueToday = isDueToday(task.due_date, task.completed)

  const handleSave = () => {
    if (!editTitle.trim()) {
      alert('Title cannot be empty')
      return
    }

    onUpdate({
      title: editTitle.trim(),
      description: editDescription.trim() || null,
      priority: editPriority, // Phase III: Include priority
      due_date: editDueDate, // Phase III: Include due_date
    })
    setIsEditing(false)
  }

  const handleCancel = () => {
    setEditTitle(task.title)
    setEditDescription(task.description || '')
    setEditPriority(task.priority)
    setEditDueDate(task.due_date)
    setIsEditing(false)
  }

  const handleToggleComplete = () => {
    onUpdate({ completed: !task.completed })
  }

  const handleDelete = () => {
    setShowDeleteConfirm(false)
    onDelete()
  }

  if (isEditing) {
    return (
      <div className="bg-white p-4 rounded-lg shadow border border-gray-200">
        <div className="space-y-3">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Title *
            </label>
            <input
              type="text"
              value={editTitle}
              onChange={(e) => setEditTitle(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Task title"
              maxLength={1000}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            <textarea
              value={editDescription}
              onChange={(e) => setEditDescription(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Task description (optional)"
              rows={3}
              maxLength={10000}
            />
          </div>
          {/* Phase III: Priority Selector in Edit Mode */}
          <PrioritySelector
            value={editPriority}
            onChange={setEditPriority}
            required={true}
          />
          {/* Phase III: Due Date Picker in Edit Mode */}
          <DateTimePicker
            label="Due Date"
            value={editDueDate}
            onChange={setEditDueDate}
            required={false}
            includeTime={true}
          />
          <div className="flex gap-2">
            <button
              onClick={handleSave}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              Save
            </button>
            <button
              onClick={handleCancel}
              className="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div
      className={`bg-white p-4 rounded-lg shadow border-2 hover:shadow-md transition-shadow ${
        taskIsOverdue
          ? 'border-red-300 bg-red-50'
          : taskIsDueToday
          ? 'border-yellow-300 bg-yellow-50'
          : 'border-gray-200'
      }`}
    >
      <div className="flex items-start gap-3">
        {/* Checkbox for completion */}
        <input
          type="checkbox"
          checked={task.completed}
          onChange={handleToggleComplete}
          className="mt-1 h-5 w-5 text-blue-600 focus:ring-blue-500 border-gray-300 rounded cursor-pointer"
        />

        {/* Task content */}
        <div className="flex-1 min-w-0">
          {/* Phase III: Priority and Due Date Badges */}
          <div className="flex items-center gap-2 mb-1 flex-wrap">
            <span
              className={`inline-flex items-center px-2 py-1 rounded-md text-xs font-medium border ${getPriorityBadgeStyles(
                task.priority
              )}`}
            >
              {getPriorityIcon(task.priority)} {task.priority.charAt(0).toUpperCase() + task.priority.slice(1)}
            </span>
            {/* Phase III: Due Date Badge (FR-015, FR-016) */}
            {task.due_date && (
              <span
                className={`inline-flex items-center px-2 py-1 rounded-md text-xs font-medium border ${
                  taskIsOverdue
                    ? 'bg-red-100 text-red-800 border-red-300'
                    : taskIsDueToday
                    ? 'bg-yellow-100 text-yellow-800 border-yellow-300'
                    : 'bg-blue-100 text-blue-800 border-blue-200'
                }`}
              >
                {taskIsOverdue ? '⚠️ Overdue' : taskIsDueToday ? '📅 Due Today' : '📅'} {formatDueDate(task.due_date)}
              </span>
            )}
            {/* Phase III: Recurring Badge */}
            {task.is_recurring && (
              <span className="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium border bg-purple-100 text-purple-800 border-purple-200">
                🔁 {task.recurrence_pattern}
              </span>
            )}
            {/* Phase III: Reminder Badge */}
            {task.reminder_time && !task.completed && (
              <span className="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium border bg-indigo-100 text-indigo-800 border-indigo-200">
                🔔 Reminder
              </span>
            )}
          </div>
          <h3
            className={`text-lg font-medium ${
              task.completed ? 'line-through text-gray-500' : 'text-gray-900'
            }`}
          >
            {task.title}
          </h3>
          {task.description && (
            <p
              className={`mt-1 text-sm ${
                task.completed ? 'line-through text-gray-400' : 'text-gray-600'
              }`}
            >
              {task.description}
            </p>
          )}
          <p className="mt-2 text-xs text-gray-400" suppressHydrationWarning>
            Created: {new Date(task.created_at).toLocaleString()}
            {task.updated_at && ` • Updated: ${new Date(task.updated_at).toLocaleString()}`}
          </p>
        </div>

        {/* Action buttons */}
        <div className="flex gap-2">
          <button
            onClick={() => setIsEditing(true)}
            className="p-2 text-blue-600 hover:bg-blue-50 rounded-md transition-colors"
            title="Edit task"
          >
            <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
              />
            </svg>
          </button>
          <button
            onClick={() => setShowDeleteConfirm(true)}
            className="p-2 text-red-600 hover:bg-red-50 rounded-md transition-colors"
            title="Delete task"
          >
            <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
              />
            </svg>
          </button>
        </div>
      </div>

      {/* Delete confirmation dialog */}
      {showDeleteConfirm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg shadow-xl max-w-md">
            <h3 className="text-lg font-medium text-gray-900 mb-2">Delete Task?</h3>
            <p className="text-sm text-gray-600 mb-4">
              Are you sure you want to delete this task? This action cannot be undone.
            </p>
            <div className="flex gap-3 justify-end">
              <button
                onClick={() => setShowDeleteConfirm(false)}
                className="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400"
              >
                Cancel
              </button>
              <button
                onClick={handleDelete}
                className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
