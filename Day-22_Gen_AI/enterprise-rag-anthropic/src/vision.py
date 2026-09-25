import base64
from pathlib import Path


def encode_image(image_path: str) -> str:
    path = Path(image_path)

    with open(path, "rb") as image_file:
        return base64.b64encode(
            image_file.read()
        ).decode("utf-8")


def build_vision_message(image_path: str, question: str):
    image_data = encode_image(image_path)

    return {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": question
            },
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": image_data
                }
            }
        ]
    }


if __name__ == "__main__":
    print("\n========== VISION MESSAGE ==========")

    print("""
A multimodal message contains:

1. Text instruction
2. Image content
3. Image encoding
""")