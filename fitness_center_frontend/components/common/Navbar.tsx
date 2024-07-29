'use client';

import { Disclosure, DisclosureButton, DisclosurePanel } from "@headlessui/react";
import { Bars3Icon, XMarkIcon } from "@heroicons/react/16/solid";
import { useAppSelector, useAppDispatch } from "@/redux/hooks";
import { useLogoutMutation } from "@/redux/features/authApiSlice";
import { usePathname } from "next/navigation";
import { logout as setLogout } from "@/redux/features/authSlices";
import { NavLink } from '@/components/common';
import { useEffect, useState } from 'react';

export default function Navbar() {
    const pathname = usePathname();
    const dispatch = useAppDispatch();
    const [logout] = useLogoutMutation();
    
    const { isAuthenticated: reduxIsAuthenticated, user } = useAppSelector(state => state.auth);

    // Gestione dello stato locale
    const [isAuthenticated, setIsAuthenticated] = useState(reduxIsAuthenticated);

    useEffect(() => {
        setIsAuthenticated(reduxIsAuthenticated);
    }, [reduxIsAuthenticated]);

    const handleLogout = () => {
        logout(undefined)
            .unwrap()
            .then(() => {
                dispatch(setLogout());
                // Rimuove il token dal localStorage o esegui altre operazioni necessarie
                localStorage.removeItem('authToken');
            })
            .catch(error => {
                console.error('Errore durante il logout:', error);
            });
    };

    const handleRedirect = (url: string) => {
        window.location.href = url;
    };

    const isSelected = (path: string) => pathname === path;

    const authLinks = (isMobile: boolean) => (
        <>
            <NavLink
                onClick={() => handleRedirect(`${process.env.NEXT_PUBLIC_SSO_FE}/dashboard`)}
                isMobile={isMobile}
            >
                Dashboard
            </NavLink>
            <NavLink
                onClick={handleLogout}
                isMobile={isMobile}
            >
                Logout
            </NavLink>
        </>
    );

    const guestLinks = (isMobile: boolean) => (
        <>
            <NavLink
                isSelected={isSelected('/auth/login')}
                isMobile={isMobile}
                onClick={() => handleRedirect(`${process.env.NEXT_PUBLIC_SSO_FE}/auth/login`)}
            >
                Login
            </NavLink>
            <NavLink
                isSelected={isSelected('/auth/register')}
                isMobile={isMobile}
                onClick={() => handleRedirect(`${process.env.NEXT_PUBLIC_SSO_FE}/auth/register`)}
            >
                Register
            </NavLink>
        </>
    );

    const userPhoto = user?.photo;
    const isPhotoValid = userPhoto && userPhoto !== 'null';

    return (
        <Disclosure as="nav" className="bg-gray-800">
            {({ open }) => (
                <>
                    <div className="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8">
                        <div className="relative flex h-20 items-center justify-between">
                            <div className="absolute inset-y-0 left-0 flex items-center sm:hidden">
                                <DisclosureButton className="relative inline-flex items-center justify-center rounded-md p-2 text-gray-400 hover:bg-gray-700 hover:text-white focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white">
                                    <span className="absolute -inset-0.5" />
                                    <span className="sr-only">Open main menu</span>
                                    {open ? (
                                        <XMarkIcon className="block h-6 w-6" aria-hidden="true" />
                                    ) : (
                                        <Bars3Icon className="block h-6 w-6" aria-hidden="true" />
                                    )}
                                </DisclosureButton>
                            </div>
                            <div className="flex flex-1 items-center justify-between sm:items-stretch sm:justify-start">
                                <div className="flex flex-shrink-0 items-center">
                                    <NavLink onClick={() => handleRedirect(`${process.env.NEXT_PUBLIC_SSO_FE}/`)}>
                                        <img
                                            className="h-12 w-12 rounded-full border"
                                            src="https://drive.google.com/thumbnail?id=1CJaUldQhiZAnplWB7WTFb3AeBk3uGj2F"
                                            alt="FitWorld"
                                        />
                                    </NavLink>
                                </div>
                                <div className="hidden sm:ml-6 sm:flex sm:space-x-4 sm:flex-1">
                                    {isAuthenticated ? authLinks(false) : guestLinks(false)}
                                </div>
                                <div className="flex items-center">
                                    <div
                                        className="h-12 w-12 rounded-full cursor-pointer"
                                        onClick={() => handleRedirect(`${process.env.NEXT_PUBLIC_SSO_FE}/dashboard`)}
                                    >
                                        {isAuthenticated ? (
                                            isPhotoValid ? (
                                                <img
                                                    className="h-12 w-12 rounded-full border ml-auto"
                                                    src={userPhoto}
                                                    alt="User profile"
                                                />
                                            ) : (
                                                <div className="h-12 w-12 rounded-full bg-gray-500 flex items-center justify-center text-center center ml-auto text-white text-xl font-bold">
                                                    {user?.first_name && user?.first_name !== 'None' &&
                                                    user?.last_name && user?.last_name !== 'None' ? (
                                                        <>
                                                            {user.first_name.charAt(0)}
                                                            {user.last_name.charAt(0)}
                                                        </>
                                                    ) : (
                                                        'User'
                                                    )}
                                                </div>
                                            )
                                        ) : (
                                            <div className="h-12 w-12 rounded-full bg-gray-500 flex items-center justify-center ml-auto">
                                                <svg
                                                    className="h-6 w-6 text-white"
                                                    fill="none"
                                                    stroke="currentColor"
                                                    viewBox="0 0 24 24"
                                                    xmlns="http://www.w3.org/2000/svg"
                                                >
                                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 12c2.28 0 4-1.72 4-4s-1.72-4-4-4-4 1.72-4 4 1.72 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"></path>
                                                </svg>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <DisclosurePanel className="sm:hidden">
                        <div className="space-y-1 px-2 pb-3 pt-2">
                            {isAuthenticated ? authLinks(true) : guestLinks(true)}
                        </div>
                    </DisclosurePanel>
                </>
            )}
        </Disclosure>
    );
}
