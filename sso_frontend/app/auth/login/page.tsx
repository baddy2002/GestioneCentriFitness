import Link from 'next/link'
import { LoginForm } from '@/components/forms'
import { Metadata } from 'next';
import { SocialButtons } from '@/components/common';
export const metadata = {
  title: 'FitWorld | Login',
  description: 'FitWorld login page',
};

export default function Page() {

  return (
    <div className="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
    <div className="sm:mx-auto sm:w-full sm:max-w-sm">
      <img
        className="mx-auto h-10 w-auto"
        src="https://drive.google.com/thumbnail?id=1CJaUldQhiZAnplWB7WTFb3AeBk3uGj2F"
        alt="FitWorld"
      />
      <h2 className="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">
        Login with your account
      </h2>
    </div>

    <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
      <LoginForm />
      <SocialButtons />
      <p className="mt-10 text-center text-sm text-gray-500">
            Don&apos;t have an account?{' '}
            <Link 
              href="/auth/register" 
              className="font-semibold leading-6 text-indigo-600 hover:text-indigo-500"
              >
              Register here
            </Link>
          </p>
    </div>
  </div>
  );
}
