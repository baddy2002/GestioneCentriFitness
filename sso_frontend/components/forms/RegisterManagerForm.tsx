
'use client';

import { useManagerRegister } from "@/hooks";
import { Form } from '@/components/forms';

export default function RegisterManagerForm() {
    const {
        first_name, email, p_iva, password, re_password, isLoading, onChange, onSubmit
      } = useManagerRegister();
    
      const config = [
        {
            labelText: 'First name',
            labelId: 'first_name',
            type: 'text',
            value: first_name,
            required: true 
        },
        {
            labelText: 'Email address',
            labelId: 'email',
            type: 'email',
            value: email,
            required: true 
        },
        {
            labelText: 'P. IVA',
            labelId: 'p_iva',
            type: 'text',
            value: p_iva,
            required: true 
        },
        {
            labelText: 'Password',
            labelId: 'password',
            type: 'password',
            value: password,
            required: true 
        },
        {
            labelText: 'Confirm Password',
            labelId: 're_password',
            type: 'password',
            value: re_password,
            required: true 
        }

      ];

      return (
        <Form 
            config={config}
            isLoading={isLoading}
            btnText="Sign up"
            onChange={onChange}
            onSubmit={onSubmit}
        />
      );
}