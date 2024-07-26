'use client';

import { useEffect } from 'react';
import { useVerifyMutation, useRetrieveUserCompleteQuery } from '@/redux/features/authApiSlice';
import { setAuth, finishInitialLoad } from '@/redux/features/authSlices';
import { useAppDispatch } from '@/redux/hooks';

export default function useVerify() {
    const dispatch = useAppDispatch();
    const { data: user, refetch: fetchUserComplete } = useRetrieveUserCompleteQuery();
    const [verify] = useVerifyMutation();

    useEffect(() => {
        // Funzione per recuperare il token
        const getToken = () => {
            // Prova a ottenere il token dall'intestazione Authorization
            const authHeader = window.localStorage.getItem('authToken'); // Supponiamo che tu stia memorizzando in localStorage
            if (authHeader) {
                return authHeader;
            }

            // Prova a ottenere il token dal cookie
            const cookies = document.cookie.split('; ').reduce<Record<string, string>>((acc, cookie) => {
                const [name, value] = cookie.split('=');
                acc[name] = value;
                return acc;
            }, {});
            
            return cookies['access'] || null;
        };

        // Recupera il token
        const token = getToken();

        // Chiama la funzione verify con il token recuperato
        verify(token)
            .unwrap()
            .then(async () => {
                await fetchUserComplete();

                if (user) {
                    const loggedUser = {
                        id: user.id,
                        first_name: user.first_name,
                        last_name: user.last_name,
                        email: user.email,
                        data_iscrizione: user.data_iscrizione,
                        photo: user.photo,
                    };
                    dispatch(setAuth(loggedUser));
                } else {
                    dispatch(setAuth(null));
                }
            })
            .finally(() => {
                dispatch(finishInitialLoad());
            });
    }, [dispatch, fetchUserComplete, user, verify]);
}
