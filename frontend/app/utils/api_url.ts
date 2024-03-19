export const getBaseApiUrl = () => {
  if (process.env.NODE_ENV === "development") {
    return "http://localhost:8000";
  }
  if (!process.env.BASE_API_URL) {
    throw new Error("BASE_API_URL must be set if not in development.");
  }
  return process.env.BASE_API_URL;
};
