import React, { useState} from 'react';
import './CloudAI.css';


const moodsOptions = [
    {
        emoji: "☕",
        label: "Coffee",
        value: "coffee"
    },
    {
        emoji: "🍔",
        label: "Food",
        value: "food"
    },
    {
        emoji: "🏋️",
        label: "Workout",
        value: "workout"
    },
    {
        emoji: "🎉",
        label: "Party",
        value: "party"
    },
    {
        emoji: "🛍️",
        label: "Shopping",
        value: "shopping"
    },
    {
        emoji: "🎨",
        label: "Arts",
        value: "artsy"
    },
    {
        emoji: "🌳",
        label: "Outdoors",
        value: "adventurous"
    },
    {
        emoji: "📚",
        label: "Study",
        value: "education"
    }
];


function CloudAI ({setSelectedMood, goToHomepage}) {
    const [localSelectedMood, setLocalSelectedMood] = useState("");
    const [customMood] = useState("");

    const handleSubmit = () => {
        // Save selected mood
        setSelectedMood(localSelectedMood)
        // navigate to homepage
        goToHomepage();
    };

    const handleMoodClick = (mood) => {
        setLocalSelectedMood(mood.value);
    }



    return (
        <div className='homepage-container'>
            <div className='cloud'>☁️</div>

            <h1 className='cloud-title'>What's the Move for today?</h1>

            <p className='cloud-subtitle'>Pick the vibe you're feeling, and I'll find something you'll enjoy.</p>

            <div className='mood-options'>
                {moodsOptions.map((mood) => (
                    <button
                         key={mood.label}
                        className={`mood-button ${localSelectedMood === mood.value ? 'selected' :''}`}
                        onClick = {() => handleMoodClick(mood)}
                    >
                        <span className='emoji'>{mood.emoji}</span>
                        <span>{mood.label}</span>
                    </button>
                ))}
            </div>

            <div className='mood-input-container'>
                <button
                    className="submit-mood"
                    onClick={handleSubmit}
                    disabled={!localSelectedMood && customMood.trim() === ""}
                >
                    Find My Move
                </button>
            </div>
        </div>
    )
}

export default CloudAI;
