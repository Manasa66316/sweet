import api from "../api/axios";
import { useEffect, useState } from "react";

export default function Protected() {
  const [data, setData] = useState("");

  useEffect(() => {
    api.get("/protected")
      .then(res => setData(res.data.message))
      .catch(() => alert("Unauthorized"));
  }, []);

  return <h2>{data}</h2>;
}
