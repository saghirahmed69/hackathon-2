/**
 * DateTimePicker Component
 *
 * Date and optional time input component for due dates and reminders.
 * Part of User Story 2: Task Due Dates (FR-009, FR-010)
 */

interface DateTimePickerProps {
  label: string
  value: string | null
  onChange: (value: string | null) => void
  required?: boolean
  className?: string
  includeTime?: boolean
}

export default function DateTimePicker({
  label,
  value,
  onChange,
  required = false,
  className = '',
  includeTime = true,
}: DateTimePickerProps) {
  const handleClear = () => {
    onChange(null)
  }

  return (
    <div className={className}>
      <label className="block text-sm font-medium text-gray-700 mb-1">
        {label} {required && <span className="text-red-500">*</span>}
      </label>
      <div className="flex gap-2">
        <input
          type={includeTime ? 'datetime-local' : 'date'}
          value={value ? (includeTime ? value.slice(0, 16) : value.slice(0, 10)) : ''}
          onChange={(e) => {
            const newValue = e.target.value
            if (newValue) {
              // Convert to ISO 8601 format
              const isoValue = includeTime ? `${newValue}:00` : `${newValue}T00:00:00`
              onChange(isoValue)
            } else {
              onChange(null)
            }
          }}
          required={required}
          className="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        />
        {!required && value && (
          <button
            type="button"
            onClick={handleClear}
            className="px-3 py-2 text-sm text-gray-600 hover:text-red-600 border border-gray-300 rounded-md hover:border-red-300 transition-colors"
            title="Clear date"
          >
            Clear
          </button>
        )}
      </div>
      {!required && (
        <p className="mt-1 text-xs text-gray-500">Optional - leave empty if not applicable</p>
      )}
    </div>
  )
}
