import { defineStore } from 'pinia'
import axios from 'axios'
// import api from '../api' // Remove or clarify if api is needed

export const useUserStore = defineStore('user', {
    state: () => ({
        user: null,
        token: localStorage.getItem('token') || null,
        isLoggedIn: !!localStorage.getItem('token'),
        role: localStorage.getItem('role') || null // Store role in state and local storage
    }),

    getters: {
        isStudent: (state) => state.role === 'student',
        isTeacher: (state) => state.role === 'teacher',
        isAdmin: (state) => state.role === 'admin'
    },

    actions: {
        async login(credentials) {
            try {
                // Use the correct API endpoint and handle response
                const response = await axios.post('/api/auth/login/', credentials);
                this.token = response.data.token;
                this.user = response.data.user; // Assuming user details are in response.data.user
                this.role = response.data.user?.role; // Assuming role is nested in user object
                this.isLoggedIn = true;
                localStorage.setItem('token', this.token);
                localStorage.setItem('role', this.role || ''); // Store role
                // Set default Authorization header for future requests
                axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`;
                return response.data; // Return response data
            } catch (error) {
                this.logout(); // Ensure state is clean on login failure
                console.error('Login failed:', error);
                throw error;
            }
        },

        async register(userData) {
            try {
                // Use the correct API endpoint
                const response = await axios.post('/api/auth/register/', userData);
                console.log('Registration successful:', response.data);
                // Registration success does not necessarily mean login, just return success data
                return response.data;
            } catch (error) {
                console.error('Registration failed:', error);
                throw error;
            }
        },

        logout() {
            this.user = null;
            this.token = null;
            this.isLoggedIn = false;
            this.role = null;
            localStorage.removeItem('token');
            localStorage.removeItem('role');
            // Remove the Authorization header
            delete axios.defaults.headers.common['Authorization'];
        },

        // Action to check user status on app load
        async checkAuth() {
            const token = localStorage.getItem('token');
            if (token) {
                this.token = token;
                axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`;
                try {
                    // Call backend endpoint to validate token and get user info
                    const response = await axios.get('/api/auth/user/');
                    this.user = response.data;
                    this.role = response.data?.role;
                    this.isLoggedIn = true;
                    localStorage.setItem('role', this.role || ''); // Ensure role is stored on load
                } catch (error) {
                    console.error('Token validation failed, logging out:', error);
                    this.logout(); // Log out if token is invalid
                }
            } else {
                this.logout(); // Ensure logged out state if no token
            }
        },

        async fetchUserProfile() {
            try {
                const response = await axios.get('/api/users/profile/')
                this.user = response
                return response
            } catch (error) {
                throw error
            }
        }
    }
}) 