'use client';

import { useState } from 'react';
import { Spinner } from '@/components/common';

interface Config {
    label: string;
    value: string | undefined;
    key: string;  
    readOnly: boolean; 
}

interface Props {
    config: Config[];
    onSave: (data: { [key: string]: string }) => void; // Callback per inviare i dati aggiornati
}

export default function List({ config, onSave }: Props) {
    const [values, setValues] = useState<{ [key: string]: string }>(
        config.reduce((acc, item) => ({ ...acc, [item.key]: item.value || '' }), {})
    );
    
    const handleChange = (key: string, value: string) => {
        setValues({ ...values, [key]: value });
    };

    const handleSave = () => {
        onSave(values);
        
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
                            <input
                                type="text"
                                value={values[key]}
                                onChange={(e) => handleChange(key, e.target.value)}
                                readOnly={readOnly}
                                className={`text-sm font-semibold leading-6 text-gray-900 border border-gray-300 rounded px-2 ${readOnly ? 'bg-gray-200' : ''}`}
                            />
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
