import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
    title: "Enterprise AI Assistant",
    description:
        "AI assistant for data engineering incident investigation"
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en">
            <body>
                <header>
                    <strong>
                        Enterprise AI Assistant
                    </strong>
                </header>

                {children}
            </body>
        </html>
    );
}