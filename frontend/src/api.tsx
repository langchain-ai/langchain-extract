/* Contains all the API calls to the backend server */
import axios from "axios";

export type ExtractorData = {
  uuid: string;
  name: string;
  description: string;
  schema: any;
};

export const getExtractor = async ({ queryKey }): ExtractorData => {
  const [_, uuid] = queryKey;
  const response = await axios.get(`/extractors/${uuid}`);
  return response.data;
};export const listExtractors = async () => {
  const response = await axios.get("/extractors");
  return response.data;
};


export const runExtraction = async (extractionRequest, file) => {
  console.log(extractionRequest)
  const response = await axios.postForm("/extract", extractionRequest);
  return response.data;
};

