import {
  Spinner,
  Table,
  TableCaption,
  TableContainer,
  Tbody,
  Td,
  Th,
  Thead,
  Tr,
} from "@chakra-ui/react";

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function getColumns(records: Array<Record<string, any>>): Array<any> {
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
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  data: { data: Array<Record<string, any>> } | undefined;
  isPending: boolean;
}) => {
  // scan all the results to determine the columns
  // then display the results in a table
  const actualData = data?.data;
  const columns = actualData ? getColumns(actualData) : [];

  if (isPending) {
    return (
      <Spinner
        thickness="4px"
        speed="0.65s"
        emptyColor="gray.200"
        color="blue.500"
        size="xl"
      />
    );
  }

  return (
    <div>
      <TableContainer>
        <Table>
          <TableCaption>Extraction Results</TableCaption>
          <Thead>
            <Tr>
              {columns.map((column, idx) => (
                <Th key={`table-header-${idx}`}>{column}</Th>
              ))}
            </Tr>
          </Thead>
          <Tbody>
            {actualData?.map((row, index) => {
              return (
                <Tr key={index}>
                  {columns.map((column, idx) => (
                    <Td key={`table-data-${idx}`}>{row[column]}</Td>
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
