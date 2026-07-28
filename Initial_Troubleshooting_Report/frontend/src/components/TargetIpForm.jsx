function TargetIpForm({targetIP, setTargetIP, handleSubmit, isLoading}) {
    return (

        <form className="target-form" onSubmit={handleSubmit} aria-busy={isLoading}>

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
    )
}

export default TargetIpForm