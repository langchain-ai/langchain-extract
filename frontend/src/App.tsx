import React from "react";

import { IconButton, useDisclosure } from "@chakra-ui/react";
import { Bars3Icon } from "@heroicons/react/24/outline";
import { ExtractorPlayground } from "./components/ExtractorPlayground";
import { ListExtractors } from "./components/ListExtractors";
import { Sidebar } from "./components/Sidebar";

<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
  <path strokeLinecap="round" strokeLinejoin="round" d="M6.75 12a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0ZM12.75 12a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0ZM18.75 12a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z" />
</svg>

const App = () => {
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
        {/* <PlacementExample/> */}
        <div className="flex justify-between bg-slate-200 mb-4 p-3 items-center">
          <IconButton aria-label="Menu" icon={<Bars3Icon/>} onClick={onOpen} size="lg" isRound={true}></IconButton>
          <div className="text-s text-rose-800">
            <strong>Research Preview</strong>: this app is unauthenticated and all data can be found. Do not use with
            sensitive data.
          </div>
          <div>🦜 LangChain Extract</div>
        </div>
        <div className="flex m-auto w-5/6">
          <ExtractorPlayground extractor_id={extractorId} />
        </div>

        <h1> temporary for convenience </h1>

        <ListExtractors onSelect={onSelect} />
      </div>
    </>
  );
};

export default App;
