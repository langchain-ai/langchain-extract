import { Button, Heading } from "@chakra-ui/react";
import { useMutation } from "@tanstack/react-query";
import { runExtraction, useRunExtraction } from "../api";
import { Extractor } from "./Extractor";
import { ResultsTable } from "./ResultsTable";
import { useParams } from "react-router";
import { Textarea } from '@chakra-ui/react'

import React from "react";

/**
 * Playground to work with an existing extractor.
 */
export const Playground = () => {
  let { extractorId } = useParams();
  const { data, isPending, mutate } = useMutation({ mutationFn: runExtraction });
  const [isDisabled, setIsDisabled] = React.useState(false);
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    let request = {
      extractor_id: extractorId,
    };

    if (event.currentTarget.text.value) {
      Object.assign(request, { text: event.currentTarget.text.value });
    } else {
      Object.assign(request, { file: event.currentTarget.file.files[0] });
    }

    mutate(request);
  };

  const handleChange = (event: React.FormEvent<HTMLFormElement>) => {
    if (event.currentTarget.text.value === "" && event.currentTarget.file.files.length === 0) {
      setIsDisabled(true);
      return;
    } else {
      // Also disable if both are present
      if (event.currentTarget.text.value !== "" && event.currentTarget.file.files.length !== 0) {
        setIsDisabled(true);
        return;
      }
    }

    setIsDisabled(false);
  };

  return (
    <div className="w-full flex-col justify-between">
      <div className="m-auto">
        <div>
          <Extractor extractorId={extractorId} />
        </div>
        <form
          className="m-auto flex flex-col content-between gap-5 mt-10 mb-10"
          onSubmit={handleSubmit}
          onChange={handleChange}
        >
          <input type="file" name="file" className="file-input " />
          <div className="divider">OR</div>
          <Textarea placeholder="Enter text to extract information from..." name="text" className="textarea textarea-bordered h-3/4" autoFocus />
          <Button type="submit" disabled={isDisabled}>
            Run
          </Button>
        </form>
      </div>
      <div className="m-auto">
        <ResultsTable data={data} isPending={isPending} />
      </div>
    </div>
  );
};
