"""
Flask dashboard for AgentWatch
"""

from flask import Flask, render_template_string, jsonify, request
from .storage import Storage


DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>AgentWatch Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #f5f7fa;
            padding: 20px;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        .header h1 { font-size: 2em; margin-bottom: 10px; }
        .header p { opacity: 0.9; }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .stat-card h3 {
            color: #666;
            font-size: 0.9em;
            margin-bottom: 10px;
        }
        .stat-card .value {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        .agents-list {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        .agents-list h2 {
            margin-bottom: 20px;
            color: #333;
        }
        .agent-card {
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 15px;
        }
        .agent-name {
            font-size: 1.3em;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        }
        .agent-stats {
            display: flex;
            gap: 20px;
            font-size: 0.9em;
            color: #666;
        }
        .calls-list {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .calls-list h2 {
            margin-bottom: 20px;
            color: #333;
        }
        .call-card {
            border-left: 4px solid #4caf50;
            padding: 15px;
            margin-bottom: 10px;
            background: #f9f9f9;
            border-radius: 4px;
        }
        .call-card.error {
            border-left-color: #f44336;
        }
        .call-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 5px;
        }
        .call-agent {
            font-weight: bold;
            color: #333;
        }
        .call-time {
            color: #999;
            font-size: 0.9em;
        }
        .call-stats {
            font-size: 0.85em;
            color: #666;
        }
        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #999;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>👁️ AgentWatch</h1>
        <p>Open Source Observability for AI Agents</p>
    </div>

    <div class="stats">
        <div class="stat-card">
            <h3>Total Agents</h3>
            <div class="value" id="total-agents">0</div>
        </div>
        <div class="stat-card">
            <h3>Total Calls</h3>
            <div class="value" id="total-calls">0</div>
        </div>
        <div class="stat-card">
            <h3>Total Cost</h3>
            <div class="value" id="total-cost">$0.00</div>
        </div>
    </div>

    <div class="agents-list">
        <h2>📋 Agents</h2>
        <div id="agents-container"></div>
    </div>

    <div class="calls-list">
        <h2>📞 Recent Calls</h2>
        <div id="calls-container"></div>
    </div>

    <script>
        async function loadData() {
            // Load stats
            const statsRes = await fetch('/api/stats');
            const stats = await statsRes.json();
            
            document.getElementById('total-agents').textContent = stats.total_agents || 0;
            document.getElementById('total-calls').textContent = stats.total_calls || 0;
            document.getElementById('total-cost').textContent = '$' + (stats.total_cost || 0).toFixed(2);
            
            // Load agents
            const agentsRes = await fetch('/api/agents');
            const agents = await agentsRes.json();
            
            const agentsContainer = document.getElementById('agents-container');
            if (agents.length === 0) {
                agentsContainer.innerHTML = '<div class="empty-state">No agents yet. Start using @watch.agent() decorator!</div>';
            } else {
                agentsContainer.innerHTML = agents.map(agent => `
                    <div class="agent-card">
                        <div class="agent-name">${agent.name}</div>
                        <div class="agent-stats">
                            <span>📞 ${agent.total_calls} calls</span>
                            <span>💰 $${agent.total_cost.toFixed(2)}</span>
                            <span>⚡ ${agent.avg_duration_ms.toFixed(0)}ms avg</span>
                            <span>❌ ${agent.total_errors} errors</span>
                        </div>
                    </div>
                `).join('');
            }
            
            // Load recent calls
            const callsRes = await fetch('/api/calls?limit=20');
            const calls = await callsRes.json();
            
            const callsContainer = document.getElementById('calls-container');
            if (calls.length === 0) {
                callsContainer.innerHTML = '<div class="empty-state">No calls yet.</div>';
            } else {
                callsContainer.innerHTML = calls.map(call => `
                    <div class="call-card ${call.status === 'error' ? 'error' : ''}">
                        <div class="call-header">
                            <span class="call-agent">${call.agent_name}</span>
                            <span class="call-time">${new Date(call.timestamp).toLocaleString()}</span>
                        </div>
                        <div class="call-stats">
                            ${call.status === 'success' ? '✅' : '❌'} ${call.status} | 
                            ⚡ ${call.duration_ms}ms | 
                            💰 $${call.cost.toFixed(4)}
                            ${call.error ? ' | ⚠️ ' + call.error : ''}
                        </div>
                    </div>
                `).join('');
            }
        }
        
        // Load data on page load
        loadData();
        
        // Refresh every 5 seconds
        setInterval(loadData, 5000);
    </script>
</body>
</html>
"""


def start_dashboard(storage: Storage, port: int = 3000, debug: bool = False):
    """Start Flask dashboard"""
    app = Flask(__name__)
    
    @app.route('/')
    def index():
        return render_template_string(DASHBOARD_HTML)
    
    @app.route('/api/stats')
    def api_stats():
        return jsonify(storage.get_stats())
    
    @app.route('/api/agents')
    def api_agents():
        return jsonify(storage.list_agents())
    
    @app.route('/api/calls')
    def api_calls():
        limit = int(request.args.get('limit', 100))
        agent_name = request.args.get('agent_name')
        return jsonify(storage.get_calls(agent_name, limit))
    
    print(f"\n🚀 AgentWatch Dashboard running on http://localhost:{port}\n")
    app.run(host='0.0.0.0', port=port, debug=debug)
