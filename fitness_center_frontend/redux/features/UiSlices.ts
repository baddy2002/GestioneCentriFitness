import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface UiState {
  selectedEntity: 'centers' | 'employees' | 'exits';
}

const initialState: UiState = {
  selectedEntity: 'centers', // Imposta un valore predefinito
};

const uiSlice = createSlice({
  name: 'ui',
  initialState,
  reducers: {
    setSelectedEntity: (state, action: PayloadAction<'centers' | 'employees' | 'exits'>) => {
      state.selectedEntity = action.payload;
    },
  },
});

export const { setSelectedEntity } = uiSlice.actions;

export default uiSlice.reducer;
