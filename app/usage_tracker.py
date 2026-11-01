usage_data = {
    "total_requests": 0,
    "prompt_tokens": 0,
    "completion_tokens": 0,
    "total_tokens": 0
}


def record_usage(usage):
    prompt = usage.get("prompt_tokens") or 0
    completion = usage.get("completion_tokens") or 0

    usage_data["total_requests"] += 1
    usage_data["prompt_tokens"] += prompt
    usage_data["completion_tokens"] += completion
    usage_data["total_tokens"] += prompt + completion


def get_usage():
    return usage_data.copy()