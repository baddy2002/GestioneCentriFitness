import { useEffect, useRef } from "react";
import { useRouter, useSearchParams } from "next/navigation"
import { setAuth } from "@/redux/features/authSlices";
import { useAppDispatch } from "@/redux/hooks";
import { toast } from "react-toastify";
import { useRetrieveUserCompleteQuery } from "@/redux/features/authApiSlice";

export default function useSocialAuth(autheticate: any, provider: string){
    
    const router = useRouter();
    const dispatch = useAppDispatch();
    const searchParams = useSearchParams();
    const { data: user, refetch: fetchUserComplete } = useRetrieveUserCompleteQuery();
    const effectRan = useRef(false);


    useEffect(() =>{
        
        const state = searchParams.get('state');
        const code = searchParams.get('code');

        if (state && code && !effectRan.current){
            autheticate({provider, state, code})
                .unwrap()
                .then( async () =>{
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
