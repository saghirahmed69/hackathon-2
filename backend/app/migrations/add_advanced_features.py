"""
Database migration script for Advanced Task Management Features.

This migration adds 5 new columns to the tasks table:
- priority (enum: high, medium, low, NOT NULL, default 'medium')
- due_date (timestamp, NULLABLE)
- is_recurring (boolean, NOT NULL, default false)
- recurrence_pattern (enum: daily, weekly, monthly, NULLABLE)
- reminder_time (timestamp, NULLABLE)

Also creates indexes for performance optimization.

Usage:
    Run this script manually via psql or database client:
    psql <connection_string> -f add_advanced_features.sql
"""

# SQL migration script
MIGRATION_SQL = """
-- Advanced Task Management Features Migration
-- Date: 2025-12-26
-- Purpose: Add priority, due dates, recurring tasks, and reminders

BEGIN;

-- Step 1: Add new columns to tasks table
ALTER TABLE tasks
    ADD COLUMN priority VARCHAR(10) NOT NULL DEFAULT 'medium'
        CHECK (priority IN ('high', 'medium', 'low')),
    ADD COLUMN due_date TIMESTAMP NULL,
    ADD COLUMN is_recurring BOOLEAN NOT NULL DEFAULT FALSE,
    ADD COLUMN recurrence_pattern VARCHAR(20) NULL
        CHECK (recurrence_pattern IS NULL OR recurrence_pattern IN ('daily', 'weekly', 'monthly')),
    ADD COLUMN reminder_time TIMESTAMP NULL;

-- Step 2: Backfill existing tasks with default values
-- (priority already set to 'medium' via DEFAULT)
-- (is_recurring already set to FALSE via DEFAULT)
-- (nullable fields already set to NULL)

-- Step 3: Create indexes for performance
CREATE INDEX idx_tasks_priority ON tasks(user_id, priority);
CREATE INDEX idx_tasks_due_date ON tasks(user_id, due_date) WHERE due_date IS NOT NULL;
CREATE INDEX idx_tasks_reminder ON tasks(reminder_time) WHERE reminder_time IS NOT NULL;

-- Step 4: Add comments for documentation
COMMENT ON COLUMN tasks.priority IS 'Task priority level: high, medium, or low';
COMMENT ON COLUMN tasks.due_date IS 'Optional due date/time for task completion';
COMMENT ON COLUMN tasks.is_recurring IS 'Whether task regenerates when completed';
COMMENT ON COLUMN tasks.recurrence_pattern IS 'Recurrence frequency: daily, weekly, or monthly';
COMMENT ON COLUMN tasks.reminder_time IS 'Optional timestamp for browser notification reminder';

COMMIT;
"""

# Rollback script
ROLLBACK_SQL = """
-- Rollback Advanced Task Management Features Migration

BEGIN;

-- Drop indexes
DROP INDEX IF EXISTS idx_tasks_reminder;
DROP INDEX IF EXISTS idx_tasks_due_date;
DROP INDEX IF EXISTS idx_tasks_priority;

-- Drop columns
ALTER TABLE tasks
    DROP COLUMN IF EXISTS reminder_time,
    DROP COLUMN IF EXISTS recurrence_pattern,
    DROP COLUMN IF EXISTS is_recurring,
    DROP COLUMN IF EXISTS due_date,
    DROP COLUMN IF EXISTS priority;

COMMIT;
"""


def get_migration_sql() -> str:
    """
    Get the forward migration SQL script.

    Returns:
        SQL script to apply migration
    """
    return MIGRATION_SQL


def get_rollback_sql() -> str:
    """
    Get the rollback migration SQL script.

    Returns:
        SQL script to rollback migration
    """
    return ROLLBACK_SQL


if __name__ == "__main__":
    print("=== Advanced Task Management Features Migration ===")
    print("\n--- Forward Migration SQL ---")
    print(MIGRATION_SQL)
    print("\n--- Rollback SQL ---")
    print(ROLLBACK_SQL)
    print("\nTo apply this migration:")
    print("1. Connect to your Neon PostgreSQL database")
    print("2. Run the SQL commands from get_migration_sql()")
    print("3. Verify with: SELECT column_name, data_type FROM information_schema.columns WHERE table_name='tasks';")
    print("\nTo rollback this migration:")
    print("1. Run the SQL commands from get_rollback_sql()")
