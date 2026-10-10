from dataclasses import dataclass
import json


@dataclass
class Message:
    role: str
    content: str

    def to_dict(self) -> dict[str, str]:
        return {
            "role": self.role,
            "content": self.content
        }


messages = [
    Message(role="user", content="Who invented basketball?"),
    Message(role="assistant", content="Dr. James Naismith"),
    Message(role="user", content="Are you sure?"),
    Message(role="assistant", content="Yes, I am."),
    Message(role="user", content="Thanks")
]

user_records = []

for message in messages:
    if message.role == "user":
        user_records.append(message.to_dict())

for record in user_records:
    print(record["content"])

with open("message_list.json", "w") as file:
    json.dump(user_records, file)

with open("message_list.json", "r") as file:
    loaded_records = json.load(file)

print(loaded_records[0]["content"])

while True:
    user_role = input("Enter a role, or 'quit' to finish: ")

    if user_role == "quit":
        break

    user_content = input("Enter message content: ")

    new_message = Message(
        role=user_role,
        content=user_content
    )

    messages.append(new_message)

for message in messages:
    print(message.role, message.content)

all_records = []

for message in messages:
    all_records.append(message.to_dict())

with open("message_list.json", "w") as file:
    json.dump(all_records, file, indent=2)