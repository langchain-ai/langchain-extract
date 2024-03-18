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
} from '@chakra-ui/react'

import {
  ArrowTopRightOnSquareIcon,
  EllipsisVerticalIcon,
  PencilSquareIcon,
  TrashIcon,
} from '@heroicons/react/24/outline'
import { useMutation } from '@tanstack/react-query'
import axios from 'axios'
import { NavLink, useNavigate } from 'react-router-dom'
import { ShareModal } from './ShareModal'
import { useDeleteExtractor, useGetExtractors } from '../api'
import React from 'react'

const NewIconImported = () => {
  return <Icon as={PencilSquareIcon} />
}

const TrashIconImported = () => {
  return <Icon as={TrashIcon} />
}

const EllipsisIconImported = () => {
  return <Icon as={EllipsisVerticalIcon} />
}

const ArrowTopRightImported = () => {
  return <Icon as={ArrowTopRightOnSquareIcon} />
}

export function Sidebar() {
  const navigate = useNavigate()
  const { isOpen, onClose, onOpen } = useDisclosure()
  const [shareUUID, setShareUUID] = React.useState('' as string)
  const { data } = useGetExtractors()
  const deleteExtractor = useDeleteExtractor()
  const mutateShare = useMutation({
    mutationFn: (uuid: string) => axios.post(`/extractors/${uuid}/share`),
    onSuccess: (data) => {
      console.log(data)
      setShareUUID(data.data.share_uuid)
      onOpen()
    },
  })

  const buttons = data?.map((extractor: any) => {
    return (
      <Flex flexDirection="column" key={extractor.uuid} w="100%">
        <Flex alignItems="center">
          <ChakraLink
            p={1}
            as={NavLink}
            to={`/e/${extractor.uuid}`}
            _activeLink={{
              border: '1px black',
              borderBottomStyle: 'solid',
              borderRadius: 1,
            }}
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
              icon={<EllipsisIconImported />}
              variant="outline"
            />
            <MenuList>
              <MenuItem
                icon={<ArrowTopRightImported />}
                onClick={() => {
                  mutateShare.mutate(extractor.uuid)
                }}
              >
                Share
                {isOpen && (
                  <ShareModal shareUUID={shareUUID} isOpen={isOpen} onClose={onClose}></ShareModal>
                )}
              </MenuItem>
              <MenuItem
                icon={<TrashIconImported />}
                onClick={() => deleteExtractor.mutate(extractor.uuid)}
              >
                Delete
              </MenuItem>
            </MenuList>
          </Menu>
        </Flex>
        <Text p={1} noOfLines={1} color={'gray'}>
          {extractor.description}
        </Text>
      </Flex>
    )
  })

  return (
    <div>
      <VStack>
        <Button
          rightIcon={<NewIconImported />}
          w="80%"
          onClick={() => navigate('/new')}
        >
          New
        </Button>
        <Divider />
        {buttons}
      </VStack>
    </div>
  )
}
