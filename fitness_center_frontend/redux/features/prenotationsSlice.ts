// redux/prenotationsSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

// Definisci l'interfaccia per i dati dei centri
export interface Prenotation {
  uuid: string;
  from_hour: string;
  to_hour: string;
  manager_id: string;
  total: number;
  center_uuid: string,
  employee_uuid: string,
  type: string,
  is_active: boolean;
}

// Definisci l'interfaccia per lo stato
interface PrenotationsState {
  prenotationData: Prenotation[]; // Stato per memorizzare i dati dei centri
}

// Stato iniziale
const initialprenotationsState: PrenotationsState = {
  prenotationData: [],
};

// Crea lo slice
const prenotationsSlice = createSlice({
  name: 'prenotations',
  initialState: initialprenotationsState,
  reducers: {
    setPrenotationsData(state, action: PayloadAction<Prenotation[]>) {
      state.prenotationData = action.payload;
    },

  }
});

// Esporta le azioni e il reducer
export const { setPrenotationsData } = prenotationsSlice.actions;
export default prenotationsSlice.reducer;
