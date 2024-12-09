"use client";

import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LoginPage from "./auth/page";
import ProfilePage from "./profile/page"; // Import the Profile page
import AddUser from "./addUser/page";

const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<LoginPage />} />
                <Route path="/profile" element={<ProfilePage />} />
                <Route path="/addUser" element={<AddUser />} />
            </Routes>
        </Router>
    );
};

export default App;
