'use client';

import { useState } from 'react';
import { Spinner } from '@/components/common';

interface Config {
    type: string;
    label: string;
    value: string | File | undefined;
    key: string;  
    readOnly: boolean; 
}

interface Props {
    config: Config[];
    onSave: (data: FormData) => void; // Callback per inviare i dati aggiornati
}

export default function List({ config, onSave }: Props) {
    const [values, setValues] = useState<{ [key: string]: string }>(
        config.reduce((acc, item) => ({ ...acc, [item.key]: item.value || '' }), {})
    );

    const [file, setFile] = useState<File | null>(null); // Stato per gestire il file caricato
    
    const handleChange = (key: string, value: any) => {
        if (key === 'photo') {
            // Se il campo è una foto, aggiorna il file nel caso ci sia un file selezionato
            setFile(value);
        } else {
            setValues({ ...values, [key]: value });
        }
    };

    const handleSave = () => {
        const formData = new FormData();
        for (const key in values) {
            formData.append(key, values[key]);
        }
        // Aggiungi il file al FormData se è stato caricato
        if (file) {
            formData.append('photo', file);
        }
        onSave(formData);
    };
    const getDirectImageUrl = (url: string) => {
        console.log(url);
        return url;
    };

    return (
        <>
            <ul className="divide-y divide-gray-100">
                {config.map(({ label, key, readOnly }) => (
                    <li key={key} className="flex justify-between gap-x-6 py-5">
                        <div>
                            <p className="text-sm font-semibold leading-6 text-gray-900">
                                {label}
                            </p>
                        </div>
                        <div>
                            {key === 'photo' ? (
                                // Se il campo è "photo", mostra l'immagine corrente e l'input file
                                <div className="flex items-center space-x-4">
                                    
                                    {typeof values.photo === 'string' && values.photo !== '' && (
                                        <img
                                        
                                            src={getDirectImageUrl(values.photo)}
                                            alt="User profile"
                                            className="h-16 w-16 rounded-full border"
                                        />
                                    )}
                                    <input
                                        type="file"
                                        accept="image/*"
                                        onChange={(e) => handleChange(key, e.target.files?.[0] || null)}
                                        className="text-sm font-semibold leading-6 text-gray-900 border border-gray-300 rounded px-2"
                                    />
                                </div>
                            ) : (
                                <input
                                    type="text"
                                    value={values[key]}
                                    onChange={(e) => handleChange(key, e.target.value)}
                                    readOnly={readOnly}
                                    className={`text-sm font-semibold leading-6 text-gray-900 border border-gray-300 rounded px-2 ${readOnly ? 'bg-gray-200' : ''}`}
                                />
                            )}
                        </div>
                    </li>
                ))}
            </ul>
            <button
                onClick={handleSave}
                className="mt-4 bg-blue-500 text-white px-4 py-2 rounded"
            >
                Save
            </button>
        </>
    );
}
