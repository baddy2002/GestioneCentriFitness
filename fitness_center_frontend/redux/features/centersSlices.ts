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
  centerData: Center[]; // Stato per memorizzare i dati dei centri
}

// Stato iniziale
const initialCentersState: CentersState = {
  centerData: [],
};

// Crea lo slice
const centersSlice = createSlice({
  name: 'centers',
  initialState: initialCentersState,
  reducers: {
    setCentersData(state, action: PayloadAction<Center[]>) {
      state.centerData = action.payload;
    },
    clearCentersData(state) {
      state.centerData = [];
    }
  }
});

// Esporta le azioni e il reducer
export const { setCentersData, clearCentersData } = centersSlice.actions;
export default centersSlice.reducer;
