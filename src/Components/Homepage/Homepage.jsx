import React, { useState, useEffect } from "react";
import TinderCard from "react-tinder-card";
import "./Homepage.css";


function Homepage({currentUser, selectedMood, goToBookmarks, goToCloudAI, setBookmarkedUsers, onLogout}) {

    const [cards, setCards] = useState([]);

    useEffect(() => {
        if (!selectedMood) return;

        // Get user's location
        navigator.geolocation.getCurrentPosition((position) => {


           const moods = [
                "coffee",
                "food",
                "workout",
                "party",
                "shopping",
                "artsy",
                "adventurous",
                "education"
            ];

            const payload = {
                longitude: position.coords.longitude,
                latitude: position.coords.latitude
            };

            if (moods.includes(selectedMood)) {
                payload.mood = selectedMood;
            } else {
                payload.user_input = selectedMood;
            }
        
            fetch("http://127.0.0.1:5555/recommendations", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                },
                body: JSON.stringify(payload),
            })
            .then(res => res.json())
            .then(data => {
                console.log("Recommendations:", data);
                setCards(data.recommendations)
            })
            .catch(err => console.error("Error:", err));


        });
    }, [selectedMood]);

    

    const removeCard = (placeId) => {
        setCards((prevCards) =>
            prevCards.filter((card) => card.place_id !== placeId)
        );
    };

    const handleSwipe = (direction, place) => {
        console.log(`${direction} swipe:`, place.name);

        if (direction === "right") {
            console.log("Liked:", place);
        }

        removeCard(place.place_id);
    };

    const handleLike = async () => {

        if(!currentUser){
            alert("Please log in first.");
            return;
        }

        if (cards.length === 0) return;

        const topCard = cards[0];

        const payload = {
            user_id: currentUser.id,
            ...topCard
        };

        

        const response = await fetch("http://127.0.0.1:5555/bookmark", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            body: JSON.stringify(payload)
        });

        try {
            const data = await response.json();

            if(response.ok){
                setBookmarkedUsers((prevBookmarks) => [
                    ...prevBookmarks,
                    topCard
                ]);
                
                removeCard(topCard.place_id);
            }
            else {
                alert(data.message)
            }
        }
        catch(error) {
            console.error(error);
            alert("Unable to save bookmark.")
        }
    };

    const handlePass = () => {
        if (cards.length === 0) return;

        const topCard = cards[0];

        console.log("Passed:", topCard);

        removeCard(topCard.place_id);
    };

    return (
        <div className="card">

            {/* ---------- Navigation ---------- */}

            <div className="navigation-buttons">

                <button
                    className="nav-button"
                    onClick={goToCloudAI}
                >
                    ☁ Cloud AI
                </button>

                <button
                    className="nav-button"
                    onClick={goToBookmarks}
                >
                    📚 Bookmarks
                </button>

                <button
                    className="nav-button logout"
                    onClick={onLogout}
                >
                    🚪 Logout
                </button>

            </div>

            {/* ---------- Header ---------- */}

            <div className="user-details">

                <h3>
                    Discover Moves In{" "}
                    {cards.length > 0 ? cards[0].city : "Miami"}
                </h3>

                <img
                    src="https://img.icons8.com/material-outlined/24/808080/address.png"
                    alt="Location"
                    className="location"
                />

            </div>

            {/* ---------- Cards ---------- */}

            <div className="cardbox">

                {[...cards].reverse().map((place) => (

                    <TinderCard
                        key={place.place_id}
                        className="tindercard"
                        preventSwipe={["up", "down"]}
                        onSwipe={(dir) => handleSwipe(dir, place)}
                    >

                        <div className="card-details">

                            <img
                                src={place.image}
                                alt={place.name}
                                className="card-image"
                            />

                            <div className="userdetails">

                                <h3>{place.name}</h3>

                                <h6>
                                    ⭐ {place.rating} • {place.distance_miles} mi
                                </h6>

                                <h6>📍 {place.address}</h6>

                            </div>

                        </div>

                    </TinderCard>

                ))}

            </div>

            {/* ---------- Action Buttons ---------- */}

            <div className="card-actions">

                <button
                    className="action-btn pass"
                    onClick={handlePass}
                >
                    ❌
                </button>

                <button
                    className="action-btn like"
                    onClick={handleLike}
                >
                    ❤️
                </button>

            </div>

        </div>
    );
}

export default Homepage;