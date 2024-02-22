import "./App.css";

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
              {extractor.uuid} | {extractor.description}
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
  <div>
    <textarea></textarea>
    <button></button>
  </div>;
};

const App = () => {
  // const { data } = useSWR("/ready", fetcher);
  // log the liveliness probe result
  // console.log(data);

  return (
    <>
      <QueryClientProvider client={queryClient}>
        <Extract />
        <h1>Extract</h1>
        <ExtractionWidget />
      </QueryClientProvider>
    </>
  );
};

export default App;
