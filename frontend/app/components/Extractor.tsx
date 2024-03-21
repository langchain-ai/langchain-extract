"use client";

import {
  Tab,
  TabList,
  TabPanel,
  TabPanels,
  Tabs,
  Text,
} from "@chakra-ui/react";
import Form from "@rjsf/chakra-ui";
import validator from "@rjsf/validator-ajv8";
import { docco } from "react-syntax-highlighter/dist/esm/styles/hljs";

import SyntaxHighlighter from "react-syntax-highlighter";
import { useGetExtractor } from "../utils/api";

type ExtractorProps = {
  extractorId: string;
  isShared: boolean;
};

export const Extractor = ({ extractorId, isShared }: ExtractorProps) => {
  const { data, isLoading, isError } = useGetExtractor(extractorId, isShared);
  if (isLoading) {
    return <div>Loading...</div>;
  }
  if (isError) {
    return <div>Unable to load extractor with ID: {extractorId}</div>;
  }

  if (data === undefined) {
    throw new Error("Data is undefined");
  }

  return (
    <div className="mr-auto">
      <Tabs className="mt-5" variant={"enclosed"} colorScheme="blue" size="sm">
        <TabList>
          <Tab>Form</Tab>
          <Tab>Code</Tab>
        </TabList>
        <TabPanels>
          <TabPanel>
            <Form schema={data.schema} validator={validator}>
              {true} {/* Disables the submit button */}
            </Form>
          </TabPanel>
          <TabPanel>
            <Text className="mt-1 mb-5">
              This shows the raw JSON Schema that describes what information the
              extractor will be extracting from the content.
            </Text>
            <SyntaxHighlighter language="json" style={docco}>
              {JSON.stringify(data.schema, null, 2)}
            </SyntaxHighlighter>
          </TabPanel>
        </TabPanels>
      </Tabs>
    </div>
  );
};
