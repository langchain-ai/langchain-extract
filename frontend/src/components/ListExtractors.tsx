import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import axios from "axios";
import React from "react";
import { listExtractors } from "../api";

export const ListExtractors = ({ onSelect }) => {
  const queryClient = useQueryClient();
  const { data: extractors, isLoading, isError } = useQuery({ queryKey: ["getExtractors"], queryFn: listExtractors });

  const deleteExtractor = useMutation({
    mutationFn: (uuid) => axios.delete(`/extractors/${uuid}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["getExtractors"] });
    },
  });

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (isError) {
    return <div>Error</div>;
  }

  return (
    <div className="flex-col justify-between h-full">
      <ul className="mt-5">
        {extractors?.map((extractor: any) => {
          return (
            <li key={extractor.uuid} className="hover:bg-slate-100 p-3" onClick={onSelect.bind(null, extractor.uuid)}>
              {extractor.uuid}
              {extractor.name}
              {/* <button onClick={() => deleteExtractor.mutate(extractor.uuid)}>Delete</button> */}
            </li>
          );
        }
        )}
      </ul>
  </div>
  );
};
