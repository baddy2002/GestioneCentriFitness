'use client';

import { useEffect, useState } from 'react';
import { useSearchParams, usePathname, useRouter } from 'next/navigation';
import { Footer, Navbar, PageLayout } from '@/components/common';
import CustomProvider from '@/redux/provider';
import { Setup } from '@/components/utils';
import { Inter } from 'next/font/google';

const inter = Inter({ subsets: ["latin"] });

export default function CenterDetailLayout({ children }: { children: React.ReactNode }) {
  const searchParams = useSearchParams();
  const pathname = usePathname();
  const router = useRouter();
  const [isRedirecting, setIsRedirecting] = useState(false);

  useEffect(() => {
    const fromUrl = searchParams.get('from');
    
    if (fromUrl && !fromUrl.startsWith('/centers/')) {
      setIsRedirecting(true);
      router.push(pathname);
    }
  }, [searchParams, pathname, router]);

  if (isRedirecting) {
    router.push(pathname)
  }

  const menuItems = [
    { text: 'Back to Centers', href: `/centers?from=${encodeURIComponent(pathname)}`, requiredRole: [] },
    
  ];

  return (
    <html lang="en">
      <body className={inter.className}>
        <CustomProvider>
          <Setup />
          <Navbar />
          <PageLayout menuItems={menuItems}>
          {children}
          </PageLayout>
          <Footer />
        </CustomProvider>
      </body>
    </html>
  );
}
