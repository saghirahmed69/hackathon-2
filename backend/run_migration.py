"""
Run the Phase III database migration.
"""
import asyncio
from sqlalchemy import text
from app.database import engine
from app.migrations.add_advanced_features import get_migration_sql


async def run_migration():
    """Execute the Phase III migration SQL."""
    print("=== Running Phase III Migration ===\n")

    # Split migration into individual statements
    statements = [
        # Add new columns
        """
        ALTER TABLE tasks
            ADD COLUMN IF NOT EXISTS priority VARCHAR(10) NOT NULL DEFAULT 'medium'
                CHECK (priority IN ('high', 'medium', 'low')),
            ADD COLUMN IF NOT EXISTS due_date TIMESTAMP NULL,
            ADD COLUMN IF NOT EXISTS is_recurring BOOLEAN NOT NULL DEFAULT FALSE,
            ADD COLUMN IF NOT EXISTS recurrence_pattern VARCHAR(20) NULL
                CHECK (recurrence_pattern IS NULL OR recurrence_pattern IN ('daily', 'weekly', 'monthly')),
            ADD COLUMN IF NOT EXISTS reminder_time TIMESTAMP NULL
        """,
        # Create indexes
        "CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(user_id, priority)",
        "CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks(user_id, due_date) WHERE due_date IS NOT NULL",
        "CREATE INDEX IF NOT EXISTS idx_tasks_reminder ON tasks(reminder_time) WHERE reminder_time IS NOT NULL",
    ]

    try:
        async with engine.begin() as conn:
            print("Executing migration SQL...")
            for stmt in statements:
                await conn.execute(text(stmt))
            print("✅ Migration completed successfully!\n")

            # Verify columns were added
            result = await conn.execute(text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = 'tasks'
                ORDER BY ordinal_position;
            """))

            print("Current tasks table schema:")
            print("-" * 60)
            for row in result:
                nullable = "NULL" if row[2] == "YES" else "NOT NULL"
                print(f"  {row[0]:20s} {row[1]:20s} {nullable}")
            print("-" * 60)

    except Exception as e:
        print(f"❌ Migration failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(run_migration())
