import { configureStore } from "@reduxjs/toolkit"
import { apiSlice } from "./services/appSlices";
import authReducer from "./features/authSlices";

export const store =  
    configureStore({
        reducer: {
            [apiSlice.reducerPath] : apiSlice.reducer,
            auth: authReducer,
        },
        middleware: getDefaultMiddleware => getDefaultMiddleware().concat(apiSlice.middleware),
        devTools: process.env.NODE_ENV !== 'production',
    })

export type RootState = ReturnType<typeof store['getState']>;
export type AppDispatch = (typeof store)['dispatch'];