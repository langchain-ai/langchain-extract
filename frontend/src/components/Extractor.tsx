import { Text, Tab, TabList, TabPanel, TabPanels, Tabs } from "@chakra-ui/react";
import Form from "@rjsf/chakra-ui";
import validator from "@rjsf/validator-ajv8";
import { useQuery } from "@tanstack/react-query";
import { useGetExtractor } from "../api";

import { Input, InputGroup, InputLeftAddon, VStack } from "@chakra-ui/react";
import SyntaxHighlighter from "react-syntax-highlighter";
import { docco } from "react-syntax-highlighter/dist/esm/styles/hljs";

export const Extractor = ({ extractorId }: { extractorId: string }) => {
  const { data, isLoading, isError } = useGetExtractor(extractorId);
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
      <VStack align={"left"}>
        <Text>
          <strong>Name: </strong> {data.name}
        </Text>
        <Text>
          <strong>Description: </strong>
          {data.description}
        </Text>
        <Text>
          <strong>Instructions: </strong>
          {data.instruction}
        </Text>
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
