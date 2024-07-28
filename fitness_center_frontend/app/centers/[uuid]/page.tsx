// app/centers/[uuid]/page.tsx
'use client';

import React from 'react';
import { useParams } from 'next/navigation'; // Usa useParams per ottenere i parametri della rotta
import { useFetchCentersQuery } from '@/redux/features/centerApiSLice'; // Assicurati che il nome sia corretto

const CenterDetails: React.FC = () => {
  const { uuid } = useParams(); // Recupera il parametro uuid dalla rotta
  const { data: centersData } = useFetchCentersQuery(); // Ottieni i dati dei centri

  // Trova il centro con l'UUID corrispondente
  const center = centersData?.centers.find(c => c.uuid === uuid);

  if (!center) {
    return <p>Centro non trovato</p>;
  }
  

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">{center.name}</h1>
      <p><strong>Descrizione:</strong> {center.description}</p>
      <p><strong>Manager ID:</strong> {center.manager_id}</p>
      <p><strong>Provincia:</strong> {center.province}</p>
      <p><strong>Città:</strong> {center.city}</p>
      <p><strong>Via:</strong> {center.street}</p>
      <p><strong>Numero Civico:</strong> {center.house_number}</p>
      <p><strong>Attivo:</strong> {center.is_active ? 'Sì' : 'No'}</p>
    </div>
  );
};

export default CenterDetails;
