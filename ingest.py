import os
from rag import add_note

path = "knowledge"

for file in os.listdir(path):

    full = os.path.join(path, file)

    if os.path.isfile(full):

        with open(full, "r") as f:

            add_note(
                f.read(),
                file
            )

print("Knowledge ingested")
