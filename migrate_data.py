import sqlite3
import toml
import os
from supabase import create_client

def migrate_data():
    """
    Migrate data from local SQLite database to Supabase.
    """
    print("🚀 Starting migration from SQLite to Supabase...")
    
    # 1. Connect to SQLite
    db_file = os.path.join(os.path.dirname(__file__), "study_sessions.db")
    if not os.path.exists(db_file):
        print(f"❌ SQLite database not found at {db_file}")
        return

    try:
        conn = sqlite3.connect(db_file)
        conn.row_factory = sqlite3.Row
        cursor = conn.execute("SELECT * FROM sessions")
        rows = cursor.fetchall()
        sessions = [dict(row) for row in rows]
        conn.close()
        print(f"✅ Found {len(sessions)} sessions in SQLite.")
    except Exception as e:
        print(f"❌ Error reading SQLite: {e}")
        return

    if not sessions:
        print("⚠️ No sessions to migrate.")
        return

    # 2. Connect to Supabase
    secrets_file = os.path.join(os.path.dirname(__file__), ".streamlit", "secrets.toml")
    if not os.path.exists(secrets_file):
        print(f"❌ Secrets file not found at {secrets_file}")
        return

    try:
        secrets = toml.load(secrets_file)
        # Handle both structure formats
        if "supabase" in secrets:
            url = secrets["supabase"]["url"]
            key = secrets["supabase"]["key"]
        else:
            url = secrets["SUPABASE_URL"]
            key = secrets["SUPABASE_KEY"]
            
        supabase = create_client(url, key)
        print("✅ Connected to Supabase.")
    except Exception as e:
        print(f"❌ Error connecting to Supabase: {e}")
        return

    # 3. Insert data
    print("📤 Uploading sessions to Supabase...")
    success_count = 0
    error_count = 0
    
    for session in sessions:
        try:
            # Clean up data if necessary (e.g. ensure types match)
            # Supabase expects standard JSON types
            
            # Upsert to avoid duplicates if running multiple times
            supabase.table("study_sessions").upsert(session).execute()
            success_count += 1
            print(f"  - Migrated session {session.get('day')}: {session.get('topic')}")
        except Exception as e:
            error_count += 1
            print(f"  ❌ Failed to migrate session {session.get('id')}")
            print(f"     Error type: {type(e)}")
            print(f"     Error details: {e}")
            if hasattr(e, 'code'):
                print(f"     Code: {e.code}")
            if hasattr(e, 'details'):
                print(f"     Details: {e.details}")
            if hasattr(e, 'message'):
                print(f"     Message: {e.message}")

    print("\n🏁 Migration complete!")
    print(f"✅ Successfully migrated: {success_count}")
    print(f"❌ Failed: {error_count}")

if __name__ == "__main__":
    migrate_data()
