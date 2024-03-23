import React, { useState } from 'react'
import { Form, Button } from 'react-bootstrap'
import {Link} from 'react-router-dom'

const LoginPage=()=> {
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')

    const LOGIN = () => {
        console.log("Form submitted");
        console.log(email);
        console.log(password);

        setEmail("");
        setPassword("");
    }


    return(
        <div className="container">
            <div className="form">
                <h1>Login Form</h1>
                <form>
                    <Form.Group>
                        <Form.Label>Email</Form.Label>
                        <Form.Control type="email" placeholder='email'
                            value={email}
                            name="email"
                            onChange={(e) => { setEmail(e.target.value) }} />
                        <br></br>
                        <Form.Label>Password</Form.Label>
                        <Form.Control type="password" placeholder='password'
                            value={password}
                            name="password"
                            onChange={(e) => { setPassword(e.target.value) }} />
                    </Form.Group>
                    <br></br>
                    <Form.Group>
                        <Button as="sub" variant="primary" onClick={LOGIN}>
                            Login
                        </Button>
                    </Form.Group>
                    <br></br>
                    <Form.Group>
                        <small>Don't have an account? <Link to="/signup">Create one</Link></small>
                    </Form.Group>
                </form>
            </div>
        </div>
    )
}

export default LoginPage