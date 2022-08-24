import './App.css';
import Movies from "./components/Movies"
import UserList from "./components/UserList"
import {useState} from "react"
import {UserContext} from './UserContext'

function App() {
  const [currentUser, setCurrentUser] = useState(1);
  return (
      <>
        <UserContext.Provider value={{currentUser, setCurrentUser}}>
          <UserList></UserList>
          <Movies></Movies>
        </UserContext.Provider>
      </>
  );
}

export default App;
