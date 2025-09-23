# TODO: Implement User Authentication UI Changes

## Completed Steps
- [x] Modified app/routes/auth_routes.py to store user data in session after login
- [x] Updated logout to clear all session data
- [x] Added get_user_from_session function in app/models/users.py
- [x] Updated app/routes/main_routes.py to use session-stored user data

## Next Steps
- Test the login flow to ensure username displays correctly after login
- Verify logout clears the session and shows login/signup again
