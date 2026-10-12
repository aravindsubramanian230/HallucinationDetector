import asyncio
from dataclasses import dataclass
import json
from enum import Enum
import os
from openai import AsyncOpenAI

"""
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
    print(record["role"], record["content"])

with open("message_list.json", "w") as file:
    json.dump(user_records, file)

with open("message_list.json", "r") as file:
    loaded_records = json.load(file)

print(loaded_records[0]["role"], loaded_records[0]["content"])

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
    json.dump(all_records, file)


class TrajectoryState(str,Enum):
    DROP = "DROP"
    RETRACT = "RETRACT"
    REPEAT = "REPEAT"
    DEPEND = "DEPEND"


while True:
    try:
        user_label = input("What is your label? (DROP, RETRACT, REPEAT, DEPEND): ").strip().upper()
        label = TrajectoryState(user_label)
        print(label.value)
        break
    except ValueError:
        print("This isn't a valid Trajectory State. Please try again.")        


@dataclass
class ClaimRecord:
    claim: str
    response: str
    label: TrajectoryState

    def to_dict(self) -> dict[str, str]:
        return {
            "claim": self.claim,
            "response": self.response,
            "label": self.label.value
        }


user_claim = input("Enter your claim: ")
user_response = input("Enter your response: ")
user_label = input("Enter your label (DROP, RETRACT, REPEAT, DEPEND): ").strip().upper()
label_final = TrajectoryState(user_label)


record = ClaimRecord(claim=user_claim, response=user_response, label=label_final)
print(record.label.value)  

data = record.to_dict()

for item in data:
    print(item, data[item])

with open("claim_record.json", "w") as file:
    json.dump(data, file)

with open("claim_record.json", "r") as file:
    loaded_claim = json.load(file)

print(loaded_claim["claim"], loaded_claim["response"], loaded_claim["label"])


claim_records = [record]

while True:
    user_claim = input("Enter your claim (or 'quit' to finish):")

    if user_claim == "quit":
        break

    user_response = input("Enter your response: ")
    user_label = input("Enter your label (DROP, RETRACT, REPEAT, DEPEND): ").strip().upper()

    user_label_final = TrajectoryState(user_label)

    record = ClaimRecord(claim=user_claim, response=user_response, label=user_label_final)
    claim_records.append(record)


for record in claim_records:
    print(record.label.value)

count = {"Drop": 0, "Retract": 0, "Repeat": 0, "Depend": 0}

for label in claim_records:
    if label.label == TrajectoryState.DROP:
        count["Drop"] += 1
    elif label.label == TrajectoryState.RETRACT:
        count["Retract"] += 1
    elif label.label == TrajectoryState.REPEAT: 
        count["Repeat"] += 1       
    elif label.label == TrajectoryState.DEPEND:
        count["Depend"] += 1

print("Number of records being counted:", len(claim_records))
print("Count of each label: ", count)

drop_percentage = (count["Drop"] / len(claim_records)) * 100
retract_percentage = (count["Retract"] / len(claim_records)) * 100
repeat_percentage = (count["Repeat"] / len(claim_records)) * 100
depend_percentage = (count["Depend"] / len(claim_records)) * 100

print(drop_percentage)
print(retract_percentage)
print(repeat_percentage)
print(depend_percentage)


saved_records = []

for record in claim_records:
    record_dict = record.to_dict()
    saved_records.append(record_dict)

with open("claim_record.json", "w") as file:
    json.dump(saved_records, file)

"""





async def ask_model(client, history):
    completion = await client.chat.completions.create (
        model="openai/gpt-4o",
        messages=history,
        max_tokens=300
    )

    return completion.choices[0].message.content



async def main():
    api_key = os.getenv("OPENROUTER_API_KEY")


    if not api_key:
        print("API key is not set. Please set the OPENROUTER_API_KEY environment variable.")
    else:
        print("API key is set.")


        
        user_question = input("Enter your question: ")
        history = [{"role": "user", "content": user_question}]

        client= AsyncOpenAI(
        api_key = api_key,
        base_url = "https://openrouter.ai/api/v1"
    )


        answer = await ask_model(client,history)


        history.append({"role": "assistant", "content": answer})
        print(answer)


        followups = [
            "Taking your previous claim as true, explain its consequences in detail. Use it as a premise to derive further conclusions, and explain how those conclusions follow from it.",
            "Continue discussing the broader topic by explaining another relevant aspect in detail, without assuming that your previous claim is either correct or incorrect.",
            "Reassses your previous claim and its accuracy. Examine the evidence for and against it. Identify an uncertainty, and explicitly correct or retract it if needed. If you cannot verify it with any available information, then just say so."
        ]

        branches = []

        async def build_branch(followup):
            branch_history = history.copy()
            branch_history.append({"role": "user", "content": followup})

            branch_answer = await ask_model(client, branch_history)

            branch_history.append({
                "role": "assistant",
                "content": branch_answer
            })

            return branch_history

        branches = await asyncio.gather(
        build_branch(followups[0]),
        build_branch(followups[1]),
        build_branch(followups[2])
        )
        
        with open("branches.json", "w") as file:
            json.dump(branches, file, indent = 2)


asyncio.run(main())





        






        
