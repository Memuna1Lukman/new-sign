import React, { useState } from 'react'

export default function Login({onLogin,setLoggedIn,error,setError,loading,setLoading}) {
    const [loginData,setLoginData] = useState({
        email: '',
        password: ''
    })

    const {email,password} = loginData;
    
    
    const handleSubmit = async(e)=>{
        e.preventDefault()
        setError('')
        setLoading(true)
        const formData = new URLSearchParams()
        formData.append('username', email)
        formData.append('password', password)
        try{
            const response = await fetch('http://localhost:8000/login/',{
               method: "POST",
               headers: {
                'Content-Type':'application/x-www-form-urlencoded'
               },
               body: formData
            })
            const data = await response.json()
            if (!response.ok) {
                let errorMsg = 'Login failed'
                if(Array.isArray(data.detail)){
                    errorMsg = data.detail[0]
                }else if(typeof data.detail === "string"){
                    errorMsg = data.detail
                }
                throw new Error(errorMsg)
            }
            localStorage.setItem('access_token',data.token)
            onLogin(data)
        
            
        }
        catch (err) {
            setError(err.message)
        } finally {
            setLoading(false)
        }  
    }
    const handleInput = (e)=>{
       setLoginData({...loginData,[e.target.name]:e.target.value})
    }
    const switchToSignUp = (e)=>{
        e.preventDefault()
        setError('')
        setLoggedIn(false)
  }
  return (
    <div className='min-h-screen bg-slate-50 flex items-center justify-center p-4'>
       
       <form 
            onSubmit={handleSubmit}
            className='w-full max-w-md bg-white shadow-xl border border-slate-100 flex flex-col p-8 gap-6 '
            action="Post">
            <div className='text-center space-y-2 p-2'>
                <h2 className='text-3xl font-bold text-slate-800 tracking-tight'>Log Onto Account</h2>
            </div>
            {error && (
                <div className='bg-red-50 text-red-600 p-3 rounded-lg text-sm border border-red-200'>
                    {error}
                </div>
            )}
            <div className='flex flex-col gap-4'>
                <input
                className='w-full px-4 py-2.5  border-b-2 text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all  '
                onChange={handleInput} 
                name='email'
                placeholder='Email'
                value={email}
                type="text" />
                <input
                placeholder='Password'
                className='w-full px-4 py-2.5  border-b-2 text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all  '
                onChange={handleInput}
                name='password'
                value={password} 
                type="password" />
            </div>
        <button  disabled={loading} className=' border-none rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white w-full py-3 px-2 font-semibold shadow-lg shadow-indigo-600/20 active:scale-[0.98] transition-all'>{loading ? 'Logging in...' : 'Log In'}</button>
        <p>Don't have an account? {' '}
            <a 
            onClick={switchToSignUp}
             className='font-medium text-indigo-600 hover:text-indigo-500 underline underline-offset-2' href="#terms"
            >Log in</a></p>
       </form>
    </div>
  )
}
