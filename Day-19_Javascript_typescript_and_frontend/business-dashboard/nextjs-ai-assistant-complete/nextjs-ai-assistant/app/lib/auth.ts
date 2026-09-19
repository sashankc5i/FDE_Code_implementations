import { cookies } from "next/headers";

export async function isAuthenticated(): Promise<boolean> {
    const cookieStore = await cookies();

    const session =
        cookieStore.get("ai_session");

    return session?.value === "authenticated";
}