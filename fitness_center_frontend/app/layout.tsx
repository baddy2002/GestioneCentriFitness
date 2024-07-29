import "@/styles/globals.css";
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { Navbar, Footer } from "@/components/common";
import { Setup } from "@/components/utils";
import CustomProvider from "@/redux/provider";


const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "FitWorld",
  description: "Prenota visite e lezioni da personal trainer e nutrizionisti registrati",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
     
      <body className={inter.className}>
 
        <CustomProvider>
        <Setup />
          <Navbar />
            {children}
          <Footer />
        </CustomProvider>
      </body>

    </html>
  );
}