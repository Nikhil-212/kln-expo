-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    language_preference TEXT NOT NULL DEFAULT 'en',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create user_history table
CREATE TABLE IF NOT EXISTS user_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    action TEXT NOT NULL,
    details TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for better performance
CREATE INDEX IF NOT EXISTS idx_user_history_user_id ON user_history(user_id);
CREATE INDEX IF NOT EXISTS idx_user_history_timestamp ON user_history(timestamp);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
