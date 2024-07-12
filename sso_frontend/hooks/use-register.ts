'use client';
import { useState, ChangeEvent, FormEvent } from "react";
import { useRegisterMutation } from "@/redux/features/authApiSlice";
import { useRouter } from "next/navigation";
import { toast } from "react-toastify";


export default function useRegister() {
    const router = useRouter();
    const[register, {isLoading}] = useRegisterMutation();
  
    const[formData, setFormData] = useState ({
      first_name :'',
      email :'',
      password :'',
      re_password :'',
    })
  
    const {first_name, email, password, re_password} = formData;
  
    const onChange = (event: ChangeEvent<HTMLInputElement>) => {
      
      const {name, value} = event.target;
  
      setFormData({...formData, [name] : value});
    }
  
    const onSubmit = (event: FormEvent<HTMLFormElement>) => {
      event.preventDefault();
  
      register({first_name, email, password, re_password})
        .unwrap()
        .then(()=> {
          toast.success('Please check your email to verify the account')
          router.push('/auth/login')
        })
        .catch(()=>{
          toast.error('Failed to register the account')
        })
    }
  return { first_name, email, password, re_password, isLoading, onChange, onSubmit};
}