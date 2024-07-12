import { ChangeEvent } from "react";
import Link from "next/link";

interface Props{
    labelId: string;
    type: string;
    onChange: (event: ChangeEvent<HTMLInputElement>) => void;
    value: string;
    link?: {
        linkText: string;
        linkUrl: string;
    },
    children: React.ReactNode;
    required?: boolean;
}

export default function Input({ labelId, type, children, value, link, required=false, onChange }: Props) {
    return (
        <div>
            <div className="flex justify-between align-center">
                <label htmlFor={labelId} className="block text-sm font-medium leading-6 text-gray-900">
                    {children}
                </label>
                {link && (
                    <div className="text-sm">
                        <Link className="font-semibold text-indigo-600 hover:text-indigo-500" href={link.linkUrl}>
                            {link.linkText}
                        </Link>
                    </div>
                )}
            </div>
           
            <div className="mt-2">
                <input
                id={labelId}
                name={labelId}
                type={type}
                required={required}
                className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                value={value}
                onChange={onChange}
                />
            </div>
        </div>
    );
}