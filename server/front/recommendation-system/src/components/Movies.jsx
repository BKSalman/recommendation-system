import {useEffect, useState, useContext} from 'react'
import {UserContext} from '../UserContext'
import '../App.css';

function Movies() {
  const {currentUser, setCurrentUser} = useContext(UserContext);
  const [moviePosters, setMoviePosters] = useState([]);
  const [estimates, setEstimates] = useState([]);
  useEffect(()=>{
    fetch(
      `http://localhost:5000/api/movie-list/${currentUser}`,{
        method: 'GET',
      })
      .then((result)=> result.json())
      .then((movies) => {
        let promises = [];
        for(let i=0; i < 10 ; i++) {
          const index = movies.length - Math.floor(movies.length/4) - i;
          promises.push(fetch(
            `http://localhost:5000/api/poster/${movies[index]}`,{
          method: 'GET',
          }).then((result)=> result.json()))
        }

        Promise.all(promises)
          .then(posters => setMoviePosters(posters))
        promises = [];
        for(let i=0; i < 10 ; i++) {
          const index = movies.length - Math.floor(movies.length/4) - i;
          promises.push(fetch(
            `http://localhost:5000/api/estimate?user_id=${currentUser}&movie_id=${movies[index]}`,{
          method: 'GET',
          }).then((result)=> result.json()))
        }
          
        Promise.all(promises)
          .then(estimates => setEstimates(estimates))
      })
  }, [currentUser])
  return (
    <div className='grid'>
      {[...Array(10)].map((x, i) =>
        <div>
          <img alt='movie-poster' src={moviePosters[i]} key={moviePosters[i]}/>
          <div key={`${i}-${estimates[i]}`}>{estimates[i]}</div>
        </div>
      )}
    </div>
  )
}

export default Movies