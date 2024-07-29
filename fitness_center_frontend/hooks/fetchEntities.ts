// hooks/useFetchEntities.ts
import { FetchCentersResponse, FetchEmployeesResponse, FetchExitsResponse, useFetchCentersQuery, useFetchEmployeesWithManagerIdQuery, useFetchExitsWithManagerIdQuery, useFetchCentersWithManagerIdQuery } from '@/redux/features/centerApiSLice';


export function useFetchEntities(entity: string, params: any) {
    switch (entity) {
      case 'centers':
        console.log("manager:"+params.managerId)
        return useFetchCentersQuery(params)
      case 'employees':
        return useFetchEmployeesWithManagerIdQuery(params);
      case 'exits':
        return useFetchExitsWithManagerIdQuery(params);
      default:
        throw new Error('Invalid entity type');
    }
  }
