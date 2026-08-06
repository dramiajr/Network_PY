import { useState } from 'react'

function PasswordBox({password, setPassword}) {
    const [showPassword, setShowPassword] = useState(false)
    return (
        <div>
            <label htmlFor="password">Password</label>

            <div className='password-input-box'>
                <input 
                type={showPassword ? 'text' : 'password'}
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                />

                <button
                type="button"
                className="password-toggle"
                aria-label="Hold to show password"
                onPointerDown={() => setShowPassword(true)}
                onPointerUp={() => setShowPassword(false)}
                onPointerLeave={() => setShowPassword(false)}
                onPointerCancel={() => setShowPassword(false)}
                onKeyDown={(event) => {
                    if (event.key === ' ' || event.key === 'Enter') {
                        setShowPassword(true)
                        }
                }}
                onKeyUp={(event) => {
                    if (event.key === ' ' || event.key === 'Enter') {
                        setShowPassword(false)
                        }
                }}
                onBlur={() => setShowPassword(false)}
                >
                    <span aria-hidden="true">👁</span>
                </button>
            </div>
        </div>
    )
}

export default PasswordBox