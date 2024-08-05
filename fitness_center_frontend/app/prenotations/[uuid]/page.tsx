'use client';
import React from 'react';
import { useParams } from 'next/navigation';
import { useSelector } from 'react-redux';
import { RootState } from '@/redux/store';
import { Prenotation } from '@/redux/features/centerApiSLice';
import { usePathname } from 'next/navigation';

// Questo componente assume che i dati siano disponibili nel Redux store
const DetailPage: React.FC = () => {
  const pathname = usePathname();
  const { uuid } = useParams();

  // Ottieni i dati delle prenotazioni dallo stato globale
  const { prenotationsData } = useSelector((state: RootState) => ({
    prenotationsData: state.prenotations.prenotationData,
  }));

  // Trova la prenotazione con l'UUID specificato
  const prenotation = prenotationsData.find((item: Prenotation) => item.uuid === uuid);

  if (!prenotation) {
    return <p>Prenotazione non trovata</p>;
  }

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Dettagli Prenotazione</h1>
      <div className="border border-gray-300 p-4 rounded">
        <p><strong>ID:</strong> {prenotation.uuid}</p>
        <p><strong>Employee:</strong> {prenotation.employee_uuid || 'N/A'}</p>
        <p><strong>Totale:</strong> {prenotation.total || 'N/A'}</p>
        <p><strong>Ore di inizio:</strong> {prenotation.from_hour || 'N/A'}</p>
        <p><strong>Ore di fine:</strong> {prenotation.to_hour || 'N/A'}</p>
        <p><strong>Tipo:</strong> {prenotation.type || 'N/A'}</p>
        {/* Aggiungi altri dettagli se necessari */}
      </div>
    </div>
  );
};

export default DetailPage;
