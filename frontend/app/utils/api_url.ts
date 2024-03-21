export const getBaseApiUrl = () => {
  if (process.env.NODE_ENV === "development") {
    return "http://localhost:8000";
  }
  return window.location.origin;
};
