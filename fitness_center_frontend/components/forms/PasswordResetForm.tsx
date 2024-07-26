
'use client';

import { useResetPassword } from '@/hooks';
import { Form } from '@/components/forms';

export default function PasswordResetForm() {
    const {
        email, isLoading, onChange, onSubmit
      } = useResetPassword();
    
      const config = [
        {
            labelText: 'Email address',
            labelId: 'email',
            type: 'email',
            value: email,
            required: true 
        },
      ];

      return (
        <Form 
            config={config}
            isLoading={isLoading}
            btnText="Reset password"
            onChange={onChange}
            onSubmit={onSubmit}
        />
      );
}