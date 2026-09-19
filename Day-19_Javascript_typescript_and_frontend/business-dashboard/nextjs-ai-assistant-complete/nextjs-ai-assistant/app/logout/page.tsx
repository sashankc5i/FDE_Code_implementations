import {
    logoutAction
} from "@/app/actions";

export default function LogoutPage() {

    return (
        <main className="container narrow">

            <section className="panel">

                <h1>
                    Sign out
                </h1>

                <form
                    action={logoutAction}
                >

                    <button
                        className="button"
                        type="submit"
                    >
                        Sign out
                    </button>

                </form>

            </section>

        </main>
    );
}