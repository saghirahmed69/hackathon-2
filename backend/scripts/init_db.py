"""
Database initialization script.
Creates all tables defined in SQLModel models.
"""

import asyncio
from sqlmodel import SQLModel

from app.database import engine
from app.models.user import User  # Import all models to register them


async def init_database():
    """
    Create all database tables.

    This function creates all tables defined in SQLModel models
    in the Neon PostgreSQL database.
    """
    print("🔄 Creating database tables...")

    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(SQLModel.metadata.create_all)

    print("✅ Database tables created successfully!")
    print(f"📋 Tables created: {', '.join(SQLModel.metadata.tables.keys())}")


async def verify_schema():
    """
    Verify database schema matches expected structure.
    """
    print("\n🔍 Verifying database schema...")

    # Check users table
    if 'users' in SQLModel.metadata.tables:
        users_table = SQLModel.metadata.tables['users']
        print(f"✅ users table exists")
        print(f"   Columns: {', '.join([col.name for col in users_table.columns])}")

        # Verify expected columns
        expected_columns = {'id', 'email', 'hashed_password', 'created_at'}
        actual_columns = {col.name for col in users_table.columns}

        if expected_columns == actual_columns:
            print("✅ users table schema matches data-model.md")
        else:
            missing = expected_columns - actual_columns
            extra = actual_columns - expected_columns
            if missing:
                print(f"⚠️  Missing columns: {missing}")
            if extra:
                print(f"⚠️  Extra columns: {extra}")
    else:
        print("❌ users table not found in metadata")


async def main():
    """Main execution function."""
    print("=" * 60)
    print("Database Initialization - Phase II Web Todo App")
    print("=" * 60)

    try:
        await init_database()
        await verify_schema()
        print("\n✅ Database initialization complete!")
    except Exception as e:
        print(f"\n❌ Database initialization failed: {e}")
        raise
    finally:
        # Close engine
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
