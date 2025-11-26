const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function login(email: string, password: string) {
  const res = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  if (!res.ok) {
    alert("Грешни данни");
    return;
  }

  const data = await res.json();
  alert("Успешен вход!");
  localStorage.setItem("token", data.access_token);

  return data;
}
