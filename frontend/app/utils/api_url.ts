export const getBaseApiUrl = () => {
  if (process.env.NODE_ENV === "development") {
    return "http://localhost:8000";
  }

  // If not defined assume assume served from same domain
  return "./";
};
