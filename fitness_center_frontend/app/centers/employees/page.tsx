'use client';
import React from 'react';
import { useSelector } from 'react-redux';
import { RootState } from '@/redux/store';
import Link from 'next/link'; // Importa Link per la navigazione

const Home: React.FC = () => {
  const centersData = useSelector((state: RootState) => state.centers.data);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Centri</h1>
      {centersData.length > 0 ? (
        <ul>
          {centersData.map(center => (
            <li key={center.uuid} className="border-b border-gray-400 pb-4 mb-4 flex justify-between items-center">
              <div>
                <h2 className="text-xl font-semibold">{center.name}</h2>
                {center.description && <p>{center.description}</p>}
              </div>
              <Link href={`/centers/${center.uuid}`} className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600">
                Details
              </Link>
            </li>
          ))}
        </ul>
      ) : (
        <p>Nessun centro trovato</p>
      )}
    </div>
  );
};

export default Home;
