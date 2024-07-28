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
    const [values, setValues] = useState<{ [key: string]: string | File | undefined }>(
        config.reduce((acc, item) => ({ ...acc, [item.key]: item.value }), {})
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
            if (values[key] !== undefined) {
                formData.append(key, values[key] as string | Blob);
            }
        }
        // Aggiungi il file al FormData se è stato caricato
        if (file) {
            formData.append('photo', file);
        }
        onSave(formData);
    };

    const handleRemovePhoto = () => {
        setFile(null);
        setValues({ ...values, photo: undefined }); // Rimuovi la foto dai valori
    };

    return (
        <ul className="divide-y divide-gray-100">
            {config.map(({ label, key, readOnly, type }) => (
                <li key={key} className="flex justify-between gap-x-6 py-5">
                    <div>
                        <p className="text-sm font-semibold leading-6 text-gray-900">
                            {label}
                        </p>
                    </div>
                    <div>
                        <div className="flex items-center space-x-4">
                            {type === 'photo' ? (
                                <>
                                    {file || values[key] ? (
                                        <>
                                            <img
                                                className="h-12 w-12 rounded-full border"
                                                src={URL.createObjectURL(file || values[key] as File)}
                                                alt={label}
                                            />
                                            <button
                                                type="button"
                                                onClick={handleRemovePhoto}
                                                className="ml-4 text-red-500"
                                            >
                                                Remove
                                            </button>
                                        </>
                                    ) : (
                                        <p>No photo</p>
                                    )}
                                </>
                            ) : (
                                <input
                                    type={type}
                                    value={values[key] as string || ''}
                                    onChange={(e) => handleChange(key, e.target.value)}
                                    readOnly={readOnly}
                                    className="border px-2 py-1 rounded"
                                />
                            )}
                        </div>
                    </div>
                </li>
            ))}
            <button onClick={handleSave} className="mt-4 bg-blue-500 text-white px-4 py-2 rounded">
                Save
            </button>
        </ul>
    );
}
