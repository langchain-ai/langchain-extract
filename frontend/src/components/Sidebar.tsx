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
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import axios from "axios";
import { Link, NavLink } from "react-router-dom";
import { listExtractors } from "../api";

interface Props {
  onOpen: Function;
  onClose: Function;
  isOpen: boolean;
}

const NewIconImported = () => {
  return <Icon as={PencilSquareIcon} />;
};

const TrashIconImported = () => {
  return <Icon as={TrashIcon} />;
};

export function Sidebar({ isOpen, onClose }: Props) {
  const queryClient = useQueryClient();
  const { data, isLoading, isError } = useQuery({ queryKey: ["getExtractors"], queryFn: listExtractors });

  const deleteExtractor = useMutation({
    mutationFn: (uuid) => axios.delete(`/extractors/${uuid}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["getExtractors"] });
    },
  });

  const buttons = data?.map((extractor: any) => {
    return (
      <Flex flexDirection="column" key={extractor.uuid} w="100%">
        <Flex alignItems="center">
          <ChakraLink
            p={1}
            as={NavLink}
            to={`/e/${extractor.uuid}`}
            _activeLink={{ border: "1px black", borderBottomStyle: "solid", borderRadius: 1 }}
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
        <Button rightIcon={<NewIconImported />} w="80%">
          New
        </Button>
        <Divider />
        {buttons}
      </VStack>
    </div>
  );
}
