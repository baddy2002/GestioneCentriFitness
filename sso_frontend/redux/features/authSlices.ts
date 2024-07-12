import { createSlice } from "@reduxjs/toolkit";

interface authState {
    isAuthenticated: boolean;
    isLoading: boolean;
};

const initialState = {
    isAuthenticated: false,
    isLoading: false,
} as authState;

const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {
        setAuth: state => {
            state.isAuthenticated = true;
        },
        logout: state => {
            state.isAuthenticated = false;
        },
        finishInitialLoad: state => {
            state.isLoading = false;
        },
    },
});


export const {setAuth, logout, finishInitialLoad} = authSlice.actions;
export default authSlice.reducer;