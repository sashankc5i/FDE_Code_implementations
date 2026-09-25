import time


def stream_response(text: str):
    words = text.split()

    for word in words:
        yield word + " "
        time.sleep(0.2)


if __name__ == "__main__":
    response = (
        "HTTP 401 errors commonly occur because "
        "the authentication token is invalid or expired."
    )

    print("\n========== STREAMING ==========\n")

    for chunk in stream_response(response):
        print(chunk, end="", flush=True)

    print("\n")