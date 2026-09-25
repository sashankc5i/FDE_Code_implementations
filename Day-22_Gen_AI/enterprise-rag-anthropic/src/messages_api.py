from dataclasses import dataclass


@dataclass
class MockTextBlock:
    type: str
    text: str


@dataclass
class MockMessageResponse:
    id: str
    model: str
    role: str
    content: list
    stop_reason: str


def create_mock_message():
    return MockMessageResponse(
        id="msg_training_001",
        model="claude-training-model",
        role="assistant",
        content=[
            MockTextBlock(
                type="text",
                text="HTTP 401 means the request is not properly authenticated."
            )
        ],
        stop_reason="end_turn"
    )


if __name__ == "__main__":
    response = create_mock_message()

    print("\n========== MESSAGES API ==========")

    print(f"\nResponse ID:")
    print(response.id)

    print(f"\nModel:")
    print(response.model)

    print(f"\nRole:")
    print(response.role)

    print(f"\nStop reason:")
    print(response.stop_reason)

    print("\nContent:")

    for block in response.content:
        print(f"Block type: {block.type}")
        print(f"Text: {block.text}")