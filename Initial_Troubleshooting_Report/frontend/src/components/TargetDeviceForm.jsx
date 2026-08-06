import InterfaceField from './InterfaceField'
import PasswordBox from './PasswordField'
import SubmitButton from './RunCheckButton'

function TargetDeviceForm({ targetIP, setTargetIP, interfaceType, setInterfaceType, interfaceNumber, setInterfaceNumber, username, setUsername, password, setPassword, handleSubmit, handleCancel, isLoading }) {

    return (

        <form className="target-form" onSubmit={handleSubmit} aria-busy={isLoading}>

          <div>
            <label htmlFor="target-ip">Enter Target IP </label>
            <input autoFocus
              id="target-ip"
              type="text"
              value={targetIP}
              onChange={(event) => setTargetIP(event.target.value)}
            />
          </div>

          <InterfaceField
          interfaceType={interfaceType}
          setInterfaceType={setInterfaceType}
          interfaceNumber={interfaceNumber}
          setInterfaceNumber={setInterfaceNumber}
          />

          <div>
            <label htmlFor="username"> Username </label>
            <input
              id="username"
              type="text"
              value={username}
              onChange={(event) => setUsername(event.target.value)}
            />
          </div>

          <PasswordBox
          password={password}
          setPassword={setPassword}
          />


          <SubmitButton
          isLoading={isLoading}
          handleCancel={handleCancel}
          />

        </form>
    )
}

export default TargetDeviceForm
