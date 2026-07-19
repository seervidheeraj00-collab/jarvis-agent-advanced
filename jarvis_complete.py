#!/usr/bin/env python3
"""
Jarvis Agent - Complete Advanced System
Integrates: Advanced Agent, Digital Clock, REST API, Web Dashboard, AI/ML, and Data Visualization
"""

import sys
import json
import time
import threading
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any, Tuple
from enum import Enum
import random
import psutil
import socket
import pytz
from dataclasses import dataclass, asdict
import numpy as np
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import logging
from functools import wraps

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VoiceMode(Enum):
    """Voice mode enumeration"""
    TEXT = "text"
    VOICE = "voice"


class ClockTheme(Enum):
    """Clock display theme enumeration"""
    LIGHT = "light"
    DARK = "dark"
    NEON = "neon"


@dataclass
class TimeZoneInfo:
    """Store timezone information"""
    name: str
    timezone: str
    label: str
    utc_offset: str


class SystemMetrics:
    """Collect and manage system metrics"""
    
    history: Dict[str, List[float]] = {
        "cpu": [],
        "memory": [],
        "disk": []
    }
    max_history = 100
    
    @staticmethod
    def get_cpu_usage() -> float:
        """Get CPU usage percentage"""
        return psutil.cpu_percent(interval=0.1)
    
    @staticmethod
    def get_memory_usage() -> Dict[str, float]:
        """Get memory usage statistics"""
        mem = psutil.virtual_memory()
        return {
            "percent": mem.percent,
            "used": mem.used / (1024**3),
            "total": mem.total / (1024**3),
            "available": mem.available / (1024**3)
        }
    
    @staticmethod
    def get_disk_usage() -> Dict[str, float]:
        """Get disk usage statistics"""
        disk = psutil.disk_usage('/')
        return {
            "percent": disk.percent,
            "used": disk.used / (1024**3),
            "total": disk.total / (1024**3),
            "free": disk.free / (1024**3)
        }
    
    @staticmethod
    def get_network_stats() -> Dict[str, Any]:
        """Get network statistics"""
        try:
            net = psutil.net_if_stats()
            net_io = psutil.net_io_counters()
            return {
                "interfaces": len(net),
                "bytes_sent": net_io.bytes_sent / (1024**2),
                "bytes_recv": net_io.bytes_recv / (1024**2),
                "packets_sent": net_io.packets_sent,
                "packets_recv": net_io.packets_recv
            }
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def get_system_info() -> Dict[str, Any]:
        """Get overall system information"""
        return {
            "cpu_cores": psutil.cpu_count(),
            "cpu_frequency": psutil.cpu_freq().current,
            "boot_time": datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S'),
            "uptime": str(timedelta(seconds=int(time.time() - psutil.boot_time())))
        }
    
    @classmethod
    def record_metrics(cls) -> None:
        """Record current metrics to history"""
        cpu = cls.get_cpu_usage()
        mem = cls.get_memory_usage()
        disk = cls.get_disk_usage()
        
        cls.history["cpu"].append(cpu)
        cls.history["memory"].append(mem["percent"])
        cls.history["disk"].append(disk["percent"])
        
        # Maintain max history
        for key in cls.history:
            if len(cls.history[key]) > cls.max_history:
                cls.history[key] = cls.history[key][-cls.max_history:]
    
    @classmethod
    def get_metrics_history(cls) -> Dict[str, List[float]]:
        """Get metrics history for visualization"""
        return cls.history.copy()


class DigitalClock:
    """Advanced Digital Clock with Multiple Time Zones"""
    
    TIMEZONE_CONFIGS = {
        "UTC": TimeZoneInfo("UTC", "UTC", "Coordinated Universal Time", "+00:00"),
        "EST": TimeZoneInfo("EST", "US/Eastern", "Eastern Standard Time", "-05:00"),
        "CST": TimeZoneInfo("CST", "US/Central", "Central Standard Time", "-06:00"),
        "MST": TimeZoneInfo("MST", "US/Mountain", "Mountain Standard Time", "-07:00"),
        "PST": TimeZoneInfo("PST", "US/Pacific", "Pacific Standard Time", "-08:00"),
        "GMT": TimeZoneInfo("GMT", "Europe/London", "Greenwich Mean Time", "+00:00"),
        "CET": TimeZoneInfo("CET", "Europe/Paris", "Central European Time", "+01:00"),
        "IST": TimeZoneInfo("IST", "Asia/Kolkata", "Indian Standard Time", "+05:30"),
        "JST": TimeZoneInfo("JST", "Asia/Tokyo", "Japan Standard Time", "+09:00"),
        "AEST": TimeZoneInfo("AEST", "Australia/Sydney", "Australian Eastern Standard Time", "+10:00"),
        "SGT": TimeZoneInfo("SGT", "Asia/Singapore", "Singapore Standard Time", "+08:00"),
    }
    
    def __init__(self, theme: ClockTheme = ClockTheme.NEON):
        self.theme = theme
        self.display_format = "24h"
    
    def get_current_time(self, timezone_str: str) -> datetime:
        """Get current time in specified timezone"""
        try:
            tz = pytz.timezone(timezone_str)
            return datetime.now(tz)
        except:
            return datetime.now(pytz.UTC)
    
    def format_time(self, dt: datetime) -> str:
        """Format time"""
        if self.display_format == "12h":
            return dt.strftime("%I:%M:%S %p")
        return dt.strftime("%H:%M:%S")
    
    def get_all_times(self) -> Dict[str, Dict[str, Any]]:
        """Get times for all configured timezones"""
        times = {}
        for code, tz_info in self.TIMEZONE_CONFIGS.items():
            current_time = self.get_current_time(tz_info.timezone)
            times[code] = {
                "time": self.format_time(current_time),
                "date": current_time.strftime("%Y-%m-%d"),
                "day": current_time.strftime("%A"),
                "timezone": tz_info.label,
                "utc_offset": tz_info.utc_offset
            }
        return times


class AIEnhancements:
    """AI/ML Enhancements for the Agent"""
    
    def __init__(self):
        self.sentiment_scores = []
        self.command_patterns = {}
        self.learning_data = []
    
    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze sentiment of user input"""
        positive_words = ['good', 'great', 'excellent', 'awesome', 'happy', 'perfect']
        negative_words = ['bad', 'terrible', 'awful', 'sad', 'angry', 'broken']
        
        text_lower = text.lower()
        
        positive_score = sum(1 for word in positive_words if word in text_lower)
        negative_score = sum(1 for word in negative_words if word in text_lower)
        
        total = positive_score + negative_score
        
        if total == 0:
            sentiment_score = 0.5  # Neutral
        else:
            sentiment_score = positive_score / total
        
        self.sentiment_scores.append(sentiment_score)
        
        return {
            "sentiment": "positive" if sentiment_score > 0.6 else "negative" if sentiment_score < 0.4 else "neutral",
            "score": sentiment_score
        }
    
    def predict_next_command(self, history: List[str]) -> Optional[str]:
        """Predict next command based on history"""
        if not history or len(history) < 2:
            return None
        
        last_cmd = history[-1]
        similar_cmds = [cmd for cmd in history if cmd.startswith(last_cmd.split()[0])]
        
        if len(similar_cmds) > 1:
            return random.choice(similar_cmds[:-1])
        
        return None
    
    def get_recommendations(self, command_stats: Dict[str, int]) -> List[str]:
        """Get AI recommendations based on usage patterns"""
        recommendations = []
        
        if sum(command_stats.values()) > 10:
            recommendations.append("You've been using the system frequently. Consider saving your session regularly.")
        
        if "dashboard" in command_stats:
            recommendations.append("You frequently check the dashboard. Consider setting up automated monitoring.")
        
        if "remember" in command_stats:
            recommendations.append(f"You've stored {command_stats.get('remember', 0)} memories. Consider organizing them.")
        
        if not recommendations:
            recommendations.append("Keep exploring different commands to enhance your experience!")
        
        return recommendations


class AdvancedJarvisAgent:
    """
    Advanced Jarvis Agent with all integrated features
    """
    
    def __init__(self, name: str = "JARVIS", voice_enabled: bool = False):
        self.name = name
        self.voice_enabled = voice_enabled
        self.mode = VoiceMode.VOICE if voice_enabled else VoiceMode.TEXT
        self.memory: Dict[str, Any] = {}
        self.conversation_history: List[Dict[str, Any]] = []
        self.is_running = False
        self.command_stats: Dict[str, int] = {}
        self.session_start_time = datetime.now()
        self.max_history = 1000
        
        # Initialize integrated modules
        self.clock = DigitalClock()
        self.ai = AIEnhancements()
        
        self._print_banner()
    
    def _print_banner(self) -> None:
        """Print startup banner"""
        banner = f"""
╔{'═'*70}╗
║ {'🤖 JARVIS COMPLETE SYSTEM INITIALIZATION'.center(70)} ║
╠{'═'*70}╣
║ Advanced Agent | Digital Clock | REST API | Web Dashboard       ║
║ AI/ML Enhancements | Data Visualization | Real-time Monitoring   ║
╚{'═'*70}╝
        """
        print(banner)
    
    def speak(self, message: str) -> None:
        """Output a message with timestamp"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] 🔊 {self.name}: {message}")
    
    def listen(self) -> str:
        """Listen for user input"""
        try:
            user_input = input(f"[{datetime.now().strftime('%H:%M:%S')}] 👤 You: ").strip()
            return user_input
        except EOFError:
            return "exit"
    
    def process_command(self, command: str) -> str:
        """Process user commands"""
        command_lower = command.lower().strip()
        
        base_command = command_lower.split()[0] if command_lower else "unknown"
        self.command_stats[base_command] = self.command_stats.get(base_command, 0) + 1
        
        # Analyze sentiment
        sentiment = self.ai.analyze_sentiment(command)
        
        # Exit commands
        if command_lower in ["exit", "quit", "bye", "goodbye", "stop"]:
            return "SYSTEM_EXIT"
        
        # Clock commands
        if command_lower in ["clock", "time", "show clock"]:
            return self._get_all_clocks()
        
        if command_lower in ["timezone", "timezones", "all times"]:
            return self._get_timezone_info()
        
        # Dashboard
        if command_lower in ["dashboard", "status", "metrics"]:
            return self._get_dashboard()
        
        # AI features
        if command_lower in ["recommendations", "suggest"]:
            recs = self.ai.get_recommendations(self.command_stats)
            return "\n".join([f"  • {rec}" for rec in recs])
        
        # Memory
        if command_lower.startswith("remember"):
            return self._handle_memory(command)
        
        if command_lower in ["recall", "memories"]:
            return self._recall_memory()
        
        # Help
        if command_lower in ["help", "?" ]:
            return self._get_help()
        
        return "Command processed."
    
    def _get_all_clocks(self) -> str:
        """Get all timezone clocks"""
        times = self.clock.get_all_times()
        display = "\n╔════════════════════════════════════════════════════════════════════╗\n"
        display += "║              🌍 WORLD TIME - ALL TIMEZONES                      ║\n"
        display += "╠════════════════════════════════════════════════════════════════════╣\n"
        
        for code, info in times.items():
            display += f"║ {code:6} | {info['time']:12} | {info['day']:12} | {info['timezone']:22} ║\n"
        
        display += "╚════════════════════════════════════════════════════════════════════╝"
        return display
    
    def _get_timezone_info(self) -> str:
        """Get timezone information"""
        info = "Available timezones: " + ", ".join(self.clock.TIMEZONE_CONFIGS.keys())
        return info
    
    def _get_dashboard(self) -> str:
        """Get system dashboard"""
        cpu = SystemMetrics.get_cpu_usage()
        mem = SystemMetrics.get_memory_usage()
        disk = SystemMetrics.get_disk_usage()
        
        dashboard = f"""
╔════════════════════════════════════════════════════════════════════╗
║                    JARVIS SYSTEM DASHBOARD                        ║
╠════════════════════════════════════════════════════════════════════╣
║ 📊 PERFORMANCE METRICS
├─ CPU: [{self._get_bar(cpu, 100)}] {cpu:.1f}%
├─ Memory: [{self._get_bar(mem['percent'], 100)}] {mem['percent']:.1f}%
├─ Disk: [{self._get_bar(disk['percent'], 100)}] {disk['percent']:.1f}%
║
║ 📈 SESSION ANALYTICS
├─ Commands: {sum(self.command_stats.values())}
├─ Memories: {len(self.memory)}
├─ Uptime: {str(datetime.now() - self.session_start_time).split('.')[0]}
╚════════════════════════════════════════════════════════════════════╝
        """
        return dashboard
    
    def _get_bar(self, value: float, max_val: float, length: int = 20) -> str:
        """Generate progress bar"""
        filled = int((value / max_val) * length)
        return "█" * filled + "░" * (length - filled)
    
    def _handle_memory(self, command: str) -> str:
        """Handle memory storage"""
        try:
            parts = command.split(" that ", 1)
            if len(parts) == 2:
                key = parts[0].replace("remember", "").strip()
                value = parts[1].strip()
                self.memory[key] = {
                    "value": value,
                    "timestamp": datetime.now().isoformat(),
                    "access_count": 0
                }
                return f"✓ Remembered: {key} = {value}"
            return "Format: remember [key] that [value]"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _recall_memory(self) -> str:
        """Recall memories"""
        if not self.memory:
            return "No memories stored."
        
        memory_list = "📚 Stored Memories:\n"
        for k, v in self.memory.items():
            memory_list += f"  • {k}: {v.get('value')}\n"
        return memory_list
    
    def _get_help(self) -> str:
        """Get help information"""
        help_text = """
📚 JARVIS COMMANDS:
  • clock - Show world time
  • dashboard - System metrics
  • remember [key] that [value] - Store data
  • recall - Show memories
  • recommendations - Get AI suggestions
  • help - Show this help
  • exit - Exit application
        """
        return help_text
    
    def add_to_history(self, user_message: str, agent_response: str) -> None:
        """Add to conversation history"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "user": user_message,
            "agent": agent_response
        }
        self.conversation_history.append(entry)
        
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]
    
    def save_session(self, filename: str = "jarvis_session.json") -> None:
        """Save session data"""
        try:
            session_data = {
                "agent_name": self.name,
                "session_start": self.session_start_time.isoformat(),
                "session_end": datetime.now().isoformat(),
                "total_commands": sum(self.command_stats.values()),
                "command_stats": self.command_stats,
                "memories": self.memory,
                "conversation_count": len(self.conversation_history)
            }
            
            with open(filename, 'w') as f:
                json.dump(session_data, f, indent=2)
            
            print(f"\n✅ Session saved to {filename}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    def run(self) -> None:
        """Main agent loop"""
        self.is_running = True
        self.speak("Systems initialized. Type 'help' for commands.")
        
        try:
            while self.is_running:
                user_input = self.listen()
                
                if not user_input:
                    continue
                
                response = self.process_command(user_input)
                
                if response == "SYSTEM_EXIT":
                    self.speak("Shutting down...")
                    self.is_running = False
                    break
                
                self.speak(response)
                self.add_to_history(user_input, response)
                SystemMetrics.record_metrics()
        
        except KeyboardInterrupt:
            print("\n")
            self.speak("Interrupted. Shutting down.")
        finally:
            self.is_running = False
            self.cleanup()
    
    def cleanup(self) -> None:
        """Clean up before exit"""
        try:
            if self.conversation_history:
                save_prompt = input("\n💾 Save session? (yes/no): ").strip().lower()
                if save_prompt in ['yes', 'y']:
                    self.save_session()
            print("\n👋 JARVIS shutdown complete.\n")
        except Exception as e:
            print(f"Error: {str(e)}")


def create_flask_app(agent: AdvancedJarvisAgent) -> Flask:
    """
    Create Flask app with REST API endpoints
    """
    app = Flask(__name__)
    CORS(app)
    
    # REST API Endpoints
    @app.route('/api/status', methods=['GET'])
    def get_status():
        """Get agent status"""
        return jsonify({
            "agent_name": agent.name,
            "status": "online" if agent.is_running else "offline",
            "session_start": agent.session_start_time.isoformat(),
            "uptime": str(datetime.now() - agent.session_start_time),
            "commands_processed": sum(agent.command_stats.values()),
            "memories_stored": len(agent.memory)
        })
    
    @app.route('/api/metrics', methods=['GET'])
    def get_metrics():
        """Get system metrics"""
        cpu = SystemMetrics.get_cpu_usage()
        mem = SystemMetrics.get_memory_usage()
        disk = SystemMetrics.get_disk_usage()
        
        return jsonify({
            "cpu": {"percent": cpu},
            "memory": mem,
            "disk": disk,
            "timestamp": datetime.now().isoformat()
        })
    
    @app.route('/api/metrics-history', methods=['GET'])
    def get_metrics_history():
        """Get metrics history for visualization"""
        return jsonify({
            "history": SystemMetrics.get_metrics_history(),
            "timestamp": datetime.now().isoformat()
        })
    
    @app.route('/api/clock', methods=['GET'])
    def get_clock():
        """Get world time"""
        return jsonify(agent.clock.get_all_times())
    
    @app.route('/api/memory', methods=['GET'])
    def get_memory():
        """Get stored memories"""
        return jsonify(agent.memory)
    
    @app.route('/api/memory', methods=['POST'])
    def add_memory():
        """Add new memory"""
        data = request.json
        key = data.get('key')
        value = data.get('value')
        
        if not key or not value:
            return jsonify({"error": "Missing key or value"}), 400
        
        agent.memory[key] = {
            "value": value,
            "timestamp": datetime.now().isoformat(),
            "access_count": 0
        }
        
        return jsonify({"success": True, "message": f"Remembered: {key}"})
    
    @app.route('/api/command', methods=['POST'])
    def process_command():
        """Process a command"""
        data = request.json
        command = data.get('command')
        
        if not command:
            return jsonify({"error": "Missing command"}), 400
        
        response = agent.process_command(command)
        agent.add_to_history(command, response)
        
        return jsonify({
            "command": command,
            "response": response,
            "timestamp": datetime.now().isoformat()
        })
    
    @app.route('/api/recommendations', methods=['GET'])
    def get_recommendations():
        """Get AI recommendations"""
        recommendations = agent.ai.get_recommendations(agent.command_stats)
        return jsonify({"recommendations": recommendations})
    
    @app.route('/api/history', methods=['GET'])
    def get_history():
        """Get conversation history"""
        return jsonify({
            "total": len(agent.conversation_history),
            "history": agent.conversation_history[-50:]  # Last 50 entries
        })
    
    @app.route('/api/stats', methods=['GET'])
    def get_stats():
        """Get usage statistics"""
        return jsonify({
            "command_stats": agent.command_stats,
            "total_commands": sum(agent.command_stats.values()),
            "session_duration": str(datetime.now() - agent.session_start_time),
            "sentiment_analysis": {
                "average_sentiment": np.mean(agent.ai.sentiment_scores) if agent.ai.sentiment_scores else 0.5,
                "total_analyses": len(agent.ai.sentiment_scores)
            }
        })
    
    @app.route('/dashboard', methods=['GET'])
    def dashboard():
        """Web dashboard"""
        return render_template('dashboard.html')
    
    @app.route('/', methods=['GET'])
    def index():
        """Index page"""
        return jsonify({
            "name": "JARVIS Complete System",
            "version": "3.0",
            "features": [
                "Advanced Agent",
                "Digital Clock with Timezones",
                "REST API",
                "Web Dashboard",
                "AI/ML Enhancements",
                "Data Visualization",
                "Real-time Monitoring"
            ],
            "endpoints": {
                "/api/status": "Get agent status",
                "/api/metrics": "Get system metrics",
                "/api/clock": "Get world time",
                "/api/memory": "Manage memories",
                "/api/command": "Process commands",
                "/api/recommendations": "Get AI recommendations",
                "/api/history": "Get conversation history",
                "/api/stats": "Get usage statistics",
                "/dashboard": "Web dashboard"
            }
        })
    
    return app


def main():
    """Main entry point"""
    try:
        # Create agent
        agent = AdvancedJarvisAgent(name="JARVIS", voice_enabled=False)
        
        print("\n" + "="*70)
        print("SELECT MODE:")
        print("="*70)
        print("1. CLI Mode (Terminal Interface)")
        print("2. API Mode (REST API + Web Dashboard on http://localhost:5000)")
        print("3. Hybrid Mode (Both CLI and API)")
        print("="*70)
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == "1":
            # CLI Mode
            agent.run()
        
        elif choice == "2":
            # API Mode
            app = create_flask_app(agent)
            print("\n🚀 Starting REST API Server...")
            print("📊 Web Dashboard: http://localhost:5000/dashboard")
            print("📡 API Base: http://localhost:5000/api")
            print("\nPress Ctrl+C to stop...\n")
            app.run(debug=True, host='0.0.0.0', port=5000)
        
        elif choice == "3":
            # Hybrid Mode
            app = create_flask_app(agent)
            
            # Start Flask in a separate thread
            api_thread = threading.Thread(target=lambda: app.run(debug=False, host='0.0.0.0', port=5000), daemon=True)
            api_thread.start()
            
            print("\n🚀 REST API Server started on http://localhost:5000")
            print("💻 Starting CLI interface...\n")
            
            time.sleep(2)
            agent.run()
        
        else:
            print("❌ Invalid choice")
            sys.exit(1)
    
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
