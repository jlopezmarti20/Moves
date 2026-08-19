import React, { useState } from 'react';
import title from '../../assets/logo.png';
import './LoginSignup.css';

function LoginSignup({ onLogin, setCurrentUser }) {
    const [action, setAction] = useState("Login");
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = async () => {


        // Build request body
        const payload = {
            username: name,
            email: email, 
            password: password
        }

        // Sign up
        if (action === "Sign up"){
            const response = await fetch("http://127.0.0.1:5555/signup", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                body: JSON.stringify(payload)
            });
        
            const data = await response.json();

            if(response.ok) {
                alert(data.message);

                if (onLogin){
                    onLogin();
                }
            }
            else {
                alert(data.message);
            }
        }

        // LOGIN
        else{
            if (action === "Login"){
                const response = await fetch("http://127.0.0.1:5555/login", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Accept": "application/json"
                    },
                    body: JSON.stringify(payload)
                });

                const data = await response.json();

                if (response.ok){

                    setCurrentUser(data.user)
                    localStorage.setItem("currentUser", JSON.stringify(data.user));

                    if(onLogin){
                        onLogin();
                    }
                }
                else {
                    alert(data.message)
                }
                
            }
            
        }
    
    };

    return (
        <div className='container'>
            <div className='header'>
                <img src={title} alt="App Logo" className='logo' /> 
            </div>
            <div className='login-form'>
                {action === "Sign Up" && (
                    <div className='form-field'>
                    <input
                    type='text'
                    placeholder='Name'
                    value={name}
                    onChange={(event) => setName(event.target.value)}
                    />
                    </div>
                )}
                
            
                <div className = 'form-field'>
                    <input
                    type = 'email'
                    placeholder='Email'
                    value = {email}
                    onChange={(event) => setEmail(event.target.value)}
                    />          
                </div>

                <div className = 'form-field'>
                    <input
                    type = 'password'
                    placeholder='Password'
                    value = {password}
                    onChange={(event) => setPassword(event.target.value)}
                    />          
                </div> 
            </div>

            {action === "Login" && (
                <div className="forgot-password">
                    Lost Password? <span>Click Here!</span>
                </div>
            )}


            <div className='submit-container'>
                <div
                className={action === "Login" ? "submit gray" : "submit"}
                    onClick={() => setAction("Sign Up")}
                >
                    Sign Up

                </div>
                
            
                <div
                className={action === "Sign Up" ? "submit gray" : "submit"}
                onClick={() => setAction("Login")}
                >
                Login
                </div>
            </div>
            
           <button
           className="submit submit-main"
           onClick={handleSubmit}>
            Submit
            </button>
            
        </div>

    )

}

export default LoginSignup;