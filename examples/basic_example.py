"""
Basic example of using AgentWatch
"""

from agentwatch import watch
import time
import random


@watch.agent(name="email-sender", tags=["production", "email"])
def send_email(to: str, subject: str, body: str):
    """Simulated email sending agent"""
    print(f"📧 Sending email to {to}")
    time.sleep(random.uniform(0.1, 0.5))  # Simulate API call
    
    # Simulate occasional failures
    if random.random() < 0.1:
        raise Exception("SMTP connection failed")
    
    return {"status": "sent", "message_id": f"msg_{random.randint(1000, 9999)}"}


@watch.agent(name="data-processor", tags=["production", "etl"])
def process_data(data: list):
    """Simulated data processing agent"""
    print(f"⚙️ Processing {len(data)} items")
    time.sleep(random.uniform(0.2, 0.8))
    
    processed = [item.upper() for item in data]
    return {"processed": len(processed), "items": processed}


@watch.agent(name="slack-notifier", tags=["notifications"])
def send_slack_message(channel: str, message: str):
    """Simulated Slack notification agent"""
    print(f"💬 Sending to #{channel}: {message}")
    time.sleep(random.uniform(0.05, 0.2))
    return {"ok": True, "channel": channel}


if __name__ == "__main__":
    print("🚀 Running AgentWatch example...\n")
    
    # Simulate some agent calls
    for i in range(10):
        try:
            # Email agent
            result = send_email(
                to=f"user{i}@example.com",
                subject="Test Email",
                body="Hello from AgentWatch!"
            )
            print(f"✅ Email sent: {result}\n")
        except Exception as e:
            print(f"❌ Email failed: {e}\n")
        
        # Data processor
        data = [f"item_{j}" for j in range(random.randint(5, 15))]
        result = process_data(data)
        print(f"✅ Data processed: {result}\n")
        
        # Slack notifier
        result = send_slack_message(
            channel="general",
            message=f"Batch {i} completed"
        )
        print(f"✅ Slack sent: {result}\n")
        
        time.sleep(0.5)
    
    print("\n📊 Statistics:")
    stats = watch.stats()
    print(f"Total agents: {stats['total_agents']}")
    print(f"Total calls: {stats['total_calls']}")
    print(f"Total cost: ${stats['total_cost']:.4f}")
    
    print("\n🎯 Starting dashboard on http://localhost:3000")
    print("Press Ctrl+C to stop\n")
    
    watch.dashboard(port=3000)
