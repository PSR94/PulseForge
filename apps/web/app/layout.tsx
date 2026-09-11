import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "PulseForge — Real-Time AI Event Intelligence",
  description: "Evidence-linked temporal intelligence for a changing world.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
