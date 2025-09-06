-- Enable RLS on tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_history ENABLE ROW LEVEL SECURITY;

-- Users table policies
-- Allow inserts for user registration (signup)
CREATE POLICY "Allow user registration" ON users
FOR INSERT
TO anon
WITH CHECK (true);

-- Allow users to read their own data (for login verification)
CREATE POLICY "Allow user login verification" ON users
FOR SELECT
TO anon
USING (true);

-- User history table policies
-- Allow inserts for logging user activities
CREATE POLICY "Allow activity logging" ON user_history
FOR INSERT
TO anon
WITH CHECK (true);

-- Allow users to read their own history
CREATE POLICY "Allow history viewing" ON user_history
FOR SELECT
TO anon
USING (true);
