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
        retrieveUser: builder.query<User, void>({
            query: () => '/users/me/',
            
        }),
        retrieveUserComplete: builder.query<UserComplete, void>({
            query: () => '/complete/',
            
        }),
        ModifyUserComplete: builder.mutation({
            query: ({id, email, first_name, last_name, data_iscrizione, photo} ) => ({
                url: '/complete/',
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: {id, email, first_name, last_name, data_iscrizione, photo}
            }),
            
        }),
        socialAuthenticate: builder.mutation<CreateUserResponse, SocialAuthArgs> ({
            query: ({provider, state, code }) => ({
                url: `o/${provider}/?state=${encodeURIComponent(state)}&code=${encodeURIComponent(code)}`,
                method: 'POST',
                headers: {
                    Accept: 'application/json',
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
            }),
        }),
        login: builder.mutation({
            query: ({ email, password }) => ({
                url: '/jwt/create',
                method: 'POST',
               body: {email, password}
            }),
        }),
        register: builder.mutation({
            query: ({ first_name, email, password, re_password }) => ({
                url: '/users/',
                method: 'POST',
               body: {first_name, email, password, re_password}
            }),
        }),
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
        activation: builder.mutation({
            query: ({uid, token}) => ({
                url: 'users/activation/',
                method: 'POST',
                body: {uid, token},
            }),
        }),
        resetPassword: builder.mutation({
            query: ({email}) => ({
                url: '/users/reset_password/',
                method: 'POST',
                body: {email},
            }),
        }),
        resetPasswordConfirmUrl: builder.mutation({
            query: ({uid, token, new_password, re_new_password }) => ({
                url: '/users/reset_password_confirm/',
                method: 'POST',
                body: {uid, token, new_password, re_new_password},
            }),
        }),
    }),
});


export const { 
    useRetrieveUserQuery,
    useRetrieveUserCompleteQuery,
    useModifyUserCompleteMutation,
    useSocialAuthenticateMutation,
    useLoginMutation,
    useRegisterMutation,
    useVerifyMutation,
    useLogoutMutation, 
    useActivationMutation,
    useResetPasswordMutation,
    useResetPasswordConfirmUrlMutation,
} = authApiSlice;