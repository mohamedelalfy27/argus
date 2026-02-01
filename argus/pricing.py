"""
Automatic cost calculation for LLM providers
"""

from typing import Optional, Dict, Any


# OpenAI Pricing (as of February 2026)
# https://openai.com/pricing
# NOTE: All prices are per 1M tokens (not 1K!)
OPENAI_PRICING = {
    # GPT-5 Family (Latest)
    "gpt-5.2": {
        "input": 1.75 / 1_000_000,    # $1.75 per 1M input tokens
        "output": 14.00 / 1_000_000,  # $14.00 per 1M output tokens
    },
    "gpt-5.1": {
        "input": 1.25 / 1_000_000,
        "output": 10.00 / 1_000_000,
    },
    "gpt-5": {
        "input": 1.25 / 1_000_000,
        "output": 10.00 / 1_000_000,
    },
    "gpt-5-mini": {
        "input": 0.25 / 1_000_000,
        "output": 2.00 / 1_000_000,
    },
    "gpt-5-nano": {
        "input": 0.05 / 1_000_000,
        "output": 0.40 / 1_000_000,
    },
    "gpt-5.2-pro": {
        "input": 21.00 / 1_000_000,
        "output": 168.00 / 1_000_000,
    },
    "gpt-5-pro": {
        "input": 15.00 / 1_000_000,
        "output": 120.00 / 1_000_000,
    },
    
    # GPT-5 Specialized (Chat variants)
    "gpt-5.2-chat-latest": {
        "input": 1.75 / 1_000_000,
        "output": 14.00 / 1_000_000,
    },
    "gpt-5.1-chat-latest": {
        "input": 1.25 / 1_000_000,
        "output": 10.00 / 1_000_000,
    },
    "gpt-5-chat-latest": {
        "input": 1.25 / 1_000_000,
        "output": 10.00 / 1_000_000,
    },
    
    # GPT-5 Specialized (Codex variants)
    "gpt-5.2-codex": {
        "input": 1.75 / 1_000_000,
        "output": 14.00 / 1_000_000,
    },
    "gpt-5.1-codex-max": {
        "input": 1.25 / 1_000_000,
        "output": 10.00 / 1_000_000,
    },
    "gpt-5.1-codex": {
        "input": 1.25 / 1_000_000,
        "output": 10.00 / 1_000_000,
    },
    "gpt-5-codex": {
        "input": 1.25 / 1_000_000,
        "output": 10.00 / 1_000_000,
    },
    
    # GPT-4.1 Family
    "gpt-4.1": {
        "input": 2.00 / 1_000_000,
        "output": 8.00 / 1_000_000,
    },
    "gpt-4.1-mini": {
        "input": 0.40 / 1_000_000,
        "output": 1.60 / 1_000_000,
    },
    "gpt-4.1-nano": {
        "input": 0.10 / 1_000_000,
        "output": 0.40 / 1_000_000,
    },
    
    # GPT-4o (Omni)
    "gpt-4o": {
        "input": 2.50 / 1_000_000,
        "output": 10.00 / 1_000_000,
    },
    "gpt-4o-2024-05-13": {
        "input": 5.00 / 1_000_000,
        "output": 15.00 / 1_000_000,
    },
    "gpt-4o-mini": {
        "input": 0.15 / 1_000_000,
        "output": 0.60 / 1_000_000,
    },
    
    # GPT-Realtime (Voice)
    "gpt-realtime": {
        "input": 4.00 / 1_000_000,
        "output": 16.00 / 1_000_000,
    },
    "gpt-realtime-mini": {
        "input": 0.60 / 1_000_000,
        "output": 2.40 / 1_000_000,
    },
    
    # GPT-4 Turbo (Legacy)
    "gpt-4-turbo": {
        "input": 0.01 / 1000,   # $0.01 per 1K input tokens
        "output": 0.03 / 1000,  # $0.03 per 1K output tokens
    },
    "gpt-4-turbo-preview": {
        "input": 0.01 / 1000,
        "output": 0.03 / 1000,
    },
    "gpt-4-1106-preview": {
        "input": 0.01 / 1000,
        "output": 0.03 / 1000,
    },
    "gpt-4-0125-preview": {
        "input": 0.01 / 1000,
        "output": 0.03 / 1000,
    },
    
    # GPT-4
    "gpt-4": {
        "input": 0.03 / 1000,   # $0.03 per 1K input tokens
        "output": 0.06 / 1000,  # $0.06 per 1K output tokens
    },
    "gpt-4-0613": {
        "input": 0.03 / 1000,
        "output": 0.06 / 1000,
    },
    "gpt-4-32k": {
        "input": 0.06 / 1000,
        "output": 0.12 / 1000,
    },
    "gpt-4-32k-0613": {
        "input": 0.06 / 1000,
        "output": 0.12 / 1000,
    },
    
    # GPT-3.5 Turbo
    "gpt-3.5-turbo": {
        "input": 0.0005 / 1000,   # $0.0005 per 1K input tokens
        "output": 0.0015 / 1000,  # $0.0015 per 1K output tokens
    },
    "gpt-3.5-turbo-0125": {
        "input": 0.0005 / 1000,
        "output": 0.0015 / 1000,
    },
    "gpt-3.5-turbo-1106": {
        "input": 0.001 / 1000,
        "output": 0.002 / 1000,
    },
    "gpt-3.5-turbo-16k": {
        "input": 0.003 / 1000,
        "output": 0.004 / 1000,
    },
    
    # GPT-4o (Omni)
    "gpt-4o": {
        "input": 0.005 / 1000,
        "output": 0.015 / 1000,
    },
    "gpt-4o-mini": {
        "input": 0.00015 / 1000,
        "output": 0.0006 / 1000,
    },
}


# Anthropic Claude Pricing
# https://www.anthropic.com/pricing
ANTHROPIC_PRICING = {
    "claude-3-opus-20240229": {
        "input": 0.015 / 1000,   # $15 per 1M input tokens
        "output": 0.075 / 1000,  # $75 per 1M output tokens
    },
    "claude-3-sonnet-20240229": {
        "input": 0.003 / 1000,   # $3 per 1M input tokens
        "output": 0.015 / 1000,  # $15 per 1M output tokens
    },
    "claude-3-haiku-20240307": {
        "input": 0.00025 / 1000,  # $0.25 per 1M input tokens
        "output": 0.00125 / 1000, # $1.25 per 1M output tokens
    },
    "claude-2.1": {
        "input": 0.008 / 1000,
        "output": 0.024 / 1000,
    },
    "claude-2.0": {
        "input": 0.008 / 1000,
        "output": 0.024 / 1000,
    },
    "claude-instant-1.2": {
        "input": 0.0008 / 1000,
        "output": 0.0024 / 1000,
    },
}


# Cohere Pricing
# https://cohere.com/pricing
COHERE_PRICING = {
    "command": {
        "input": 0.001 / 1000,
        "output": 0.002 / 1000,
    },
    "command-light": {
        "input": 0.0003 / 1000,
        "output": 0.0006 / 1000,
    },
}


def calculate_openai_cost(
    model: str,
    input_tokens: int,
    output_tokens: int
) -> float:
    """
    Calculate cost for OpenAI API call
    
    Args:
        model: Model name (e.g., "gpt-4", "gpt-3.5-turbo")
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens
    
    Returns:
        Cost in USD
    
    Example:
        >>> calculate_openai_cost("gpt-4", 1000, 500)
        0.06  # $0.03 for input + $0.03 for output
    """
    if model not in OPENAI_PRICING:
        # Try to match partial model name
        for key in OPENAI_PRICING:
            if model.startswith(key):
                model = key
                break
        else:
            # Unknown model, return 0
            return 0.0
    
    pricing = OPENAI_PRICING[model]
    input_cost = input_tokens * pricing["input"]
    output_cost = output_tokens * pricing["output"]
    
    return input_cost + output_cost


def calculate_anthropic_cost(
    model: str,
    input_tokens: int,
    output_tokens: int
) -> float:
    """
    Calculate cost for Anthropic Claude API call
    
    Args:
        model: Model name (e.g., "claude-3-opus-20240229")
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens
    
    Returns:
        Cost in USD
    """
    if model not in ANTHROPIC_PRICING:
        # Try to match partial model name
        for key in ANTHROPIC_PRICING:
            if model.startswith(key) or key.startswith(model):
                model = key
                break
        else:
            return 0.0
    
    pricing = ANTHROPIC_PRICING[model]
    input_cost = input_tokens * pricing["input"]
    output_cost = output_tokens * pricing["output"]
    
    return input_cost + output_cost


def calculate_cohere_cost(
    model: str,
    input_tokens: int,
    output_tokens: int
) -> float:
    """
    Calculate cost for Cohere API call
    
    Args:
        model: Model name (e.g., "command", "command-light")
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens
    
    Returns:
        Cost in USD
    """
    if model not in COHERE_PRICING:
        return 0.0
    
    pricing = COHERE_PRICING[model]
    input_cost = input_tokens * pricing["input"]
    output_cost = output_tokens * pricing["output"]
    
    return input_cost + output_cost


def calculate_cost(
    provider: str,
    model: str,
    input_tokens: int,
    output_tokens: int
) -> float:
    """
    Calculate cost for any LLM provider
    
    Args:
        provider: Provider name ("openai", "anthropic", "cohere")
        model: Model name
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens
    
    Returns:
        Cost in USD
    
    Example:
        >>> calculate_cost("openai", "gpt-4", 1000, 500)
        0.06
        >>> calculate_cost("anthropic", "claude-3-opus-20240229", 1000, 500)
        0.0525
    """
    provider = provider.lower()
    
    if provider == "openai":
        return calculate_openai_cost(model, input_tokens, output_tokens)
    elif provider == "anthropic":
        return calculate_anthropic_cost(model, input_tokens, output_tokens)
    elif provider == "cohere":
        return calculate_cohere_cost(model, input_tokens, output_tokens)
    else:
        return 0.0


def extract_openai_usage(response: Any) -> Optional[Dict[str, int]]:
    """
    Extract token usage from OpenAI response
    
    Args:
        response: OpenAI API response object
    
    Returns:
        Dict with input_tokens and output_tokens, or None
    
    Example:
        >>> response = openai.ChatCompletion.create(...)
        >>> usage = extract_openai_usage(response)
        >>> print(usage)
        {'input_tokens': 100, 'output_tokens': 50}
    """
    try:
        if hasattr(response, 'usage'):
            usage = response.usage
            return {
                'input_tokens': usage.prompt_tokens,
                'output_tokens': usage.completion_tokens,
                'total_tokens': usage.total_tokens
            }
    except Exception:
        pass
    
    return None


def extract_anthropic_usage(response: Any) -> Optional[Dict[str, int]]:
    """
    Extract token usage from Anthropic response
    
    Args:
        response: Anthropic API response object
    
    Returns:
        Dict with input_tokens and output_tokens, or None
    """
    try:
        if hasattr(response, 'usage'):
            usage = response.usage
            return {
                'input_tokens': usage.input_tokens,
                'output_tokens': usage.output_tokens,
                'total_tokens': usage.input_tokens + usage.output_tokens
            }
    except Exception:
        pass
    
    return None
