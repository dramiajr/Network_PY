import { useState } from 'react'
import './App.css'

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
        `http://127.0.0.1:8000/ping?ip_address=${encodeURIComponent(trimmedTargetIP)}`,
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
            Run report for intial Switch troubleshooting summary. Work the findings from there.
          </p>
          <hr />
        </div>
      </section>
      <section className="center">
        <main>
          <form onSubmit={handleSubmit} aria-busy={isLoading}>
            <label htmlFor="target-ip">Enter Target IP </label>
            <input
              id="target-ip"
              type="text"
              value={targetIP}
              onChange={(event) => setTargetIP(event.target.value)}
            />
            <button
              type="submit"
              className="submit"
              disabled={isLoading}
            >
              {isLoading ? 'Running…' : 'Run Checks'}
            </button>
          </form>
          <div className="report-section">
            <h2>Report</h2>
            <hr />
            <output aria-live="polite">
              {requestError && (
                <p className="request-error" role="alert">
                  {requestError}
                </p>
              )}
              {pingResult && (
                pingResult.request_status === 'invalid' ? (
                  <div>
                    <p>
                      {pingResult.message}
                    </p>
                    <p>
                      {pingResult.invalid_address}
                    </p>
                  </div>
                ) : (
                <div>
                  <p>
                    Ping Status: {pingResult.ping_status}
                  </p>
                  <pre>
                    {pingResult.ping_output_raw}
                  </pre>
                </div>
                )
              )}
            </output>
          </div>
        </main>
      </section>
    </>
  )
}

export default App
