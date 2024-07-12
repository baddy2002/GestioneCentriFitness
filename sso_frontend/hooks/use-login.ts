'use client';

import { useLoginMutation } from "@/redux/features/authApiSlice";
import { useRouter } from "next/navigation";
import { useState, ChangeEvent, FormEvent } from "react";
import { toast } from "react-toastify";
import { setAuth } from "@/redux/features/authSlices";
import { useAppDispatch } from "@/redux/hooks";


export default function useLogin() {
    const router = useRouter();
    const dispatch = useAppDispatch();
    const[login, {isLoading}] = useLoginMutation();
  
    const[formData, setFormData] = useState ({
      email :'',
      password :'',
    })
  
    const {email, password} = formData;
  
    const onChange = (event: ChangeEvent<HTMLInputElement>) => {
      
      const {name, value} = event.target;
  
      setFormData({...formData, [name] : value});
    }
  
    const onSubmit = (event: FormEvent<HTMLFormElement>) => {
      event.preventDefault();
  
      login({email, password})
        .unwrap()
        .then(()=> {
          dispatch(setAuth());
          toast.success('Logged in succesfully');
          router.push('/dashboard');
        })
        .catch(()=>{
          toast.error('Failed to Log in');
        })
    }
  return { email, password, isLoading, onChange, onSubmit};
}