import './navbar.css'

function NavBar({ isLoggedin, onLogout }) {
  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <h1>HS3 Drive</h1>
      </div>
      {isLoggedin && (
        <button className="logout-btn" onClick={onLogout}>
          Logout
        </button>
      )}
    </nav>
  )
}

export default NavBar