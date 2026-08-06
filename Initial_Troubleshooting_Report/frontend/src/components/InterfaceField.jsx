function InterfaceField({interfaceType, setInterfaceType, interfaceNumber, setInterfaceNumber}) {
    
    const handleChange = (event) => {
        setInterfaceType(event.target.value)
    }

    return (
        <div className="interface-field">
            
            <div className="interface-inputs">
                
                <label htmlFor="interface-Type">Interface Type</label>

                <select id="interface-type" value={interfaceType} onChange={handleChange}>
                    <option value="">Interface Type</option>
                    <option value="Fa">FastEthernet</option>
                    <option value="Gi">GigabitEthernet</option>
                    <option value="Te">TenGigabitEthernet</option>
                </select>
                
                <label htmlFor="interface-number">Interface Number</label>

                <input 
                id="interface-number"
                type="text"
                value={interfaceNumber}
                onChange={(event) =>
                    setInterfaceNumber(event.target.value)
                } 
                />
            </div>
        </div>
    )
}

export default InterfaceField