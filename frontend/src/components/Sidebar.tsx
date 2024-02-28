import { Button, Drawer, DrawerBody, DrawerContent, DrawerOverlay, VStack } from "@chakra-ui/react";
import { PencilSquareIcon } from "@heroicons/react/24/outline";

interface Props {
  onOpen: Function;
  onClose: Function;
  isOpen: boolean;
}

export function Sidebar({ isOpen, onOpen, onClose }: Props) {
  return (
    <>
      <Drawer placement={"left"} variant="sidebar" onClose={onClose} isOpen={isOpen}>
        <DrawerOverlay />
        <DrawerContent>
          <DrawerBody>
            <VStack gap={5}>
              <Button w="100%" rightIcon={<PencilSquareIcon />}>
                New
              </Button>
              <Button w="100%">Extractor A</Button>
              <Button w="100%">Extractor 2</Button>
              <Button w="100%"></Button>
            </VStack>
          </DrawerBody>
        </DrawerContent>
      </Drawer>
    </>
  );
}
