import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'CalAI MVP',
  description: 'AI-powered calibration and diagnostics intelligence platform for automotive engineers.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
