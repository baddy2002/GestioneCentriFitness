// app/employees/[uuid]/page.tsx
'use client';

import React from 'react';
import { useParams } from 'next/navigation';
import { useFetchEmployeesQuery } from '@/redux/features/centerApiSLice';
import Field from '@/components/common/Field';
import { UserRole } from '@/components/common/Menu'; 
import { useState, useEffect } from 'react';
import { useUserGroupsQuery } from '@/redux/features/authApiSlice';


const EmployeeDetails: React.FC = () => {
  const { uid } = useParams();
  const { data: employeesData } = useFetchEmployeesQuery();
  const [userRoles, setUserRoles] = useState<UserRole[]>(['customer']);
  const { data: group } = useUserGroupsQuery();
  
  useEffect(() => {
    if (group) {
      setUserRoles(group.groups);
    }
  }, [group]);

  const employee = employeesData?.employees.find(e => e.uuid === uid);

  if (!employee) {
    return <p className="p-4 text-red-500">Centro non trovato</p>;
  }

  return (
    <div className="p-4 bg-white shadow-lg rounded-lg max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-6 text-gray-800">{employee.first_name + " "+ employee.last_name}</h1>
      <Field label="Email" value={employee.email} roles={userRoles} allowedRoles={['admin', 'manager']} />
      <Field label="Type" value={employee.type} roles={userRoles} allowedRoles={['admin', 'manager']} />
      <Field label="Fiscal code" value={employee.fiscalCode} roles={userRoles} allowedRoles={['admin', 'manager']} />
      {employee.end_contract_date != null ? <Field label="End contract date" value={employee.end_contract_date} roles={userRoles} allowedRoles={['admin', 'manager']} /> : ('')}
      <Field label="Salary" value={employee.salary} roles={userRoles} allowedRoles={['all']} />
      <Field label="Hiring date" value={employee.hiring_date} roles={userRoles} allowedRoles={['all']} />
    </div>
  );
};

export default EmployeeDetails;
