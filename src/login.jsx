import './login.css'
import { useState } from 'react'


function Login({ onLogin })
{
    const [username, setUsername]=useState("");
    const [password, setPassword]=useState("");
    const [error, setError]=useState("");

    const id="HarshaK";
    const pass="password";

    const checkLogin =(e)=>
    {
        e.preventDefault();
        if(username==id && password==pass)
        {
            onLogin(); 
            setError("");
        }
        else
        {
            setError("Wrong Username or Password!!. Please try again.");
        }
    };
    
    return (
        <div className='loginContainer'>
            {error && <p style={{color: 'red'}}>{error}</p>}
            <h1>Login</h1>
            <form id="loginForm" onSubmit={checkLogin}>
                <label>Username: </label>
                <input type='text' id="username" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Enter Your Username..."></input>
                <br></br>
                <label>Password: </label>
                <input type='password' id="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Enter Your Password..."></input>
                <br></br>
                <button type="submit" id="subBtn">Submit</button>
            </form>
        </div>
    );
}

export default Login