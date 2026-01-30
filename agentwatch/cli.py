#!/usr/bin/env python3
"""
AgentWatch CLI - Command line interface
"""

import argparse
import sys
from agentwatch import Watch


def main():
    parser = argparse.ArgumentParser(
        description="AgentWatch - Open Source Observability for AI Agents"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Dashboard command
    dashboard_parser = subparsers.add_parser("dashboard", help="Start dashboard")
    dashboard_parser.add_argument(
        "--port", "-p",
        type=int,
        default=3000,
        help="Port to run dashboard on (default: 3000)"
    )
    dashboard_parser.add_argument(
        "--db",
        type=str,
        default="agentwatch.db",
        help="Database path (default: agentwatch.db)"
    )
    dashboard_parser.add_argument(
        "--debug",
        action="store_true",
        help="Run in debug mode"
    )
    
    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Show statistics")
    stats_parser.add_argument(
        "--agent",
        type=str,
        help="Filter by agent name"
    )
    stats_parser.add_argument(
        "--db",
        type=str,
        default="agentwatch.db",
        help="Database path (default: agentwatch.db)"
    )
    
    # List command
    list_parser = subparsers.add_parser("list", help="List all agents")
    list_parser.add_argument(
        "--db",
        type=str,
        default="agentwatch.db",
        help="Database path (default: agentwatch.db)"
    )
    
    # Export command
    export_parser = subparsers.add_parser("export", help="Export data")
    export_parser.add_argument(
        "filename",
        type=str,
        help="Output filename"
    )
    export_parser.add_argument(
        "--format",
        type=str,
        choices=["csv", "json"],
        default="csv",
        help="Export format (default: csv)"
    )
    export_parser.add_argument(
        "--db",
        type=str,
        default="agentwatch.db",
        help="Database path (default: agentwatch.db)"
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Initialize Watch
    watch = Watch(db_path=args.db)
    
    # Execute command
    if args.command == "dashboard":
        print(f"🚀 Starting AgentWatch Dashboard on http://localhost:{args.port}")
        print("Press Ctrl+C to stop\n")
        watch.dashboard(port=args.port, debug=args.debug)
    
    elif args.command == "stats":
        stats = watch.stats(agent_name=args.agent)
        
        if args.agent:
            print(f"\n📊 Stats for '{args.agent}':")
            print(f"Total calls: {stats.get('total_calls', 0)}")
            print(f"Total cost: ${stats.get('total_cost', 0):.4f}")
            print(f"Total errors: {stats.get('total_errors', 0)}")
            print(f"Avg duration: {stats.get('avg_duration_ms', 0):.0f}ms")
            print(f"Error rate: {stats.get('error_rate', 0)*100:.1f}%")
        else:
            print(f"\n📊 Overall Stats:")
            print(f"Total agents: {stats.get('total_agents', 0)}")
            print(f"Total calls: {stats.get('total_calls', 0)}")
            print(f"Total cost: ${stats.get('total_cost', 0):.4f}")
            
            if stats.get('agents'):
                print("\n🤖 Agents:")
                for agent in stats['agents']:
                    print(f"  • {agent['name']}: {agent['total_calls']} calls, ${agent['total_cost']:.4f}")
    
    elif args.command == "list":
        agents = watch.list_agents()
        
        if not agents:
            print("\n⚠️  No agents found. Start using @watch.agent() decorator!")
        else:
            print(f"\n🤖 Found {len(agents)} agent(s):\n")
            for agent in agents:
                print(f"📋 {agent['name']}")
                print(f"   Tags: {', '.join(agent['tags']) if agent['tags'] else 'none'}")
                print(f"   Calls: {agent['total_calls']}")
                print(f"   Cost: ${agent['total_cost']:.4f}")
                print(f"   Errors: {agent['total_errors']}")
                print(f"   Avg duration: {agent['avg_duration_ms']:.0f}ms")
                print()
    
    elif args.command == "export":
        watch.export(args.filename, format=args.format)
        print(f"✅ Exported to {args.filename}")


if __name__ == "__main__":
    main()
