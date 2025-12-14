import api from "../api/axios";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();

    const res = await api.post("/auth/login", {
      email: e.target.email.value,
      password: e.target.password.value,
    });

    login(res.data.access_token);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="email" placeholder="Email" />
      <input name="password" type="password" placeholder="Password" />
      <button>Login</button>
    </form>
  );
}

