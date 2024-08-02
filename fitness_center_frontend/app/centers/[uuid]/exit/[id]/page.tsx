// app/centers/[uuid]/page.tsx
'use client';

import React from 'react';
import { useParams } from 'next/navigation';
import { useFetchExitsQuery } from '@/redux/features/centerApiSLice';
import Field from '@/components/common/Field';
import { UserRole } from '@/components/common/Menu'; 
import { useState, useEffect } from 'react';
import { useUserGroupsQuery } from '@/redux/features/authApiSlice';


const CenterDetails: React.FC = () => {
  const { id } = useParams();
  const { data: exitsData } = useFetchExitsQuery();
  const [userRoles, setUserRoles] = useState<UserRole[]>(['customer']);
  const { data: group } = useUserGroupsQuery();
  
  useEffect(() => {
    if (group) {
      setUserRoles(group.groups);
    }
  }, [group]);

  const exit = exitsData?.centers.find(c => c.uuid === uuid);

  if (!center) {
    return <p className="p-4 text-red-500">Centro non trovato</p>;
  }

  return (
    <div className="p-4 bg-white shadow-lg rounded-lg max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-6 text-gray-800">{center.name}</h1>
      <Field label="Descrizione" value={center.description} roles={userRoles} allowedRoles={['admin', 'manager']} />
      <Field label="Manager ID" value={center.manager_id} roles={userRoles} allowedRoles={['admin']} />
      <Field label="Provincia" value={center.province} roles={userRoles} allowedRoles={['all']} />
      <Field label="Città" value={center.city} roles={userRoles} allowedRoles={['all']} />
      <Field label="Via" value={center.street} roles={userRoles} allowedRoles={['all']} />
      <Field label="Numero Civico" value={center.house_number} roles={userRoles} allowedRoles={['all']} />
      <Field label="Attivo" value={center.is_active} roles={userRoles} allowedRoles={['admin']} />
    </div>
  );
};

export default CenterDetails;
