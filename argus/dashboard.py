"""
Modern Flask dashboard for Argus - Professional UI/UX
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
            /* Modern color system - inspired by Vercel/Linear */
            --bg-base: #fafafa;
            --bg-surface: #ffffff;
            --bg-elevated: #ffffff;
            --bg-overlay: rgba(0, 0, 0, 0.02);
            
            --border-subtle: #eaeaea;
            --border-default: #d4d4d4;
            --border-strong: #a3a3a3;
            
            --text-primary: #171717;
            --text-secondary: #737373;
            --text-tertiary: #a3a3a3;
            
            --accent-blue: #0070f3;
            --accent-purple: #7928ca;
            --accent-pink: #ff0080;
            --accent-green: #00d084;
            --accent-orange: #f5a623;
            --accent-red: #ff3b30;
            
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
            
            --radius-sm: 6px;
            --radius-md: 8px;
            --radius-lg: 12px;
            --radius-xl: 16px;
            
            --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
            --transition-base: 200ms cubic-bezier(0.4, 0, 0.2, 1);
            --transition-slow: 300ms cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        /* Dark mode support */
        @media (prefers-color-scheme: dark) {
            :root {
                --bg-base: #000000;
                --bg-surface: #0a0a0a;
                --bg-elevated: #111111;
                --bg-overlay: rgba(255, 255, 255, 0.02);
                
                --border-subtle: #1a1a1a;
                --border-default: #2a2a2a;
                --border-strong: #3a3a3a;
                
                --text-primary: #ededed;
                --text-secondary: #a3a3a3;
                --text-tertiary: #737373;
                
                --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.3);
                --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.4);
                --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
                --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.6);
            }
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: var(--bg-base);
            color: var(--text-primary);
            line-height: 1.5;
            min-height: 100vh;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }
        
        /* Layout */
        .app {
            display: flex;
            min-height: 100vh;
        }
        
        /* Sidebar */
        .sidebar {
            width: 240px;
            background: var(--bg-surface);
            border-right: 1px solid var(--border-subtle);
            padding: 24px 16px;
            display: flex;
            flex-direction: column;
            gap: 32px;
            position: sticky;
            top: 0;
            height: 100vh;
        }
        
        .logo {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 0 8px;
        }
        
        .logo-icon {
            width: 32px;
            height: 32px;
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
            border-radius: var(--radius-md);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
        }
        
        .logo-text {
            font-size: 18px;
            font-weight: 600;
            letter-spacing: -0.02em;
        }
        
        .nav {
            display: flex;
            flex-direction: column;
            gap: 2px;
        }
        
        .nav-item {
            padding: 8px 12px;
            border-radius: var(--radius-md);
            font-size: 14px;
            font-weight: 500;
            color: var(--text-secondary);
            cursor: pointer;
            transition: all var(--transition-fast);
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .nav-item:hover {
            background: var(--bg-overlay);
            color: var(--text-primary);
        }
        
        .nav-item.active {
            background: var(--bg-overlay);
            color: var(--text-primary);
        }
        
        .nav-icon {
            width: 18px;
            height: 18px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        /* Main Content */
        .main {
            flex: 1;
            padding: 32px;
            max-width: 1400px;
            margin: 0 auto;
            width: 100%;
        }
        
        /* Header */
        .page-header {
            margin-bottom: 32px;
        }
        
        .page-title {
            font-size: 28px;
            font-weight: 600;
            letter-spacing: -0.02em;
            margin-bottom: 4px;
        }
        
        .page-subtitle {
            font-size: 14px;
            color: var(--text-secondary);
        }
        
        /* Stats Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 16px;
            margin-bottom: 32px;
        }
        
        .stat-card {
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-lg);
            padding: 20px;
            transition: all var(--transition-base);
            position: relative;
            overflow: hidden;
        }
        
        .stat-card:hover {
            border-color: var(--border-default);
            box-shadow: var(--shadow-sm);
            transform: translateY(-1px);
        }
        
        .stat-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 12px;
        }
        
        .stat-label {
            font-size: 13px;
            font-weight: 500;
            color: var(--text-secondary);
            letter-spacing: -0.01em;
        }
        
        .stat-icon {
            width: 32px;
            height: 32px;
            border-radius: var(--radius-md);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
        }
        
        .stat-icon.blue { background: rgba(0, 112, 243, 0.1); }
        .stat-icon.green { background: rgba(0, 208, 132, 0.1); }
        .stat-icon.purple { background: rgba(121, 40, 202, 0.1); }
        .stat-icon.orange { background: rgba(245, 166, 35, 0.1); }
        
        .stat-value {
            font-size: 32px;
            font-weight: 600;
            letter-spacing: -0.02em;
            margin-bottom: 8px;
        }
        
        .stat-change {
            font-size: 12px;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 4px;
        }
        
        .stat-change.positive { color: var(--accent-green); }
        .stat-change.negative { color: var(--accent-red); }
        
        /* Section */
        .section {
            margin-bottom: 32px;
        }
        
        .section-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 16px;
        }
        
        .section-title {
            font-size: 18px;
            font-weight: 600;
            letter-spacing: -0.01em;
        }
        
        .section-actions {
            display: flex;
            gap: 8px;
        }
        
        .btn {
            padding: 6px 12px;
            border-radius: var(--radius-md);
            font-size: 13px;
            font-weight: 500;
            border: 1px solid var(--border-default);
            background: var(--bg-surface);
            color: var(--text-primary);
            cursor: pointer;
            transition: all var(--transition-fast);
        }
        
        .btn:hover {
            border-color: var(--border-strong);
            background: var(--bg-overlay);
        }
        
        /* Agent Cards */
        .agents-grid {
            display: grid;
            gap: 16px;
        }
        
        .agent-card {
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-lg);
            padding: 20px;
            transition: all var(--transition-base);
            cursor: pointer;
        }
        
        .agent-card:hover {
            border-color: var(--border-default);
            box-shadow: var(--shadow-md);
        }
        
        .agent-header {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            margin-bottom: 16px;
        }
        
        .agent-info {
            flex: 1;
        }
        
        .agent-name {
            font-size: 16px;
            font-weight: 600;
            letter-spacing: -0.01em;
            margin-bottom: 4px;
        }
        
        .agent-tags {
            display: flex;
            gap: 6px;
            flex-wrap: wrap;
        }
        
        .tag {
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 500;
            background: var(--bg-overlay);
            color: var(--text-secondary);
            border: 1px solid var(--border-subtle);
        }
        
        .agent-status {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--accent-green);
            box-shadow: 0 0 0 3px rgba(0, 208, 132, 0.2);
        }
        
        .agent-metrics {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            padding-top: 16px;
            border-top: 1px solid var(--border-subtle);
        }
        
        .metric {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }
        
        .metric-label {
            font-size: 11px;
            font-weight: 500;
            color: var(--text-tertiary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .metric-value {
            font-size: 20px;
            font-weight: 600;
            letter-spacing: -0.01em;
        }
        
        .metric-value.success { color: var(--accent-green); }
        .metric-value.error { color: var(--accent-red); }
        
        /* Activity Feed */
        .activity-feed {
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-lg);
            overflow: hidden;
        }
        
        .activity-item {
            padding: 16px 20px;
            border-bottom: 1px solid var(--border-subtle);
            transition: background var(--transition-fast);
        }
        
        .activity-item:last-child {
            border-bottom: none;
        }
        
        .activity-item:hover {
            background: var(--bg-overlay);
        }
        
        .activity-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 8px;
        }
        
        .activity-agent {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 14px;
            font-weight: 500;
        }
        
        .status-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
        }
        
        .status-dot.success { background: var(--accent-green); }
        .status-dot.error { background: var(--accent-red); }
        
        .activity-time {
            font-size: 12px;
            color: var(--text-tertiary);
        }
        
        .activity-metrics {
            display: flex;
            gap: 16px;
            font-size: 12px;
            color: var(--text-secondary);
        }
        
        .activity-metric {
            display: flex;
            align-items: center;
            gap: 4px;
        }
        
        /* Empty State */
        .empty-state {
            text-align: center;
            padding: 60px 20px;
        }
        
        .empty-icon {
            width: 64px;
            height: 64px;
            margin: 0 auto 16px;
            background: var(--bg-overlay);
            border-radius: var(--radius-xl);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 32px;
        }
        
        .empty-title {
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 4px;
        }
        
        .empty-text {
            font-size: 14px;
            color: var(--text-secondary);
        }
        
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .fade-in {
            animation: fadeIn 0.3s ease-out;
        }
        
        /* Responsive */
        @media (max-width: 1024px) {
            .sidebar {
                width: 200px;
            }
        }
        
        @media (max-width: 768px) {
            .sidebar {
                display: none;
            }
            
            .main {
                padding: 20px;
            }
            
            .stats-grid {
                grid-template-columns: 1fr;
            }
            
            .agent-metrics {
                grid-template-columns: repeat(2, 1fr);
            }
        }
    </style>
</head>
<body>
    <div class="app">
        <!-- Sidebar -->
        <div class="sidebar">
            <div class="logo">
                <div class="logo-icon">👁️</div>
                <div class="logo-text">Argus</div>
            </div>
            
            <nav class="nav">
                <div class="nav-item active">
                    <div class="nav-icon">📊</div>
                    <span>Overview</span>
                </div>
                <div class="nav-item">
                    <div class="nav-icon">🤖</div>
                    <span>Agents</span>
                </div>
                <div class="nav-item">
                    <div class="nav-icon">📞</div>
                    <span>Activity</span>
                </div>
                <div class="nav-item">
                    <div class="nav-icon">💰</div>
                    <span>Costs</span>
                </div>
                <div class="nav-item">
                    <div class="nav-icon">⚠️</div>
                    <span>Errors</span>
                </div>
            </nav>
        </div>

        <!-- Main Content -->
        <div class="main">
            <!-- Page Header -->
            <div class="page-header">
                <h1 class="page-title">Overview</h1>
                <p class="page-subtitle">Real-time observability for your AI agents</p>
            </div>

            <!-- Stats Grid -->
            <div class="stats-grid">
                <div class="stat-card fade-in">
                    <div class="stat-header">
                        <div class="stat-label">Total Agents</div>
                        <div class="stat-icon blue">🤖</div>
                    </div>
                    <div class="stat-value" id="total-agents">0</div>
                    <div class="stat-change positive">
                        <span>↗</span>
                        <span>Active now</span>
                    </div>
                </div>
                
                <div class="stat-card fade-in" style="animation-delay: 0.05s">
                    <div class="stat-header">
                        <div class="stat-label">Total Calls</div>
                        <div class="stat-icon green">📞</div>
                    </div>
                    <div class="stat-value" id="total-calls">0</div>
                    <div class="stat-change positive">
                        <span>↗</span>
                        <span>Last 24h</span>
                    </div>
                </div>
                
                <div class="stat-card fade-in" style="animation-delay: 0.1s">
                    <div class="stat-header">
                        <div class="stat-label">Total Cost</div>
                        <div class="stat-icon purple">💰</div>
                    </div>
                    <div class="stat-value" id="total-cost">$0.00</div>
                    <div class="stat-change">
                        <span>All time</span>
                    </div>
                </div>
                
                <div class="stat-card fade-in" style="animation-delay: 0.15s">
                    <div class="stat-header">
                        <div class="stat-label">Avg Latency</div>
                        <div class="stat-icon orange">⚡</div>
                    </div>
                    <div class="stat-value" id="avg-latency">0ms</div>
                    <div class="stat-change positive">
                        <span>↗</span>
                        <span>Improving</span>
                    </div>
                </div>
            </div>

            <!-- Agents Section -->
            <div class="section">
                <div class="section-header">
                    <h2 class="section-title">Active Agents</h2>
                    <div class="section-actions">
                        <button class="btn">Filter</button>
                        <button class="btn">Sort</button>
                    </div>
                </div>
                <div class="agents-grid" id="agents-container"></div>
            </div>

            <!-- Recent Activity -->
            <div class="section">
                <div class="section-header">
                    <h2 class="section-title">Recent Activity</h2>
                    <div class="section-actions">
                        <button class="btn">View All</button>
                    </div>
                </div>
                <div class="activity-feed" id="activity-container"></div>
            </div>
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
                
                // Calculate avg latency
                const agentsRes = await fetch('/api/agents');
                const agents = await agentsRes.json();
                
                if (agents.length > 0) {
                    const avgLatency = agents.reduce((sum, a) => sum + a.avg_duration_ms, 0) / agents.length;
                    document.getElementById('avg-latency').textContent = Math.round(avgLatency) + 'ms';
                }
                
                // Load agents
                const agentsContainer = document.getElementById('agents-container');
                if (agents.length === 0) {
                    agentsContainer.innerHTML = `
                        <div class="empty-state">
                            <div class="empty-icon">🤖</div>
                            <div class="empty-title">No agents yet</div>
                            <div class="empty-text">Start using @watch.agent() decorator to track your AI agents</div>
                        </div>
                    `;
                } else {
                    agentsContainer.innerHTML = agents.map((agent, i) => `
                        <div class="agent-card fade-in" style="animation-delay: ${i * 0.05}s">
                            <div class="agent-header">
                                <div class="agent-info">
                                    <div class="agent-name">${agent.name}</div>
                                    <div class="agent-tags">
                                        ${(agent.tags || []).map(tag => `<span class="tag">${tag}</span>`).join('')}
                                    </div>
                                </div>
                                <div class="agent-status"></div>
                            </div>
                            <div class="agent-metrics">
                                <div class="metric">
                                    <div class="metric-label">Calls</div>
                                    <div class="metric-value">${agent.total_calls.toLocaleString()}</div>
                                </div>
                                <div class="metric">
                                    <div class="metric-label">Latency</div>
                                    <div class="metric-value">${Math.round(agent.avg_duration_ms)}ms</div>
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
                const callsRes = await fetch('/api/calls?limit=10');
                const calls = await callsRes.json();
                
                const activityContainer = document.getElementById('activity-container');
                if (calls.length === 0) {
                    activityContainer.innerHTML = `
                        <div class="empty-state">
                            <div class="empty-icon">📞</div>
                            <div class="empty-title">No activity yet</div>
                            <div class="empty-text">Agent calls will appear here</div>
                        </div>
                    `;
                } else {
                    activityContainer.innerHTML = calls.map(call => {
                        const timeAgo = getTimeAgo(new Date(call.timestamp));
                        return `
                            <div class="activity-item">
                                <div class="activity-header">
                                    <div class="activity-agent">
                                        <span class="status-dot ${call.status === 'error' ? 'error' : 'success'}"></span>
                                        <span>${call.agent_name}</span>
                                    </div>
                                    <div class="activity-time">${timeAgo}</div>
                                </div>
                                <div class="activity-metrics">
                                    <div class="activity-metric">
                                        <span>⚡</span>
                                        <span>${call.duration_ms}ms</span>
                                    </div>
                                    <div class="activity-metric">
                                        <span>💰</span>
                                        <span>$${call.cost.toFixed(4)}</span>
                                    </div>
                                    ${call.error ? `
                                        <div class="activity-metric">
                                            <span>⚠️</span>
                                            <span>${call.error}</span>
                                        </div>
                                    ` : ''}
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
    """Start Flask dashboard with modern UI"""
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
