'use client';
import React from 'react';
import { useSelector } from 'react-redux';
import { RootState } from '@/redux/store';
import Link from 'next/link';
import { Employee, Center, Exit } from '@/redux/features/centerApiSLice';

const Page: React.FC = () => {
  // Ottieni i dati e l'entità selezionata dallo stato globale
  const {  exitsData } = useSelector((state: RootState) => ({
    exitsData: state.exits.exitData,
  }));
  

  // Determina i dati e il titolo basato sull'entità selezionata
  let data: any[] = exitsData;
  let title = 'Employees';

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">{title}</h1>
      {data.length > 0 ? (
        <ul>
          {data.map(item => {
            let linkHref=`/centers/${item.center_uuid}/exit/${item.uuid}`

            return (
              <li key={item.uuid} className="border-b border-gray-400 pb-4 mb-4 flex justify-between items-center">
                <div>
                  <>
                      <h2 className="text-xl font-semibold">{item.description || 'Descrizione non disponibile'}</h2>
                      <p>{`Tipo: ${item.type || 'Tipo non disponibile'}`}</p>
                      <p>{`Importo: ${item.amount || 'Importo non disponibile'}`}</p>
                      <p>{`Frequenza: ${item.frequency || 'Frequenza non disponibile'} mesi`}</p>
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
