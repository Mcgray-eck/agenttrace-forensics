from src.tools.file_reader import read_file
from src.policy.access_policy import check_file_access

def decide_action(user_input: str) -> dict:
    text = user_input.lower()

    if "secret" in text:
        return {
            "type": "tool_request",
            "tool": "read_file",
            "path": "sandbox/secret/credentials.txt"
        }

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
            policy_result = check_file_access(decision["path"])

            print("Policy decision:")
            print(policy_result)

            if policy_result["policy_decision"] == "ALLOW":
                result = read_file(decision["path"])

                print("Tool result:")
                print(result)
            else:
                print("Tool blocked.")

if __name__ == "__main__":
    main()