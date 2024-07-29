'use client';

import { useEffect } from 'react';
import { useVerifyMutation, useRetrieveUserCompleteQuery } from '@/redux/features/authApiSlice';
import { setAuth, finishInitialLoad } from '@/redux/features/authSlices';
import { useAppDispatch } from '@/redux/hooks';
import { toast } from 'react-toastify';

interface UserComplete {
    id: string;
    email: string;
    first_name: string;
    last_name: string;
    data_iscrizione: string;
    photo: string;
    group: string;
}

export default function useVerify() {
    const dispatch = useAppDispatch();
    const { data: userCompleteData, refetch: fetchUserComplete } = useRetrieveUserCompleteQuery();
    const [verify] = useVerifyMutation();

    useEffect(() => {
        const fetchData = async () => {
            try {
                await verify().unwrap(); // Effettua la verifica
                if (userCompleteData) {
                    // Aggiorna lo stato dell'utente se i dati sono disponibili
                    dispatch(setAuth({
                        id: userCompleteData.id,
                        first_name: userCompleteData.first_name,
                        last_name: userCompleteData.last_name,
                        email: userCompleteData.email,
                        data_iscrizione: userCompleteData.data_iscrizione,
                        photo: userCompleteData.photo,
                    }));
                } else {
                    
                    dispatch(setAuth(null));
                }
            } catch (error) {
                console.error('Errore durante la verifica o il recupero delle informazioni utente:', error);
               
            } finally {
                dispatch(finishInitialLoad());
            }
        };

        fetchData();
    }, [dispatch, verify, userCompleteData]);
}
