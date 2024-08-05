'use client';
import React from 'react';
import { useSelector } from 'react-redux';
import { RootState } from '@/redux/store';
import Link from 'next/link';
import { Prenotation } from '@/redux/features/prenotationsSlice'; // Assicurati che l'interfaccia Prenotation sia esportata
import { usePathname } from 'next/navigation';

const Page: React.FC = () => {
  // Ottieni i dati delle prenotazioni e l'entità selezionata dallo stato globale
  const { prenotationsData, selectedEntity } = useSelector((state: RootState) => ({
    prenotationsData: state.prenotations.prenotationData,
    selectedEntity: state.ui.selectedEntity, // Assicurati che selectedEntity sia corretto per le prenotazioni
  }));

  console.log("prenotationsData:", prenotationsData);


  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Prenotazioni</h1>
      {prenotationsData && prenotationsData.length > 0 ? (
        <ul>
          {prenotationsData.map((item: Prenotation) => {
            // Costruisci l'URL per la pagina dei dettagli della prenotazione
            const linkHref = `/prenotations/${item.uuid}`;

            return (
              <li key={item.uuid} className="border-b border-gray-400 pb-4 mb-4 flex justify-between items-center">
                <div>
                  <h2 className="text-xl font-semibold">{item.employee_uuid || 'Descrizione non disponibile'}</h2>
                  <p>{`Totale: ${item.total || 'Totale non disponibile'}`}</p>
                  <p>{`Ore di inizio: ${item.from_hour || 'Ore di inizio non disponibili'}`}</p>
                </div>
                
                <Link href={linkHref} className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600">
                  Dettagli
                </Link>
              </li>
            );
          })}
        </ul>
      ) : (
        <p>Nessuna prenotazione trovata</p>
      )}
    </div>
  );
};

export default Page;
