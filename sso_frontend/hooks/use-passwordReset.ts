'use client';

import { useState, ChangeEvent, FormEvent } from "react";
import { useResetPasswordMutation } from "@/redux/features/authApiSlice";
import { toast } from "react-toastify";


export default function useResetPassword() {
    const [resetPassword, { isLoading }] = useResetPasswordMutation()
    const [email, setEmail] = useState('');
  
    const onChange = (event: ChangeEvent<HTMLInputElement>) => {
      
      const {name, value} = event.target;
  
      setEmail(event.target.value);
    }
  
    const onSubmit = (event: FormEvent<HTMLFormElement>) => {
      event.preventDefault();
  
      resetPassword({email})
        .unwrap()
        .then(()=> {
          toast.success('Please check your email to reset the password')
        })
        .catch(()=>{
          toast.error('Failed to send request')
        })
    }
  return { email, isLoading, onChange, onSubmit};
}