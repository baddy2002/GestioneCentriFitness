import { useSocialAuth } from "@/hooks";
import { useSocialAuthenticateMutation } from "@/redux/features/authApiSlice";

export default function SocialAuth() {
  const [facebookAuthenticate] = useSocialAuthenticateMutation();
  useSocialAuth(facebookAuthenticate, 'facebook');
  return null;
}