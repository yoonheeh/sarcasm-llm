
interface Turn {
    model: string;
    response: {
        sarcasm_presence: boolean;
        message: string;
    };
}

interface EvaluationResult {
    evaluation_result: string;
}

class SarcasmEvaluator {
    private evaluateButton: HTMLButtonElement;
    private sarcasmLevelSelect: HTMLSelectElement;
    private conversationOutput: HTMLDivElement;
    private evaluationResultOutput: HTMLDivElement;
    private eventSource: EventSource | null = null;

    constructor() {
        this.evaluateButton = document.getElementById('evaluateButton') as HTMLButtonElement;
        this.sarcasmLevelSelect = document.getElementById('sarcasmLevel') as HTMLSelectElement;
        this.conversationOutput = document.getElementById('conversationOutput') as HTMLDivElement;
        this.evaluationResultOutput = document.getElementById('evaluationResultOutput') as HTMLDivElement;
    }

    public initialize(): void {
        this.evaluateButton.addEventListener('click', () => this.startEvaluation());
    }

    private startEvaluation(): void {
        const sarcasmLevel = this.sarcasmLevelSelect.value;
        this.setLoadingState(true);
        this.clearOutput();

        this.eventSource = new EventSource(`/api/evaluate?sarcasm_level=${sarcasmLevel}`);
        this.eventSource.onmessage = (event) => this.handleMessage(event);
        this.eventSource.onerror = (error) => this.handleError(error);
    }

    private handleMessage(event: MessageEvent): void {
        const data: Turn | EvaluationResult = JSON.parse(event.data);

        if ('evaluation_result' in data) {
            this.displayEvaluationResult(data.evaluation_result);
            this.closeEventSource();
        } else {
            this.displayTurn(data);
        }
    }

    private displayTurn(turn: Turn): void {
        const { model, response } = turn;
        const p = document.createElement('p');
        p.innerHTML = `<strong>${model}:</strong> ${response.message} (Sarcasm: ${response.sarcasm_presence})`;
        this.conversationOutput.appendChild(p);
    }

    private displayEvaluationResult(result: string): void {
        this.evaluationResultOutput.innerText = result;
    }

    private handleError(error: Event): void {
        console.error('EventSource failed:', error);
        this.conversationOutput.innerText = 'Error: Could not get conversation.';
        this.evaluationResultOutput.innerText = 'Error: Could not get evaluation result.';
        this.closeEventSource();
    }

    private setLoadingState(isLoading: boolean): void {
        this.evaluateButton.disabled = isLoading;
    }

    private clearOutput(): void {
        this.conversationOutput.innerHTML = '';
        this.evaluationResultOutput.innerHTML = '';
    }

    private closeEventSource(): void {
        if (this.eventSource) {
            this.eventSource.close();
            this.eventSource = null;
        }
        this.setLoadingState(false);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const app = new SarcasmEvaluator();
    app.initialize();
});
