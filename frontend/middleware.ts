import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { v4 as uuidv4 } from "uuid";

// Automatically set a 'user_id' cookie if one doesn't exist
// This function will run on every page request, so we can
// guarantee that a 'user_id' cookie will always be set.
const USER_ID_COOKIE_KEY = "user_id";

export function middleware(request: NextRequest) {
  const response = NextResponse.next();
  const userId = request.cookies.get(USER_ID_COOKIE_KEY);

  if (!userId) {
    response.cookies.set(USER_ID_COOKIE_KEY, uuidv4(), {
      maxAge: 60 * 60 * 24 * 365, // 1 year
      sameSite: "strict",
      path: "/",
      httpOnly: true,
    });
  }
  return response;
}
