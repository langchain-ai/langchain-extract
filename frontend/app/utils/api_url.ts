export const getBaseApiUrl = () => {
  if (process.env.NODE_ENV === "development") {
    return "http://localhost:8000";
  }
  if (!process.env.NEXT_PUBLIC_BASE_API_URL) {
    throw new Error(
      "NEXT_PUBLIC_BASE_API_URL must be set if not in development.",
    );
  }
  return process.env.NEXT_PUBLIC_BASE_API_URL;
};
