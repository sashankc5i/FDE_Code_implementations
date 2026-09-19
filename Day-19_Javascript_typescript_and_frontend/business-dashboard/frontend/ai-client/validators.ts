import type {
    ChatResponseDTO,
    AnalyzeResponseDTO,
    AIHealthResponseDTO
} from "./types";


function isObject(
    value: unknown
): value is Record<string, unknown> {

    return (
        typeof value === "object" &&
        value !== null
    );
}


export function validateChatResponse(
    value: unknown
): ChatResponseDTO {

    if (!isObject(value)) {
        throw new Error(
            "Invalid chat response: expected an object"
        );
    }


    if (
        typeof value.requestId !== "string" ||
        typeof value.answer !== "string" ||
        typeof value.model !== "string"
    ) {
        throw new Error(
            "Invalid chat response structure"
        );
    }


    return {
        requestId: value.requestId,
        answer: value.answer,
        model: value.model
    };
}


export function validateAnalyzeResponse(
    value: unknown
): AnalyzeResponseDTO {

    if (!isObject(value)) {
        throw new Error(
            "Invalid analysis response: expected an object"
        );
    }


    if (
        typeof value.requestId !== "string" ||
        typeof value.analysisType !== "string" ||
        typeof value.result !== "string" ||
        typeof value.confidence !== "number"
    ) {
        throw new Error(
            "Invalid analysis response structure"
        );
    }


    return {
        requestId: value.requestId,
        analysisType: value.analysisType,
        result: value.result,
        confidence: value.confidence
    };
}


export function validateHealthResponse(
    value: unknown
): AIHealthResponseDTO {

    if (!isObject(value)) {
        throw new Error(
            "Invalid health response: expected an object"
        );
    }


    if (
        typeof value.status !== "string" ||
        typeof value.service !== "string" ||
        typeof value.model !== "string"
    ) {
        throw new Error(
            "Invalid health response structure"
        );
    }


    return {
        status: value.status,
        service: value.service,
        model: value.model
    };
}