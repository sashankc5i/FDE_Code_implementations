"use server";

import {
    cookies
} from "next/headers";

import {
    redirect
} from "next/navigation";

export async function loginAction(
    formData: FormData
) {
    const username =
        String(
            formData.get(
                "username"
            ) ?? ""
        );

    const password =
        String(
            formData.get(
                "password"
            ) ?? ""
        );

    const expectedUser =
        process.env.DEMO_AUTH_USER ??
        "demo-user";

    const expectedPassword =
        process.env.DEMO_AUTH_PASSWORD ??
        "demo-password";

    if (
        username !== expectedUser ||
        password !== expectedPassword
    ) {
        redirect(
            "/login?error=invalid"
        );
    }

    const cookieStore =
        await cookies();

    cookieStore.set(
        "ai_session",
        "authenticated",
        {
            httpOnly: true,

            sameSite: "lax",

            secure:
                process.env.NODE_ENV ===
                "production",

            path: "/",

            maxAge:
                60 * 60 * 8
        }
    );

    redirect("/chat");
}

export async function logoutAction() {
    const cookieStore =
        await cookies();

    cookieStore.delete(
        "ai_session"
    );

    redirect("/login");
}

export async function createConversation(
    formData: FormData
) {
    const cookieStore =
        await cookies();

    const session =
        cookieStore.get(
            "ai_session"
        );

    if (
        session?.value !==
        "authenticated"
    ) {
        redirect("/login");
    }

    const title =
        String(
            formData.get(
                "title"
            ) ?? ""
        ).trim();

    if (!title) {
        throw new Error(
            "Conversation title is required"
        );
    }

    /*
     * Production implementation:
     *
     * Save conversation to Azure SQL
     * and associate it with the
     * authenticated Entra ID user.
     */

    return {
        conversationId:
            `CONV-${Date.now()}`,

        title
    };
}