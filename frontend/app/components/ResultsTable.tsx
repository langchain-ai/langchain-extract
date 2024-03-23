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

import { ExtractionResponse } from "../utils/api";

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null;
}

function getColumns(records: unknown[]): Array<string> {
  // Create a set to store unique keys
  const uniqueKeys = new Set<string>();

  // Iterate over each record in the list
  records.forEach((record) => {
    // For each key in the current record, add it to the set
    if (!isRecord(record)) {
      return;
    }
    Object.keys(record).forEach((key) => {
      if (typeof key === "string") {
        uniqueKeys.add(key);
      }
    });
  });

  // Convert the set back into an array and return it
  return Array.from(uniqueKeys);
}

/*
 * This function takes a value and returns a string representation of it.
 * If the value is an array, it will join the elements with a comma and space.
 * If the value is an object, it will create an array of strings representing
 * each key-value pair, then join them with a comma and space.
 * Otherwise, it will return the string representation of the value.
 * @param value - The value to display
 * @returns The string representation of the value
 */
function getDisplayValue(value: unknown): string {
  if (Array.isArray(value)) {
    return value.map(getDisplayValue).join(", ");
  }
  if (isRecord(value)) {
    // Creating an array of strings representing each key-value pair,
    // then joining them with a comma and space.
    return Object.entries(value)
      .map(([key, val]) => `${key}: ${getDisplayValue(val)}`)
      .join(", ");
  }
  return String(value);
}

export const ResultsTable = ({
  data,
  isPending,
}: {
  data: ExtractionResponse | undefined;
  isPending: boolean;
}) => {
  // scan all the results to determine the columns
  // then display the results in a table
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

  const actualData = data?.data;
  const columns = actualData ? getColumns(actualData) : [];

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
                    // Check if the row has the column,
                    // if not, display an empty cell
                    <Td key={`table-cell-${idx}`}>
                      {isRecord(row) && column in row
                        ? getDisplayValue(row[column])
                        : ""}
                    </Td>
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
