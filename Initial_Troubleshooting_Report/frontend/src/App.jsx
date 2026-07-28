import { useState } from 'react'
import './App.css'
import TargetIpForm from './components/TargetIpForm'
import PingReport from './components/PingReport'
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

function App() {

  const [targetIP, setTargetIP] = useState('')
  const [pingResult, setPingResult] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [requestError, setRequestError] = useState('')

  async function handleSubmit(event) {
    event.preventDefault()

    if (isLoading) {
      return
    }

    setPingResult(null)
    setRequestError('')

    const trimmedTargetIP = targetIP.trim()

    if (!trimmedTargetIP) {
      setRequestError('Enter a target IP address before running the check.')
      return
    }

    setIsLoading(true)
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), 5000)

    try {
      const response = await fetch(
        `${API_BASE_URL}/ping?ip_address=${encodeURIComponent(trimmedTargetIP)}`,
        { signal: controller.signal }
      )

      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`)
      }

      const data = await response.json()
      setPingResult(data)
    } catch (error) {
      console.error('Ping request failed:', error)

      if (error.name === 'AbortError') {
        setRequestError(
          'The ping request timed out after five seconds. Make sure the FastAPI server is running and responding, then try again.'
        )
      } else {
        setRequestError(
          'Unable to run the ping check. Make sure the FastAPI server is running and try again.'
        )
      }
    } finally {
      clearTimeout(timeoutId)
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
            handleSubmit={handleSubmit}
            isLoading={isLoading}
          />
          <div className="report-section">
            <h2>Report</h2>
            <hr />
            <PingReport
              pingResult={pingResult}
              requestError={requestError}
            />
          </div>
        </main>
      </section>
    </>
  )
}

export default App
