import { Spinner, Table, TableCaption, TableContainer, Tbody, Td, Th, Thead, Tr } from "@chakra-ui/react";
import { useClipboard } from '@chakra-ui/react'

function getColumns(records: object[]) {
  // Create a set to store unique keys
  const uniqueKeys = new Set();

  // Iterate over each record in the list
  records.forEach((record) => {
    // For each key in the current record, add it to the set
    Object.keys(record).forEach((key) => {
      uniqueKeys.add(key);
    });
  });

  // Convert the set back into an array and return it
  return Array.from(uniqueKeys);
}

export const ResultsTable = ({
  data,
  isPending,
}: {
  data: { data: object[] } | undefined;
  isPending: boolean;
}) => {
  // scan all the results to determine the columns
  // then display the results in a table
  const actualData = data?.data;
  const { onCopy, value, setValue, hasCopied } = useClipboard("");
  const columns = actualData ? getColumns(actualData) : [];

  if (isPending) {
    return <Spinner thickness="4px" speed="0.65s" emptyColor="gray.200" color="blue.500" size="xl" />;
  }

  return (
    <div>
      <TableContainer>
        <Table>
          <TableCaption>Extraction Results</TableCaption>
          <Thead>
            <Tr>
              {columns.map((column) => (
                <Th>{column}</Th>
              ))}
            </Tr>
          </Thead>
          <Tbody>
            {actualData?.map((row, index) => {
              return (
                <Tr key={index}>
                  {columns.map((column) => (
                    <Td>{row[column]}</Td>
                  ))}
                </Tr>
              );
            })}
          </Tbody>
        </Table>
      </TableContainer>
    </div>
  );
};
