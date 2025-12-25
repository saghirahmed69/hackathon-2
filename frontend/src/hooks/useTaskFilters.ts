/**
 * useTaskFilters Hook
 *
 * Manages task filter and sort state (Phase III)
 */

import { useState } from 'react'
import { TaskFilterParams, PriorityLevel } from '@/lib/types'

export function useTaskFilters() {
  const [search, setSearch] = useState('')
  const [status, setStatus] = useState<'pending' | 'completed' | ''>('')
  const [priority, setPriority] = useState<PriorityLevel | ''>('')
  const [dueDate, setDueDate] = useState('')
  const [sortBy, setSortBy] = useState<'due_date' | 'priority' | 'title' | ''>('')
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc')

  const getFilterParams = (): TaskFilterParams => {
    const params: TaskFilterParams = {}

    if (search) params.search = search
    if (status) params.status = status as 'pending' | 'completed'
    if (priority) params.priority = priority as PriorityLevel
    if (dueDate) params.due_date = dueDate
    if (sortBy) params.sort_by = sortBy as 'due_date' | 'priority' | 'title'
    if (sortOrder) params.sort_order = sortOrder

    return params
  }

  const clearFilters = () => {
    setSearch('')
    setStatus('')
    setPriority('')
    setDueDate('')
    setSortBy('')
    setSortOrder('asc')
  }

  const hasActiveFilters = Boolean(search || status || priority || dueDate || sortBy)

  return {
    search,
    setSearch,
    status,
    setStatus,
    priority,
    setPriority,
    dueDate,
    setDueDate,
    sortBy,
    setSortBy,
    sortOrder,
    setSortOrder,
    getFilterParams,
    clearFilters,
    hasActiveFilters,
  }
}
