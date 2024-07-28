import { List } from "postcss/lib/list";
import { apiSlice } from "../services/appSlices";

interface User{
    first_name: string;
    email: string;
};

interface UserComplete{
    id: string;
    email: string;
    first_name: string;
    last_name: string;
    data_iscrizione: string;
    photo: string;
    group: string;
};

interface SocialAuthArgs{
    provider: string;
    state: string;
    code: string;
};

interface CreateUserResponse{
    success: boolean;
    user: User;
};
type UserRole = 'admin' | 'manager' | 'nutritionist' | 'trainer' | 'customer';
interface Group{
    groups: UserRole[];
};

interface Photo{
    photo: string;
};

const authApiSlice = apiSlice.injectEndpoints ({
    endpoints: builder => ({
        logout: builder.mutation({
            query: () => ({
                url: '/logout/',
                method: 'POST',
            }),
        }),
        verify: builder.mutation<void, void>({
            query: () => ({
                url: 'jwt/verify',
                method: 'POST',
            }),
        }),
        userPhoto: builder.query<Photo, void>({
            query: () => ({
                url: '/informations/photo',
            }),
        }),
        userGroups: builder.query<Group, void>({
            query: () => ({
                url: '/informations/groups',
            }),
        }),
        retrieveUserComplete: builder.query<UserComplete, void>({
            query: () => '/informations/complete',
            
        }),
    }),
});


export const { 
    useLogoutMutation, 
    useVerifyMutation,
    useUserGroupsQuery,
    useUserPhotoQuery,
    useRetrieveUserCompleteQuery
} = authApiSlice