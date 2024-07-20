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
        type: 'text',
        label: 'User id',
        value: user?.id,
        key: 'id',
        readOnly: true
      },
      {
        type: 'text',
        label: 'First name',
        value: user?.first_name,
        key: 'first_name',
        readOnly: false
      },
      {
        type: 'email',
        label: 'Email',
        value: user?.email,
        key: 'email',
        readOnly: false
      },
      {
        type: 'text',
        label: 'Last name',
        value: user?.last_name,
        key: 'last_name',
        readOnly: false
      },
      {
        type: 'text',
        label: 'Data iscrizione',
        value: user?.data_iscrizione,
        key: 'data_iscrizione',
        readOnly: true
      },
      {
        type: 'text',
        label: 'Photo',
        value: user?.photo,
        key: 'photo',
        readOnly: false
      },
      {
        type: 'text',
        label: 'Group',
        value: user?.group,
        key: 'group',
        readOnly: true
      },
    ];
    const handleSave = async (data: FormData) => {
      try {
           // Log each key-value pair in the FormData
           data.forEach((value, key) => {
            console.log(key, value);
        });
          await updateUser(data).unwrap();
          const updatedUser = {
            id: data.get('id') as string,
            first_name: data.get('first_name') as string,
            last_name: data.get('last_name') as string,
            email: data.get('email') as string,
            data_iscrizione: data.get('data_iscrizione') as string,
            photo: data.get('photo') as string,
            group: data.get('group') as string,
          };
          dispatch(setAuth(updateUser));
          toast.success('User updated successfully');
          //window.location.reload();
      } catch (error) {
          toast.error('Error updating user: ');
      }
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
  