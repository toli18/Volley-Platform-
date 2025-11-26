"use client";

import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="bg-white shadow py-4 px-6 flex items-center justify-between">
      <Link href="/" className="font-bold text-lg">Volley Platform</Link>

      <div className="space-x-4">
        <Link href="/dashboard" className="hover:underline">Dashboard</Link>
        <Link href="/login" className="hover:underline">Вход</Link>
      </div>
    </nav>
  );
}
