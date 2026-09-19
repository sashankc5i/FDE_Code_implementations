"use client";

import {
    useState
} from "react";

interface ChatResponse {
    requestId: string;
    answer: string;
    model: string;
}

export default function ChatInput() {

    const [
        message,
        setMessage
    ] = useState("");

    const [
        response,
        setResponse
    ] = useState<ChatResponse | null>(
        null
    );

    const [
        streamedAnswer,
        setStreamedAnswer
    ] = useState("");

    const [
        isLoading,
        setIsLoading
    ] = useState(false);

    const [
        isStreaming,
        setIsStreaming
    ] = useState(false);

    const [
        error,
        setError
    ] = useState<string | null>(
        null
    );

    async function handleSubmit() {

        if (!message.trim()) {
            return;
        }

        setIsLoading(true);
        setError(null);
        setResponse(null);

        try {

            const apiResponse =
                await fetch(
                    "/api/chat",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify({
                                message
                            })
                    }
                );

            if (!apiResponse.ok) {
                throw new Error(
                    "AI request failed"
                );
            }

            const data =
                (await apiResponse.json()) as ChatResponse;

            setResponse(data);
            setMessage("");

        } catch (error) {

            console.error(error);

            setError(
                "Unable to contact the AI assistant."
            );

        } finally {

            setIsLoading(false);
        }
    }

    async function handleStreamingSubmit() {

        if (!message.trim()) {
            return;
        }

        setIsStreaming(true);
        setError(null);
        setResponse(null);
        setStreamedAnswer("");

        try {

            const apiResponse =
                await fetch(
                    "/api/chat/stream",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify({
                                message
                            })
                    }
                );

            if (
                !apiResponse.ok ||
                !apiResponse.body
            ) {
                throw new Error(
                    "Streaming request failed"
                );
            }

            const reader =
                apiResponse.body
                    .getReader();

            const decoder =
                new TextDecoder();

            let accumulated = "";

            while (true) {

                const {
                    value,
                    done
                } =
                    await reader.read();

                if (done) {
                    break;
                }

                const chunk =
                    decoder.decode(
                        value,
                        {
                            stream: true
                        }
                    );

                accumulated += chunk;

                setStreamedAnswer(
                    accumulated
                );
            }

            setMessage("");

        } catch (error) {

            console.error(error);

            setError(
                "Unable to stream the AI response."
            );

        } finally {

            setIsStreaming(false);
        }
    }

    return (
        <section className="chat">

            <div className="chat-input-row">

                <input
                    value={message}

                    onChange={(event) =>
                        setMessage(
                            event.target.value
                        )
                    }

                    onKeyDown={(event) => {

                        if (
                            event.key ===
                                "Enter" &&
                            !isLoading &&
                            !isStreaming
                        ) {
                            handleSubmit();
                        }
                    }}

                    placeholder="Ask about a pipeline incident..."

                    disabled={
                        isLoading ||
                        isStreaming
                    }
                />

                <button
                    className="button"

                    onClick={
                        handleSubmit
                    }

                    disabled={
                        isLoading ||
                        isStreaming ||
                        !message.trim()
                    }
                >
                    {isLoading
                        ? "Thinking..."
                        : "Ask"}
                </button>

                <button
                    className="button secondary"

                    onClick={
                        handleStreamingSubmit
                    }

                    disabled={
                        isLoading ||
                        isStreaming ||
                        !message.trim()
                    }
                >
                    {isStreaming
                        ? "Streaming..."
                        : "Stream"}
                </button>

            </div>

            {error && (
                <p className="error">
                    {error}
                </p>
            )}

            {response && (
                <article className="response-card">

                    <h2>
                        AI Response
                    </h2>

                    <p>
                        {response.answer}
                    </p>

                    <small>
                        Request:
                        {" "}
                        {response.requestId}

                        {" • "}

                        Model:
                        {" "}
                        {response.model}
                    </small>

                </article>
            )}

            {streamedAnswer && (
                <article className="response-card">

                    <h2>
                        Streaming Response
                    </h2>

                    <p>
                        {streamedAnswer}
                    </p>

                </article>
            )}

        </section>
    );
}