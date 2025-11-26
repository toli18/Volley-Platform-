"use client";

import { useState } from "react";
import { login } from "../../../lib/api";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  async function submit(e: any) {
    e.preventDefault();
    await login(email, password);
  }

  return (
    <div className="max-w-md mx-auto mt-16 bg-white p-6 shadow rounded">
      <h1 className="text-2xl font-bold mb-4">Вход</h1>
      <form onSubmit={submit} className="space-y-4">
        <input
          type="email"
          placeholder="Имейл"
          onChange={(e) => setEmail(e.target.value)}
          className="border w-full p-2"
        />
        <input
          type="password"
          placeholder="Парола"
          onChange={(e) => setPassword(e.target.value)}
          className="border w-full p-2"
        />
        <button className="bg-blue-600 text-white p-2 w-full rounded">
          Вход
        </button>
      </form>
    </div>
  );
}
