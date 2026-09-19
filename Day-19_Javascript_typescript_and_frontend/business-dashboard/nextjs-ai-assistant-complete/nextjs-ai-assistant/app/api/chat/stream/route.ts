import { NextRequest } from "next/server";

export const runtime = "nodejs";

export async function POST(
    request: NextRequest
) {
    const body =
        await request.json() as {
            message?: string;
            conversationId?: string;
        };

    if (!body.message?.trim()) {
        return new Response(
            "Message is required",
            {
                status: 400
            }
        );
    }

    const backendURL =
        process.env.AI_BACKEND_URL;

    if (!backendURL) {
        return new Response(
            "AI backend is not configured",
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
        return new Response(
            "AI backend request failed",
            {
                status:
                    backendResponse.status
            }
        );
    }

    const raw =
        await backendResponse.json() as {
            answer?: unknown;
        };

    if (
        typeof raw.answer !== "string"
    ) {
        return new Response(
            "Invalid AI response",
            {
                status: 502
            }
        );
    }

    const answer = raw.answer;

    const encoder =
        new TextEncoder();

    const stream =
        new ReadableStream({
            async start(controller) {

                try {

                    const chunks =
                        answer.split(
                            /(\s+)/
                        );

                    for (
                        const chunk
                        of chunks
                    ) {

                        controller.enqueue(
                            encoder.encode(
                                chunk
                            )
                        );

                        await new Promise(
                            resolve =>
                                setTimeout(
                                    resolve,
                                    35
                                )
                        );
                    }

                } catch (error) {

                    console.error(
                        "Streaming error:",
                        error
                    );

                    controller.error(
                        error
                    );

                } finally {

                    controller.close();
                }
            }
        });

    return new Response(
        stream,
        {
            headers: {
                "Content-Type":
                    "text/plain; charset=utf-8",

                "Cache-Control":
                    "no-cache, no-transform",

                "X-Accel-Buffering":
                    "no"
            }
        }
    );
}