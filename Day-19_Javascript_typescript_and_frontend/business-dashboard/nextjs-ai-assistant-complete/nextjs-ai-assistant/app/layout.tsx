import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = { title: "Enterprise AI Assistant", description: "FDE training AI assistant" };
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="en"><body><header><strong>Enterprise AI Assistant</strong><nav><a href="/">Home</a><a href="/chat">AI Assistant</a><a href="/incidents">Incidents</a><a href="/logout">Logout</a></nav></header>{children}</body></html>}
