import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.tsx";
import Root from "./routes/root.tsx";
import "./index.css";
import { v4 as uuidv4 } from "uuid";
import { ChakraProvider } from "@chakra-ui/react";

import { createBrowserRouter, RouterProvider } from "react-router-dom";

if (document.cookie.indexOf("user_id") === -1) {
  document.cookie = `opengpts_user_id=${uuidv4()}`;
}

const queryClient = new QueryClient();

// const router = createBrowserRouter([
//   {
//     path: "/",
//     element: <Root />,
//     errorElement: <div>404</div>,
//     children: [
//       {
//         path: "extractors/:uuid",
//         // element: <Extractor />,
//       },
//     ],
//   },
// ]);

const root =  ReactDOM.createRoot(document.getElementById("root") as HTMLElement);
root.render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <ChakraProvider>
        <App />
      </ChakraProvider>
      {/* <RouterProvider router={router}/> */}
    </QueryClientProvider>
  </React.StrictMode>
);
