import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import axios from "axios";

import SyntaxHighlighter from "react-syntax-highlighter";
import { docco } from "react-syntax-highlighter/dist/esm/styles/hljs";

const getExtractors = async () => {
  const response = await axios.get("/extractors");
  return response.data;
};


const runExtraction = async (extractionRequest) => {
  const response = await axios.postForm("/extract", extractionRequest);
  return response.data;
};

const ListExtractors = () => {
  const queryClient = useQueryClient();
  const { data: extractors, isLoading, isError } = useQuery({ queryKey: ["getExtractors"], queryFn: getExtractors });

  const deleteExtractor = useMutation({
    mutationFn: (uuid) => axios.delete(`/extractors/${uuid}`),
    onSuccess: () => {
      queryClient.invalidateQueries("getExtractors");
    }
  },
  )

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (isError) {
    return <div>Error</div>;
  }


  return (
    <div>
      <Heading>Extractors</Heading>
      <table className="table">
        <thead>
          <tr>
            <th>Description</th>
            <th>Schema</th>
          </tr>
        </thead>
        <tbody>
          {extractors?.map((extractor: any) => {
            return (
              <tr key={extractor.uuid} className="hover:bg-green-100">
                <td>{extractor.description}</td>
                <td>{JSON.stringify(extractor.schema)}</td>
                <td className="hover:tran"><button className="button " onClick={() => deleteExtractor.mutate(extractor.uuid)}>X</button></td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

const Heading = ({ children }) => {
  return <h1 className="text-5xl font-bold">{children}</h1>;
};

/**
 * Widget to extract content from text given an extractor
 */
const ExtractionWidget = ({}) => {
  // const { data, isPending, mutate } = useExtractUsingExistingExtractorExtractPost();
  const { data, isPending, mutate } = useMutation({ mutationFn: runExtraction });
  const uuid = "1494bdb8-e4ed-43b8-9a2a-f6ac4a318096";
  const text = "hello my name is chester and i am 23 years old.";
  const handleSubmit = (event) => {
    event.preventDefault();

    const request = {
      extractor_id: event.target.extractorId.value,
      text: event.target.text.value,
    };
    console.log(request);
    mutate(request);
  };

  return (
    <div className="w-4/5 m-auto">
      <Heading>Extraction</Heading>
      <form className="m-auto flex flex-col content-between gap-5 mt-10" onSubmit={handleSubmit}>
        <input
          type="text"
          name="extractorId"
          placeholder="extractor id"
          className="input input-bordered"
          defaultValue={uuid}
        />
        <input type="file" name="file" className="file-input " />
        <div className="divider">OR</div>
        <textarea placeholder="Text" name="text" className="textarea textarea-bordered h-3/4" defaultValue={text} />
        <button className="btn" type="submit">
          Run
        </button>
      </form>
      <ExtractionResults data={data} isPending={isPending} />
    </div>
  );
};

const ExtractionResults = ({ data, isPending }) => {
  return (
    <div className="mt-1">
      <Heading>Results</Heading>

      {isPending ? (
        <div>Loading...</div>
      ) : (
        <div>
          <SyntaxHighlighter language="javascript" style={docco}>
            {JSON.stringify(data, null, 2)}
          </SyntaxHighlighter>
        </div>
      )}
    </div>
  );
};

const App = () => {
  return (
    <>
      <div className="flex flex-col justify-between h-3/4 overfow-auto">
        <ListExtractors />
        <ExtractionWidget />
      </div>
    </>
  );
};

export default App;
