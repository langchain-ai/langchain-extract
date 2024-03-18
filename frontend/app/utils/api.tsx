/* Expose API hooks for use in components */
import axios from "axios";
import { useQuery, useQueryClient, useMutation, MutationFunction, QueryFunctionContext } from "@tanstack/react-query";

export type ExtractorData = {
  uuid: string;
  name: string;
  description: string;
  schema: any;
};

type GetExtractorQueryKey = [string, string]; // [queryKey, uuid]

type OnSuccessFn = (data: { uuid: string }) => void;

const getExtractor = async ({ queryKey }: QueryFunctionContext<GetExtractorQueryKey>): Promise<ExtractorData> => {
  const [_, uuid] = queryKey;
  const response = await axios.get(`/extractors/${uuid}`);
  return response.data;
};

const listExtractors = async () => {
  const response = await axios.get("/extractors");
  return response.data;
};

const createExtractor: MutationFunction<any, any> = async (extractor) => {
  const response = await axios.post("/extractors", extractor);
  return response.data;
};

export const suggestExtractor = async ({ description, jsonSchema }: { description: string, jsonSchema: string }) => {
  if (description === "") {
    return {};
  }
  const response = await axios.post("/suggest", { description, jsonSchema });
  return response.data;
};

export const runExtraction: MutationFunction<any, any> = async (extractionRequest) => {
  const response = await axios.postForm("/extract", extractionRequest);
  return response.data;
};

export const useRunExtraction = () => {
  return useMutation({ mutationFn: runExtraction });
};

export const useGetExtractor = (uuid: string) => {
  return useQuery({ queryKey: ["getExtractor", uuid], queryFn: getExtractor });
};

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

export const useCreateExtractor = ({ onSuccess }: { onSuccess: OnSuccessFn }) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: createExtractor,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ["getExtractors"] });
      onSuccess(data);
    },
  });
};
