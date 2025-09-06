import os
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def add_user_history(user_id, action, details=None):
    try:
        data = {
            'user_id': user_id,
            'action': action,
            'details': details,
            'timestamp': datetime.utcnow().isoformat()
        }
        response = supabase.table('user_history').insert(data).execute()
        return response.data
    except Exception as e:
        print(f"Supabase connection error in add_user_history: {e}")
        return None

def get_user_history(user_id, limit=50):
    response = supabase.table('user_history').select('*').eq('user_id', user_id).order('timestamp', desc=True).limit(limit).execute()
    return response.data
