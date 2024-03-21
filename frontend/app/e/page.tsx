"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useSearchParams } from "next/navigation";
import { Playground } from "../components/Playground";

export default function Page() {
  const searchParams = useSearchParams();
  const { push } = useRouter();
  const extractorId = searchParams.get("extractorId");

  useEffect(() => {
    if (typeof window === "undefined") return;
    if (!extractorId) {
      push("/new");
    }
  }, [extractorId]);

  if (!extractorId) {
    return <div>Loading...</div>;
  }

  return <Playground extractorId={extractorId} isShared={false} />;
}
