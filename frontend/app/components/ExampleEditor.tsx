"use client";

import {
  AbsoluteCenter,
  Box,
  Button,
  Divider,
  IconButton,
  Table,
  TableCaption,
  Tbody,
  Td,
  Text,
  Th,
  Thead,
  Tr,
} from "@chakra-ui/react";

import { TrashIcon } from "@heroicons/react/24/outline";
import Form from "@rjsf/chakra-ui";
import validator from "@rjsf/validator-ajv8";
import { docco } from "react-syntax-highlighter/dist/esm/styles/hljs";

import SyntaxHighlighter from "react-syntax-highlighter";
import {
  useCreateExample,
  useDeleteExample,
  useGetExtractor,
  useListExamples,
} from "../utils/api";

type ExtractorProps = {
  extractorId: string;
  isShared: boolean;
};

/**
 * Component to view and manage an extractor.
 */
const Examples = ({ extractorId }: { extractorId: string }) => {
  const listExamplesQuery = useListExamples({
    extractor_id: extractorId,
    limit: 10,
    offset: 0, // Hard code pagination for now
  });
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
    <div className="w-5/5">
      {data && data.length === 0 ? (
        <Text>Use the form below to add examples to the extractor</Text>
      ) : (
        <Table variant="simple">
          <TableCaption placement={"top"}>
            View and Delete Examples
          </TableCaption>
          <Thead>
            <Tr>
              <Th>Content</Th>
              <Th>Output</Th>
              <Th>Action</Th>
            </Tr>
          </Thead>
          <Tbody>
            {data &&
              data.map((example) => (
                <Tr key={example.uuid}>
                  <Td>{example.content}</Td>
                  <Td>
                    <SyntaxHighlighter language="json" style={docco}>
                      {JSON.stringify(example.output, null, 2)}
                    </SyntaxHighlighter>
                  </Td>
                  <Td>
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
                  </Td>
                </Tr>
              ))}
          </Tbody>
        </Table>
      )}
    </div>
  );
};

export const ExampleEditor = ({ extractorId, isShared }: ExtractorProps) => {
  const { data, isLoading, isError } = useGetExtractor(extractorId, isShared);
  const createExampleMutation = useCreateExample();
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
    properties: {
      content: {
        type: "string",
        title: "Content",
      },
      output: {
        // Array of data.schema
        type: "array",
        items: {
          ...data.schema,
          title: undefined,
          description: undefined,
        },
      },
    },
    required: ["content"],
  };

  const UISchema = {
    content: {
      "ui:autoFocus": true,
      "ui:placeholder": "Enter contact to extract",
      "ui:widget": "textarea",
      "ui:description": "Enter the text to extract information from",
    },
    output: {
      "ui:autoFocus": false,
      "ui:title": "Outputs",
    },
  };

  const handleAddExample = (
    /* eslint-disable @typescript-eslint/no-explicit-any */
    formData: any,
  ) => {
    createExampleMutation.mutate({
      extractor_id: extractorId,
      content: formData.formData.content,
      output: [formData.formData.output],
    });
  };

  return (
    <div className="mr-auto">
      <Examples extractorId={extractorId} />
      <Box position="relative" padding="10">
        <Divider />
        <AbsoluteCenter bg="white" px="4">
          <Text>Add</Text>
        </AbsoluteCenter>
      </Box>
      <Form
        // @ts-expect-error - Need to investigate
        schema={newSchema}
        uiSchema={UISchema}
        validator={validator}
        onSubmit={(formData) => handleAddExample(formData)}
      >
        <div>
          <Button type="submit">Add Example</Button>
        </div>
      </Form>
    </div>
  );
};
