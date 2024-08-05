// app/exits/[uuid]/page.tsx
'use client';

import React from 'react';
import { useParams } from 'next/navigation';
import { useFetchExitsQuery } from '@/redux/features/centerApiSLice';
import Field from '@/components/common/Field';
import { UserRole } from '@/components/common/Menu'; 
import { useState, useEffect } from 'react';
import { useUserGroupsQuery } from '@/redux/features/authApiSlice';


const ExitDetails: React.FC = () => {
  const { id } = useParams();
  const { data: exitsData } = useFetchExitsQuery();
  const [userRoles, setUserRoles] = useState<UserRole[]>(['customer']);
  const { data: group } = useUserGroupsQuery();
  
  useEffect(() => {
    if (group) {
      setUserRoles(group.groups);
    }
  }, [group]);

  const exit = exitsData?.exits.find(e => e.uuid === id);

  if (!exit) {
    return <p className="p-4 text-red-500">Centro non trovato</p>;
  }

  return (
    <div className="p-4 bg-white shadow-lg rounded-lg max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-6 text-gray-800">{exit.amount}</h1>
      <Field label="Description" value={exit.description} roles={userRoles} allowedRoles={['admin', 'manager']} />
      <Field label="Type" value={exit.type} roles={userRoles} allowedRoles={['admin', 'manager']} />
      <Field label="Start date" value={exit.start_date} roles={userRoles} allowedRoles={['admin', 'manager']} />
      {exit.expiration_date != null ? <Field label="Expiration date" value={exit.expiration_date} roles={userRoles} allowedRoles={['admin', 'manager']} /> : ('')}
      <Field label="Frequency" value={exit.frequency} roles={userRoles} allowedRoles={['all']} />
      <Field label="Start date" value={exit.start_date} roles={userRoles} allowedRoles={['all']} />

    </div>
  );
};

export default ExitDetails;
