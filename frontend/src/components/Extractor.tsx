import { Tab, TabList, TabPanel, TabPanels, Tabs } from "@chakra-ui/react";
import Form from "@rjsf/chakra-ui";
import validator from "@rjsf/validator-ajv8";
import { useQuery } from "@tanstack/react-query";
import { getExtractor } from "../api";

import {
  Input,
  InputGroup,
  InputLeftAddon,
  VStack
} from "@chakra-ui/react";
import SyntaxHighlighter from "react-syntax-highlighter";
import { docco } from "react-syntax-highlighter/dist/esm/styles/hljs";


export const Extractor = ({ extractor_id }: { extractor_id: string }) => {
  const { data, isLoading, isError } = useQuery({ queryKey: ["getExtractor", extractor_id], queryFn: getExtractor });
  if (isLoading) {
    return <div>Loading...</div>;
  }
  if (isError) {
    return <div>Error</div>;
  }

  if (data === undefined) {
    throw new Error("Data is undefined");
  }

  return (
    <div className="mr-auto">
      <VStack spacing={4} align={"stretch"}>
        <InputGroup>
          <InputLeftAddon>Name</InputLeftAddon>
          <Input type="name" placeholder={data.name} disabled={true} />
          <InputLeftAddon>Description</InputLeftAddon>
          <Input type="name" placeholder={data.description} disabled={true} />
        </InputGroup>
      </VStack>
      <Tabs className="mt-5">
        <TabList>
          <Tab>JSON Schema</Tab>
          <Tab>As Form</Tab>
        </TabList>
        <TabPanels>
          <TabPanel>
            <SyntaxHighlighter language="javascript" style={docco}>
              {JSON.stringify(data.schema, null, 2)}
            </SyntaxHighlighter>
          </TabPanel>
          <TabPanel>
            <Form
              schema={data.schema}
              validator={validator}
              children={true} // Hide the submit button
            />
          </TabPanel>
        </TabPanels>
      </Tabs>
    </div>
  );
};
