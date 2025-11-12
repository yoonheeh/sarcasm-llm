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

interface AppOptions {
    models: { value: string; label: string }[];
    sarcasm_levels: { value: string; label: string }[];
}

declare const showdown: any;

class SarcasmEvaluator {
    private evaluateButton: HTMLButtonElement;
    private sarcasmLevelSelect: HTMLSelectElement;
    private modelToEvaluateSelect: HTMLSelectElement;
    private conversationOutput: HTMLDivElement;
    private evaluationResultOutput: HTMLDivElement;
    private loadingSpinner: HTMLDivElement; // Changed from loadingBar
    private eventSource: EventSource | null = null;
    private converter: any;

    constructor() {
        this.evaluateButton = document.getElementById('evaluateButton') as HTMLButtonElement;
        this.sarcasmLevelSelect = document.getElementById('sarcasmLevel') as HTMLSelectElement;
        this.modelToEvaluateSelect = document.getElementById('modelToEvaluate') as HTMLSelectElement;
        this.conversationOutput = document.getElementById('conversationOutput') as HTMLDivElement;
        this.evaluationResultOutput = document.getElementById('evaluationResultOutput') as HTMLDivElement;
        this.loadingSpinner = document.getElementById('loadingSpinner') as HTMLDivElement; // Changed ID
        this.converter = new showdown.Converter();
    }

    public async initialize(): Promise<void> {
        this.evaluateButton.addEventListener('click', () => this.startEvaluation());
        await this.loadOptions();
    }

    private async loadOptions(): Promise<void> {
        try {
            const response = await fetch('/api/options');
            const options: AppOptions = await response.json();

            this.populateSelect(this.modelToEvaluateSelect, options.models);
            this.populateSelect(this.sarcasmLevelSelect, options.sarcasm_levels);

        } catch (error) {
            console.error('Error loading options:', error);
            // Handle error appropriately, e.g., show a message to the user
        }
    }

    private populateSelect(select: HTMLSelectElement, options: { value: string; label: string }[]): void {
        select.innerHTML = '';
        for (const option of options) {
            const opt = document.createElement('option');
            opt.value = option.value;
            opt.textContent = option.label;
            select.appendChild(opt);
        }
    }

    private startEvaluation(): void {
        const sarcasmLevel = this.sarcasmLevelSelect.value;
        const modelToEvaluate = this.modelToEvaluateSelect.value;
        this.setLoadingState(true);
        this.clearOutput();

        this.eventSource = new EventSource(`/api/evaluate?sarcasm_level=${sarcasmLevel}&model_to_evaluate=${modelToEvaluate}`);
        this.eventSource.onmessage = (event) => this.handleMessage(event);
        this.eventSource.onerror = (error) => this.handleError(error);
    }

    private handleMessage(event: MessageEvent): void {
        const data: Turn | EvaluationResult | { status: string } = JSON.parse(event.data);

        if ('status' in data) {
            if (data.status === 'evaluating') {
                this.evaluationResultOutput.innerHTML = '<h2>Evaluation Result</h2>';
                this.loadingSpinner.style.display = 'block'; // Changed from loadingBar
            }
        } else if ('evaluation_result' in data) {
            this.displayEvaluationResult(data.evaluation_result);
            this.closeEventSource();
        } else {
            this.displayTurn(data as Turn);
        }
    }

    private displayTurn(turn: Turn): void {
        const { model, response } = turn;
        const p = document.createElement('p');
        p.innerHTML = `<strong>${model}:</strong> ${response.message} (Sarcasm: ${response.sarcasm_presence})`;
        this.conversationOutput.appendChild(p);
    }

    private displayEvaluationResult(result: string): void {
        const html = this.converter.makeHtml(result);
        this.evaluationResultOutput.innerHTML += html;
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
        this.loadingSpinner.style.display = 'none'; // Changed from loadingBar
        this.setLoadingState(false);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const app = new SarcasmEvaluator();
    app.initialize();
});