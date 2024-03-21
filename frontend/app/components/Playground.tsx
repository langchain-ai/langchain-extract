"use client";

import {
  Button,
  Textarea,
  Heading,
  Tab,
  Tabs,
  TabList,
  TabPanel,
  TabPanels,
  Text,
} from "@chakra-ui/react";
import { useMutation } from "@tanstack/react-query";
import React from "react";
import SyntaxHighlighter from "react-syntax-highlighter";
import { docco } from "react-syntax-highlighter/dist/esm/styles/hljs";
import { runExtraction } from "../utils/api";
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
  const [isDisabled, setIsDisabled] = React.useState(false);
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const request = {
      extractor_id: extractorId,
    };

    if (event.currentTarget.text.value) {
      Object.assign(request, { text: event.currentTarget.text.value });
    } else {
      Object.assign(request, { file: event.currentTarget.file.files[0] });
    }

    mutate([request, isShared]);
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
        <form
          className="m-auto flex flex-col content-between gap-5 mt-10 mb-10"
          onSubmit={handleSubmit}
          onChange={handleChange}
        >
          <input type="file" name="file" className="file-input " />
          <div className="divider">OR</div>
          <Textarea
            placeholder="Enter text to extract information from..."
            name="text"
            className="textarea textarea-bordered h-3/4"
            autoFocus
          />
          <Button type="submit" disabled={isDisabled}>
            Run
          </Button>
        </form>
      </div>
      <div className="m-auto">
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
                This shows the raw JSON Schema that describes what information
                the extractor will be extracting from the content.
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
