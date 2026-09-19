import {
    AIClient,
    APIError
} from "./index";


const client = new AIClient(
    "http://127.0.0.1:8000"
);


async function testAIClient(): Promise<void> {

    try {

        const health =
            await client.health();

        console.log(
            "AI Health:",
            health
        );


        const chatResponse =
            await client.chat({
                message:
                    "Why did my Customer 360 pipeline fail?",
                conversationId:
                    "CONV-001"
            });

        console.log(
            "AI Chat:",
            chatResponse
        );


        const analysisResponse =
            await client.analyze({
                text:
                    "Customer 360 failed because customer_segment was missing.",
                analysisType:
                    "root-cause"
            });

        console.log(
            "AI Analysis:",
            analysisResponse
        );

    } catch (error) {

        if (error instanceof APIError) {

            console.error(
                "AI API Error:",
                error.status,
                error.endpoint,
                error.message
            );

        } else {

            console.error(
                "Unexpected error:",
                error
            );
        }
    }
}


testAIClient();