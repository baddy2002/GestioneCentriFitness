import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import type {
  BaseQueryFn,
  FetchArgs,
  FetchBaseQueryError,
} from '@reduxjs/toolkit/query'
import { setAuth, logout } from '@/redux/features/authSlices'
import { Mutex } from 'async-mutex'


// create a new mutex
const mutex = new Mutex()
const baseQuery = fetchBaseQuery({ 
    baseUrl: `${process.env.NEXT_PUBLIC_SSO}/api`,
    credentials: 'include',
})
const centerQuery = fetchBaseQuery({ 
    baseUrl: `${process.env.NEXT_PUBLIC_HOST}/api`,
    credentials: 'include',
})
const baseQueryWithReauth: BaseQueryFn<
  string | FetchArgs,
  unknown,
  FetchBaseQueryError
> = async (args, api, extraOptions) => {
  // wait until the mutex is available without locking it
  await mutex.waitForUnlock()
  let result = await centerQuery(args, api, extraOptions)
  if (result.error && result.error.status === 401) {
    // checking whether the mutex is locked
    if (!mutex.isLocked()) {
      const release = await mutex.acquire()
      try {
        const refreshResult = await baseQuery(
          {
            url: '/jwt/refresh',
            method: 'POST'
          },
          api,
          extraOptions
        )
        if (refreshResult.data) {
          api.dispatch(setAuth(null))
          result = await baseQuery(args, api, extraOptions)
        } else {
          api.dispatch(logout())
        }
      } finally {
        // release must be called once the mutex should be released again.
        release()
      }
    } else {
      // wait until the mutex is available without locking it
      await mutex.waitForUnlock()
      result = await baseQuery(args, api, extraOptions)
    }
  }
  return result
}


export const centerApiSlice = createApi({
    reducerPath: 'centerApi',
    baseQuery: baseQueryWithReauth,
    endpoints: builder => ({}),
});