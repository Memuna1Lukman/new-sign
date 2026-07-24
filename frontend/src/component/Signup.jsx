import React,{useState} from 'react'

export default function Signup({onSignUp,setLoggedIn,error,setError,loading,setLoading}) {
  const [form,formData] = useState({
    username : '',
    email : '',
    password : ''
  })
  const { username, email, password } = form; 
  
  const handleInput = (e)=>{
    formData({...form,[e.target.name]:e.target.value})
  }

  const handleSubmit = async (e)=>{
       e.preventDefault()
       setError('')
       setLoading(true)
       try{
        const response = await fetch("http://localhost:8000/user/",{
            method: 'POST',
            headers: {
                'Content-Type':'application/json'
            },
            body: JSON.stringify(form)
        })
        const data = await response.json()
        console.log(data)
        console.log(Array.isArray(data.detail))
        if (!response.ok) {
          let errorMsg = 'Registration Failed'
          if(Array.isArray(data.detail)){
            errorMsg = data.detail[0].msg
          }
          else if ((typeof data.detail === 'string')){
            errorMsg = data.detail
          }
          throw new Error(errorMsg)
        }
        onSignUp(data)
       }
    catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }   
  }
  const switchToLogin = (e)=>{
    e.preventDefault()
    setError('')
    setLoggedIn(true)
  }
  return (
    <div className='min-h-screen bg-slate-50 flex items-center justify-center p-4'>

        <form 
           onSubmit={handleSubmit}
           className='w-full max-w-md bg-white shadow-xl border border-slate-100 flex flex-col p-8 gap-6 '
           action="#">
           <div className='text-center space-y-2 p-2'>
            <h2 className='text-3xl font-bold text-slate-800 tracking-tight'>Your Account</h2>
            <p className='text-sm text-slate-500'>Get started with your profile today.</p>
           </div>
           {error && (
                <div className='bg-red-50 text-red-600 p-3 rounded-lg text-sm border border-red-200'>
                    {error}
                </div>
            )}
           <div className='flex flex-col gap-4'>
            
               <input
                    name='username'
                    value={username} 
                    onChange={handleInput}
                    placeholder='Username'
                    className='w-full px-4 py-2.5  border-b-2 text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all  '
                    type="text" />


               <input
                    name='email'
                    onChange={handleInput}
                    value={email}
                    placeholder='Email'
                    className='w-full px-4 py-2.5  border-b-2 text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all  '
                    type="text" />


                <input 
                    name='password'
                    value={password}
                    onChange={handleInput}
                    className='w-full px-4 py-2.5  border-b-2 text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all  '
                    placeholder='password'
                    type="password" />
            </div>
            
                

            
            <div className="flex gap-3">

                <input
                    className='border' 
                    type="checkbox" />

               <p>Do you agree with the {' '}
                <a 
                     className='font-medium text-indigo-600 hover:text-indigo-500 underline underline-offset-2' href="#terms">Terms and conditions</a>of this site</p>


            </div>
           <button disabled={loading} className=' border-none rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white w-full py-3 px-2 font-semibold shadow-lg shadow-indigo-600/20 active:scale-[0.98] transition-all'>{loading ? 'Registering...' : 'Sign Up'}</button>


           <p>Already have an account? 
            <a 
            onClick={switchToLogin}
             className='font-medium text-indigo-600 hover:text-indigo-500 underline underline-offset-2' href="#terms"
            >Log in</a></p>

           

        </form>
    </div>
  )
}
