import {
  Spacer,
  Flex,
  Link,
  Button,
  Drawer,
  DrawerBody,
  DrawerContent,
  DrawerOverlay,
  VStack,
  HStack,
  IconButton,
  Divider,
  MenuDivider,
  Text,
} from "@chakra-ui/react";
import { PencilSquareIcon, TrashIcon } from "@heroicons/react/24/outline";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { listExtractors } from "../api";

interface Props {
  onOpen: Function;
  onClose: Function;
  isOpen: boolean;
}

export const ListExtractors = ({ onSelect }) => {
  const { data: extractors, isLoading, isError } = useQuery({ queryKey: ["getExtractors"], queryFn: listExtractors });

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (isError) {
    return <div>Error</div>;
  }

  return (
    <div className="flex-col justify-between h-full">
      <ul className="mt-5">
        {extractors?.map((extractor: any) => {
          return (
            <li key={extractor.uuid} className="hover:bg-slate-100 p-3" onClick={onSelect.bind(null, extractor.uuid)}>
              {extractor.uuid}
              {extractor.name}
              {/* <button onClick={() => deleteExtractor.mutate(extractor.uuid)}>Delete</button> */}
            </li>
          );
        })}
      </ul>
    </div>
  );
};

export function Sidebar({ isOpen, onOpen, onClose }: Props) {
  const queryClient = useQueryClient();
  const navigate = useNavigate();
  const { data, isLoading, isError } = useQuery({ queryKey: ["getExtractors"], queryFn: listExtractors });

  const deleteExtractor = useMutation({
    mutationFn: (uuid) => axios.delete(`/extractors/${uuid}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["getExtractors"] });
    },
  });

  const buttons = data?.map((extractor: any) => {
    return (
      <Flex flexDirection="column" key={extractor.uuid} width="90%">
        <Flex alignItems="center">
          <Link w="100%" onClick={() => navigate(`/e/${extractor.uuid}`)}>
            <strong>{extractor.name}</strong>
          </Link>
          <Spacer />
          <IconButton
            icon={<TrashIcon />}
            aria-label="Delete Extractor"
            size="sm"
            onClick={() => {
              deleteExtractor.mutate(extractor.uuid);
            }}
          />
        </Flex>
        <Text noOfLines={1} color={"gray"}>
          {extractor.description}
        </Text>
      </Flex>
    );
  });

  return (
    <>
      <Drawer placement={"left"} variant="sidebar" onClose={onClose} isOpen={isOpen}>
        <DrawerOverlay />
        <DrawerContent>
          <DrawerBody>
            <VStack gap={5} marginTop={5}>
              <Button w="100%" rightIcon={<PencilSquareIcon />}>
                New
              </Button>
              <Divider />
              {buttons}
            </VStack>
          </DrawerBody>
        </DrawerContent>
      </Drawer>
    </>
  );
}
