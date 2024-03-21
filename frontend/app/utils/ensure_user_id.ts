import Cookie from "js-cookie";
import { v4 as uuidv4 } from 'uuid';

const USER_ID_COOKIE_KEY = "user_id";

export function ensureUserId() {
  const userId = Cookie.get(USER_ID_COOKIE_KEY);

  if (!userId) {
    const newUserId = uuidv4();
    Cookie.set(USER_ID_COOKIE_KEY, newUserId, {
      httpOnly: true,
      sameSite: 'strict',
      path: '/',
    });
  }
}