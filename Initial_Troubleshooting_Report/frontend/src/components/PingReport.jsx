function PingReport ({ pingResult, pingRequestError }) {
    return (
        <output aria-live="polite">
              {pingRequestError && (
                <p className="ping-request-error" role="alert">
                  {pingRequestError}
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
    )
}

export default PingReport