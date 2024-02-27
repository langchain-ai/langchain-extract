import React from "react";

import { useDisclosure, Radio, RadioGroup, Stack } from '@chakra-ui/react'
import { ResultsTable } from "./components/ResultsTable";
import { Button } from '@chakra-ui/react'
import {
  Drawer,
  DrawerBody,
  DrawerFooter,
  DrawerHeader,
  DrawerOverlay,
  DrawerContent,
  DrawerCloseButton,
} from '@chakra-ui/react'
import { Heading } from "./components/Heading";
import { ExtractorPlayground } from "./components/ExtractorPlayground";
import { ListExtractors } from "./components/ListExtractors";

/**
 * Component to create a new extractor with fields for name, description, schema, and examples
 */
const CreateExtractor = ({}) => {
  // You might use a mutation hook here if you're using something like React Query for state management
  // const { mutate, isLoading } = useMutation({ mutationFn: createExtractorFunction });
  return (
    <div className="w-4/5 m-auto">
      <Heading>Create New Extractor</Heading>
      <form className="m-auto flex flex-col content-between gap-5 mt-10">
        <input type="text" name="name" placeholder="Name" className="input input-bordered" required />
        <textarea name="description" placeholder="Description" className="textarea textarea-bordered h-1/4" required />
        <textarea name="schema" placeholder="Schema" className="textarea textarea-bordered h-1/4" required />
        <textarea name="examples" placeholder="Examples" className="textarea textarea-bordered h-1/4" required />
        <button className="btn" type="submit">
          Create
        </button>
      </form>
    </div>
  );
};

function PlacementExample() {
  const { isOpen, onOpen, onClose } = useDisclosure()
  const [placement, setPlacement] = React.useState('right')

  return (
    <>
      <Button colorScheme='blue' onClick={onOpen}>
        LangChain Extract
      </Button>
      <Drawer placement='left' onClose={onClose} isOpen={isOpen}>
        <DrawerOverlay />
        <DrawerContent>
          <DrawerHeader borderBottomWidth='1px'>Basic Drawer</DrawerHeader>
          <DrawerBody>
            <ListExtractors onSelect={() => {}} />
          </DrawerBody>
        </DrawerContent>
      </Drawer>
    </>
  )
}

const App = () => {
  const initialExtractor = "6fec248a-8846-4939-9da2-eb7db0f642a7";
  const [extractorId, setExtractorId] = React.useState(initialExtractor);

  const onSelect = (extractorId: string) => {
    setExtractorId(extractorId);
  };



  return (
    <>
      {/* <SideBar /> */}
      <div className="flex flex-col w-100% h-full">
    {/* <PlacementExample/> */}
        <div className="flex justify-between bg-slate-200 mb-2 p-2">
          <div>LangChain Extract</div>
          <div className="text-s text-rose-800">
            Research Preview: this is unauthenticated and all data can be found.
            Do not use with sensitive data.
          </div>
        </div>
        <div className="flex">
          <ListExtractors onSelect={onSelect} />
          <ExtractorPlayground extractor_id={extractorId} />
        </div>
      </div>
    </>
  );
};


export default App;