import {
    NextRequest,
    NextResponse
} from "next/server";

interface ChatRequest {
    message: string;
    conversationId?: string;
}

interface ChatResponse {
    requestId: string;
    answer: string;
    model: string;
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
                    error: "Message is required"
                },
                {
                    status: 400
                }
            );
        }

        const backendURL =
            process.env.AI_BACKEND_URL;

        if (!backendURL) {
            console.error(
                "AI_BACKEND_URL is not configured"
            );

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
                    body: JSON.stringify(body)
                }
            );

        if (!backendResponse.ok) {
            console.error(
                "AI backend returned:",
                backendResponse.status
            );

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

        const data = await backendResponse.json() as ChatResponse;

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