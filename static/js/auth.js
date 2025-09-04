// Authentication related functions
class Auth {
    static isLoggedIn() {
        return localStorage.getItem('token') !== null;
    }

    static getToken() {
        return localStorage.getItem('token');
    }

    static setToken(token) {
        localStorage.setItem('token', token);
    }

    static clearToken() {
        localStorage.removeItem('token');
    }

    static async login(username, password) {
        try {
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });

            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.error || 'Login failed');
            }

            const data = await response.json();
            this.setToken(data.token);
            return data;
        } catch (error) {
            throw error;
        }
    }

    static async signup(username, password) {
        try {
            const response = await fetch('/api/auth/signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });

            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.error || 'Signup failed');
            }

            return await response.json();
        } catch (error) {
            throw error;
        }
    }

    static logout() {
        this.clearToken();
        window.location.href = '/';
    }

    static async makeAuthenticatedRequest(url, options = {}) {
        const token = this.getToken();
        if (!token) {
            throw new Error('No authentication token found');
        }

        const headers = {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
            ...options.headers
        };

        const response = await fetch(url, {
            ...options,
            headers
        });

        if (response.status === 401) {
            this.clearToken();
            window.location.href = '/login.html';
            throw new Error('Session expired. Please log in again.');
        }

        return response;
    }
}
