'use client';

import { ImGoogle, ImFacebook } from "react-icons/im";
import { SocialButton } from "."
import { continueWithFacebook, continueWithGoogle } from "@/utils";

interface Props{
    provider: 'google' | 'facebook';
    children: React.ReactNode;
    [rest: string]: any;
}

export default function SocialButtons() {
    

    return (
        <div className="flex justify-between items-center gap-2 mt-5">
            <SocialButton provider="google" onClick={continueWithGoogle}>
                <ImGoogle className="mr-3"/> Google
            </SocialButton>
            <SocialButton provider="facebook" onClick={continueWithFacebook}>
                <ImFacebook className="mr-3"/> Facebook
            </SocialButton>
        </div>
    );
}