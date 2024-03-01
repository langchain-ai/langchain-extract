import { ChakraProvider, IconButton, useDisclosure } from "@chakra-ui/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import React from "react";
import { Playground } from "./components/Playground";
import { Sidebar } from "./components/Sidebar";
import "./index.css";
import { Bars3Icon } from "@heroicons/react/24/outline";
import { BrowserRouter, Route, Routes, Outlet } from "react-router-dom";
import ErrorPage from "./routes/ErrorPage";

const queryClient = new QueryClient();

const Root = () => {
  const { isOpen, onOpen, onClose } = useDisclosure();

  return (
    <>
      <Sidebar isOpen={isOpen} onOpen={onOpen} onClose={onClose} />
      <div className="flex flex-col w-100% h-full">
        <div className="flex justify-between bg-slate-200 mb-4 p-3 items-center">
          <IconButton aria-label="Menu" icon={<Bars3Icon />} onClick={onOpen} size="lg" isRound={true}></IconButton>
          <div className="text-s text-rose-800">
            <strong>Research Preview</strong>: this app is unauthenticated and all data can be found. Do not use with
            sensitive data.
          </div>
          <div>🦜 LangChain Extract</div>
        </div>
        <div className="m-auto w-5/6">
          <Outlet />
        </div>
      </div>
    </>
  );
};

const Main = () => {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route element={<Root />}>
            <Route path="/" element={<div>Nothing selected</div>} />
            <Route path="/e/:extractorId" element={<Playground />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </>
  );
};

const App = () => {
  return (
    <React.StrictMode>
      <QueryClientProvider client={queryClient}>
        <ChakraProvider>
          <Main />
        </ChakraProvider>
      </QueryClientProvider>
    </React.StrictMode>
  );
};

export default App;
