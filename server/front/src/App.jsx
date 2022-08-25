import './App.css';
import Movies from "./components/Movies"
import UserList from "./components/UserList"
import { useState, createContext } from "react"
import { UserContext } from './UserContext'
import { Routes, Route, Link, BrowserRouter } from "react-router-dom";
import TopRecommendations from './components/TopRecommendations';

export const UsersContext = createContext([])

function App() {
  const [currentUser, setCurrentUser] = useState(1);
  const [users, setUsers] = useState([])
  return (
    <BrowserRouter>
      <UsersContext.Provider value={{ users, setUsers }}>
        <UserContext.Provider value={{ currentUser, setCurrentUser }}>
          <div className='app'>
            <UserList></UserList>
            <Routes>
              <Route path="/" element={<Movies />} />
              <Route path="recommend" element={<TopRecommendations />} />
            </Routes>
          </div>
        </UserContext.Provider>
      </UsersContext.Provider>
    </BrowserRouter>
  );
}

export default App;
