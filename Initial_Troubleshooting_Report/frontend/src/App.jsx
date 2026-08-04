import { useState } from 'react'
import './App.css'
import TargetIpForm from './components/TargetIpForm'
import PingReport from './components/PingReport'
import SwitchSideReport from './components/SwitchSideReport'
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

function App() {

  const [targetIP, setTargetIP] = useState('')
  const [interfaceType, setInterfaceType] = useState("Gi")
  const [interfaceNumber, setInterfaceNumber] = useState('')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [pingResult, setPingResult] = useState(null)
  const [switchResult, setSwitchResult] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [pingError, setPingError] = useState('')
  const [switchError, setSwitchError] = useState('')

  async function handleSubmit(event) {
    event.preventDefault()

    if (isLoading) {
      return
    }

    setPingResult(null)
    setSwitchResult(null)
    setPingError('')
    setSwitchError('')

    const trimmedTargetIP = targetIP.trim()

    if (!trimmedTargetIP) {
      setPingError('Enter a target IP address before running the check.')
      return
    }

    const apiRequestBody = {
      ip_address: trimmedTargetIP,
      interface_type: interfaceType,
      interface_number: interfaceNumber,
      username: username,
      password: password
    }

    setIsLoading(true)

    try {

      const pingPromise = startPingWorkflow()
      const switchSidePromise = startSwitchSideWorkflow()

      async function startPingWorkflow() {
        const pingController = new AbortController()
        const pingTimeoutId = setTimeout(() => pingController.abort(), 5000)

        try {
          const pingResponse = await fetch(
            `${API_BASE_URL}/ping?ip_address=${encodeURIComponent(trimmedTargetIP)}`,
            { signal: pingController.signal }
          )
          const pingData = await pingResponse.json()
          if (!pingResponse.ok) {
            setPingError(pingData.message)
          } else {
            setPingResult(pingData)
          }
        } catch (error) {
          console.error('Ping request failed:', error)

          if (error.name === 'AbortError') {
            setPingError(
              'The ping request timed out after five seconds. Make sure the FastAPI server is running and responding, then try again.'
            )
          } else {
            setPingError(
              'Unable to run the ping check. Make sure the FastAPI server is running and try again.'
              )
            }
        } finally {
          clearTimeout(pingTimeoutId)
        }
      }

      async function startSwitchSideWorkflow() {
        const switchSideController = new AbortController()
        const switchTimeoutId = setTimeout(() => switchSideController.abort(), 15000)

        try {
          const switchResponse = await fetch(
            `${API_BASE_URL}/switch-side`,
            {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify(apiRequestBody),
              signal: switchSideController.signal
            }
          )

          const switchSideData = await switchResponse.json()
          
          if (!switchResponse.ok) {
            setSwitchError(switchSideData.message)
            return
          }

          setSwitchResult(switchSideData)
        
        } catch (error) {
          console.error('Switch-side request failed:', error)
          if (error.name === 'AbortError') {
            setSwitchError(
              'The switch-side request took too long and was cancelled.'
            )
          } else {
            setSwitchError(
              'Unable to reach the troubleshooting API. Make sure the FastAPI server is running and try again.'
              )
            }
        } finally {
          clearTimeout(switchTimeoutId)
        }
      }
      
      await Promise.all([pingPromise, switchSidePromise])
      
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <>
      <section className="center">
        <div>
          <h1>Initial Troubleshooting Report</h1>
          <p>
            Run report for initial Switch troubleshooting summary. Work the findings from there.
          </p>
          <hr />
        </div>
      </section>
      <section className="center">
        <main>
          <TargetIpForm
            targetIP={targetIP}
            setTargetIP={setTargetIP}
            interfaceType={interfaceType}
            setInterfaceType={setInterfaceType}
            interfaceNumber={interfaceNumber}
            setInterfaceNumber={setInterfaceNumber}
            username={username}
            setUsername={setUsername}
            password={password}
            setPassword={setPassword}
            handleSubmit={handleSubmit}
            isLoading={isLoading}
          />
          <div className="report-section">
            <h2>Report</h2>
            <hr />
            <PingReport
              pingResult={pingResult}
              pingRequestError={pingError}
            />
            <hr />
            <SwitchSideReport
              switchResult={switchResult}
              switchRequestError={switchError}
            />
          </div>
        </main>
      </section>
    </>
  )
}

export default App
