// components/PageLayout.tsx
'use client';

import React, { useEffect, useState } from 'react';
import Menu, { MenuItem, UserRole } from './Menu';
import { useUserGroupsQuery } from "@/redux/features/authApiSlice";
import { useAppSelector } from '@/redux/hooks';

interface PageLayoutProps {
  children: React.ReactNode;
  menuItems: MenuItem[];
}

const PageLayout: React.FC<PageLayoutProps> = ({ children, menuItems }) => {
  const { data: group } = useUserGroupsQuery();
  const [userRoles, setUserRoles] = useState<UserRole[]>(['customer']);

  const user = useAppSelector(state => state.auth.user);

  useEffect(() => {
    if (group) {
      setUserRoles(group.groups);
    }
  }, [group]);


  return (
    <div className="flex h-screen">
      <Menu roles={userRoles} menuItems={menuItems} />
      {/* Main Content */}
      <main className="flex-1 bg-gray-100 p-4">
        {children}
      </main>
    </div>
  );
};

export default PageLayout;
