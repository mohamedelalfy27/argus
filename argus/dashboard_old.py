"""
Flask dashboard for Argus
"""

from flask import Flask, render_template_string, jsonify, request
from .storage import Storage


DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Argus — AI Agent Observability</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * { 
            margin: 0; 
            padding: 0; 
            box-sizing: border-box; 
        }
        
        :root {
            --bg-primary: #0a0a0a;
            --bg-secondary: #111111;
            --bg-tertiary: #1a1a1a;
            --border-color: #2a2a2a;
            --text-primary: #ffffff;
            --text-secondary: #a0a0a0;
            --text-tertiary: #666666;
            --accent-primary: #3b82f6;
            --accent-secondary: #8b5cf6;
            --success: #10b981;
            --error: #ef4444;
            --warning: #f59e0b;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            min-height: 100vh;
            overflow-x: hidden;
        }
        
        /* Animated background */
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 20% 50%, rgba(59, 130, 246, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(139, 92, 246, 0.1) 0%, transparent 50%);
            pointer-events: none;
            z-index: 0;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 40px 20px;
            position: relative;
            z-index: 1;
        }
        
        /* Header */
        .header {
            margin-bottom: 48px;
            animation: fadeInDown 0.6s ease-out;
        }
        
        .logo {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
        }
        
        .logo-icon {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
        }
        
        .logo-text {
            font-size: 28px;
            font-weight: 700;
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .tagline {
            color: var(--text-secondary);
            font-size: 14px;
            margin-left: 52px;
        }
        
        /* Stats Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
            animation: fadeInUp 0.6s ease-out 0.1s both;
        }
        
        .stat-card {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 24px;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.05), rgba(139, 92, 246, 0.05));
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        
        .stat-card:hover {
            border-color: var(--accent-primary);
            transform: translateY(-2px);
        }
        
        .stat-card:hover::before {
            opacity: 1;
        }
        
        .stat-label {
            color: var(--text-secondary);
            font-size: 13px;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }
        
        .stat-value {
            font-size: 36px;
            font-weight: 700;
            background: linear-gradient(135deg, var(--text-primary), var(--text-secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        /* Section */
        .section {
            margin-bottom: 40px;
            animation: fadeInUp 0.6s ease-out 0.2s both;
        }
        
        .section-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 20px;
        }
        
        .section-title {
            font-size: 20px;
            font-weight: 600;
            color: var(--text-primary);
        }
        
        .section-badge {
            background: var(--bg-tertiary);
            border: 1px solid var(--border-color);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            color: var(--text-secondary);
            font-weight: 500;
        }
        
        /* Agent Cards */
        .agents-grid {
            display: grid;
            gap: 16px;
        }
        
        .agent-card {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .agent-card:hover {
            border-color: var(--accent-primary);
            transform: translateX(4px);
        }
        
        .agent-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 16px;
        }
        
        .agent-name {
            font-size: 16px;
            font-weight: 600;
            color: var(--text-primary);
        }
        
        .agent-tags {
            display: flex;
            gap: 6px;
        }
        
        .tag {
            background: var(--bg-tertiary);
            border: 1px solid var(--border-color);
            padding: 2px 8px;
            border-radius: 6px;
            font-size: 11px;
            color: var(--text-secondary);
        }
        
        .agent-metrics {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
        }
        
        .metric {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }
        
        .metric-label {
            font-size: 11px;
            color: var(--text-tertiary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .metric-value {
            font-size: 18px;
            font-weight: 600;
            color: var(--text-primary);
        }
        
        .metric-value.success {
            color: var(--success);
        }
        
        .metric-value.error {
            color: var(--error);
        }
        
        /* Calls List */
        .calls-list {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        
        .call-card {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-left: 3px solid var(--success);
            border-radius: 8px;
            padding: 16px;
            transition: all 0.2s ease;
        }
        
        .call-card.error {
            border-left-color: var(--error);
        }
        
        .call-card:hover {
            background: var(--bg-tertiary);
        }
        
        .call-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 8px;
        }
        
        .call-agent {
            font-size: 14px;
            font-weight: 600;
            color: var(--text-primary);
        }
        
        .call-time {
            font-size: 12px;
            color: var(--text-tertiary);
        }
        
        .call-metrics {
            display: flex;
            gap: 16px;
            font-size: 12px;
            color: var(--text-secondary);
        }
        
        .call-metric {
            display: flex;
            align-items: center;
            gap: 4px;
        }
        
        /* Empty State */
        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: var(--text-tertiary);
        }
        
        .empty-icon {
            font-size: 48px;
            margin-bottom: 16px;
            opacity: 0.5;
        }
        
        .empty-text {
            font-size: 14px;
        }
        
        /* Animations */
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Status Indicator */
        .status-indicator {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            margin-right: 6px;
        }
        
        .status-indicator.success {
            background: var(--success);
            box-shadow: 0 0 8px var(--success);
        }
        
        .status-indicator.error {
            background: var(--error);
            box-shadow: 0 0 8px var(--error);
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .agent-metrics {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .stats-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <div class="logo">
                <div class="logo-icon">👁️</div>
                <div class="logo-text">Argus</div>
            </div>
            <div class="tagline">Real-time observability for AI agents</div>
        </div>

        <!-- Stats Grid -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Total Agents</div>
                <div class="stat-value" id="total-agents">0</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Total Calls</div>
                <div class="stat-value" id="total-calls">0</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Total Cost</div>
                <div class="stat-value" id="total-cost">$0.00</div>
            </div>
        </div>

        <!-- Agents Section -->
        <div class="section">
            <div class="section-header">
                <div class="section-title">Agents</div>
                <div class="section-badge" id="agents-count">0 active</div>
            </div>
            <div class="agents-grid" id="agents-container"></div>
        </div>

        <!-- Recent Calls Section -->
        <div class="section">
            <div class="section-header">
                <div class="section-title">Recent Activity</div>
                <div class="section-badge" id="calls-count">0 calls</div>
            </div>
            <div class="calls-list" id="calls-container"></div>
        </div>
    </div>

    <script>
        async function loadData() {
            try {
                // Load stats
                const statsRes = await fetch('/api/stats');
                const stats = await statsRes.json();
                
                document.getElementById('total-agents').textContent = stats.total_agents || 0;
                document.getElementById('total-calls').textContent = (stats.total_calls || 0).toLocaleString();
                document.getElementById('total-cost').textContent = '$' + (stats.total_cost || 0).toFixed(2);
                
                // Load agents
                const agentsRes = await fetch('/api/agents');
                const agents = await agentsRes.json();
                
                document.getElementById('agents-count').textContent = `${agents.length} active`;
                
                const agentsContainer = document.getElementById('agents-container');
                if (agents.length === 0) {
                    agentsContainer.innerHTML = `
                        <div class="empty-state">
                            <div class="empty-icon">🤖</div>
                            <div class="empty-text">No agents yet. Start using @watch.agent() decorator!</div>
                        </div>
                    `;
                } else {
                    agentsContainer.innerHTML = agents.map(agent => `
                        <div class="agent-card">
                            <div class="agent-header">
                                <div class="agent-name">${agent.name}</div>
                                <div class="agent-tags">
                                    ${(agent.tags || []).map(tag => `<span class="tag">${tag}</span>`).join('')}
                                </div>
                            </div>
                            <div class="agent-metrics">
                                <div class="metric">
                                    <div class="metric-label">Calls</div>
                                    <div class="metric-value">${agent.total_calls.toLocaleString()}</div>
                                </div>
                                <div class="metric">
                                    <div class="metric-label">Avg Time</div>
                                    <div class="metric-value">${agent.avg_duration_ms.toFixed(0)}ms</div>
                                </div>
                                <div class="metric">
                                    <div class="metric-label">Cost</div>
                                    <div class="metric-value success">$${agent.total_cost.toFixed(2)}</div>
                                </div>
                                <div class="metric">
                                    <div class="metric-label">Errors</div>
                                    <div class="metric-value ${agent.total_errors > 0 ? 'error' : ''}">${agent.total_errors}</div>
                                </div>
                            </div>
                        </div>
                    `).join('');
                }
                
                // Load recent calls
                const callsRes = await fetch('/api/calls?limit=20');
                const calls = await callsRes.json();
                
                document.getElementById('calls-count').textContent = `${calls.length} calls`;
                
                const callsContainer = document.getElementById('calls-container');
                if (calls.length === 0) {
                    callsContainer.innerHTML = `
                        <div class="empty-state">
                            <div class="empty-icon">📞</div>
                            <div class="empty-text">No calls yet.</div>
                        </div>
                    `;
                } else {
                    callsContainer.innerHTML = calls.map(call => {
                        const timeAgo = getTimeAgo(new Date(call.timestamp));
                        return `
                            <div class="call-card ${call.status === 'error' ? 'error' : ''}">
                                <div class="call-header">
                                    <div class="call-agent">
                                        <span class="status-indicator ${call.status === 'error' ? 'error' : 'success'}"></span>
                                        ${call.agent_name}
                                    </div>
                                    <div class="call-time">${timeAgo}</div>
                                </div>
                                <div class="call-metrics">
                                    <div class="call-metric">⚡ ${call.duration_ms}ms</div>
                                    <div class="call-metric">💰 $${call.cost.toFixed(4)}</div>
                                    ${call.error ? `<div class="call-metric">⚠️ ${call.error}</div>` : ''}
                                </div>
                            </div>
                        `;
                    }).join('');
                }
            } catch (error) {
                console.error('Error loading data:', error);
            }
        }
        
        function getTimeAgo(date) {
            const seconds = Math.floor((new Date() - date) / 1000);
            
            if (seconds < 60) return 'just now';
            if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
            if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
            return `${Math.floor(seconds / 86400)}d ago`;
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
    
    print(f"\n🚀 Argus Dashboard running on http://localhost:{port}\n")
    app.run(host='0.0.0.0', port=port, debug=debug)
