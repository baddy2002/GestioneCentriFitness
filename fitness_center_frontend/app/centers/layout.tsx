'use client'

import React, { useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { PageLayout } from "@/components/common";
import { Inter } from "next/font/google";
import { useFetchCentersQuery, useFetchCentersWithManagerIdQuery } from '@/redux/features/centerApiSLice';
import { useAppSelector, useAppDispatch } from '@/redux/hooks';
import { MenuItem } from "@/components/common/Menu";
import { setCentersData } from '@/redux/features/centersSlices';
import FilterModal from '@/components/common/FilterModal';

interface Filters {
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

  const [filters, setFilters] = useState<Filters>({
    orderBy: '',
    name: '',
    description: '',
    province: '',
    city: '',
    open: false,
  });

  const { refetch: refetchCenters } = useFetchCentersQuery({
    orderBy: filters.orderBy,
    name: filters.name,
    description: filters.description,
    province: filters.province,
    city: filters.city,
  });

  const { refetch: refetchMyList } = useFetchCentersWithManagerIdQuery({
    managerId,
    orderBy: filters.orderBy,
    name: filters.name,
    description: filters.description,
    province: filters.province,
    city: filters.city,
  }, { skip: !managerId });

  const handleFilterChange = useCallback((newFilters: Partial<Filters>) => {
    setFilters(prevFilters => ({ ...prevFilters, ...newFilters }));
  }, []);

  const applyFilters = useCallback(async () => {
    try {
      let result;
      if (managerId) {
        result = await refetchMyList();
      } else {
        result = await refetchCenters();
      }

      if (result && result.data) {
        dispatch(setCentersData(result.data.centers));
      }
      router.push('/centers');
    } catch (error) {
      console.error('Error fetching centers:', error);
    }
  }, [filters, managerId, refetchCenters, refetchMyList, dispatch, router]);

  const menuItems: MenuItem[] = [
    { text: 'Add Center', href: '/centers/add', requiredRole: ['manager', 'admin'] },
    { text: 'My List', action: async () => {
        if (managerId) {
          try {
            const result = await refetchMyList();
            if (result && result.data) {
              dispatch(setCentersData(result.data.centers));
              router.push('/centers');
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
          const result = await refetchCenters();
          if (result && result.data) {
            dispatch(setCentersData(result.data.centers));
            router.push('/centers');
          }
        } catch (error) {
          console.error('Error fetching all centers:', error);
        }
      },
      requiredRole: ['trainer', 'nutritionist', 'manager', 'admin']
    },
    { text: 'Filters', action: () => setFilters(prev => ({ ...prev, open: true })),
      requiredRole: ['customer', 'trainer', 'nutritionist', 'manager', 'admin']
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
