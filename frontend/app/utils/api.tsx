"use client";
/* Expose API hooks for use in components */
import axios from "axios";
import {
  useQuery,
  useQueryClient,
  useMutation,
  MutationFunction,
  QueryFunctionContext,
} from "@tanstack/react-query";
import { v4 as uuidv4 } from "uuid";
import { getBaseApiUrl } from "./api_url";

type ExtractorData = {
  uuid: string;
  name: string;
  description: string;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  schema: any;
};

const getApiKey = (): string => {
  const key = localStorage.getItem("lc-extract-key");
  if (!key) {
    // Generate key
    const newKey = uuidv4();
    localStorage.setItem("lc-extract-key", newKey);
    return newKey;
  }
  return key;
};

// Create an instance with custom headers
export const axiosClient = axios.create({
  headers: {
    "x-key": getApiKey(),
  },
});

type GetExtractorQueryKey = [string, string, boolean]; // [queryKey, uuid, isShared]

type OnSuccessFn = (data: { uuid: string }) => void;

const getExtractor = async ({
  queryKey,
}: QueryFunctionContext<GetExtractorQueryKey>): Promise<ExtractorData> => {
  const [, uuid, isShared] = queryKey;
  const baseUrl = getBaseApiUrl();
  if (isShared) {
    const response = await axiosClient.get(
      `${baseUrl}/shared/extractors/${uuid}`,
    );
    return response.data;
  } else {
    const response = await axiosClient.get(`${baseUrl}/extractors/${uuid}`);
    return response.data;
  }
};

const listExtractors = async () => {
  const baseUrl = getBaseApiUrl();
  const response = await axiosClient.get(`${baseUrl}/extractors`);
  return response.data;
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const createExtractor: MutationFunction<any, any> = async (extractor) => {
  const baseUrl = getBaseApiUrl();
  const response = await axiosClient.post(`${baseUrl}/extractors`, extractor);
  return response.data;
};

export type ServerConfiguration = {
  available_models: string[];
  max_file_size_mb: number;
  accepted_mimetypes: string[];
};

const getConfiguration = async (): Promise<ServerConfiguration> => {
  const baseUrl = getBaseApiUrl();
  const response = await axiosClient.get(`${baseUrl}/configuration`);
  return response.data;
};

export const useConfiguration = () => {
  return useQuery({
    queryKey: ["getConfiguration"],
    queryFn: getConfiguration,
  });
};

export const suggestExtractor = async ({
  description,
  jsonSchema,
}: {
  description: string;
  jsonSchema: string;
}) => {
  if (description === "") {
    return {};
  }
  const baseUrl = getBaseApiUrl();
  const response = await axiosClient.post(`${baseUrl}/suggest`, {
    description,
    jsonSchema,
  });
  return response.data;
};

type ExtractionRequest = {
  extractor_id: string;
  text?: string;
  file?: File;
};

type ExtractionResponse = {
  data: unknown[];
};

export const runExtraction: MutationFunction<
  ExtractionResponse,
  [ExtractionRequest, boolean]
> = async ([extractionRequest, isShared]) => {
  const endpoint = isShared ? "extract/shared" : "extract";
  const baseUrl = getBaseApiUrl();
  const response = await axiosClient.postForm(
    `${baseUrl}/${endpoint}`,
    extractionRequest,
  );
  return response.data;
};

export const useRunExtraction = () => {
  return useMutation({ mutationFn: runExtraction });
};

export const useGetExtractor = (uuid: string, isShared: boolean) => {
  return useQuery({
    queryKey: ["getExtractor", uuid, isShared],
    queryFn: getExtractor,
  });
};

export const useGetExtractors = () => {
  return useQuery({ queryKey: ["getExtractors"], queryFn: listExtractors });
};

export const useDeleteExtractor = () => {
  const baseUrl = getBaseApiUrl();
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (uuid: string) =>
      axiosClient.delete(`${baseUrl}/extractors/${uuid}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["getExtractors"] });
    },
  });
};

export const useCreateExtractor = ({
  onSuccess,
}: {
  onSuccess: OnSuccessFn;
}) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: createExtractor,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ["getExtractors"] });
      onSuccess(data);
    },
  });
};
