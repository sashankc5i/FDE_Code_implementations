export interface ChatRequestDTO {
    message: string;
    conversationId?: string;
}


export interface ChatResponseDTO {
    requestId: string;
    answer: string;
    model: string;
}


export interface AnalyzeRequestDTO {
    text: string;
    analysisType: string;
}


export interface AnalyzeResponseDTO {
    requestId: string;
    analysisType: string;
    result: string;
    confidence: number;
}


export interface AIHealthResponseDTO {
    status: string;
    service: string;
    model: string;
}


// Utility type examples

export type ChatRequestUpdate =
    Partial<ChatRequestDTO>;


export type ChatMetadata =
    Pick<
        ChatResponseDTO,
        "requestId" | "model"
    >;