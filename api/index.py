from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sys, json, traceback

from agent import PandexHub, PandexAgent

app = Flask(__name__)
CORS(app)

# Global hub instance
current_hub = None

@app.route('/')
def playground():
    """Serve the playground frontend"""
    return render_template('playground.html')

@app.route('/api/hub', methods=['POST'])
def create_or_update_hub():
    """Create or update the working PandexHub"""
    global current_hub
    try:
        config = request.get_json()
        if not config:
            return jsonify({"error": "Configuration is required"}), 400
        
        current_hub = PandexHub(config)
        return jsonify({
            "status": "success",
            "message": "Hub created/updated successfully",
            "agents": list(current_hub.agents.keys())
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }), 500

@app.route('/api/hub', methods=['GET'])
def get_hub_info():
    """Get information about the current hub"""
    global current_hub
    if current_hub is None:
        return jsonify({"error": "No hub initialized"}), 404
    
    return jsonify({
        "status": "success",
        "agents": list(current_hub.agents.keys()),
        "hub_status": current_hub.get_status()
    })

@app.route('/api/hub/status', methods=['GET'])
def get_hub_status():
    """Get status from PandexHub"""
    global current_hub
    if current_hub is None:
        return jsonify({"error": "No hub initialized"}), 404
    
    return jsonify({
        "status": "success",
        "hub_status": current_hub.get_status()
    })

@app.route('/api/agent/<agent_name>/execute', methods=['POST'])
def execute_agent(agent_name):
    """Execute a PandexAgent in the working PandexHub"""
    global current_hub
    if current_hub is None:
        return jsonify({"error": "No hub initialized"}), 404
    
    if agent_name not in current_hub.agents:
        return jsonify({"error": f"Agent '{agent_name}' not found"}), 404
    
    try:
        plan = request.get_json() or {}
        agent = current_hub.agents[agent_name]
        result = agent.execute(plan)
        
        return jsonify({
            "status": "success",
            "agent": agent_name,
            "result": result
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }), 500

@app.route('/api/agent/<agent_name>/result', methods=['GET'])
def get_agent_result(agent_name):
    """Get the result of a PandexAgent"""
    global current_hub
    if current_hub is None:
        return jsonify({"error": "No hub initialized"}), 404
    
    if agent_name not in current_hub.agents:
        return jsonify({"error": f"Agent '{agent_name}' not found"}), 404
    
    try:
        agent = current_hub.agents[agent_name]
        return jsonify({
            "status": "success",
            "agent": agent_name,
            "result": agent.result,
            "plan": agent.plan
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }), 500

@app.route('/api/agent/<agent_name>/config', methods=['PUT'])
def update_agent_config(agent_name):
    """Update configuration of a specific agent"""
    global current_hub
    if current_hub is None:
        return jsonify({"error": "No hub initialized"}), 404
    
    if agent_name not in current_hub.agents:
        return jsonify({"error": f"Agent '{agent_name}' not found"}), 404
    
    try:
        new_config = request.get_json()
        if not new_config:
            return jsonify({"error": "Configuration is required"}), 400
        
        # Update the agent's configuration
        agent = current_hub.agents[agent_name]
        old_config = agent.config.copy()
        agent.config.update(new_config)
        
        # Reset the agent's result if configuration changed significantly
        # This ensures the agent will run with the new configuration
        agent.result = {"status": -1, "output": None}
        agent.plan = {}
        
        return jsonify({
            "status": "success",
            "agent": agent_name,
            "message": f"Agent '{agent_name}' configuration updated successfully",
            "old_config": old_config,
            "new_config": agent.config
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }), 500

@app.route('/api/agents', methods=['GET'])
def list_agents():
    """List all available agents"""
    global current_hub
    if current_hub is None:
        return jsonify({"error": "No hub initialized"}), 404
    
    agents_info = {}
    for name, agent in current_hub.agents.items():
        agents_info[name] = {
            "name": agent.name,
            "config": agent.config,
            "vars": list(agent.config.get("vars", {}).keys()),
            "result_status": agent.result.get("status", -1),
            "has_output": agent.result.get("output") is not None
        }
    
    return jsonify({
        "status": "success",
        "agents": agents_info
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port = "3333")