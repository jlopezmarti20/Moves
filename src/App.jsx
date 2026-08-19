
import "./App.css";



import LoginSignup from "./Components/LoginSignup/LoginSignup";
import Homepage from "./Components/Homepage/Homepage";
import CloudAI from "./Components/CloudAI/CloudAI";
import Bookmarks from "./Components/Bookmarks/Bookmarks";
import { useState, useEffect } from "react";

function App() {
    const [currentPage, setCurrentPage] = useState("login");

    const [bookmarkedUsers, setBookmarkedUsers] = useState([]);

    const [selectedMood, setSelectedMood] = useState("");

    const [currentUser, setCurrentUser] = useState(null);

    const handleLogout = () => {
        localStorage.removeItem("currentUser");

        setCurrentUser(null);
        setSelectedMood("");
        setBookmarkedUsers([]);

        setCurrentPage("login");
    };


    useEffect(() => {

    const savedUser = localStorage.getItem("currentUser");

        if (savedUser) {

            const user = JSON.parse(savedUser);

            setCurrentUser(user);

            setCurrentPage("cloudai");
        }

    }, []);

    return (
        <div className="app">

            {currentPage === "login" && (
                <LoginSignup
                    onLogin={() => setCurrentPage("cloudai")}
                    setCurrentUser={setCurrentUser}
                />
            )}

            {currentPage === "homepage" && (
                <Homepage
                    currentUser={currentUser}
                    selectedMood={selectedMood}
                    bookmarkedUsers={bookmarkedUsers}
                    setBookmarkedUsers={setBookmarkedUsers}
                    goToBookmarks={() => setCurrentPage("bookmarks")}
                    goToCloudAI={() => setCurrentPage("cloudai")}
                    onLogout={handleLogout}
                />
            )}

            {currentPage === "cloudai" && (
                <CloudAI
                    setSelectedMood={setSelectedMood}
                    goToHomepage={() => setCurrentPage("homepage")}
                    onLogout={handleLogout}
                />
            )}

            {currentPage === "bookmarks" && (
                <Bookmarks
                    currentUser={currentUser}
                    goBack={() => setCurrentPage("homepage")}
                    onLogout={handleLogout}
                />
            )}

        </div>
    );
}

export default App;