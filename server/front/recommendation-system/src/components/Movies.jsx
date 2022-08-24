import {useEffect} from 'react'

function Movies() {
  useEffect(()=>{
    fetch(
      "http://localhost:5000/"
    )
  })
  return (
    <div>Movies</div>
  )
}

export default Movies