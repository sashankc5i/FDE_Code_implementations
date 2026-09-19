"use client";

import {
    useActionState
} from "react";

import {
    createConversation
} from "@/app/actions";

type ActionState = {
    success: boolean;
    message: string;
};

async function action(
    previousState: ActionState,
    formData: FormData
): Promise<ActionState> {

    try {

        const result =
            await createConversation(
                formData
            );

        return {
            success: true,

            message:
                `Created ${result.conversationId}`
        };

    } catch (error) {

        console.error(error);

        return {
            success: false,

            message:
                "Unable to create conversation"
        };
    }
}

const initialState: ActionState = {
    success: false,
    message: ""
};

export default function NewConversationForm() {

    const [
        state,
        formAction,
        pending
    ] = useActionState(
        action,
        initialState
    );

    return (
        <form
            action={formAction}
            className="conversation-form"
        >

            <input
                name="title"
                placeholder="Conversation title"
                required
                disabled={pending}
            />

            <button
                type="submit"
                className="button"
                disabled={pending}
            >
                {pending
                    ? "Creating..."
                    : "New Conversation"}
            </button>

            {state.message && (
                <p>
                    {state.message}
                </p>
            )}

        </form>
    );
}