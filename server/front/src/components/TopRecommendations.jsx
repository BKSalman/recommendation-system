import { useEffect, useState, useContext } from 'react'
import { UserContext } from '../UserContext'
import '../App.css';

function TopRecommendations() {
    const { currentUser, setCurrentUser } = useContext(UserContext);
    const [moviePosters, setMoviePosters] = useState([]);
    useEffect(() => {
        fetch(
            `http://localhost:5000/api/recommend/${currentUser}`, {
            method: 'GET',
        })
            .then((result) => result.json())
            .then((movies) => {
                let promises = [];
                for (const movie of movies) {
                    promises.push(fetch(
                        `http://localhost:5000/api/poster/${movie[0]}`, {
                        method: 'GET',
                    }).then((result) => result.json()))
                }

                Promise.all(promises)
                    .then(posters => setMoviePosters(posters))
            })
    }, [currentUser])
    return (
        <>
            <h1>Top Recommendations</h1>
            <div className='grid'>
                {[...Array(10)].map((x, i) =>
                    <div>
                        {/* <div key={moviePosters[i]}>{moviePosters[i]}</div> */}
                        <img alt='movie-poster' src={moviePosters[i]} key={moviePosters[i]} />
                    </div>
                )}
            </div>
        </>
    )
}

export default TopRecommendations