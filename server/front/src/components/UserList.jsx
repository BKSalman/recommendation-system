import { useEffect, useContext, useState, createContext } from 'react'
import { UserContext } from '../UserContext'
import { UsersContext } from "../App"

function UserList() {

  const changeSelection = (e) => {
    setCurrentUser(e.target.value)
  }

  const { currentUser, setCurrentUser } = useContext(UserContext);
  const { users, setUsers } = useContext(UsersContext);
  useEffect(() => {
    fetch(
      `http://localhost:5000/api/user-list`, {
      method: 'GET',
    })
      .then((result) => result.json())
      .then(users => setUsers(users))
  }, [currentUser])
  return (
    <select onChange={changeSelection} name="" id="">
      {users.map((user) => (
        <option key={user} value={user}>{user}</option>
      ))}
    </select>
  )
}

export default UserList