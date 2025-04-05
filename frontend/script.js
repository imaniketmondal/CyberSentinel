async function scanPorts() {
    const outputElement = document.getElementById("output");
    outputElement.innerHTML = "Scanning...";

    try {
        const response = await fetch("http://127.0.0.1:8000/scan");
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
        
        const data = await response.json();
        if (!data || !data.ports || !Array.isArray(data.ports)) throw new Error("Invalid response format");

        if (data.ports.length === 0) {
            outputElement.innerHTML = `<p>No open ports detected.</p>`;
            return;
        }

        let tableHTML = `<table border="1">
            <tr>
                <th>Port</th>
                <th>Status</th>
                <th>Risk Level</th>
                <th>Action</th>
            </tr>`;

        data.ports.forEach(portInfo => {
            let color = portInfo.status === "THREAT" ? "red" : "green";
            let closeButton = portInfo.status === "THREAT" 
                ? `<button onclick="closePort(${portInfo.port})">Close</button>` 
                : "N/A";

            tableHTML += `<tr style="color: ${color};">
                <td>${portInfo.port}</td>
                <td>${portInfo.status}</td>
                <td>${portInfo.risk}</td>
                <td>${closeButton}</td>
            </tr>`;
        });

        tableHTML += `</table>`;

        // ✅ Add the "Send Report" button after scanning
        tableHTML += `<button onclick="sendReport()">Send Report via SMS</button>`;

        outputElement.innerHTML = `<h3>Open Ports & Threat Levels</h3>${tableHTML}`;
    } catch (error) {
        outputElement.innerHTML = `<p>Error fetching data: ${error.message}</p>`;
    }
}

async function closePort(port) {
    try {
        const response = await fetch("http://127.0.0.1:8000/close_port", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ port: Number(port) })
        });

        const result = await response.json();
        alert(result.message || "Error closing port");

        // Refresh scan results after closing port
        scanPorts();
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}

async function sendReport() {
    try {
        const response = await fetch("http://127.0.0.1:8000/send_report", {
            method: "POST"
        });

        const result = await response.json();
        alert(result.message || "Error sending report");
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}
