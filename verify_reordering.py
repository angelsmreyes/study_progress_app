import streamlit as st
from utils import data_manager
import time

# Mock secrets for local testing if needed, but assuming env is set up
# st.secrets should be available if running via streamlit or if we mock it.
# Since we are running via python, we might need to load secrets manually if not using streamlit run.
# However, data_manager uses st.secrets. Let's assume we run this with `streamlit run` or mock st.secrets.

def verify_reordering():
    print("🚀 Starting reordering verification...")
    
    # 1. Clear existing test sessions (optional, but safer to just add new ones and check relative order)
    # For safety, let's just add 3 sessions with specific dates.
    
    timestamp = int(time.time())
    
    s1 = {
        "id": f"test_s1_{timestamp}",
        "date": "2025-01-01",
        "topic": "Test Session 1",
        "category": "Test",
        "duration": "1h",
        "daily_win": "Win 1",
        "difficulty": "Medio",
        "focus_level": "Medio"
    }
    
    s2 = {
        "id": f"test_s2_{timestamp}",
        "date": "2025-01-03", # Later date
        "topic": "Test Session 2",
        "category": "Test",
        "duration": "1h",
        "daily_win": "Win 2",
        "difficulty": "Medio",
        "focus_level": "Medio"
    }
    
    s3 = {
        "id": f"test_s3_{timestamp}",
        "date": "2025-01-02", # Middle date, should be inserted between 1 and 2
        "topic": "Test Session 3",
        "category": "Test",
        "duration": "1h",
        "daily_win": "Win 3",
        "difficulty": "Medio",
        "focus_level": "Medio"
    }
    
    print("1️⃣ Adding Session 1 (2025-01-01)...")
    data_manager.add_session(s1)
    
    print("2️⃣ Adding Session 2 (2025-01-03)...")
    data_manager.add_session(s2)
    
    print("3️⃣ Adding Session 3 (2025-01-02) - Should trigger reorder...")
    data_manager.add_session(s3)
    
    # Verify order
    print("🔍 Verifying order...")
    s1_fetched = data_manager.get_session_by_id(s1['id'])
    s2_fetched = data_manager.get_session_by_id(s2['id'])
    s3_fetched = data_manager.get_session_by_id(s3['id'])
    
    print(f"Session 1 Day: {s1_fetched['day']} (Expected < S3)")
    print(f"Session 3 Day: {s3_fetched['day']} (Expected < S2)")
    print(f"Session 2 Day: {s2_fetched['day']} (Expected > S3)")
    
    if s1_fetched['day'] < s3_fetched['day'] < s2_fetched['day']:
        print("✅ Order is correct!")
    else:
        print("❌ Order is INCORRECT!")
        
    # Clean up
    print("🧹 Cleaning up test sessions...")
    data_manager.delete_session(s1['id'])
    data_manager.delete_session(s2['id'])
    data_manager.delete_session(s3['id'])
    print("✅ Cleanup complete.")

if __name__ == "__main__":
    # We need to mock st.secrets if running directly with python
    import toml
    try:
        secrets = toml.load(".streamlit/secrets.toml")
        st.secrets = secrets
        verify_reordering()
    except Exception as e:
        print(f"Could not load secrets or run verification: {e}")
