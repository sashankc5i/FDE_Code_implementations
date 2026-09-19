"use client";

import { useState } from "react";

interface ChatResponse {
    requestId: string;
    answer: string;
    model: string;
}

export default function ChatInput() {
    const [message, setMessage] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [response, setResponse] =
        useState<ChatResponse | null>(null);
    const [error, setError] =
        useState<string | null>(null);

    async function handleSubmit() {
        if (!message.trim()) {
            return;
        }

        setIsLoading(true);
        setError(null);
        setResponse(null);

        try {
            const apiResponse = await fetch(
                "/api/chat",
                {
                    method: "POST",
                    headers: {
                        "Content-Type":
                            "application/json"
                    },
                    body: JSON.stringify({
                        message
                    })
                }
            );

            if (!apiResponse.ok) {
                throw new Error(
                    "Failed to contact AI assistant"
                );
            }

            const data = (await apiResponse.json()) as ChatResponse;

            setResponse(data);
            setMessage("");

        } catch (error) {

            console.error(
                "Chat error:",
                error
            );

            setError(
                "Unable to get a response from the AI assistant."
            );

        } finally {
            setIsLoading(false);
        }
    }

    return (
        <section>
            <div>
                <input
                    value={message}
                    onChange={(event) =>
                        setMessage(event.target.value)
                    }
                    onKeyDown={(event) => {
                        if (
                            event.key === "Enter" &&
                            !isLoading
                        ) {
                            handleSubmit();
                        }
                    }}
                    placeholder="Ask about a pipeline incident..."
                    disabled={isLoading}
                />

                <button
                    onClick={handleSubmit}
                    disabled={
                        isLoading ||
                        !message.trim()
                    }
                >
                    {isLoading
                        ? "Thinking..."
                        : "Send"}
                </button>
            </div>

            {error && (
                <p>
                    {error}
                </p>
            )}

            {response && (
                <div>
                    <h2>
                        AI Response
                    </h2>

                    <p>
                        {response.answer}
                    </p>

                    <small>
                        Model: {response.model}
                    </small>
                </div>
            )}
        </section>
    );
}