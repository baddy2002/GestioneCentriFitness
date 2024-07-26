'use client';

import { useEffect } from 'react';
import { useVerifyMutation} from '@/redux/features/authApiSlice';
import { setAuth, finishInitialLoad } from '@/redux/features/authSlices';
import { useAppDispatch } from '@/redux/hooks';

export default function useVerify() {
    const dispatch = useAppDispatch();

    const [verify] = useVerifyMutation();

    useEffect(() => {
        verify(undefined)
            .unwrap()
            .then(async () =>{
                dispatch(setAuth(null));
            })
            .finally(()=>{
                dispatch(finishInitialLoad());
            })
    }, []);
}