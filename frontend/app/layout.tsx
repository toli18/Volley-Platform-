import "./globals.css";
import Navbar from "../components/Navbar";

export const metadata = {
  title: "Volley Platform",
  description: "Training platform for Bulgarian volleyball clubs",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="bg">
      <body className="min-h-screen">
        <Navbar />
        <main className="p-4">{children}</main>
      </body>
    </html>
  );
}
