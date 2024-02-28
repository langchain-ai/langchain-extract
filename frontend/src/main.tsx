import { ChakraProvider } from "@chakra-ui/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import React from "react";
import ReactDOM from "react-dom/client";
import { v4 as uuidv4 } from "uuid";
import App from "./App.tsx";
import "./index.css";

if (document.cookie.indexOf("user_id") === -1) {
  document.cookie = `extract_user_id=${uuidv4()}`;
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

import { render } from "react-dom";

const rootElement = document.getElementById("root");

render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <ChakraProvider>
        <App />
      </ChakraProvider>
      {/* <RouterProvider router={router}/> */}
    </QueryClientProvider>
  </React.StrictMode>,
  rootElement
);
