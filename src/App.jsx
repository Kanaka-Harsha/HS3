import { useState } from 'react'
import Upload from './upload'
import Login from './login'
import './App.css'

function App() {

  const [isLoggedin, setIsLoggedIn] = useState(() => {
    return localStorage.getItem("isLoggedin") === "true";
  });

  const handleLogin = () => {
    localStorage.setItem("isLoggedin", "true");
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    localStorage.removeItem("isLoggedin");
    setIsLoggedIn(false);
  };

  return (
    <div id="container">
      <h1 className="header">H-Drive</h1>
      
      {isLoggedin ? (
        <>
          <Upload />
          <button onClick={handleLogout}>
             Log Out
          </button>
        </>
      ) : (
        <Login onLogin={handleLogin} />
      )}
    </div>
  )
}

export default App
