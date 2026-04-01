export function useAuth() {
  const client = useSupabaseClient()
  const user = useSupabaseUser()

  async function signInWithGitHub() {
    const { error } = await client.auth.signInWithOAuth({
      provider: 'github',
      options: { redirectTo: `${window.location.origin}/confirm` },
    })
    if (error) throw error
  }

  async function signInWithGoogle() {
    const { error } = await client.auth.signInWithOAuth({
      provider: 'google',
      options: { redirectTo: `${window.location.origin}/confirm` },
    })
    if (error) throw error
  }

  async function signOut() {
    const { error } = await client.auth.signOut()
    if (error) throw error
    navigateTo('/login')
  }

  return { user, signInWithGitHub, signInWithGoogle, signOut }
}
