// redux/employeesSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

// Definisci l'interfaccia per i dati dei dipendenti
interface Employee {
  uuid: string;
  first_name: string;
  last_name: string;
  DOB: string;
  salary: number;
  fiscalCode: string;
  email: string;
  type: string;
  hiring_date: string;
  end_contract_date: string | null;
  attachments_uuid: string;
  center_uuid: string;
  is_active: boolean;
}

// Definisci l'interfaccia per lo stato
interface EmployeesState {
  employeeData: Employee[]; // Stato per memorizzare i dati dei dipendenti
}

// Stato iniziale
const initialEmployeesState: EmployeesState = {
  employeeData: [],
};

// Crea lo slice
const employeesSlice = createSlice({
  name: 'employees',
  initialState: initialEmployeesState,
  reducers: {
    setEmployeesData(state, action: PayloadAction<Employee[]>) {
      state.employeeData = action.payload;
    },
    clearEmployeesData(state) {
      state.employeeData = [];
    }
  }
});

// Esporta le azioni e il reducer
export const { setEmployeesData, clearEmployeesData } = employeesSlice.actions;
export default employeesSlice.reducer;
