"use client";
import {
  Button,
  Heading,
  Tab,
  Box,
  Divider,
  AbsoluteCenter,
  TabList,
  TabPanel,
  TabPanels,
  Tabs,
  Text,
  Textarea,
  FormControl,
  FormLabel,
  HStack,
  Radio,
  RadioGroup,
} from "@chakra-ui/react";
import { useMutation } from "@tanstack/react-query";
import React from "react";
import SyntaxHighlighter from "react-syntax-highlighter";
import { docco } from "react-syntax-highlighter/dist/esm/styles/hljs";
import { runExtraction, useConfiguration } from "../utils/api";
import { Extractor } from "./Extractor";
import { ResultsTable } from "./ResultsTable";

interface PlaygroundProps {
  /**
   * The playground currently support viewing
   * both shared and non-shared extractors
   */
  extractorId: string;
  isShared: boolean;
}

/**
 * Playground to work with an existing extractor.
 */
export const Playground = (props: PlaygroundProps) => {
  const { extractorId, isShared } = props;
  const { data, isPending, mutate } = useMutation({
    mutationFn: runExtraction,
  });

  const requestServerConfig = useConfiguration();
  const [isDisabled, setIsDisabled] = React.useState(true);

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const request = {
      extractor_id: extractorId,
      model_name: event.currentTarget.modelId.value,
    };

    if (event.currentTarget.text.value) {
      Object.assign(request, { text: event.currentTarget.text.value });
    } else {
      Object.assign(request, { file: event.currentTarget.file.files[0] });
    }

    mutate([request, isShared]);
  };

  const handleKeyDown = (event: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault(); // Prevent the default Enter action
      if (isDisabled) {
        return;
      }

      event.currentTarget.form?.dispatchEvent(
        new Event("submit", { cancelable: true, bubbles: true }),
      );
    }
  };

  const handleChange = (event: React.FormEvent<HTMLFormElement>) => {
    if (
      event.currentTarget.text.value === "" &&
      event.currentTarget.file.files.length === 0
    ) {
      setIsDisabled(true);
      return;
    }
    // Also disable if both are present
    if (
      event.currentTarget.text.value !== "" &&
      event.currentTarget.file.files.length !== 0
    ) {
      setIsDisabled(true);
      return;
    }

    setIsDisabled(false);
  };

  return (
    <div className="w-full flex-col justify-between">
      <div className="m-auto">
        {isShared && <Heading>Using a shared exractor</Heading>}
        <div>
          <Extractor extractorId={extractorId} isShared={isShared} />
        </div>
        <Heading>Extract</Heading>

        <form
          className="m-auto flex flex-col content-between gap-5 mt-10 mb-10"
          onSubmit={handleSubmit}
          onChange={handleChange}
        >
          {requestServerConfig.isFetched && (
            <FormControl as="fieldset">
              <FormLabel as="legend">Extraction Model</FormLabel>
              <RadioGroup
                name="modelId"
                defaultValue={requestServerConfig.data?.models[0].name}
              >
                <HStack spacing="24px">
                  {requestServerConfig.data?.models.map((model) => (
                    <Radio value={model.name} key={model.name}>
                      {model.description}
                    </Radio>
                  ))}
                </HStack>
              </RadioGroup>
            </FormControl>
          )}
          {requestServerConfig.isFetched && (
            <>
              <input
                type="file"
                name="file"
                accept={requestServerConfig.data?.accepted_mimetypes.join(", ")}
                color="blue"
                className="border-2 border-dashed border-gray-300 rounded-md p-4 w-full file:mr-4"
              />
              <Text fontSize="xs">
                Max file size is: {requestServerConfig.data?.max_file_size_mb}MB
              </Text>
              <Text fontSize="xs">
                Supported mimetypes:{" "}
                {requestServerConfig.data?.accepted_mimetypes.join(", ")}
              </Text>
            </>
          )}
          <Box position="relative" padding="10">
            <Divider />
            <AbsoluteCenter bg="white" px="4">
              OR
            </AbsoluteCenter>
          </Box>
          <Textarea
            placeholder="Enter text to extract information from..."
            name="text"
            className="textarea textarea-bordered h-3/4"
            autoFocus
            onKeyDown={handleKeyDown}
          />
          <Button type="submit" isDisabled={isDisabled}>
            Run
          </Button>
        </form>
      </div>
      <div className="m-auto">
        {data?.content_too_long && (
          <Text color={"red"} margin={5}>
            The content was too long to be processed. Extraction was run on a
            truncated version of the content.
          </Text>
        )}
        <Tabs variant={"enclosed"} colorScheme="blue" size="sm">
          <TabList>
            <Tab>Table</Tab>
            <Tab>JSON</Tab>
          </TabList>
          <TabPanels>
            <TabPanel>
              <ResultsTable data={data} isPending={isPending} />
            </TabPanel>
            <TabPanel>
              <Text className="mt-1 mb-5">
                Shows the output from the extractor in JSON format.
              </Text>
              <SyntaxHighlighter language="json" style={docco}>
                {JSON.stringify(data, null, 2)}
              </SyntaxHighlighter>
            </TabPanel>
          </TabPanels>
        </Tabs>
      </div>
    </div>
  );
};
