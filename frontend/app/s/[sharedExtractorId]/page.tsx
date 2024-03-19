"use client";

import { Playground } from "../../components/Playground";

interface ExtractorPageProps {
  params: {
    sharedExtractorId: string;
  };
}

export default function Page({ params }: ExtractorPageProps) {
  return <Playground extractorId={params.sharedExtractorId} isShared={true} />;
}
