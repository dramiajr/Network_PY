function SubmitButton({ isLoading, handleCancel }) {

    return (
        <div>

            <button
            type="submit"
            className="submit"
            disabled={isLoading}        
            >
                {isLoading ? 'Running…' : 'Run Checks'}
            </button>

            {
                isLoading && (
                    <button
                    type="button"
                    className="cancel"
                    onClick={handleCancel}
                    >
                        Cancel
                    </button>
                )
            }
        </div>
    )
}

export default SubmitButton