document.addEventListener('DOMContentLoaded', () => {
    const evaluateButton = document.getElementById('evaluateButton') as HTMLButtonElement;
    const sarcasmLevelSelect = document.getElementById('sarcasmLevel') as HTMLSelectElement;
    const conversationOutput = document.getElementById('conversationOutput') as HTMLDivElement;
    const evaluationResultOutput = document.getElementById('evaluationResultOutput') as HTMLDivElement;

    evaluateButton.addEventListener('click', async () => {
        const sarcasmLevel = sarcasmLevelSelect.value;

        try {
            const response = await fetch('/api/evaluate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ sarcasm_level: sarcasmLevel }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            conversationOutput.innerHTML = data.conversation.map((turn: any) => {
                const message = turn.response.message;
                const sarcasmPresence = turn.response.sarcasm_presence;
                const model = turn.model;
                return `<p><strong>${model}:</strong> ${message} (Sarcasm: ${sarcasmPresence})</p>`;
            }).join('');
            evaluationResultOutput.innerText = data.evaluation_result;
        } catch (error) {
            console.error('Error during evaluation:', error);
            conversationOutput.innerText = 'Error: Could not get conversation.';
            evaluationResultOutput.innerText = 'Error: Could not get evaluation result.';
        }
    });
});