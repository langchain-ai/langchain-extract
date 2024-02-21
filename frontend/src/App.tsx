import { useState } from "react";
import axios from "axios";
import "./App.css";
import useSWR from "swr";
// import Button from '@mui/material/Button';
import useSWRMutation from "swr/mutation";

const api = axios.create({
  baseURL: "http://localhost:8000",
});


async function fetcher(url: string) {
  return api.get(url).then((res) => res.data);
}

export function useExtract() {
  return useSWR(["/extract"], async () => {
    const response = await fetch("http://localhost:8000/extract", {
      method: "POST",
      headers: {
        'Content-Type': 'application/json', // Specify that the body content is JSON
      },
      body: JSON.stringify({
        text: "hello",
        extractor_id: "00000000-0000-0000-0000-000000000005",
      }),
    });

    if (!response.ok) throw new Error(await response.text());

    const json = await response.json();
    return json;
  });
}

const Extract = () => {
  const { data, error } = useExtract();
  return (
    <div>
      <textarea />
      <button>Extract</button>
      {error && <div>Failed to load with error message {error.message}</div>}
    </div>
  );
};

const App = () => {
  const { data } = useSWR("/ready", fetcher);
  // log the liveliness probe result
  console.log(data);

  return (
    <>
      <h1>Extract</h1>
      <Extract />
    </>
  );
};

export default App;
