// Importazioni dei tuoi slices API
import { apiSlice as appApiSlice } from './services/appSlices';
import { centerApiSlice } from './services/centersSlices';
import authReducer from './features/authSlices';
import { configureStore } from '@reduxjs/toolkit';
import centersReducer from './features/centersSlices'
// Configura lo store Redux
export const store = configureStore({
  reducer: {
    [appApiSlice.reducerPath]: appApiSlice.reducer,
    [centerApiSlice.reducerPath]: centerApiSlice.reducer,
    auth: authReducer,
    centers: centersReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware()
      .concat(appApiSlice.middleware)
      .concat(centerApiSlice.middleware),
  devTools: process.env.NODE_ENV !== 'production',
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
