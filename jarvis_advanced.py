#!/usr/bin/env python3
"""
Jarvis Agent - Advanced Version with Web Dashboard
A sophisticated voice and text-based agent with real-time analytics dashboard
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


class VoiceMode(Enum):
    """Voice mode enumeration"""
    TEXT = "text"
    VOICE = "voice"


class SystemMetrics:
    """Collect and manage system metrics"""
    
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
            "used": mem.used / (1024**3),  # GB
            "total": mem.total / (1024**3),  # GB
            "available": mem.available / (1024**3)  # GB
        }
    
    @staticmethod
    def get_disk_usage() -> Dict[str, float]:
        """Get disk usage statistics"""
        disk = psutil.disk_usage('/')
        return {
            "percent": disk.percent,
            "used": disk.used / (1024**3),  # GB
            "total": disk.total / (1024**3),  # GB
            "free": disk.free / (1024**3)  # GB
        }
    
    @staticmethod
    def get_network_stats() -> Dict[str, Any]:
        """Get network statistics"""
        try:
            net = psutil.net_if_stats()
            net_io = psutil.net_io_counters()
            return {
                "interfaces": len(net),
                "bytes_sent": net_io.bytes_sent / (1024**2),  # MB
                "bytes_recv": net_io.bytes_recv / (1024**2),  # MB
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


class AdvancedJarvisAgent:
    """
    Advanced Jarvis Agent with Dashboard Interface and Analytics
    """
    
    def __init__(self, name: str = "JARVIS", voice_enabled: bool = False, enable_dashboard: bool = True):
        """
        Initialize the Advanced Jarvis Agent
        
        Args:
            name: Name of the agent
            voice_enabled: Enable voice mode
            enable_dashboard: Enable web dashboard
        """
        self.name = name
        self.voice_enabled = voice_enabled
        self.mode = VoiceMode.VOICE if voice_enabled else VoiceMode.TEXT
        self.enable_dashboard = enable_dashboard
        self.memory: Dict[str, Any] = {}
        self.conversation_history: List[Dict[str, Any]] = []
        self.is_running = False
        self.metrics_history: List[Dict[str, Any]] = []
        self.command_stats: Dict[str, int] = {}
        self.session_start_time = datetime.now()
        self.metrics_thread = None
        self.max_history = 1000
        
        self._print_banner()
    
    def _print_banner(self) -> None:
        """Print advanced startup banner"""
        banner = f"""
╔{'═'*58}╗
║ {'🤖 JARVIS ADVANCED AGENT INITIALIZATION'.center(58)} ║
╠{'═'*58}╣
║ Name: {self.name.ljust(51)} ║
║ Mode: {self.mode.value.upper().ljust(51)} ║
║ Dashboard: {'ENABLED' if self.enable_dashboard else 'DISABLED'}.ljust(44)} ║
║ Initialized: {datetime.now().strftime('%Y-%m-%d %H:%M:%S').ljust(40)} ║
╚{'═'*58}╝
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
        """Process user commands with enhanced functionality"""
        command_lower = command.lower().strip()
        
        # Track command statistics
        base_command = command_lower.split()[0] if command_lower else "unknown"
        self.command_stats[base_command] = self.command_stats.get(base_command, 0) + 1
        
        # Exit commands
        if command_lower in ["exit", "quit", "bye", "goodbye", "stop"]:
            return "SYSTEM_EXIT"
        
        # Help command
        if command_lower in ["help", "?", "what can you do", "commands"]:
            return self._get_help()
        
        # Time command
        if command_lower in ["time", "what time is it", "current time"]:
            return f"The current time is {datetime.now().strftime('%H:%M:%S')}"
        
        # Date command
        if command_lower in ["date", "what date is it", "current date"]:
            return f"Today's date is {datetime.now().strftime('%A, %B %d, %Y')}"
        
        # Memory commands
        if command_lower.startswith("remember"):
            return self._handle_memory(command)
        
        if command_lower in ["recall", "what do you remember", "my memories"]:
            return self._recall_memory()
        
        # Calculation
        if command_lower.startswith("calculate") or command_lower.startswith("compute"):
            return self._handle_calculation(command)
        
        # System status
        if command_lower in ["status", "system status", "metrics", "diagnostics"]:
            return self._get_system_status()
        
        # Dashboard
        if command_lower in ["dashboard", "show dashboard", "analytics"]:
            return self._get_dashboard()
        
        # Session info
        if command_lower in ["session", "session info", "uptime"]:
            return self._get_session_info()
        
        # Greeting
        if command_lower in ["hello", "hi", "hey", "greetings"]:
            return f"Hello! I'm {self.name}, your advanced AI assistant. How can I help you today?"
        
        # How are you
        if command_lower in ["how are you", "status check"]:
            return f"{self.name} is fully operational. All systems nominal and ready for action!"
        
        # Weather simulation
        if command_lower in ["weather", "what's the weather"]:
            return self._get_weather()
        
        # Default response
        return self._generate_response(command)
    
    def _handle_memory(self, command: str) -> str:
        """Handle memory storage with timestamps"""
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
            return f"Error storing memory: {str(e)}"
    
    def _recall_memory(self) -> str:
        """Recall stored memories with statistics"""
        if not self.memory:
            return "No memories stored yet."
        
        memory_list = "📚 My Memories:\n"
        for k, v in self.memory.items():
            timestamp = v.get("timestamp", "N/A")[:10]
            memory_list += f"  • {k}: {v.get('value')} (stored: {timestamp})\n"
        return memory_list.strip()
    
    def _handle_calculation(self, command: str) -> str:
        """Handle mathematical calculations safely"""
        try:
            expr = command.replace("calculate", "").replace("compute", "").strip()
            
            if any(char in expr for char in ['__', 'import', 'exec', 'eval']):
                return "Security restriction: Cannot execute that expression."
            
            result = eval(expr, {"__builtins__": {}})
            return f"Result: {result}"
        except ZeroDivisionError:
            return "Error: Division by zero."
        except Exception as e:
            return f"Calculation error: {str(e)}"
    
    def _get_system_status(self) -> str:
        """Get comprehensive system status"""
        try:
            cpu = SystemMetrics.get_cpu_usage()
            mem = SystemMetrics.get_memory_usage()
            disk = SystemMetrics.get_disk_usage()
            
            status = f"""
╔ SYSTEM DIAGNOSTICS ╗
├─ CPU Usage: {cpu:.1f}%
├─ Memory: {mem['percent']:.1f}% ({mem['used']:.2f}GB / {mem['total']:.2f}GB)
├─ Disk: {disk['percent']:.1f}% ({disk['used']:.2f}GB / {disk['total']:.2f}GB)
├─ System Health: {'🟢 HEALTHY' if cpu < 80 and mem['percent'] < 80 else '🟡 WARNING' if cpu < 95 else '🔴 CRITICAL'}
╚═══════════════════╝
            """
            return status.strip()
        except Exception as e:
            return f"Error retrieving system status: {str(e)}"
    
    def _get_dashboard(self) -> str:
        """Get advanced dashboard view"""
        try:
            cpu = SystemMetrics.get_cpu_usage()
            mem = SystemMetrics.get_memory_usage()
            disk = SystemMetrics.get_disk_usage()
            sys_info = SystemMetrics.get_system_info()
            net = SystemMetrics.get_network_stats()
            
            dashboard = f"""
╔════════════════════════════════════════════════════╗
║          JARVIS ADVANCED DASHBOARD v2.0            ║
╠════════════════════════════════════════════════════╣
║ 📊 PERFORMANCE METRICS
├─ CPU: {self._get_bar(cpu, 100)} {cpu:.1f}%
├─ Memory: {self._get_bar(mem['percent'], 100)} {mem['percent']:.1f}%
├─ Disk: {self._get_bar(disk['percent'], 100)} {disk['percent']:.1f}%
║
║ 🖥️  SYSTEM INFORMATION
├─ Cores: {sys_info['cpu_cores']} | Freq: {sys_info['cpu_frequency']:.0f} MHz
├─ Boot Time: {sys_info['boot_time']}
├─ Uptime: {sys_info['uptime']}
║
║ 🌐 NETWORK STATISTICS
├─ Interfaces: {net.get('interfaces', 'N/A')}
├─ Data Sent: {net.get('bytes_sent', 0):.2f} MB
├─ Data Received: {net.get('bytes_recv', 0):.2f} MB
║
║ 📈 SESSION ANALYTICS
├─ Commands Processed: {sum(self.command_stats.values())}
├─ Unique Commands: {len(self.command_stats)}
├─ Conversation Length: {len(self.conversation_history)}
├─ Memories Stored: {len(self.memory)}
╚════════════════════════════════════════════════════╝
            """
            return dashboard.strip()
        except Exception as e:
            return f"Dashboard error: {str(e)}"
    
    def _get_session_info(self) -> str:
        """Get session information"""
        uptime = datetime.now() - self.session_start_time
        session_info = f"""
╔ SESSION INFORMATION ╗
├─ Agent: {self.name}
├─ Started: {self.session_start_time.strftime('%Y-%m-%d %H:%M:%S')}
├─ Uptime: {str(uptime).split('.')[0]}
├─ Commands: {sum(self.command_stats.values())}
├─ Memory Entries: {len(self.memory)}
├─ Conversation Turns: {len(self.conversation_history)}
╚═══════════════════════╝
        """
        return session_info.strip()
    
    def _get_weather(self) -> str:
        """Simulate weather data"""
        weather_data = {
            "temperature": random.randint(15, 35),
            "humidity": random.randint(30, 80),
            "conditions": random.choice(["Sunny", "Cloudy", "Rainy", "Clear"]),
            "wind_speed": random.randint(5, 25)
        }
        return f"Weather: {weather_data['conditions']}, {weather_data['temperature']}°C, Humidity: {weather_data['humidity']}%, Wind: {weather_data['wind_speed']} km/h"
    
    def _get_bar(self, value: float, max_val: float, length: int = 20) -> str:
        """Generate progress bar"""
        filled = int((value / max_val) * length)
        bar = "█" * filled + "░" * (length - filled)
        return f"[{bar}]"
    
    def _generate_response(self, user_input: str) -> str:
        """Generate intelligent response"""
        responses = [
            "That's interesting. Could you elaborate on that?",
            "I understand. How can I assist you further?",
            "Processing your request. What would you like me to do?",
            "Got it. Is there anything specific I can help with?",
            "Interesting point. Do you need further assistance?"
        ]
        return random.choice(responses)
    
    def _get_help(self) -> str:
        """Get comprehensive help information"""
        help_text = f"""
╔════════════════════════════════════════════════════╗
║         📚 JARVIS COMMAND REFERENCE                ║
╠════════════════════════════════════════════════════╣
║ GENERAL
├─ help, ? - Show this help menu
├─ status - System status overview
├─ dashboard - Advanced analytics dashboard
├─ session - Session information
║
║ TIME & DATE
├─ time - Current time
├─ date - Current date
║
║ MEMORY
├─ remember [key] that [value] - Store information
├─ recall - Retrieve all memories
║
║ UTILITIES
├─ calculate [expression] - Math calculations
├─ weather - Current weather simulation
║
║ SYSTEM
├─ metrics - Detailed system metrics
├─ diagnostics - Full system diagnostics
║
║ NAVIGATION
├─ exit, quit, bye - Exit application
╚════════════════════════════════════════════════════╝
        """
        return help_text.strip()
    
    def add_to_history(self, user_message: str, agent_response: str) -> None:
        """Add conversation to history with metadata"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "user": user_message,
            "agent": agent_response,
            "response_time": 0.01  # Simplified
        }
        self.conversation_history.append(entry)
        
        # Keep history manageable
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get conversation history"""
        return self.conversation_history.copy()
    
    def save_session(self, filename: str = "jarvis_session_advanced.json") -> None:
        """Save session data with full analytics"""
        try:
            session_data = {
                "agent_name": self.name,
                "mode": self.mode.value,
                "session_start": self.session_start_time.isoformat(),
                "session_end": datetime.now().isoformat(),
                "total_commands": sum(self.command_stats.values()),
                "command_stats": self.command_stats,
                "memories": self.memory,
                "conversation_count": len(self.conversation_history),
                "memories_count": len(self.memory)
            }
            
            with open(filename, 'w') as f:
                json.dump(session_data, f, indent=2)
            
            print(f"\n✅ Session saved to {filename}")
            print(f"   Commands: {sum(self.command_stats.values())}")
            print(f"   Memories: {len(self.memory)}")
            print(f"   Conversations: {len(self.conversation_history)}")
        except Exception as e:
            print(f"❌ Error saving session: {str(e)}")
    
    def run(self) -> None:
        """Main agent loop"""
        self.is_running = True
        self.speak(f"Advanced systems online. Type 'help' for commands.")
        
        try:
            while self.is_running:
                user_input = self.listen()
                
                if not user_input:
                    continue
                
                response = self.process_command(user_input)
                
                if response == "SYSTEM_EXIT":
                    self.speak("Shutting down. Goodbye!")
                    self.is_running = False
                    break
                
                self.speak(response)
                self.add_to_history(user_input, response)
        
        except KeyboardInterrupt:
            print("\n")
            self.speak("Interrupted. Initiating shutdown sequence.")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
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
            print("\n👋 JARVIS Agent shutdown complete.\n")
        except Exception as e:
            print(f"Cleanup error: {str(e)}")


def main():
    """Main entry point"""
    try:
        agent = AdvancedJarvisAgent(name="JARVIS", voice_enabled=False, enable_dashboard=True)
        agent.run()
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
