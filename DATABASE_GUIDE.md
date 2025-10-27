# 🗄️ Database Integration Guide

## ✅ What We Just Did

I've converted your app from JSON storage to **SQLite database**, which provides:

- ✅ **Persistence**: Data survives app restarts
- ✅ **Better Performance**: Faster queries and filtering
- ✅ **Lightweight**: No additional dependencies needed
- ✅ **Reliable**: Built into Python
- ✅ **Works on Streamlit Cloud**: Database file persists on cloud storage

## 📊 Changes Made

### 1. **data_manager.py** - Converted to SQLite
- Changed from JSON file to SQLite database
- All functions now use SQL queries
- Database file: `study_sessions.db`

### 2. **.gitignore** - Updated
- Added `*.db` to ignore database files
- This keeps your database local and private

## 🚀 How to Use

### Running the App with Database

1. **Activate your virtual environment:**
   ```bash
   venv\Scripts\activate
   ```

2. **Run the app:**
   ```bash
   streamlit run app.py
   ```

3. **First time running:**
   - The app will automatically create `study_sessions.db`
   - No setup needed! It's all automatic

## 💾 How the Database Works

### Database Structure

The database has one table called `sessions` with these columns:

```
- id (TEXT) - Unique identifier for each session
- day (INTEGER) - Day number (1-100)
- date (TEXT) - Date of session (YYYY-MM-DD)
- category (TEXT) - Category of study
- topic (TEXT) - Topic studied
- duration (TEXT) - Duration of session
- daily_win (TEXT) - Achievement of the day
- key_learnings (TEXT) - Key learnings
- resources (TEXT) - Resources used
- difficulty (TEXT) - Difficulty level
- focus_level (TEXT) - Focus level
- obstacles (TEXT) - Obstacles faced
- next_steps (TEXT) - Next steps
- practical_application (TEXT) - Practical application
- created_at (TEXT) - Creation timestamp
```

### Functions Available

All these functions work the same way as before:

- `load_sessions()` - Get all sessions
- `add_session(data)` - Add a new session
- `delete_session(session_id)` - Delete a session
- `get_session_by_id(session_id)` - Get specific session
- `get_sessions_count()` - Count sessions
- `get_current_streak()` - Calculate current streak
- `get_days_since_last_study()` - Days without studying
- `get_total_hours_studied()` - Total hours studied

## 🔧 Advanced Options

### Option 1: View Database with DB Browser

1. Download [DB Browser for SQLite](https://sqlitebrowser.org/)
2. Open `study_sessions.db`
3. Browse your data, run queries, export to CSV

### Option 2: Backup Your Database

**Windows:**
```bash
copy study_sessions.db study_sessions_backup.db
```

**Or use Git:**
```bash
git add study_sessions.db
git commit -m "Backup database"
git push
```

### Option 3: Migrate from JSON to Database

If you already have data in `study_sessions.json`:

1. Create a migration script:
```python
import json
import sqlite3

# Load JSON data
with open('study_sessions.json', 'r') as f:
    sessions = json.load(f)

# Connect to database
conn = sqlite3.connect('study_sessions.db')
conn.row_factory = sqlite3.Row

# Insert data
for session in sessions:
    conn.execute("""
        INSERT INTO sessions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        session.get('id'),
        session.get('day'),
        session.get('date'),
        session.get('category'),
        session.get('topic'),
        session.get('duration'),
        session.get('daily_win'),
        session.get('key_learnings'),
        session.get('resources'),
        session.get('difficulty'),
        session.get('focus_level'),
        session.get('obstacles'),
        session.get('next_steps'),
        session.get('practical_application'),
        session.get('created_at')
    ))

conn.commit()
conn.close()
print("Migration complete!")
```

### Option 4: Use Cloud Database (Production)

For production on Streamlit Cloud, consider these options:

#### A. PostgreSQL (via Railway - FREE tier available)

1. Sign up at [Railway.app](https://railway.app)
2. Create PostgreSQL database
3. Get connection string
4. Update `data_manager.py` to use PostgreSQL instead of SQLite

#### B. MongoDB Atlas (FREE tier)

1. Sign up at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create free cluster
3. Get connection string
4. Update to use MongoDB

## 📝 Common Queries

### Run SQL Queries Directly

You can add a "Developer" page to your app to run custom queries:

```python
# In app.py, add a new page

if page == "🔧 Developer Tools":
    show_developer_tools()

def show_developer_tools():
    st.markdown("## 🔧 Developer Tools")
    
    query = st.text_area("Run SQL Query:", "SELECT * FROM sessions LIMIT 10")
    
    if st.button("Execute"):
        conn = get_db_connection()
        cursor = conn.execute(query)
        results = cursor.fetchall()
        
        df = pd.DataFrame([dict(row) for row in results])
        st.dataframe(df)
        conn.close()
```

## ⚠️ Important Notes

1. **Backup Regularly**: Always backup `study_sessions.db`
2. **Git Ignore**: Database is in `.gitignore` - it won't be pushed to GitHub
3. **Streamlit Cloud**: Database persists! No data loss on restarts
4. **Size Limit**: SQLite can handle up to 281 TB (you're safe!)

## 🎯 Benefits Over JSON

| Feature | JSON | SQLite |
|---------|------|--------|
| Persistence | ❌ Lost on restart | ✅ Survives |
| Performance | Slow with many items | Fast, indexed |
| Querying | Manual filtering | SQL queries |
| Data Integrity | No validation | Built-in checks |
| Scaling | Poor | Better |
| Backup | Manual | Auto-saved |

## 🐛 Troubleshooting

### Database is locked error

**Problem:** Another process is using the database

**Solution:** 
```python
# In data_manager.py, the connection is set to:
conn = sqlite3.connect(DB_FILE, check_same_thread=False)
# This should already fix it!
```

### Reset Database

**If you want to start fresh:**

1. Delete `study_sessions.db`
2. Restart the app
3. New database will be created automatically

### View Database Size

**Check your database size:**

```bash
# Windows PowerShell
(Get-Item study_sessions.db).Length / 1KB

# Output will show size in KB
```

## 📚 Learn More

- [SQLite Official Docs](https://www.sqlite.org/docs.html)
- [Python sqlite3 Module](https://docs.python.org/3/library/sqlite3.html)
- [Streamlit State Management](https://docs.streamlit.io/library/api-reference/session-state)

---

**Your app is now database-powered! 🎉**

All your sessions will persist across restarts, and you're ready for production deployment on Streamlit Cloud!

