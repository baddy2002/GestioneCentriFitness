// redux/store.ts
import { configureStore } from '@reduxjs/toolkit';
import authReducer from './features/authSlices';
import centersReducer from './features/centersSlices';
import employeesReducer from './features/employeesSlices';
import exitsReducer from './features/exitsSlices';
import UiSliceReducer from './features/UiSlices';
import { apiSlice as appApiSlice } from './services/appSlices';
import { centerApiSlice } from './services/centersSlices';

// Configura lo store Redux
export const store = configureStore({
  reducer: {
    [appApiSlice.reducerPath]: appApiSlice.reducer,
    [centerApiSlice.reducerPath]: centerApiSlice.reducer,
    auth: authReducer,
    centers: centersReducer,
    employees: employeesReducer,
    exits: exitsReducer,
    ui: UiSliceReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware()
      .concat(appApiSlice.middleware)
      .concat(centerApiSlice.middleware),
  devTools: process.env.NODE_ENV !== 'production',
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
