import React from "react";
import { Heading } from "./Heading";

/**
 * Component to create a new extractor with fields for name, description, schema, and examples
 */
const CreateExtractor = ({ }) => {
  // You might use a mutation hook here if you're using something like React Query for state management
  // const { mutate, isLoading } = useMutation({ mutationFn: createExtractorFunction });
  return (
    <div className="w-4/5 m-auto">
      <Heading>Create New Extractor</Heading>
      <form className="m-auto flex flex-col content-between gap-5 mt-10">
        <input type="text" name="name" placeholder="Name" className="input input-bordered" required />
        <textarea name="description" placeholder="Description" className="textarea textarea-bordered h-1/4" required />
        <textarea name="schema" placeholder="Schema" className="textarea textarea-bordered h-1/4" required />
        <textarea name="examples" placeholder="Examples" className="textarea textarea-bordered h-1/4" required />
        <button className="btn" type="submit">
          Create
        </button>
      </form>
    </div>
  );
};

export default CreateExtractor