import { Metadata } from 'next';
import Link from 'next/link';

export const metadata = {
  title: 'FitWorld | Home',
  description: 'FitWorld Home page',
};

    const handleRedirect = (url: string) => {
        window.location.href = url;
    };

export default function Page() {
  return (
    <main className="bg-white">
    
      <div className="relative isolate px-6 pt-14 lg:px-8">
        <div className="mx-auto max-w-2xl py-32 sm:py-48 lg:py-56">
          <div className="text-center">
            <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
              FitWorld, the world of fitness, the fitness for everyone
            </h1>
            <p className="mt-6 text-lg leading-8 text-gray-600">
                Welcome, here you can find the best professionals to help you create the best version of you.<br></br>
                Enter our world to discover how comfortable it is to train
            </p>
            <div className="mt-10 flex items-center justify-center gap-x-6">
              <Link
                 href={`${process.env.NEXT_PUBLIC_CENTERHANDLING_FE}/centers`}
                className="rounded-md bg-indigo-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
              >
              
                Get started
              </Link>
            </div>
          </div>
        </div>
      </div>
  </main>
  );
}
