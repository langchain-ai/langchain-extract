import { Button } from "@chakra-ui/react";
import { useMutation } from "@tanstack/react-query";
import { runExtraction } from "../api";
import { Extractor } from "./Extractor";
import { Heading } from "./Heading";
import { ResultsTable } from "./ResultsTable";

/**
 * Widget to extract content from text given an extractor
 */
export const ExtractorPlayground = ({ extractor_id }: { extractor_id: string }) => {
  // const { data, isPending, mutate } = useExtractUsingExistingExtractorExtractPost();
  const { data, isPending, mutate } = useMutation({ mutationFn: runExtraction });
  const text = "hello my name is chester and i am 23 years old.";
  const handleSubmit = (event) => {
    event.preventDefault();

    const request = {
      extractor_id: extractor_id,
      text: event.target.text.value,
    };
    console.log(request);
    mutate(request);
  };

  return (
    <div className="w-full mr-2 mt-2 flex-col justify-between">
      <div className="m-auto">
        <div>
          <Extractor extractor_id={extractor_id} />
        </div>
        <form className="m-auto flex flex-col content-between gap-5 mt-10 mb-10" onSubmit={handleSubmit}>
          <input type="file" name="file" className="file-input " />
          <div className="divider">OR</div>
          <textarea placeholder="Text" name="text" className="textarea textarea-bordered h-3/4" defaultValue={text} />
          <Button type="submit">Run</Button>
        </form>
      </div>
      <Heading>Results</Heading>
      <div className="m-auto">
        <ResultsTable data={data} isPending={isPending} />
      </div>
    </div>
  );
};
