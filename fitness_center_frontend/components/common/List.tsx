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


    return (
            <ul className="divide-y divide-gray-100">
                {config.map(({ label, key, readOnly }) => (
                    <li key={key} className="flex justify-between gap-x-6 py-5">
                        <div>
                            <p className="text-sm font-semibold leading-6 text-gray-900">
                                {label}
                            </p>
                        </div>
                        <div>
                               
                                <div className="flex items-center space-x-4">
                                    
                                </div>
                           
                        </div>
                    </li>
                ))}
            </ul>
    );
}
