// hooks/useFetchEntities.ts
import { FetchCentersResponse, FetchEmployeesResponse, FetchExitsResponse, useFetchCentersQuery, useFetchEmployeesQuery, useFetchExitsQuery, useFetchCentersWithManagerIdQuery } from '@/redux/features/centerApiSLice';


export function useFetchEntities(entity: string, params: any) {
    switch (entity) {
      case 'centers':
        return useFetchCentersQuery(params)
      case 'employees':
        return useFetchEmployeesQuery(params);
      case 'exits':
        return useFetchExitsQuery(params);
      default:
        throw new Error('Invalid entity type');
    }
  }
