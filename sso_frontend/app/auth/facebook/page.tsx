'use client';

import { Spinner } from "@/components/common";
import { Suspense } from "react";
import SocialAuth from "./SocialAuth";

export default function Page() {
  return (
    <Suspense fallback={<Spinner lg />}>
      <SocialAuth />
      <div className="my-8">
        <Spinner lg />
      </div>
    </Suspense>
  );
}