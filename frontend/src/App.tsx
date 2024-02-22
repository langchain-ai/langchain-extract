import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useListExtractorsGet } from "./api/extractor-definitions/extractor-definitions";

const BASE_URL = "http://localhost:8000";

const Extract = () => {
  const { data, isLoading, isError } = useListExtractorsGet({}, { axios: { baseURL: BASE_URL } });

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (isError) {
    return <div>Error</div>;
  }
  /*  */
  const extractors = data?.data;

  return (
    <div>
      <h2>Available Extractors</h2>
      <ul>
        {extractors?.map((extractor: any) => {
          return (
            <li key={extractor.uuid}>
              {extractor.uuid} | {extractor.description} | {JSON.stringify(extractor.schema)}
            </li>
          );
        })}
      </ul>
    </div>
  );
};

const queryClient = new QueryClient();

/**
 * Widget to extract content from text given an extractor
 */
const ExtractionWidget = () => {
  return (
    <div>
      <h1>Extract</h1>
      <label htmlFor="content">
        <h2>Content</h2>
      </label>
      <textarea
        id="content"
        placeholder="Write your thoughts here..."
      ></textarea>
        <button className="bg-sky-700 px-4 py-2 text-white hover:bg-sky-800 sm:px-8 sm:py-3">Run</button>
    </div>
  );
};

const App = () => {
  // const { data } = useSWR("/ready", fetcher);
  // log the liveliness probe result
  // console.log(data);

  return (
    <>
    <h1 className="text-3xl font-bold underline">
      Hello world!
    </h1>
      <QueryClientProvider client={queryClient}>
        <Extract />
        <ExtractionWidget />
      </QueryClientProvider>
    </>
  );
};

export default App;
