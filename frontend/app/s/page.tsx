"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useEffect } from "react";
import { Playground } from "../components/Playground";

export default function Page() {
  const searchParams = useSearchParams();
  const { push } = useRouter();
  const sharedExtractorId = searchParams.get("sharedExtractorId");

  useEffect(() => {
    if (typeof window === "undefined") return;
    if (!sharedExtractorId) {
      push("/");
    }
  }, [sharedExtractorId]);

  if (!sharedExtractorId) {
    return <div>Loading...</div>;
  }

  return <Playground extractorId={sharedExtractorId} isShared={true} />;
}
