export default defineNuxtRouteMiddleware((to) => {
  const user = useSupabaseUser()
  if (!user.value && to.path !== '/login' && to.path !== '/' && to.path !== '/confirm') {
    return navigateTo('/login')
  }
})
