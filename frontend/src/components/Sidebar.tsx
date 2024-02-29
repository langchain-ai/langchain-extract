import { Button, Drawer, DrawerBody, DrawerContent, DrawerOverlay, VStack } from "@chakra-ui/react";
import { PencilSquareIcon } from "@heroicons/react/24/outline";
import { Link as ReactRouterLink, Navigate } from "react-router-dom";
import { useNavigate } from "react-router-dom";

interface Props {
  onOpen: Function;
  onClose: Function;
  isOpen: boolean;
}

export function Sidebar({ isOpen, onOpen, onClose }: Props) {
  const navigate = useNavigate();
  const url = '/e/e175194a-d9ae-44df-b6bd-c025a4309943'

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
              <Button w="100%" onClick={ () => (navigate({to: url}))}>
                Extractor A
              </Button>
              <Button w="100%">Extractor 2</Button>
              <Button w="100%"></Button>
            </VStack>
          </DrawerBody>
        </DrawerContent>
      </Drawer>
    </>
  );
}
