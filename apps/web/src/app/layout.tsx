import type { Metadata } from "next";
import { Inter, Fira_Code } from "next/font/google";
import { ViewTransitions } from "next-view-transitions";
import "./globals.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

const firaCode = Fira_Code({
  variable: "--font-fira-code",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Finance Skills",
  description:
    "Financial analysis skills for AI agents — earnings, market data, risk monitoring, and more.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <ViewTransitions>
      <html lang="en" className={`${inter.variable} ${firaCode.variable} antialiased`} style={{ colorScheme: "dark" }}>
        <body className="font-sans min-h-screen">{children}</body>
      </html>
    </ViewTransitions>
  );
}
