'use client';
import React, { useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { PageLayout } from "@/components/common";
import { Inter } from "next/font/google";
import { useFetchCentersQuery, useFetchCentersWithManagerIdQuery, useFetchEmployeesWithManagerIdQuery } from '@/redux/features/centerApiSLice';
import { useAppSelector, useAppDispatch } from '@/redux/hooks';
import { MenuItem } from "@/components/common/Menu";
import { setCentersData, clearCentersData } from '@/redux/features/centersSlices';
import FilterModal from '@/components/common/FilterModal';
import { RequireAuth } from '@/components/utils';

interface CenterFilters {
  orderBy: string;
  name: string;
  description: string;
  province: string;
  city: string;
  open: boolean;
}

const inter = Inter({ subsets: ["latin"] });

export default function CentersLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  const dispatch = useAppDispatch();
  const router = useRouter();
  const user = useAppSelector(state => state.auth?.user);
  const managerId = user?.id || '';

  const [filters, setFilters] = useState<CenterFilters>({
    orderBy: '',
    name: '',
    description: '',
    province: '',
    city: '',
    open: false,
  });

  const [appliedFilters, setAppliedFilters] = useState<CenterFilters>(filters);

  const { refetch: refetchCenters } = useFetchCentersQuery({
    orderBy: appliedFilters.orderBy,
    name: appliedFilters.name,
    description: appliedFilters.description,
    province: appliedFilters.province,
    city: appliedFilters.city,
  });

  const { refetch: refetchMyList } = useFetchCentersWithManagerIdQuery({
    managerId,
    orderBy: appliedFilters.orderBy,
    name: appliedFilters.name,
    description: appliedFilters.description,
    province: appliedFilters.province,
    city: appliedFilters.city,
  }, { skip: !managerId });

  const { refetch: refetchMyEmployees } = useFetchEmployeesWithManagerIdQuery({
    managerId,
    orderBy: appliedFilters.orderBy,
    name: appliedFilters.name,
    description: appliedFilters.description,
    province: appliedFilters.province,
    city: appliedFilters.city,
  }, { skip: !managerId });

  const handleFilterChange = useCallback((newFilters: Partial<CenterFilters>) => {
    setFilters(prevFilters => ({ ...prevFilters, ...newFilters }));
  }, []);

  const applyFilters = useCallback(async () => {
    await setAppliedFilters(filters); // Applicare i filtri (aspettare per essere sicuri vengano applicati)

    try {
      console.log('Applying filters:', appliedFilters);

      // Resettare i dati esistenti prima di effettuare una nuova richiesta
      dispatch(clearCentersData());

      let result;
      if (managerId) {
        console.log('Fetching centers with manager ID:', managerId);
        result = await refetchMyList();
      } else {
        console.log('Fetching all centers');
        result = await refetchCenters();
        console.log(result);
      }

      if (result && result.data) {
        console.log('Fetched data:', result.data);
        dispatch(setCentersData(result.data.centers));
      } else {
        console.log('No data received');
      }
      
      router.push('/centers');
    } catch (error) {
      console.error('Error fetching centers:', error);
    }
  }, [filters, managerId, refetchCenters, refetchMyList, dispatch, router]);

  const menuItems: MenuItem[] = [
    { text: 'My List', action: async () => {
        if (managerId) {
          try {
            console.log('Fetching my list with manager ID:', managerId);
            const result = await refetchMyList();
            if (result && result.data) {
              console.log('Fetched data for my list:', result.data);
              dispatch(setCentersData(result.data.centers));
              router.push('/centers');
            } else {
              console.log('No data received for my list');
            }
          } catch (error) {
            console.error('Error fetching my list:', error);
          }
        } else {
          console.error('Manager ID is not available');
        }
      },
      requiredRole: ['trainer', 'nutritionist', 'manager', 'admin']
    },
    { text: 'All Centers', action: async () => {
        try {
          console.log('Fetching all centers');
          const result = await refetchCenters();
          if (result && result.data) {
            console.log('Fetched data for all centers:', result.data);
            dispatch(setCentersData(result.data.centers));
            router.push('/centers');
          } else {
            console.log('No data received for all centers');
          }
        } catch (error) {
          console.error('Error fetching all centers:', error);
        }
      },
      requiredRole: ['trainer', 'nutritionist', 'manager', 'admin']
    },
    { text: 'Filters', action: () => setFilters(prev => ({ ...prev, open: true })),
      requiredRole: ['customer', 'trainer', 'nutritionist', 'manager', 'admin']
    },
    { text: 'My Employees', action: async () => {
      try {
        console.log('Fetching all centers');
        const result = await refetchMyEmployees();
        if (result && result.data) {
          console.log('Fetched data for all centers:', result.data);
          dispatch(setCentersData(result.data.centers));
          router.push('/centers');
        } else {
          console.log('No data received for all centers');
        }
      } catch (error) {
        console.error('Error fetching all centers:', error);
      }
    },
    requiredRole: ['admin', 'manager']
    },
    { text: 'My Exits', action: async () => {
        router.push('/centers/exits')
    },
    requiredRole: ['admin', 'manager']
  }
  ];

  return (
    
    <div className={inter.className}>
      <PageLayout menuItems={menuItems}>
        {children}
      </PageLayout>
      <FilterModal
        isOpen={filters.open}
        onClose={() => setFilters(prev => ({ ...prev, open: false }))}
        filters={filters}
        onFilterChange={handleFilterChange}
        onApplyFilters={applyFilters}
      />
    </div>
    
  );
}
