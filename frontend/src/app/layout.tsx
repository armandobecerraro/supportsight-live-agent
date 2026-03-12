import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'SupportSight Live',
  description: 'Multimodal incident support agent powered by Gemini Live API',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-gray-950 text-gray-100 min-h-screen font-sans antialiased">
        {children}
      </body>
    </html>
  );
}
