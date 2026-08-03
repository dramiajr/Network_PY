function SwitchSideReport ({ switchResult, switchRequestError }) {
    return (
        <output aria-live="polite">
            {switchRequestError && (
                <p className="switch-request-error" role="alert">
                    {switchRequestError}
                </p>
            )}
            {switchResult && (                         
                <div>
                    <p>
                    Connection Status: {switchResult.result_type}
                    </p>
                    <p>
                        {switchResult.device}
                    </p>
                    <pre>
                        {switchResult.switch_results.show_interfaces_output_raw}
                    </pre>                        
                </div>
                )}
        </output>
    )
}

export default SwitchSideReport