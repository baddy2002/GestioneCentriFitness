'use client';
import React from 'react';
import { useSelector } from 'react-redux';
import { RootState } from '@/redux/store';
import Link from 'next/link';
import { Employee, Center, Exit } from '@/redux/features/centerApiSLice';

const Page: React.FC = () => {
  // Ottieni i dati e l'entità selezionata dallo stato globale
  const {  employeesData } = useSelector((state: RootState) => ({
    employeesData: state.employees.employeeData,
  }));


  // Determina i dati e il titolo basato sull'entità selezionata
  let data: any[] = employeesData;
  let title = 'Employees';
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">{title}</h1>
      {data.length > 0 ? (
        <ul>
          {data.map(item => {
            let linkHref=`/centers/${item.center_uuid}/employee/${item.uuid}`

            return (
              <li key={item.uuid} className="border-b border-gray-400 pb-4 mb-4 flex justify-between items-center">
                <div>
                    <>
                      <h2 className="text-xl font-semibold">{`${item.first_name || 'Nome non disponibile'} ${item.last_name || 'Cognome non disponibile'}`}</h2>
                      {item.DOB && <p>{`Data di nascita: ${item.DOB}`}</p>}
                    </>
                </div>
                
                <Link href={linkHref} className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600">
                  Details
                </Link>
              </li>
            );
          })}
        </ul>
      ) : (
        <p>Nessun Employee trovato</p>
      )}
    </div>
  );
};

export default Page;
