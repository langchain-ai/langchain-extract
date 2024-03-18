import { Tab, TabList, TabPanel, TabPanels, Tabs, Text } from '@chakra-ui/react'
import Form from '@rjsf/chakra-ui'
import validator from '@rjsf/validator-ajv8'
import { useGetExtractor } from '../api'

import { VStack } from '@chakra-ui/react'
import SyntaxHighlighter from 'react-syntax-highlighter'
import { docco } from 'react-syntax-highlighter/dist/esm/styles/hljs'

export const Extractor = ({ extractorId }: { extractorId: string }) => {
  const { data, isLoading, isError } = useGetExtractor(extractorId)
  if (isLoading) {
    return <div>Loading...</div>
  }
  if (isError) {
    return <div>Error</div>
  }

  if (data === undefined) {
    throw new Error('Data is undefined')
  }
  console.log(data.schema)

  return (
    <div className="mr-auto">
      <Tabs className="mt-5" variant={'enclosed'} colorScheme="blue" size="sm">
        <TabList>
          <Tab>Form</Tab>
          <Tab>Code</Tab>
        </TabList>
        <TabPanels>
          <TabPanel>
            <Form
              schema={data.schema}
              validator={validator}
              children={true} // Hide the submit button
            />
          </TabPanel>
          <TabPanel>
            <Text className="mt-1 mb-5">
              This shows the raw JSON Schema that describes what information the
              extractor will be extracting from the content.
            </Text>
            <SyntaxHighlighter language="json" style={docco}>
              {JSON.stringify(data.schema, null, 2)}
            </SyntaxHighlighter>
          </TabPanel>
        </TabPanels>
      </Tabs>
      <VStack align={'left'}>
        {/* TO DO ADD SYSTEM MESSAGE */}
        {/* <Text>
          <strong>System Message: </strong>
          {data.instruction}
        </Text> */}
      </VStack>
    </div>
  )
}
