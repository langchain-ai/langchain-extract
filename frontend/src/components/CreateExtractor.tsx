import { Button, FormControl, FormHelperText, FormLabel, Input } from "@chakra-ui/react";
import { json } from "@codemirror/lang-json";
import { LanguageSupport } from "@codemirror/language";
import CodeMirror from "@uiw/react-codemirror";
import React from "react";
import { useNavigate } from "react-router-dom";
import { useCreateExtractor } from "../api";
import { Heading } from "./Heading";

const EXTENSIONS: { [key: string]: LanguageSupport[] } = {
  json: [json()],
};

const SCHEMA = `
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Chemical Element",
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "description": "The full name of the element."
    },
    "symbol": {
      "type": "string",
      "description": "The one or two-letter symbol of the element."
    },
    "atomicNumber": {
      "type": "integer",
      "description": "The atomic number of the element."
    },
    "atomicWeight": {
      "type": "number",
      "description": "The standard atomic weight of the element."
    },
    "category": {
      "type": "string",
      "description": "The category of the element (e.g., noble gas, alkali metal, etc.)."
    },
    "stateAtRoomTemperature": {
      "type": "string",
      "description": "The state of the element at room temperature (solid, liquid, or gas)."
    },
    "electronConfiguration": {
      "type": "string",
      "description": "The electron configuration of the element."
    },
    "electronegativity": {
      "type": "number",
      "description": "The Pauling electronegativity of the element."
    },
    "firstIonizationEnergy": {
      "type": "number",
      "description": "The energy required to remove the outermost electron."
    },
    "density": {
      "type": "number",
      "description": "The density of the element at room temperature."
    }
  },
  "required": ["name", "symbol", "atomicNumber", "atomicWeight", "category", "stateAtRoomTemperature"]
}
`;

/**
 * Component to create a new extractor with fields for name, description, schema, and examples
 */
const CreateExtractor = ({}) => {
  // You might use a mutation hook here if you're using something like React Query for state management
  const [schema, setSchema] = React.useState(SCHEMA);
  const navigate = useNavigate();
  const { mutate, isLoading } = useCreateExtractor({
    onSuccess: (data) => {
      navigate(`/e/${data.uuid}`);
    },
  });

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const name = data.get("name") as string;
    const description = data.get("description") as string;
    const instruction = data.get("instruction") as string;
    const dict_schema = JSON.parse(schema);
    mutate({ name, description, schema: dict_schema, instruction });
  };

  return (
    <div className="w-4/5 m-auto">
      <Heading>Create New Extractor</Heading>
      <form className="m-auto flex flex-col content-between gap-5 mt-10" onSubmit={handleSubmit}>
        {/* <input type="text" name="name" placeholder="Name" className="input input-bordered" required /> */}
        <FormControl id="name" isRequired>
          <FormLabel>Name</FormLabel>
          <Input name="name" autoFocus defaultValue="Unnamed" />
          <FormHelperText>Enter a name for the extractor</FormHelperText>
        </FormControl>
        <FormControl id="description" isRequired>
          <FormLabel>Description</FormLabel>
          <Input name="description" />
          <FormHelperText>Enter a description for the extractor</FormHelperText>
        </FormControl>
        <FormControl id="instruction" isRequired>
          <FormLabel>Instructions</FormLabel>
          <Input name="instruction" />
          <FormHelperText>Enter instructions for the LLM on how to use the extractor</FormHelperText>
        </FormControl>
        <FormControl>
          <FormLabel htmlFor="schema">JSON Schema</FormLabel>
          <CodeMirror
            id="schema"
            value={schema}
            onChange={(value) => setSchema(value)}
            basicSetup={{ autocompletion: true }}
            extensions={[json()]}
            minHeight="300px"
            className="border-4 border-slate-300 border-double"
          ></CodeMirror>
        </FormControl>
        <Button className="btn" type="submit">
          Create
        </Button>
      </form>
    </div>
  );
};

export default CreateExtractor;
