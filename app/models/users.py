import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_user(user_id):
    try:
        response = supabase.table('users').select('*').eq('id', user_id).execute()
        if response.data:
            return response.data[0]
    except Exception as e:
        print(f"Supabase connection error in get_user: {e}")
    return None

def get_user_by_username(username):
    try:
        response = supabase.table('users').select('*').eq('username', username).execute()
        if response.data:
            return response.data[0]
    except Exception as e:
        print(f"Supabase connection error in get_user_by_username: {e}")
    return None

def add_user(username, password_hash):
    try:
        data = {
            'username': username,
            'password_hash': password_hash
        }
        response = supabase.table('users').insert(data).execute()
        return response.data
    except Exception as e:
        print(f"Supabase connection error in add_user: {e}")
        return None
