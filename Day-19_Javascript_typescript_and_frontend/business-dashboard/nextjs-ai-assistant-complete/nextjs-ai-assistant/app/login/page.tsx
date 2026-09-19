import {
    loginAction
} from "@/app/actions";

export default async function LoginPage({
    searchParams
}: {
    searchParams: Promise<{
        error?: string;
    }>;
}) {

    const params =
        await searchParams;

    return (
        <main className="container narrow">

            <section className="panel">

                <p className="eyebrow">
                    Authentication
                </p>

                <h1>
                    Sign in
                </h1>

                {params.error ===
                    "invalid" && (
                    <p className="error">
                        Invalid credentials.
                    </p>
                )}

                <form
                    action={loginAction}
                    className="form"
                >

                    <label>
                        Username

                        <input
                            name="username"
                            required
                        />
                    </label>

                    <label>
                        Password

                        <input
                            name="password"
                            type="password"
                            required
                        />
                    </label>

                    <button
                        className="button"
                        type="submit"
                    >
                        Sign in
                    </button>

                </form>

                <p className="muted">
                    Training credentials:
                    demo-user / demo-password
                </p>

            </section>

        </main>
    );
}