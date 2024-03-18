import { ChakraProvider, useDisclosure } from '@chakra-ui/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import React from 'react'
import { BrowserRouter, Outlet, Route, Routes } from 'react-router-dom'
import CreateExtractor from './components/CreateExtractor'
import { Playground } from './components/Playground'
import { Sidebar } from './components/Sidebar'
import './index.css'

const queryClient = new QueryClient()

const Root = () => {
  const { isOpen, onOpen, onClose } = useDisclosure()

  return (
    <>
      <div className="flex flex-col w-100% h-full">
        <div className="flex justify-between bg-slate-200 mb-4 p-3 items-center gap-2">
          <div className="font-semibold">🦜⛏️ LangChain Extract</div>
          <div className="text-s text-rose-800">
            <strong>Research Preview</strong>: this app is unauthenticated and
            all data can be found. Do not use with sensitive data.
          </div>
        </div>
        <div className="flex gap-3 ml-5 mr-5">
          <div className="w-1/6">
            <Sidebar isOpen={isOpen} onOpen={onOpen} onClose={onClose} />
          </div>
          <div className="m-auto w-5/6">
            <Outlet />
          </div>
        </div>
      </div>
    </>
  )
}

const Main = () => {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route element={<Root />}>
            <Route path="/" element={<CreateExtractor />} />
            <Route path="/e/:extractorId" element={<Playground />} />
            <Route path="/new" element={<CreateExtractor />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </>
  )
}

const App = () => {
  return (
    <React.StrictMode>
      <QueryClientProvider client={queryClient}>
        <ChakraProvider>
          <Main />
        </ChakraProvider>
      </QueryClientProvider>
    </React.StrictMode>
  )
}

export default App
