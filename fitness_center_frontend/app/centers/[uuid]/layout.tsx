'use client';

import { useSearchParams, usePathname, useRouter, useParams } from 'next/navigation';
import { Footer, Navbar, PageLayout } from '@/components/common';
import CustomProvider from '@/redux/provider';
import { Setup } from '@/components/utils';
import { Inter } from 'next/font/google';
import { RootState } from '@/redux/store';
import FilterModal from '@/components/common/FilterModal';
import React, { useEffect, useState, useCallback } from 'react';
import { useSelector } from 'react-redux';
import { useAppSelector, useAppDispatch } from '@/redux/hooks';
import { setCentersData, clearCentersData } from '@/redux/features/centersSlices';
import { setEmployeesData, clearEmployeesData } from '@/redux/features/employeesSlices';
import { setExitsData, clearExitsData } from '@/redux/features/exitsSlices';
import { useFetchEntities } from '@/hooks/fetchEntities';
import { setSelectedEntity } from '@/redux/features/UiSlices';
import { MenuItem } from '@/components/common/Menu';
import { useFetchCentersQuery } from '@/redux/features/centerApiSLice';
type BaseFilters = {
  orderBy: string;
};


interface EmployeeFilters extends BaseFilters {
  first_name: string;
  last_name: string;
  type: string;
  open: boolean;
}

interface ExitFilters extends BaseFilters {
  type: string;
  amount: string;
  description: string
  expiration_date: string;
  open: boolean;
}

type Filters = EmployeeFilters | ExitFilters;

type FilterField = { label: string; name: string; placeholder: string };

const filtersFields: Record<'centers' | 'employees' | 'exits', FilterField[]> = {
  centers:[
    { label: 'Order By', name: 'orderBy', placeholder: 'e.g., last_name,-first_name' },
    { label: 'First Name', name: 'first_name', placeholder: 'First Name' },
    { label: 'Last Name', name: 'last_name', placeholder: 'Last Name' },
    { label: 'Type', name: 'type', placeholder: 'Type' },
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

const inter = Inter({ subsets: ["latin"] });

export default function CenterDetailLayout({ children }: { children: React.ReactNode }) {
  const dispatch = useAppDispatch();
  const router = useRouter();
  const { uuid } = useParams();
  const { data: centersData } = useFetchCentersQuery();
  const user = useAppSelector(state => state.auth?.user);
  const managerId = user?.id || '';
  
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);

    /*<=================================REDIRECTING==============================>*/ 
  
    const searchParams = useSearchParams();
    const pathname = usePathname();
    const [isRedirecting, setIsRedirecting] = useState(false);
  
    useEffect(() => {
      const fromUrl = searchParams.get('from');
      
      if (fromUrl && !fromUrl.startsWith('/centers/')) {
        const url = new URL(window.location.href);
        url.searchParams.delete('from');
        router.replace(url.toString());
        setIsRedirecting(true);
        router.push(pathname);
      }
    }, [searchParams, pathname, router]);
  
    if (isRedirecting) {
      setIsRedirecting(false);
      router.push(pathname)
    }
   /*<=================================END REDIRECTING==============================>*/ 


  const selectedEntity = useSelector((state: RootState) => state.ui.selectedEntity);
  const [entity, setEntity] = useState<'centers' | 'employees' | 'exits'>(selectedEntity);
  const [filters, setFilters] = useState<EmployeeFilters | ExitFilters>({
    orderBy: '',
    description: '',
    open: false,
    first_name: '',
    last_name: '',
    type: '',
    amount: '',
    expiration_date: ''
  });

  const [appliedFilters, setAppliedFilters] = useState<EmployeeFilters | ExitFilters>(filters);
  const center = centersData?.centers.find(c => c.uuid === uuid);
  const getParams = () => {
    const commonParams = {
      orderBy: appliedFilters.orderBy
    };
    
    switch (entity) {
      case 'employees':
        return {
          ...commonParams,
          center_uuid: uuid,
          first_name: (appliedFilters as EmployeeFilters).first_name,
          last_name: (appliedFilters as EmployeeFilters).last_name,
          type: (appliedFilters as EmployeeFilters).type
        };
      case 'exits':
        return {
          ...commonParams,
          center_uuid: uuid,
          type: (appliedFilters as ExitFilters).type,
          amount: (appliedFilters as ExitFilters).amount,
          expiration_date: (appliedFilters as ExitFilters).expiration_date
        };
      default:
        return {};
    }
  };

  
  const { refetch, isLoading, error, data } = useFetchEntities(entity, getParams());

  const handleFilterChange = useCallback((newFilters: Partial<EmployeeFilters | ExitFilters>) => {
    setFilters(prevFilters => ({ ...prevFilters, ...newFilters }));
  }, []);

  const applyFilters = useCallback(async () => {
    await setAppliedFilters(filters); // Applicare i filtri

    // Resettare i dati esistenti prima di effettuare una nuova richiesta
    switch (entity) {
      case 'centers':
        dispatch(clearCentersData());
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
          case 'employees':
            if ('employees' in result.data) {
              dispatch(setEmployeesData(result.data.employees));
            }
            dispatch(setSelectedEntity('employees'));
            break;
          case 'exits':
            if ('exits' in result.data) {
              dispatch(setExitsData(result.data.exits));
            }
            dispatch(setSelectedEntity('exits'));
            break;
        }
      }
      if(entity === 'exits')
        router.push(`/centers/${uuid}/exit`);
      else
        router.push(`/centers/${uuid}/employee`);
    } catch (error) {
      console.error('Error fetching entities:', error);
    }
  }, [filters, refetch, dispatch, router, entity]);

  

  const menuItems: MenuItem[] = [
    { text: 'Back to Centers', href: `/centers`, requiredRole: [] }
    , 
    { text: 'Add Employee', href: `/centers/${center?.uuid}/employee/add`, requiredRole: ['manager', 'admin'] },
    { text: 'Add Exit', href: `/centers/${center?.uuid}/exit/add`, requiredRole: ['manager', 'admin'] },
    { text: 'Filters', action: () => {if(entity === 'centers') {setEntity('employees'); dispatch(setSelectedEntity('employees'))}; setIsModalOpen(true); setFilters(prev => ({ ...prev, open: true })); },
      requiredRole: ['customer', 'trainer', 'nutritionist', 'manager', 'admin']
    },
    { text: 'Center Employees', action: async () => {
      setEntity('employees');
      setIsModalOpen(false);
        try {
          const result = await refetch();
          if (result && result.data) {
            if ('employees' in result.data) {
              dispatch(setEmployeesData(result.data.employees));
            }
            dispatch(setSelectedEntity('employees'));
            router.push(`/centers/${uuid}/employee`);
          } else {
            console.log('No data received for all employees');
          }
        } catch (error) {
          console.error('Error fetching all employees:', error);
        }
      },
      requiredRole: ['admin', 'manager']
    },
    { text: 'Center Exits', action: async () => {
      setEntity('exits');
      setIsModalOpen(false);
        try {
          const result = await refetch();
          if (result && result.data) {
            if ('exits' in result.data) {
              dispatch(setExitsData(result.data.exits));
            }
            dispatch(setSelectedEntity('exits'));
            router.push(`/centers/${uuid}/exit`);
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
    <html lang="en">
      <body className={inter.className}>
        <CustomProvider>
          <Setup />
          <Navbar />
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
          <Footer />
        </CustomProvider>
      </body>
    </html>
  );
}
