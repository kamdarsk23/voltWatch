import React from 'react'
import {Link} from 'react-router-dom'

const HomePage=()=> {
    return(
        <div className="home container">
            <h1 className="heading">Welcome to the Page </h1>
            <Link className="btn btn-primary btn-lg" to="/signup" >Get Started</Link>
        </div>
    )
}

export default HomePage