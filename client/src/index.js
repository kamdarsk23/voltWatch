import 'bootstrap/dist/css/bootstrap.min.css';
import './styles/main.css';
import React from 'react'
import ReactDOM from 'react-dom'
import Navbar from './components/navbar'
import HomePage from './components/Home'
import SignupPage from './components/Signup'
import LoginPage from './components/Login'
import CreateRecipePage from './components/CreateRecipe'
import {
    BrowserRouter as Router,Routes,Route
} from 'react-router-dom'

const App=()=>{
    return ( 
        <Router>
        <div className="app">
            <Navbar/>
            <Routes>
                <Route path="/create_recipe" element={<CreateRecipePage />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/signup" element={<SignupPage />} />
                <Route path="/" element={<HomePage />} />
            </Routes>
        </div>
        </Router>
    )
}

ReactDOM.render(<App/>,document.getElementById('root'));