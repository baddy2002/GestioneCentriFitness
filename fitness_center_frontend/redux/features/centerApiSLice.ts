// services/centersSlices.ts

import { centerApiSlice } from '../services/centersSlices'; // Assicurati di importare il tuo apiSlice principale

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

interface FetchCentersResponse {
  centers: Center[];
}

interface FetchCentersParams {
  managerId?: string;
  orderBy?: string; // Es. 'name,-province'
  name?: string;
  description?: string;
  province?: string;
  city?: string;
}

interface Employee {
  uuid: string;
  first_name: string;
  last_name: string;
  DOB: Date;
  salary: number;
  fiscalCode: string;
  email: string;
  type: string;
  hiring_date: Date;
  end_contract_date: Date;
  attachments_uuid: string;
  center_uuid: string;
  is_active: boolean;
}

interface FetchEmployeesResponse {
  centers: Employee[];
}

interface FetchEmployeesParams {
  managerId?: string;
  orderBy?: string; // Es. 'name,-province'
  name?: string;
  description?: string;
  province?: string;
  city?: string;
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
    fetchEmployeesWithManagerId: builder.query<FetchCentersResponse, FetchCentersParams>({
      query: (params) => {
        let queryString = '/employees/';
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
    addCenter: builder.mutation<void, Omit<Center, 'uuid' | 'is_active'>>({
      query: (newCenter) => ({
        url: '/centers/',
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
  useFetchEmployeesWithManagerIdQuery,
} = centersApiSlice;
