// services/centersSlices.ts

import { centerApiSlice } from '../services/centersSlices'; // Assicurati di importare il tuo apiSlice principale

export interface Center {
  uuid: string;
  name: string;
  description: string;
  manager_id: string;
  province: string;
  city: string;
  street: string;
  house_number: number;
  hour_nutritionist_price: number,
  hour_trainer_price: number,
  is_active: boolean;
}

interface FetchCentersParams {
  managerId?: string;
  orderBy?: string; 
  name?: string;
  description?: string;
  province?: string;
  city?: string;
}

export interface Employee {
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
  attachments_uuid: string | null;
  center_uuid: string;
  is_active: boolean;
}

interface FetchEmployeesParams {
  managerId?: string;
  orderBy?: string; 
  first_name?: string;
  last_name?: string;
  type?: string;
  center_uuid?: string;
}

export interface Exit {
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

interface FetchExitsParams {
  managerId?: string;
  orderBy?: string; 
  name?: string;
  description?: string;
  province?: string;
  city?: string;
  center_uuid?: string;
}


const centersApiSlice = centerApiSlice.injectEndpoints({
  endpoints: (builder) => ({
    fetchCenters: builder.query<FetchCentersResponse, FetchCentersParams | void>({
      query: (params) => {
        let queryString = '/centers/';
        if (params) {
          const queryParams = new URLSearchParams();
          if (params.managerId) queryParams.append('obj.manager_id', params.managerId);
          if (params.orderBy) {
            console.log(`fetchCenters - orderBy: ${params.orderBy}`); // Log di debug
            queryParams.append('orderBy', params.orderBy); // Passa l'orderBy senza encodeURIComponent
          }
          if (params.name) queryParams.append('like.name', params.name);
          if (params.description) queryParams.append('like.description', params.description);
          if (params.province) queryParams.append('obj.province', params.province);
          if (params.city) queryParams.append('obj.city', params.city);
          queryParams.append('startRow', '0');
          queryParams.append('pageSize', '10');
          queryString += `?${queryParams.toString()}`;
        }
        return queryString;
      },
    }),
    fetchCentersWithManagerId: builder.query<FetchCentersResponse, FetchCentersParams>({
      query: (params) => {
        let queryString = '/centers/';
        const queryParams = new URLSearchParams();
        if (params.managerId) queryParams.append('obj.manager_id', params.managerId);
        if (params.orderBy) {
          console.log(`fetchCentersWithManagerId - orderBy: ${params.orderBy}`); // Log di debug
          queryParams.append('orderBy', params.orderBy); // Passa l'orderBy senza encodeURIComponent
        }
        if (params.name) queryParams.append('like.name', params.name);
        if (params.description) queryParams.append('like.description', params.description);
        if (params.province) queryParams.append('obj.province', params.province);
        if (params.city) queryParams.append('obj.city', params.city);
        queryParams.append('startRow', '0');
        queryParams.append('pageSize', '10');
        queryString += `?${queryParams.toString()}`;
        return queryString;
      },
    }),
    fetchCentersWithEmployeeUuid: builder.query<FetchCentersResponse, string>({
      query: (employeeUuid) => `/centers/?obj.employee_uuid=${employeeUuid}`,
    }),
    fetchEmployees: builder.query<FetchEmployeesResponse, FetchEmployeesParams>({
      query: (params) => {
        let queryString = '/employees/';
        const queryParams = new URLSearchParams();
        if (params.managerId) queryParams.append('obj.manager_id', params.managerId);
        if (params.orderBy) {
          
          queryParams.append('orderBy', params.orderBy); // Passa l'orderBy senza encodeURIComponent
        }
        if (params.first_name) queryParams.append('like.name', params.first_name);
        if (params.last_name) queryParams.append('like.description', params.last_name);
        if (params.type) queryParams.append('obj.province', params.type);
        if (params.center_uuid) queryParams.append('obj.center_uuid', params.center_uuid)
       
        queryParams.append('startRow', '0');
        queryParams.append('pageSize', '10');
        queryString += `?${queryParams.toString()}`;
        return queryString;
      },
    }),
    fetchExits: builder.query<FetchExitsResponse, FetchExitsParams>({
      query: (params) => {
        let queryString = '/exits/';
        const queryParams = new URLSearchParams();
        if (params.managerId) queryParams.append('obj.manager_id', params.managerId);
        if (params.orderBy) {
          console.log(`fetchCentersWithManagerId - orderBy: ${params.orderBy}`); // Log di debug
          queryParams.append('orderBy', params.orderBy); // Passa l'orderBy senza encodeURIComponent
        }
        if (params.name) queryParams.append('like.name', params.name);
        if (params.description) queryParams.append('like.description', params.description);
        if (params.province) queryParams.append('obj.province', params.province);
        if (params.city) queryParams.append('obj.city', params.city);
        if (params.center_uuid) queryParams.append('obj.center_uuid', params.center_uuid)
        queryParams.append('startRow', '0');
        queryParams.append('pageSize', '10');
        queryString += `?${queryParams.toString()}`;
        return queryString;
      },
    }),
    addCenter: builder.mutation<void, Omit<Center, 'uuid' | 'is_active'>>({
      query: (newCenter) => ({
        url: '/centers/',
        method: 'POST',
        body: newCenter,
      }),
    }),
    addExit: builder.mutation<void, Omit<Exit, 'uuid' | 'is_active'>>({
      query: (newCenter) => ({
        url: '/exits/',
        method: 'POST',
        body: newCenter,
      }),
    }),
    addEmployee: builder.mutation<void, Omit<Employee, 'uuid' | 'is_active'>>({
      query: (newCenter) => ({
        url: '/employees/',
        method: 'POST',
        body: newCenter,
      }),
    }),
  }),
});

// Esporta i hook generati da questi endpoint
export const {
  useFetchCentersQuery,
  useFetchCentersWithManagerIdQuery,
  useAddCenterMutation,
  useAddEmployeeMutation,
  useAddExitMutation,
  useFetchEmployeesQuery,
  useFetchExitsQuery,
} = centersApiSlice;

export interface FetchCentersResponse {
  centers: Center[];
}

export interface FetchEmployeesResponse {
  employees: Employee[];
}

export interface FetchExitsResponse {
  exits: Exit[];
}