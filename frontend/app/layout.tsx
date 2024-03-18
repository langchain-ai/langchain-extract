import "./globals.css";
import { ReactNode } from "react";
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { Sidebar } from "./components/Sidebar";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Chat LangChain",
  description: "Chatbot for LangChain",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" className="h-full">
      <head>
        <link
          rel="icon"
          href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🦜</text></svg>"
        />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>LangChain Extract</title>
      </head>
      <body className={`${inter.className} h-full`}>
        <div className="flex flex-col w-100% h-full">
          <div className="flex justify-between bg-slate-200 mb-4 p-3 items-center gap-2">
            <div className="font-semibold">🦜⛏️ LangChain Extract</div>
            <div className="text-s text-rose-800">
              <strong>Research Preview</strong>: this app is unauthenticated and
              all data can be found. Do not use with sensitive data.
            </div>
          </div>
          <div className="flex gap-3 ml-5 mr-5">
            <div className="w-1/6">
              <Sidebar />
            </div>
            <div className="m-auto w-5/6">{children}</div>
          </div>
        </div>
      </body>
    </html>
  );
}
