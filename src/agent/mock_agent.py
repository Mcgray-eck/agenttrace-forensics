from src.tools.file_reader import read_file


def decide_action(user_input: str) -> dict:
    text = user_input.lower()

    if "deadline" in text:
        return {
            "type": "tool_request",
            "tool": "read_file",
            "path": "sandbox/public/project.txt"
        }

    return {
        "type": "final_response",
        "message": "No tool is needed."
    }


def main():
    user_input = input("User> ")

    decision = decide_action(user_input)

    print("Agent decision:")
    print(decision)

    if decision["type"] == "tool_request":
        if decision["tool"] == "read_file":
            result = read_file(decision["path"])

            print("Tool result:")
            print(result)


if __name__ == "__main__":
    main()