import {
    NextRequest,
    NextResponse
} from "next/server";

export function middleware(
    request: NextRequest
) {
    const session =
        request.cookies.get(
            "ai_session"
        )?.value;

    const pathname =
        request.nextUrl.pathname;

    const protectedRoute =
        pathname.startsWith("/chat") ||
        pathname.startsWith("/incidents");

    if (
        protectedRoute &&
        session !== "authenticated"
    ) {
        const loginURL =
            new URL(
                "/login",
                request.url
            );

        loginURL.searchParams.set(
            "next",
            pathname
        );

        return NextResponse.redirect(
            loginURL
        );
    }

    if (
        pathname === "/login" &&
        session === "authenticated"
    ) {
        return NextResponse.redirect(
            new URL(
                "/chat",
                request.url
            )
        );
    }

    return NextResponse.next();
}

export const config = {
    matcher: [
        "/chat/:path*",
        "/incidents/:path*",
        "/login"
    ]
};