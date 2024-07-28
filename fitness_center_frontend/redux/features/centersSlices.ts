// redux/centersSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

// Definisci l'interfaccia per i dati dei centri
interface Center {
  uuid: string;
  name: string;
  description: string;
  manager_id: string;
  province: string;
  city: string;
  street: string;
  house_number: number;
  is_active: boolean;
}

// Definisci l'interfaccia per lo stato
interface CentersState {
  data: Center[]; // Stato per memorizzare i dati dei centri
}

// Stato iniziale
const initialState: CentersState = {
  data: [],
};

// Crea lo slice
const centersSlice = createSlice({
  name: 'centers',
  initialState,
  reducers: {
    setCentersData(state, action: PayloadAction<Center[]>) {
      state.data = action.payload;
    },
  },
});

// Esporta i reducer e le azioni
export const { setCentersData } = centersSlice.actions;
export default centersSlice.reducer;
