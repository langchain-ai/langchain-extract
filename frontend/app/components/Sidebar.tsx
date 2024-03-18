"use client";

import {
  Icon,
  Button,
  Link as ChakraLink,
  Divider,
  Flex,
  IconButton,
  Spacer,
  Text,
  Tooltip,
  VStack,
} from "@chakra-ui/react";
import { PencilSquareIcon, TrashIcon } from "@heroicons/react/24/outline";
import { useRouter } from "next/navigation";
import { useDeleteExtractor, useGetExtractors } from "../utils/api";

const NewIconImported = () => {
  return <Icon as={PencilSquareIcon} />;
};

const TrashIconImported = () => {
  return <Icon as={TrashIcon} />;
};

export function Sidebar() {
  const { push } = useRouter();
  const { data } = useGetExtractors();
  const deleteExtractor = useDeleteExtractor();

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const buttons = data?.map((extractor: any) => {
    return (
      <Flex flexDirection="column" key={extractor.uuid} w="100%">
        <Flex alignItems="center">
          <ChakraLink
            p={1}
            onClick={() => push(`/e/${extractor.uuid}`)} // Use push for navigation
            _hover={{
              textDecoration: "none",
            }}
            _activeLink={{
              border: "1px black",
              borderBottomStyle: "solid",
              borderRadius: 1,
            }}
            cursor="pointer" // Add cursor pointer to indicate it's clickable
          >
            <Text noOfLines={1}>
              <strong>{extractor.name}</strong>
            </Text>
          </ChakraLink>
          <Spacer />
          <Tooltip label="Delete" fontSize="md">
            <IconButton
              icon={<TrashIconImported />}
              aria-label="Delete Extractor"
              variant="outline"
              size="sm"
              onClick={() => {
                deleteExtractor.mutate(extractor.uuid);
              }}
            />
          </Tooltip>
        </Flex>
        <Text p={1} noOfLines={1} color={"gray"}>
          {extractor.description}
        </Text>
      </Flex>
    );
  });

  return (
    <div>
      <VStack>
        <Button
          rightIcon={<NewIconImported />}
          w="80%"
          onClick={() => push("/new")}
        >
          New
        </Button>
        <Divider />
        {buttons}
      </VStack>
    </div>
  );
}
