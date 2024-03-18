"use client";

import { ToastContainer } from "react-toastify";
import CreateExtractor from "./components/CreateExtractor";

import { ChakraProvider } from "@chakra-ui/react";

export default function Home() {
  return (
    <ChakraProvider>
      <ToastContainer />
      <CreateExtractor />
    </ChakraProvider>
  );
}
