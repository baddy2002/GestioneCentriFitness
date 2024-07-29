'use client';
import React from 'react';
import { useSelector } from 'react-redux';
import { RootState } from '@/redux/store';
import Link from 'next/link';
import {Employee, Center, Exit} from '@/redux/features/centerApiSLice'
const Page: React.FC = () => {
  // Ottieni i dati e l'entità selezionata dallo stato globale
  const { centersData, employeesData, exitsData, selectedEntity } = useSelector((state: RootState) => ({
    centersData: state.centers.centerData,
    employeesData: state.employees.employeeData,
    exitsData: state.exits.exitData,
    selectedEntity: state.ui.selectedEntity, 
  }));
  console.log("State values:", { centersData, employeesData, exitsData, selectedEntity });

  // Determina i dati e il titolo basato sull'entità selezionata
  let data: any[] = [];
  let title = '';

  switch (selectedEntity) {
    case 'centers':
      data = centersData;
      title = 'Centri';
      break;
    case 'employees':
      data = employeesData;
      title = 'Dipendenti';
      break;
    case 'exits':
      data = exitsData;
      title = 'Uscite';
      break;
    default:
      data = [];
      title = 'Nessun dato';
  }
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">{title}</h1>
      {data.length > 0 ? (
        <ul>
          {data.map(item => {
            let linkHref = '';

            // Costruisci l'URL in base all'entità selezionata
            if (selectedEntity === 'centers') {
              linkHref = `/${selectedEntity}/${item.uuid}`;
            } else if (selectedEntity === 'employees') {
              linkHref = `/centers/${(item as Employee).center_uuid}/${selectedEntity}/${item.uuid}`;
            } else if (selectedEntity === 'exits') {
              linkHref = `/centers/${(item as Exit).center_uuid}/${selectedEntity}/${item.uuid}`;
            }

            return (
              <li key={item.uuid} className="border-b border-gray-400 pb-4 mb-4 flex justify-between items-center">
                <div>
                  <h2 className="text-xl font-semibold">{item.name || 'Nome non disponibile'}</h2>
                  {item.description && <p>{item.description}</p>}
                </div>
                
                <Link href={linkHref} className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600">
                  Details
                </Link>
              </li>
            );
          })}
        </ul>
      ) : (
        <p>Nessun {selectedEntity} trovato</p>
      )}
    </div>
  );
};

export default Page;