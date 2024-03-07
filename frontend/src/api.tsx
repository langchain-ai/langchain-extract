/* Contains all the API calls to the backend server */
import axios from "axios";
import { useQuery, useQueryClient, useMutation } from "@tanstack/react-query";

export type ExtractorData = {
  uuid: string;
  name: string;
  description: string;
  schema: any;
};

const getExtractor = async ({ queryKey }): ExtractorData => {
  const [_, uuid] = queryKey;
  const response = await axios.get(`/extractors/${uuid}`);
  return response.data;
};

const listExtractors = async () => {
  const response = await axios.get("/extractors");
  return response.data;
};

const createExtractor = async (extractor) => {
  const response = await axios.post("/extractors", extractor);
  return response.data;
};

export const runExtraction = async (extractionRequest) => {
  console.log(extractionRequest);
  const response = await axios.postForm("/extract", extractionRequest);
  return response.data;
};

/* API Hooks */

export const useRunExtraction = () => {
  return useMutation({ mutationFn: runExtraction });
}

export const useGetExtractor = (uuid: string) => {
  return useQuery({ queryKey: ["getExtractor", uuid], queryFn: getExtractor });
}


export const useGetExtractors = () => {
  return useQuery({ queryKey: ["getExtractors"], queryFn: listExtractors });
};

export const useDeleteExtractor = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (uuid: string) => axios.delete(`/extractors/${uuid}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["getExtractors"] });
    },
  });
};

export const useCreateExtractor = ({ onSuccess }) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: createExtractor,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ["getExtractors"] });
      onSuccess(data);
    },
  });
};
