import ChatInput from "@/components/ChatInput";
import NewConversationForm from "@/components/NewConversationForm";

export default function ChatPage() {

    return (
        <main className="container">

            <section className="panel">

                <p className="eyebrow">
                    Protected AI workspace
                </p>

                <h1>
                    AI Incident Assistant
                </h1>

                <p>
                    Investigate Customer 360
                    and other data engineering
                    incidents.
                </p>

                <NewConversationForm />

                <ChatInput />

            </section>

        </main>
    );
}