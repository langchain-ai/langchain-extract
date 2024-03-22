"use client";

import {
  Tab,
  TabList,
  TabPanel,
  TabPanels,
  Tabs,
  Text,
  Button,
  IconButton,
  Flex,
  Box,
  Container,
} from "@chakra-ui/react";

import { TrashIcon } from "@heroicons/react/24/outline";
import Form from "@rjsf/chakra-ui";
import validator from "@rjsf/validator-ajv8";
import { docco } from "react-syntax-highlighter/dist/esm/styles/hljs";

import SyntaxHighlighter from "react-syntax-highlighter";
import {
  useGetExtractor,
  useCreateExample,
  useListExamples,
  useDeleteExample,
} from "../utils/api";

type ExtractorProps = {
  extractorId: string;
  isShared: boolean;
};

/**
 * Component to view and manage an extractor.
 */
export const Examples = ({ extractorId }: ExtractorProps) => {
  const listExamplesQuery = useListExamples({ extractor_id: extractorId });
  const useDeleteMutation = useDeleteExample();
  if (listExamplesQuery.isLoading) {
    return <div>Loading...</div>;
  }
  if (listExamplesQuery.isError) {
    return (
      <div>Unable to load examples for extractor with ID: {extractorId}</div>
    );
  }
  const data = listExamplesQuery.data;
  return (
    <div>
      {data &&
        data.map((example) => (
          <div key={example.uuid}>
            <Container margin={'auto'} marginBottom={"5"} scrollBehavior={"auto"}>
              <Flex alignItems="center" justifyContent="space-between">
                <Box flex="1" marginRight="2">
                  <Text isTruncated>{example.content}</Text>
                </Box>
                <Box flex="3" marginRight="2">
                  <SyntaxHighlighter language="json" style={docco}>
                    {JSON.stringify(example.output, null, 2)}
                  </SyntaxHighlighter>
                </Box>
                <Box>
                  <IconButton
                    onClick={() =>
                      useDeleteMutation.mutate({ uuid: example.uuid })
                    }
                    variant={"outline"}
                    isLoading={useDeleteMutation.isPending}
                    colorScheme="red"
                    aria-label="Delete example"
                    icon={<TrashIcon />}
                  />
                </Box>
              </Flex>
            </Container>
          </div>
        ))}
    </div>
  );
};

export const Extractor = ({ extractorId, isShared }: ExtractorProps) => {
  const { data, isLoading, isError } = useGetExtractor(extractorId, isShared);
  const createExampleMutation = useCreateExample((data) => {}); // void function
  if (isLoading) {
    return <div>Loading...</div>;
  }
  if (isError) {
    return <div>Unable to load extractor with ID: {extractorId}</div>;
  }

  if (data === undefined) {
    throw new Error("Data is undefined");
  }

  const newSchema = {
    type: "object",
    title: "Example",
    description:
      "Example text together wtih an example of content that should be extracted.",
    properties: {
      content: {
        type: "string",
        title: "Content",
      },
      extraction: data.schema,
    },
  };

  const UISchema = {
    content: {
      "ui:autoFocus": true,
      "ui:placeholder": "Enter contact to extract",
      "ui:widget": "textarea",
    },
  };

  const handleAddExample = (
    data: any,
    event: React.FormEvent<HTMLFormElement>,
  ) => {
    console.log(data);

    createExampleMutation.mutate({
      extractor_id: extractorId,
      content: data.formData.content,
      output: [data.formData.extraction],
    });
  };

  return (
    <div className="mr-auto">
      <Tabs className="mt-5" variant={"enclosed"} colorScheme="blue" size="sm">
        <TabList>
          <Tab>Form</Tab>
          <Tab>Code</Tab>
          <Tab>Add Example</Tab>
          <Tab>View / Delete Examples</Tab>
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
          <TabPanel>
            <Text className="mt-1 mb-5">
              Use this to manage examples associated with the extractor.
            </Text>
            <Form
              schema={newSchema}
              uiSchema={UISchema}
              validator={validator}
              onSubmit={(data, event) => handleAddExample(data, event)}
            >
              <div>
                <Button type="submit">Add Example</Button>
              </div>
            </Form>
          </TabPanel>
          <TabPanel>
            <Examples extractorId={extractorId} isShared={isShared} />
          </TabPanel>
        </TabPanels>
      </Tabs>
    </div>
  );
};
