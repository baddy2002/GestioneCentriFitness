import { createSlice } from "@reduxjs/toolkit";

interface user{
    id: string;
    email: string;
    first_name: string;
    last_name: string;
    data_iscrizione: string;
    photo: string;
};

interface authState {
    isAuthenticated: boolean;
    isLoading: boolean;
    user: user | null;
};



const initialState = {
    isAuthenticated: false,
    isLoading: true,
    user: null,
} as authState;

const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {
        setAuth: (state, action) => {
            state.isAuthenticated = true;
            state.user = action.payload;
        },
        logout: state => {
            state.isAuthenticated = false;
            state.user = null; 
        },
        finishInitialLoad: state => {
            state.isAuthenticated = state.isAuthenticated;
            state.isLoading = false;
        },
    },
});


export const {setAuth, logout, finishInitialLoad} = authSlice.actions;
export default authSlice.reducer;