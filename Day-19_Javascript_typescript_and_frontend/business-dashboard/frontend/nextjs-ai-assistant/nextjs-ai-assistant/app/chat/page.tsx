export default function ChatPage() {
    return (
        <main>
            <h1>
                AI Incident Assistant
            </h1>

            <p>
                Ask questions about your
                data engineering incidents.
            </p>

            <form>
                <label htmlFor="incident-question">Your question</label>
                <input
                    id="incident-question"
                    name="question"
                    type="text"
                    placeholder="Describe an incident..."
                />
                <button type="submit">Ask</button>
            </form>
        </main>
    );
}