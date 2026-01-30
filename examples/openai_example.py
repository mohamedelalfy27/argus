"""
Example with OpenAI integration
"""

from agentwatch import watch
import os

# Uncomment when you have OpenAI installed
# from openai import OpenAI
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@watch.agent(name="gpt-assistant", tags=["openai", "production"])
def ask_gpt(prompt: str, model: str = "gpt-3.5-turbo"):
    """
    OpenAI GPT agent with cost tracking
    
    Note: Install openai first: pip install openai
    """
    # Uncomment when ready to use:
    # response = client.chat.completions.create(
    #     model=model,
    #     messages=[{"role": "user", "content": prompt}]
    # )
    # 
    # # Calculate cost (approximate)
    # input_tokens = response.usage.prompt_tokens
    # output_tokens = response.usage.completion_tokens
    # 
    # # GPT-3.5-turbo pricing (as of 2024)
    # cost = (input_tokens * 0.0015 / 1000) + (output_tokens * 0.002 / 1000)
    # 
    # return {
    #     "response": response.choices[0].message.content,
    #     "tokens": response.usage.total_tokens,
    #     "cost": cost
    # }
    
    # Placeholder for demo
    return {
        "response": f"Mock response to: {prompt}",
        "tokens": 150,
        "cost": 0.0003
    }


if __name__ == "__main__":
    print("🤖 OpenAI + AgentWatch Example\n")
    
    # Test calls
    prompts = [
        "What is the capital of France?",
        "Explain quantum computing in simple terms",
        "Write a haiku about programming"
    ]
    
    for prompt in prompts:
        print(f"📝 Prompt: {prompt}")
        result = ask_gpt(prompt)
        print(f"💬 Response: {result['response']}")
        print(f"💰 Cost: ${result['cost']:.6f}\n")
    
    # Show stats
    stats = watch.stats(agent_name="gpt-assistant")
    print(f"\n📊 GPT Assistant Stats:")
    print(f"Total calls: {stats['total_calls']}")
    print(f"Total cost: ${stats['total_cost']:.6f}")
    print(f"Avg duration: {stats['avg_duration_ms']:.0f}ms")
    
    # Start dashboard
    print("\n🎯 Dashboard: http://localhost:3000")
    watch.dashboard(port=3000)
