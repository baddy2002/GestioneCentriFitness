'use client';
import React, { useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { PageLayout } from "@/components/common";
import { Inter } from "next/font/google";
import { useAppSelector, useAppDispatch } from '@/redux/hooks';
import { MenuItem } from "@/components/common/Menu";
import { setCentersData, clearCentersData } from '@/redux/features/centersSlices';
import { setEmployeesData, clearEmployeesData } from '@/redux/features/employeesSlices';
import { setExitsData, clearExitsData } from '@/redux/features/exitsSlices';
import FilterModal from '@/components/common/FilterModal';
import { useFetchEntities } from '@/hooks/fetchEntities';
import { setSelectedEntity } from '@/redux/features/UiSlices';

const inter = Inter({ subsets: ["latin"] });

type BaseFilters = {
  orderBy: string;
};

interface CenterFilters extends BaseFilters {
  name: string;
  description: string;
  province: string;
  city: string;
  open: boolean;
}

interface EmployeeFilters extends BaseFilters {
  first_name: string;
  last_name: string;
  type: string;
  open: boolean;
}

interface ExitFilters extends BaseFilters {
  type: string;
  amount: string;
  expiration_date: string;
  open: boolean;
}

type Filters = CenterFilters | EmployeeFilters | ExitFilters;

type FilterField = { label: string; name: string; placeholder: string };

const filtersFields: Record<'centers' | 'employees' | 'exits', FilterField[]> = {
  centers: [
    { label: 'Order By', name: 'orderBy', placeholder: 'e.g., name,-province' },
    { label: 'Name', name: 'name', placeholder: 'Name' },
    { label: 'Description', name: 'description', placeholder: 'Description' },
    { label: 'Province', name: 'province', placeholder: 'Province' },
    { label: 'City', name: 'city', placeholder: 'City' },
  ],
  employees: [
    { label: 'Order By', name: 'orderBy', placeholder: 'e.g., last_name,-first_name' },
    { label: 'First Name', name: 'first_name', placeholder: 'First Name' },
    { label: 'Last Name', name: 'last_name', placeholder: 'Last Name' },
    { label: 'Type', name: 'type', placeholder: 'Type' },
  ],
  exits: [
    { label: 'Order By', name: 'orderBy', placeholder: 'e.g., amount,-expiration_date' },
    { label: 'Type', name: 'type', placeholder: 'Type' },
    { label: 'Amount', name: 'amount', placeholder: 'Amount' },
    { label: 'Expiration Date', name: 'expiration_date', placeholder: 'Expiration Date' },
  ],
};

export default function Layout({ children }: { children: React.ReactNode }) {
  const dispatch = useAppDispatch();
  const router = useRouter();
  const user = useAppSelector(state => state.auth?.user);
  const managerId = user?.id || '';
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);


  const [entity, setEntity] = useState<'centers' | 'employees' | 'exits'>('centers');
  const [filters, setFilters] = useState<CenterFilters | EmployeeFilters | ExitFilters>({
    orderBy: '',
    name: '',
    description: '',
    province: '',
    city: '',
    open: false,
    first_name: '',
    last_name: '',
    type: '',
    amount: '',
    expiration_date: ''
  });

  const [appliedFilters, setAppliedFilters] = useState<CenterFilters | EmployeeFilters | ExitFilters>(filters);
  const [isMyList, setIsMyList] = useState<boolean>(false);

  const getParams = () => {
    const commonParams = {
      orderBy: appliedFilters.orderBy
    };

    switch (entity) {
      case 'centers':
        return {
          ...commonParams,
          name: (appliedFilters as CenterFilters).name,
          description: (appliedFilters as CenterFilters).description,
          province: (appliedFilters as CenterFilters).province,
          city: (appliedFilters as CenterFilters).city,
          ...(isMyList && { managerId })
        };
      case 'employees':
        return {
          ...commonParams,
          managerId,
          first_name: (appliedFilters as EmployeeFilters).first_name,
          last_name: (appliedFilters as EmployeeFilters).last_name,
          type: (appliedFilters as EmployeeFilters).type
        };
      case 'exits':
        return {
          ...commonParams,
          managerId,
          type: (appliedFilters as ExitFilters).type,
          amount: (appliedFilters as ExitFilters).amount,
          expiration_date: (appliedFilters as ExitFilters).expiration_date
        };
      default:
        return {};
    }
  };

  const { refetch, isLoading, error, data } = useFetchEntities(entity, getParams());

  const handleFilterChange = useCallback((newFilters: Partial<CenterFilters | EmployeeFilters | ExitFilters>) => {
    setFilters(prevFilters => ({ ...prevFilters, ...newFilters }));
  }, []);

  const applyFilters = useCallback(async () => {
    await setAppliedFilters(filters); // Applicare i filtri

    // Resettare i dati esistenti prima di effettuare una nuova richiesta
    switch (entity) {
      case 'centers':
        dispatch(clearCentersData());
        break;
      case 'employees':
        dispatch(clearEmployeesData());
        break;
      case 'exits':
        dispatch(clearExitsData());
        break;
    }

    try {
      const result = await refetch(); // Usa il refetch con i parametri definiti in getParams
      if (result && result.data) {
        switch (entity) {
          case 'centers':
            if ('centers' in result.data) {
              dispatch(setCentersData(result.data.centers));
            }
            break;
          case 'employees':
            if ('employees' in result.data) {
              dispatch(setEmployeesData(result.data.employees));
            }
            break;
          case 'exits':
            if ('exits' in result.data) {
              dispatch(setExitsData(result.data.exits));
            }
            break;
        }
      }
      
      router.push('/centers');
    } catch (error) {
      console.error('Error fetching entities:', error);
    }
  }, [filters, refetch, dispatch, router, entity]);

  const menuItems: MenuItem[] = [
    { text: 'Add Center', href: '/centers/add', requiredRole: ['manager', 'admin'] },
    { text: 'My List', action: async () => {
        await setEntity('centers');
        setIsModalOpen(false);
        await setIsMyList(true);
        if (managerId) {
          try {
            const result = await refetch();
            if (result && result.data) {
              if ('centers' in result.data) {
                dispatch(setCentersData(result.data.centers));
              }
              dispatch(setSelectedEntity('centers'));
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
      await setEntity('centers');
      setIsModalOpen(false);
        await setIsMyList(false);
        try {
          const result = await refetch();
          if (result && result.data) {
            if ('centers' in result.data) {
              dispatch(setCentersData(result.data.centers));
            }
            dispatch(setSelectedEntity('centers'));
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
    { text: 'Filters', action: () => {setIsModalOpen(true); setFilters(prev => ({ ...prev, open: true })); },
      requiredRole: ['customer', 'trainer', 'nutritionist', 'manager', 'admin']
    },
    { text: 'My Employees', action: async () => {
      await setEntity('employees');
      setIsModalOpen(false);
        try {
          const result = await refetch();
          if (result && result.data) {
            if ('employees' in result.data) {
              dispatch(setEmployeesData(result.data.employees));
            }
            dispatch(setSelectedEntity('employees'));
            router.push('/centers');
          } else {
            console.log('No data received for all employees');
          }
        } catch (error) {
          console.error('Error fetching all employees:', error);
        }
      },
      requiredRole: ['admin', 'manager']
    },
    { text: 'My Exits', action: async () => {
      await setEntity('exits');
      setIsModalOpen(false);
        try {
          const result = await refetch();
          if (result && result.data) {
            if ('exits' in result.data) {
              dispatch(setExitsData(result.data.exits));
            }
            dispatch(setSelectedEntity('exits'));
            router.push('/centers');
          } else {
            console.log('No data received for all exits');
          }
        } catch (error) {
          console.error('Error fetching all exits:', error);
        }
      },
      requiredRole: ['admin', 'manager']
    }
  ];

  return (
    <PageLayout menuItems={menuItems}>
      <FilterModal
        isOpen={isModalOpen} 
        onClose={() => setIsModalOpen(false)}
        filters={filters}
        onFilterChange={handleFilterChange}
        onApplyFilters={applyFilters}
        filterFields={filtersFields[entity]}
      />
      {children}
    </PageLayout>
  );
}
