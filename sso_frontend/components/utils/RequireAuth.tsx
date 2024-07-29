'use client';

import { redirect } from "next/navigation";
import { useAppSelector } from "@/redux/hooks";
import { Spinner } from "../common";


interface Props {
    children: React.ReactNode;
}

export default function RequireAuth({children}: Props){


    const {isLoading, isAuthenticated} = useAppSelector(state => state.auth);

    if (isLoading){
        return (
            <div className="flex justify-center my-8">
                <Spinner lg />
            </div>
        )

    }
    console.log("the user is authenticated: " + !isAuthenticated)
    if (!isAuthenticated){
        redirect(`${process.env.NEXT_PUBLIC_SSO_FE}/auth/login`);

    }

    return <>
        {children}
    </>
}