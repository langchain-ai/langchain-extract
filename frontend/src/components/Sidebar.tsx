import {
  Button,
  Drawer,
  DrawerBody,
  DrawerContent,
  DrawerOverlay,
  VStack
} from "@chakra-ui/react";
import { MdModeEditOutline } from "react-icons/md";

interface Props {
  onOpen: Function;
  onClose: Function;
  isOpen: boolean;
}

export function Sidebar({ isOpen, onOpen, onClose }: Props) {
  return (
    <>
      {/* <RadioGroup defaultValue={placement} onChange={setPlacement}>
        <Stack direction="row" mb="4">
          <Radio value="top">Top</Radio>
          <Radio value="right">Right</Radio>
          <Radio value="bottom">Bottom</Radio>
          <Radio value="left">Left</Radio>
        </Stack>
      </RadioGroup> */}
      {/* <Button rightIcon={<CgDetailsMore/>} onClick={onOpen} w="100%">
      </Button> */}
      <Drawer placement={"left"} variant="sidebar" onClose={onClose} isOpen={isOpen}>
        <DrawerOverlay />
        <DrawerContent>
          <DrawerBody>
            <VStack gap={5}>
              <Button w="100%" rightIcon={<MdModeEditOutline />}>
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
