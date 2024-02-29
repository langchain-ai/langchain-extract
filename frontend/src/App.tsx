import { ChakraProvider, IconButton, useDisclosure } from "@chakra-ui/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import React from "react";
import { ExtractorPlayground } from "./components/ExtractorPlayground";
import { ListExtractors } from "./components/ListExtractors";
import { Sidebar } from "./components/Sidebar";
import "./index.css";
import { Bars3Icon } from "@heroicons/react/24/outline";
import { BrowserRouter, Route, Routes, Outlet } from "react-router-dom";
import ErrorPage from "./routes/ErrorPage";

const queryClient = new QueryClient();

const Root = () => {
  const initialExtractor = "6fec248a-8846-4939-9da2-eb7db0f642a7";
  const [extractorId, setExtractorId] = React.useState(initialExtractor);
  const { isOpen, onOpen, onClose } = useDisclosure();

  const onSelect = (extractorId: string) => {
    setExtractorId(extractorId);
  };

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
        <h1> temporary for convenience </h1>
        <ListExtractors onSelect={onSelect} />
        <div>
      </div>
      <Outlet/>
        <div>
          {/* <div className="flex m-auto w-5/6">
            <ExtractorPlayground extractor_id={extractorId} />
          </div> */}
        </div>
      </div>
    </>
  );
};

const Main = () => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route element={<Root />}>
            <Route path="/" element={<div>main</div>}/>
            <Route path="/e/:extractorId" element={<ExtractorPlayground/>}/>
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
