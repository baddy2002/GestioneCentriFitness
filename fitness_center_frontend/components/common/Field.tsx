// components/Field.tsx
'use client';

import React from 'react';
import { UserRole } from './Menu'; // Assicurati di avere l'import corretto per UserRole

interface FieldProps {
  label: string;
  value: string | number | boolean;
  roles: UserRole[];
  allowedRoles: UserRole[];
}

const Field: React.FC<FieldProps> = ({ label, value, roles, allowedRoles }) => {
  const hasAccess = roles.includes('admin') || allowedRoles.includes('all') || allowedRoles.some(role => roles.includes(role));

  if (!hasAccess) return null;

  return (
    <div className="mb-4">
      <h3 className="text-lg font-semibold">{label}</h3>
      <p className="text-gray-700">{typeof value === 'boolean' ? (value ? 'Sì' : 'No') : value}</p>
    </div>
  );
};

export default Field;
