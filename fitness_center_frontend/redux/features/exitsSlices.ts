// redux/exitsSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

// Definisci l'interfaccia per i dati delle uscite
interface Exit {
  uuid: string;
  amount: number;
  type: string;
  employee_uuid: string | null;
  frequency: number;
  description: string;
  start_date: string;
  expiration_date: string | null;
  center_uuid: string;
  is_active: boolean;
}

// Definisci l'interfaccia per lo stato
interface ExitsState {
  exitData: Exit[]; // Stato per memorizzare i dati delle uscite
}

// Stato iniziale
const initialExitsState: ExitsState = {
  exitData: [],
};

// Crea lo slice
const exitsSlice = createSlice({
  name: 'exits',
  initialState: initialExitsState,
  reducers: {
    setExitsData(state, action: PayloadAction<Exit[]>) {
      state.exitData = action.payload;
    },
    clearExitsData(state) {
      state.exitData = [];
    }
  }
});

// Esporta le azioni e il reducer
export const { setExitsData, clearExitsData } = exitsSlice.actions;
export default exitsSlice.reducer;
