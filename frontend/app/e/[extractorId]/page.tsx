"use client";

import { Playground } from "../../components/Playground";

interface ExtractorPageProps {
  params: {
    extractorId: string;
  };
}

export default function Page({ params }: ExtractorPageProps) {
  return <Playground extractorId={params.extractorId} />;
}
