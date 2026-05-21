export const auth = {
  setAuth(token: string, email: string) {
    localStorage.setItem("token", token)
    localStorage.setItem("email", email)
  },

  getToken() {
    return localStorage.getItem("token")
  },

  getEmail() {
    return localStorage.getItem("email")
  },

  logout() {
    localStorage.removeItem("token")
    localStorage.removeItem("email")
  },

  isAuthenticated() {
    return !!localStorage.getItem("token")
  },
}