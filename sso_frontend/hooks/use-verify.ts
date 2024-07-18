'use client';

import { useEffect } from 'react';
import { useVerifyMutation, useRetrieveUserCompleteQuery} from '@/redux/features/authApiSlice';
import { setAuth, finishInitialLoad } from '@/redux/features/authSlices';
import { useAppDispatch } from '@/redux/hooks';

export default function useVerify() {
    const dispatch = useAppDispatch();
    const {data: user,refetch: fetchUserComplete, isFetching} = useRetrieveUserCompleteQuery();

    const [verify] = useVerifyMutation();

    useEffect(() => {
        verify(undefined)
            .unwrap()
            .then(async () =>{
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
                  console.log(loggedUser);
                  // Imposta lo stato di autenticazione
                  dispatch(setAuth(loggedUser));
                }
                else
                    dispatch(setAuth(null));
            })
            .finally(()=>{
                dispatch(finishInitialLoad());
            })
    }, []);
}