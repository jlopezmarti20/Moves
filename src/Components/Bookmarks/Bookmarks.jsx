import './Bookmarks.css';
import {useState, useEffect} from "react";

function Bookmarks ({currentUser, goBack}) {
    const [bookmarks, setBookmarks] = useState([]);

    useEffect (() => {
        if(!currentUser) return;

        fetch(`http://127.0.0.1:5555/bookmarks/${currentUser.id}`)
            .then(res => res.json())
            .then(data => {
                setBookmarks(data.bookmarks);
            })
            .catch(err => console.error(err));

    }, [currentUser]);


    const handleDelete = async (placeId) => {

    try {

        const response = await fetch(
            `http://127.0.0.1:5555/bookmark/${placeId}/${currentUser.id}`,
            {
                method: "DELETE"
            }
        );

        const data = await response.json();

        if (response.ok) {

            setBookmarks((prevBookmarks) =>
                prevBookmarks.filter(
                    (bookmark) => bookmark.place_id !== placeId
                )
            );

        } else {
            alert(data.message);
        }

    } catch (error) {
        console.error(error);
        alert("Unable to delete bookmark.");
    }
};
    return (

        
        <div className='bookmarks-container'>

            <div className="bookmark-header">

                <button
                    className="back-button"
                    onClick={goBack}
                >
                    ← Back
                </button>

                <h2>My Moves</h2>

            </div>

            {bookmarks.length === 0 && (
                <h3 className="heading">No moves yet!</h3>
            )}
            <div className='bookmark-cardbox'>
                {bookmarks.map((data) => {
                    const mapsUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(data.address)}`;
                    return (
                        
                        <a
                            href={mapsUrl}
                            target="_blank"
                            rel="noopener noreferrer"
                            key={data.place_id}
                            className="bookmark-link"
                        >
                            <div className="bookmark-card">
                                <img
                                src={data.image}
                                alt={data.name}
                                className="bookmark-image"
                                referrerPolicy="no-referrer"
                                />
                                <div className="bookmark-info">
                                    <h3>{data.name}</h3>

                                    <h6>
                                        ⭐ {data.rating} • {data.distance_miles} mi
                                    </h6>

                                    <h6>📍 {data.address}</h6>

                                    <button
                                        className="delete-button"
                                        onClick={(event) => {
                                            event.preventDefault();
                                            handleDelete(data.place_id);
                                        }}
                                    >
                                        🗑 Delete
                                    </button>

                                </div>

                            </div>
                        </a>
                    );
                })}
            </div>


        </div>
    )
}

export default Bookmarks;