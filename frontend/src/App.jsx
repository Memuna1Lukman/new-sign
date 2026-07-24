import { useState } from 'react'
import Signup from './component/Signup'
import Login from './component/Login'

function App() {
  const [user,setUser] = useState(null)
  const [isLoggedIn,setLoggedIn] = useState(false)
  const [error,setError] = useState(false)
  const [loading,setLoading] = useState(false)


  const token = localStorage.getItem('access_token');

 

  return (
    <>
      
      <div>
      {user ? (
        <div className="min-h-screen flex items-center justify-center text-3xl font-bold text-slate-800">
          Hello {user.username}
        </div>
      ) :isLoggedIn ? (<Login onLogin={(userData)=>setUser(userData)} setLoggedIn={setLoggedIn} error={error} setError={setError} setLoadin={setLoading} loading={loading} />) : (
        <Signup onSignUp={(userData)=>setUser(userData)} setLoggedIn={setLoggedIn} error={error} setError={setError} setLoading={setLoading} loading={loading} />
      )}
    </div>
    </>
  )
}

export default App
