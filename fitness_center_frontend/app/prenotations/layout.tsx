'use client';
import React, { useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { PageLayout } from "@/components/common";
import { Inter } from "next/font/google";
import { useAppSelector, useAppDispatch } from '@/redux/hooks';
import { MenuItem } from "@/components/common/Menu";
import { setPrenotationsData } from '@/redux/features/prenotationsSlice';
import FilterModal from '@/components/common/FilterModal';
import { useFetchPrenotationsQuery } from '@/redux/features/centerApiSLice';

const inter = Inter({ subsets: ["latin"] });

type Filters = {
  orderBy: string;
  description: string;
  open: boolean;
  first_name: string;
  last_name: string;
  type: string;
  amount: string;
  from_date: string;
};

type FilterField = { label: string; name: keyof Filters; placeholder: string };

export default function Layout({ children }: { children: React.ReactNode }) {
  const dispatch = useAppDispatch();
  const router = useRouter();
  const user = useAppSelector(state => state.auth?.user);
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);

  const [filters, setFilters] = useState<Filters>({
    orderBy: '',
    description: '',
    open: false,
    first_name: '',
    last_name: '',
    type: '',
    amount: '',
    from_date: ''
  });

  const handleFilterChange = useCallback((newFilters: Partial<Filters>) => {
    setFilters(prevFilters => ({ ...prevFilters, ...newFilters }));
  }, []);

  const filterFields: FilterField[] = [
    { label: 'Order By', name: 'orderBy', placeholder: 'e.g., name,-province' },
    { label: 'Amount', name: 'amount', placeholder: 'Enter amount' },
    { label: 'Date', name: 'from_date', placeholder: 'Date' }
  ];

  const { refetch, isLoading, error, data } = useFetchPrenotationsQuery();

  const menuItems: MenuItem[] = [
    { text: 'Add Prenotation', href: '/prenotations/add', requiredRole: ['manager', 'admin'] },
    { text: 'My Prenotations', action: async () => {
      setIsModalOpen(false);
        try {
          const result = await refetch();
          if (result && result.data) {
            if ('prenotations' in result.data) {
              dispatch(setPrenotationsData(result.data.prenotations));
            }
            router.push('/prenotations');
          } else {
            console.log('No data received for all prenotations');
          }
        } catch (error) {
          console.error('Error fetching all prenotations:', error);
        }
      },
      requiredRole: ['trainer', 'nutritionist', 'manager', 'admin']
    },    { text: 'Filters', action: () => {setIsModalOpen(true); setFilters(prev => ({ ...prev, open: true })); },
    requiredRole: ['customer', 'trainer', 'nutritionist', 'manager', 'admin']
  },
    { text: 'Centers', action: async () => {
      router.push('/centers');
      },
      requiredRole: ['trainer', 'nutritionist', 'manager', 'admin']
    },    
  ];

  const applyFilters = () => {
    // Funzionalità per applicare i filtri e aggiornare i dati.
    console.log('Filters applied:', filters);
    // Potresti voler chiamare un'azione Redux o aggiornare lo stato per applicare i filtri.
  };
  

  return (
    <PageLayout menuItems={menuItems}>
<FilterModal
  isOpen={isModalOpen}
  onClose={() => setIsModalOpen(false)}
  filters={filters}
  onFilterChange={handleFilterChange}
  onApplyFilters={applyFilters}
  filterFields={filterFields}
/>
      {children}
    </PageLayout>
  );
}
