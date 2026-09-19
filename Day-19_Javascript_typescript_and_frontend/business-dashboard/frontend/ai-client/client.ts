import {
    APIError
} from "./errors";


import {
    validateChatResponse,
    validateAnalyzeResponse,
    validateHealthResponse
} from "./validators";


import type {
    ChatRequestDTO,
    ChatResponseDTO,
    AnalyzeRequestDTO,
    AnalyzeResponseDTO,
    AIHealthResponseDTO
} from "./types";


export class AIClient {

    private readonly baseURL: string;


    constructor(baseURL: string) {
        this.baseURL = baseURL;
    }


    private async request(
        endpoint: string,
        options?: RequestInit
    ): Promise<unknown> {

        const response = await fetch(
            `${this.baseURL}${endpoint}`,
            options
        );


        if (!response.ok) {

            throw new APIError(
                `AI API request failed: ${response.status} ${response.statusText}`,
                response.status,
                endpoint
            );
        }


        return await response.json();
    }


    async chat(
        request: ChatRequestDTO
    ): Promise<ChatResponseDTO> {

        const data = await this.request(
            "/api/ai/chat",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(request)
            }
        );


        return validateChatResponse(data);
    }


    async analyze(
        request: AnalyzeRequestDTO
    ): Promise<AnalyzeResponseDTO> {

        const data = await this.request(
            "/api/ai/analyze",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(request)
            }
        );


        return validateAnalyzeResponse(data);
    }


    async health(): Promise<AIHealthResponseDTO> {

        const data = await this.request(
            "/api/ai/health"
        );


        return validateHealthResponse(data);
    }
}