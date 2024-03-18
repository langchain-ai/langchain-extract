import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  Text,
  Link,
  Input,
  ModalCloseButton,
  useDisclosure,
  useClipboard,
  Flex,
  Button,
} from '@chakra-ui/react'

export function ShareModal({ shareUUID, isOpen, onClose }) {
  const url = `${window.origin}/s/${shareUUID}`
  const { onCopy, hasCopied } = useClipboard(shareUUID)

  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      {/* <ModalOverlay /> */}
      <ModalContent>
        <ModalHeader>Share Link</ModalHeader>
        <ModalCloseButton />
        <ModalBody>
          <Text>
            You can share this link with others to give them access to your
            extractor:
          </Text>
          <Flex mb={2}>
            <Input value={url} isReadOnly="true" />
            <Button onClick={onCopy}>{hasCopied ? 'Copied!' : 'Copy'}</Button>
          </Flex>
        </ModalBody>

        <ModalFooter>
          <Button colorScheme="blue" mr={3} onClick={onClose}>
            Close
          </Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  )
}
