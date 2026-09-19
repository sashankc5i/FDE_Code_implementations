function isObject(
    value: unknown
): value is Record<string, unknown> {
    return (
        typeof value === "object" &&
        value !== null
    );
}

export interface ChatResponse {
    requestId: string;
    answer: string;
    model: string;
}

export function validateChatResponse(
    value: unknown
): ChatResponse {

    if (!isObject(value)) {
        throw new Error(
            "Invalid chat response"
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