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

const authApiSlice = apiSlice.injectEndpoints ({
    endpoints: builder => ({
        verify: builder.mutation({
            query: ({token}) => ({
                url: 'jwt/verify',
                method: 'POST',
                body: {token},
            }),
        }),
        logout: builder.mutation({
            query: () => ({
                url: '/logout/',
                method: 'POST',
            }),
        }),

    }),
});


export const { 
    useVerifyMutation,
    useLogoutMutation, 
} = authApiSlice;