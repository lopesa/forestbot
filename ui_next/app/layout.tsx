import Script from 'next/script';
import './globals.css';
import { Inter } from 'next/font/google';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'Forest Info Bot',
  description: 'A RAG app for exploring a large pdf about forests'
};

export default function RootLayout({
  children
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        {/* <!-- Google tag (gtag.js) --> */}
        <Script
          async
          src="https://www.googletagmanager.com/gtag/js?id=G-8YPBL37DKV"
        ></Script>
        <Script id="google-analytics">
          {`window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date()); gtag('config', 'G-8YPBL37DKV');`}
        </Script>
      </head>
      <body className={`${inter.className} dark`}>{children}</body>
    </html>
  );
}
