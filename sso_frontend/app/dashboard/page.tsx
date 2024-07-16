'use client';

import { List, Spinner } from '@/components/common';
import { useModifyUserCompleteMutation, useRetrieveUserCompleteQuery } from '@/redux/features/authApiSlice';
import { setAuth } from '@/redux/features/authSlices';
import { useAppDispatch } from '@/redux/hooks';
import { toast } from 'react-toastify';


export default function Page() {
    const {data: user, isLoading, isFetching} = useRetrieveUserCompleteQuery();
    const [updateUser] = useModifyUserCompleteMutation();
    const dispatch = useAppDispatch();
    
    const config = [
      {
        label: 'User id',
        value: user?.id,
        key: 'id',
        readOnly: true
      },
      {
        label: 'First name',
        value: user?.first_name,
        key: 'first_name',
        readOnly: false
      },
      {
        label: 'Email',
        value: user?.email,
        key: 'email',
        readOnly: false
      },
      {
        label: 'Last name',
        value: user?.last_name,
        key: 'last_name',
        readOnly: false
      },
      {
        label: 'Data iscrizione',
        value: user?.data_iscrizione,
        key: 'data_iscrizione',
        readOnly: true
      },
      {
        label: 'Photo',
        value: user?.photo,
        key: 'photo',
        readOnly: false
      },
    ];

    const handleSave = async (data: { [key: string]: string }) => {
      
      const { id, email, first_name, last_name, data_iscrizione, photo } = data;
      console.log( { id ,email, first_name, last_name, data_iscrizione, photo });
      await updateUser({ id, email, first_name, last_name, data_iscrizione, photo })
      .unwrap()
      .then(()=> {
        dispatch(setAuth());
        toast.success('User updated succesfully');
      })
      .catch((error)=>{
        toast.error('Error updating user: ');
      })
      
    };

  if (isLoading || isFetching) {
      return (
          <div className='flex justify-center my-8'>
              <Spinner lg />
          </div>
      );
  }

    return (
      <>
        <header className="bg-white shodow">
            <div className="max-auth max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
                <h1 className="text-3xl font-bold tracking-tight text-gray-900">
                  Dashboard
                </h1>
            </div>
        </header>
        <main className="mx-auto max-w-7xl py-6 my-8 sm:px-6 lg:px-8">
            <List config={config} onSave={handleSave}/>
        </main>
      </>

    );
  }
  