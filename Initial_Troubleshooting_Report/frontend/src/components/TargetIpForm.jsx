import { useState } from 'react'

function TargetIpForm({targetIP, setTargetIP, interfaceType, setInterfaceType, interfaceNumber, setInterfaceNumber, username, setUsername, password, setPassword, handleSubmit, isLoading}) {
    const [showPassword, setShowPassword] = useState(false)

    return (

        <form className="target-form" onSubmit={handleSubmit} aria-busy={isLoading}>

          <div>
            <label htmlFor="target-ip">Enter Target IP </label>
            <input
              id="target-ip"
              type="text"
              value={targetIP}
              onChange={(event) => setTargetIP(event.target.value)}
            />
          </div>

          <div>
            <label htmlFor="target-interface"> Enter Interface </label>
            <select 
              name="interface-type" 
              id="interface-type"
              value={interfaceType}
              onChange={(event) => setInterfaceType(event.target.value)}    
              >
              <option value="">Interface Type</option>
              <option value="Fa">FastEthernet</option>
              <option value="Gi">GigabitEthernet</option>
              <option value="Te">TenGigabitEthernet</option>
            </select>

            <input 
              id="target-interface"
              type="text" 
              value={interfaceNumber}
              onChange={(event) => setInterfaceNumber(event.target.value)}           
            />
          </div>

          <div>
            <label htmlFor="username"> Username </label>
            <input
              id="username"
              type="text"
              value={username}
              onChange={(event) => setUsername(event.target.value)}
            />
          </div>

          <div>
            <label htmlFor="password"> Password </label>
            <div className="password-field">
              <input
                id="password"
                type={showPassword ? 'text' : 'password'}
                value={password}
                onChange={(event) => setPassword(event.target.value)}
              />
              <button
                type="button"
                className="password-toggle"
                aria-label={showPassword ? 'Hide password' : 'Show password'}
                aria-pressed={showPassword}
                onClick={() => setShowPassword((isVisible) => !isVisible)}
              >
                {showPassword ? 'Hide' : 'Show'}
              </button>
            </div>
          </div>

            <button
              type="submit"
              className="submit"
              disabled={isLoading}
            >     
              {isLoading ? 'Running…' : 'Run Checks'}
            </button>

        </form>
    )
}

export default TargetIpForm
