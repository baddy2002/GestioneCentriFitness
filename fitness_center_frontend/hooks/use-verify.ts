'use client';

import { useEffect } from 'react';
import { useVerifyMutation, useRetrieveUserCompleteQuery } from '@/redux/features/authApiSlice';
import { setAuth, finishInitialLoad } from '@/redux/features/authSlices';
import { useAppDispatch } from '@/redux/hooks';
import { toast } from 'react-toastify';
export default function useVerify() {
    const dispatch = useAppDispatch();
    const { data: user, refetch: fetchUserComplete } = useRetrieveUserCompleteQuery();
    const [verify] = useVerifyMutation();
    
    useEffect(() => {
        
        // Chiama la funzione verify con il token recuperato
        verify()
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
            .catch((error) =>{
                console.error('Errore:', error); // Log dell'errore completo
        // Estrarre informazioni specifiche dell'errore, se disponibili
        const errorMessage = error?.data?.message || error.message || "Errore sconosciuto";
        toast.error(`Errore: ${errorMessage}`);
            })
            .finally(() => {
                dispatch(finishInitialLoad());
            });
    }, [dispatch, fetchUserComplete, user, verify]);
}
