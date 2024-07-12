import { useSocialAuth } from "@/hooks";
import { useSocialAuthenticateMutation } from "@/redux/features/authApiSlice";

export default function SocialAuth() {
  const [googleAuthenticate] = useSocialAuthenticateMutation();
  useSocialAuth(googleAuthenticate, 'google-oauth2');
  return null;
}