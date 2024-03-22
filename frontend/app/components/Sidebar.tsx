"use client";

import {
  Button,
  Link as ChakraLink,
  Divider,
  Flex,
  Icon,
  IconButton,
  Menu,
  MenuButton,
  MenuItem,
  MenuList,
  Spacer,
  Text,
  VStack,
  useDisclosure,
} from "@chakra-ui/react";
import React from "react";
import {
  ArrowTopRightOnSquareIcon,
  EllipsisVerticalIcon,
  PencilSquareIcon,
  TrashIcon,
} from "@heroicons/react/24/outline";
import { useRouter, useParams } from "next/navigation";
import { useMutation } from "@tanstack/react-query";
import {
  useDeleteExtractor,
  useGetExtractors,
  axiosClient,
} from "../utils/api";
import { getBaseApiUrl } from "../utils/api_url";
import { ShareModal } from "./ShareModal";

export function Sidebar() {
  const [shareUUID, setShareUUID] = React.useState("");
  const params = useParams();
  const currentExtractorId = params.extractorId;

  const { isOpen, onClose, onOpen } = useDisclosure();
  const { push } = useRouter();
  const { data } = useGetExtractors();
  const deleteExtractor = useDeleteExtractor();

  const baseUrl = getBaseApiUrl();
  const mutateShare = useMutation({
    mutationFn: async (uuid: string) =>
      axiosClient.post(`${baseUrl}/extractors/${uuid}/share`),
    onSuccess: (onSuccessData) => {
      setShareUUID(onSuccessData.data.share_uuid);
      onOpen();
    },
  });

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const buttons = data?.map((extractor: any) => {
    const selectedProps =
      extractor.uuid === currentExtractorId
        ? {
            borderLeft: "4px solid gray",
            borderRadius: "4px",
            padding: "4px",
          }
        : {};
    return (
      <Flex
        flexDirection="column"
        key={extractor.uuid}
        w="100%"
        {...selectedProps}
      >
        <Flex alignItems="center">
          <ChakraLink
            p={1}
            onClick={() => push(`/e/${extractor.uuid}`)}
            cursor="pointer"
          >
            <Text noOfLines={1}>
              <strong>{extractor.name}</strong>
            </Text>
          </ChakraLink>
          <Spacer />
          <Menu>
            <MenuButton
              as={IconButton}
              aria-label="Options"
              icon={<Icon as={EllipsisVerticalIcon} />}
              variant="outline"
            />
            <MenuList>
              <MenuItem
                icon={<Icon as={ArrowTopRightOnSquareIcon} />}
                onClick={() => {
                  mutateShare.mutate(extractor.uuid);
                }}
              >
                Share
                {isOpen && (
                  <ShareModal
                    shareUUID={shareUUID}
                    isOpen={isOpen}
                    onClose={onClose}
                  />
                )}
              </MenuItem>
              <MenuItem
                icon={<Icon as={TrashIcon} />}
                onClick={() => deleteExtractor.mutate(extractor.uuid)}
              >
                Delete
              </MenuItem>
            </MenuList>
          </Menu>
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
          rightIcon={<Icon as={PencilSquareIcon} />}
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
