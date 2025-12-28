/**
 * TypeScript type definitions for API models
 */

// Type aliases for Phase III Advanced Features
export type PriorityLevel = 'high' | 'medium' | 'low'
export type RecurrencePattern = 'daily' | 'weekly' | 'monthly'

export interface User {
  id: string
  email: string
  created_at: string
}

export interface Task {
  // Phase II Core Fields
  id: string
  user_id: string
  title: string
  description: string | null
  completed: boolean
  created_at: string
  updated_at: string | null

  // Phase III Advanced Features (003-advanced-task-features)
  priority: PriorityLevel
  due_date: string | null  // ISO 8601 timestamp or null
  is_recurring: boolean
  recurrence_pattern: RecurrencePattern | null
  reminder_time: string | null  // ISO 8601 timestamp or null
}

export interface AuthResponse {
  access_token: string
  token_type: string
  user: User
}

export interface SignupRequest {
  email: string
  password: string
}

export interface SigninRequest {
  email: string
  password: string
}

export interface TaskCreateRequest {
  // Phase II Core Fields
  title: string
  description?: string

  // Phase III Advanced Features (003-advanced-task-features)
  priority?: PriorityLevel
  due_date?: string | null
  is_recurring?: boolean
  recurrence_pattern?: RecurrencePattern | null
  reminder_time?: string | null
}

export interface TaskUpdateRequest {
  // Phase II Core Fields
  title?: string
  description?: string | null
  completed?: boolean

  // Phase III Advanced Features (003-advanced-task-features)
  priority?: PriorityLevel
  due_date?: string | null
  is_recurring?: boolean
  recurrence_pattern?: RecurrencePattern | null
  reminder_time?: string | null
}

export interface TaskFilterParams {
  /**
   * Query parameters for filtering, sorting, and searching tasks.
   * All parameters are optional and can be combined.
   */
  search?: string  // Keyword search in title/description
  status?: 'pending' | 'completed'  // Filter by completion status
  priority?: PriorityLevel  // Filter by priority level
  due_date?: string  // Filter by due date (format: 'before:YYYY-MM-DD', 'after:YYYY-MM-DD', 'on:YYYY-MM-DD')
  sort_by?: 'due_date' | 'priority' | 'title'  // Sort field
  sort_order?: 'asc' | 'desc'  // Sort direction (default: 'asc')
}

export interface ApiError {
  detail: string | Array<{ loc: string[]; msg: string; type: string }>
}
