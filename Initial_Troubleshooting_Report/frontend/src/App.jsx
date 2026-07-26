import './App.css'

function App() {

  return (
    <>
      <section id="center">
        <div>
          <h1>Initial Troubleshooting Report</h1>
          <p>
            Run report for intial Switch troubleshooting summary. Work the findings from there.
          </p>
        </div>
      </section>
      <section id="center">
        <main>
          <form action="">
            <label htmlFor="target-ip">Enter Target IP </label>
            <input id="targert-ip" type="text" />
            <button
            type="button"
            className="submit"
            >
              Enter
            </button>
          </form>
          <div>
            <h2>Report</h2>
            <output>

            </output>
          </div>
        </main>
      </section>
    </>
  )
}

export default App
