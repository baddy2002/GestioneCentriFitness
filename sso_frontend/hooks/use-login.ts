'use client';

import { useLoginMutation, useRetrieveUserCompleteQuery } from "@/redux/features/authApiSlice";
import { useRouter } from "next/navigation";
import { useState, ChangeEvent, FormEvent } from "react";
import { toast } from "react-toastify";
import { setAuth } from "@/redux/features/authSlices";
import { useAppDispatch } from "@/redux/hooks";


export default function useLogin() {
    const router = useRouter();
    const dispatch = useAppDispatch();
    const[login, {isLoading}] = useLoginMutation();
    const {data: user,refetch: fetchUserComplete, isFetching} = useRetrieveUserCompleteQuery();
  
    const[formData, setFormData] = useState ({
      email :'',
      password :'',
    })
  
    const {email, password} = formData;
  
    const onChange = (event: ChangeEvent<HTMLInputElement>) => {
      
      const {name, value} = event.target;
  
      setFormData({...formData, [name] : value});
    }
  
    const onSubmit = async (event: FormEvent<HTMLFormElement>) => {
      event.preventDefault();
      try{
        await login({ email, password }).unwrap();
        
        // Effettua la chiamata per ottenere i dettagli completi dell'utente
      const response = await fetchUserComplete();
      const user = response?.data;
      console.log("DEBUG: User = " + user);
      if (user) {
          const loggedUser = {
              id: user.id,
              first_name: user.first_name,
              last_name: user.last_name,
              email: user.email,
              data_iscrizione: user.data_iscrizione,
              group: user.group,
              photo: user.photo,
          };
          console.log(loggedUser);
          // Imposta lo stato di autenticazione
          dispatch(setAuth(loggedUser));

          toast.success('Logged in successfully');
          router.push('/dashboard');
      } else {
          throw new Error('User data not found');
      }
  } catch (error) {
      toast.error('Failed to log in' + error);
  }
    }
  return { email, password, isLoading, onChange, onSubmit};
}