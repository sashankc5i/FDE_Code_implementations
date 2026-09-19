import {
    NextRequest,
    NextResponse
} from "next/server";

interface ChatRequest {
    message: string;
    conversationId?: string;
}

function validateChatResponse(
    value: unknown
): Record<string, unknown> {
    if (
        typeof value !== "object" ||
        value === null ||
        Array.isArray(value)
    ) {
        throw new Error("Invalid chat response");
    }

    return value as Record<string, unknown>;
}

export async function POST(
    request: NextRequest
) {
    try {

        const body =
            await request.json() as ChatRequest;

        if (
            !body.message ||
            body.message.trim().length === 0
        ) {
            return NextResponse.json(
                {
                    error:
                        "Message is required"
                },
                {
                    status: 400
                }
            );
        }

        const backendURL =
            process.env.AI_BACKEND_URL;

        if (!backendURL) {
            return NextResponse.json(
                {
                    error:
                        "AI backend is not configured"
                },
                {
                    status: 500
                }
            );
        }

        const backendResponse =
            await fetch(
                `${backendURL}/api/ai/chat`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type":
                            "application/json"
                    },
                    body:
                        JSON.stringify(body),
                    cache: "no-store"
                }
            );

        if (!backendResponse.ok) {
            return NextResponse.json(
                {
                    error:
                        "AI backend request failed"
                },
                {
                    status:
                        backendResponse.status
                }
            );
        }

        const raw: unknown =
            await backendResponse.json();

        const data =
            validateChatResponse(raw);

        return NextResponse.json(data);

    } catch (error) {

        console.error(
            "Chat API error:",
            error
        );

        return NextResponse.json(
            {
                error:
                    "Internal server error"
            },
            {
                status: 500
            }
        );
    }
}