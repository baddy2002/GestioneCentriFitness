import { useEffect, useRef } from "react";
import { useRouter, useSearchParams } from "next/navigation"
import { setAuth } from "@/redux/features/authSlices";
import { useAppDispatch } from "@/redux/hooks";
import { toast } from "react-toastify";


export default function useSocialAuth(autheticate: any, provider: string){
    
    const router = useRouter();
    const dispatch = useAppDispatch();
    const searchParams = useSearchParams();

    const effectRan = useRef(false);


    useEffect(() =>{
        
        const state = searchParams.get('state');
        const code = searchParams.get('code');

        if (state && code && !effectRan.current){
            autheticate({provider, state, code})
                .unwrap()
                .then(() =>{
                    dispatch(setAuth());
                    toast.success('Logged in');
                    router.push('/dashboard');
                })
                .catch(() =>{
                    toast.error('Failed to log in');
                    router.push('/auth/login');
                })
        }

        return () => {

            effectRan.current = true;
        }

    }, [autheticate, provider]);
}
