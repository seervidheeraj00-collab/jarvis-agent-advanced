# JARVIS Complete System - Advanced AI Agent

## 🚀 Overview

JARVIS is a comprehensive AI-powered system that combines:

- **Advanced Agent** - Intelligent command processing with memory management
- **Digital Clock** - Real-time world time with 11+ timezone support
- **REST API** - Complete API endpoints for all features
- **Web Dashboard** - Modern, responsive web interface
- **AI/ML Enhancements** - Sentiment analysis, recommendations, pattern learning
- **Data Visualization** - Real-time metrics tracking and visualization
- **System Monitoring** - CPU, Memory, Disk, and Network monitoring

## 📋 Features

### Core Agent Features
- Interactive command processing
- Memory management with timestamps
- Conversation history tracking
- Command statistics
- Session management
- AI-powered recommendations

### Clock Features
- Support for 11+ timezones
- 24-hour and 12-hour format
- Day and date display
- UTC offset information

### REST API Endpoints

```
GET  /api/status              - Agent status
GET  /api/metrics             - Current system metrics
GET  /api/metrics-history     - Metrics history for visualization
GET  /api/clock               - World time for all timezones
GET  /api/memory              - Get all stored memories
POST /api/memory              - Add new memory
POST /api/command             - Process a command
GET  /api/recommendations     - Get AI recommendations
GET  /api/history             - Get conversation history
GET  /api/stats               - Get usage statistics
```

### AI/ML Features
- Sentiment analysis of user input
- Command pattern prediction
- Usage-based recommendations
- Behavior learning

## 🛠️ Installation

### Requirements
- Python 3.8+
- pip (Python package manager)

### Setup

1. **Clone or download the repository**

2. **Install dependencies**
   ```bash
   pip install -r requirements-complete.txt
   ```

3. **Run JARVIS**
   ```bash
   python jarvis_complete.py
   ```

## 📱 Usage Modes

### 1. CLI Mode (Terminal Interface)
```bash
python jarvis_complete.py
# Select option: 1
```

**Available Commands:**
- `clock` - Show world time
- `timezone` - List all timezones
- `dashboard` - Show system metrics
- `remember [key] that [value]` - Store memory
- `recall` - Show all memories
- `recommendations` - Get AI suggestions
- `help` - Show help
- `exit` - Exit application

### 2. API Mode (REST API Server)
```bash
python jarvis_complete.py
# Select option: 2
```

- **REST API**: `http://localhost:5000/api`
- **Web Dashboard**: `http://localhost:5000/dashboard`

### 3. Hybrid Mode (CLI + API)
```bash
python jarvis_complete.py
# Select option: 3
```

Runs both CLI and API simultaneously.

## 📊 Dashboard Features

### Real-time Monitoring
- System status (Online/Offline)
- CPU, Memory, Disk usage with progress bars
- Command count and memory storage
- Session duration

### World Clock
- Real-time time display for all timezones
- Automatic updates every 2 seconds
- Date and timezone information

### AI Recommendations
- Personalized suggestions based on usage
- Behavior analysis
- Feature recommendations

### Performance Metrics
- Live CPU usage tracking
- Memory consumption monitoring
- Disk space utilization
- Network statistics

## 🧠 AI/ML Capabilities

### Sentiment Analysis
- Analyzes user input sentiment (positive/negative/neutral)
- Maintains sentiment history
- Helps personalize responses

### Behavior Learning
- Tracks command patterns
- Predicts next commands
- Learns user preferences

### Smart Recommendations
- Based on usage frequency
- Suggests optimizations
- Personalized feature suggestions

## 📡 API Examples

### Get Agent Status
```bash
curl http://localhost:5000/api/status
```

### Get System Metrics
```bash
curl http://localhost:5000/api/metrics
```

### Get World Time
```bash
curl http://localhost:5000/api/clock
```

### Add Memory
```bash
curl -X POST http://localhost:5000/api/memory \
  -H "Content-Type: application/json" \
  -d '{"key": "important_data", "value": "some value"}'
```

### Process Command
```bash
curl -X POST http://localhost:5000/api/command \
  -H "Content-Type: application/json" \
  -d '{"command": "show dashboard"}'
```

### Get Recommendations
```bash
curl http://localhost:5000/api/recommendations
```

## 📈 Data Visualization

### Dashboard Charts
- CPU usage over time (last 100 samples)
- Memory usage trend
- Disk space utilization
- Command frequency histogram
- Sentiment analysis graph

## 🔐 Security Considerations

- Expressions are safely evaluated with restricted builtins
- Input validation on all API endpoints
- CORS enabled for cross-origin requests
- Session data can be saved locally

## 📁 File Structure

```
jarvis-agent-advanced/
├── jarvis_complete.py          # Main application
├── requirements-complete.txt   # Python dependencies
├── templates/
│   └── dashboard.html          # Web dashboard
├── config.json                 # Configuration
├── README.md                   # Documentation
└── LICENSE                     # MIT License
```

## 🎨 Customization

### Change Dashboard Theme
```python
from jarvis_complete import DigitalClock, ClockTheme
clock = DigitalClock(theme=ClockTheme.DARK)
```

### Add Custom Timezones
```python
from jarvis_complete import DigitalClock, TimeZoneInfo
clock = DigitalClock()
clock.TIMEZONE_CONFIGS["CUSTOM"] = TimeZoneInfo(
    "CUSTOM", "Your/Timezone", "Custom Timezone", "+00:00"
)
```

### Modify API Port
```python
app.run(host='0.0.0.0', port=8000)  # Change port to 8000
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Change port in the script or:
lsof -i :5000  # Find process
kill -9 <PID>  # Kill process
```

### Missing Dependencies
```bash
pip install --upgrade -r requirements-complete.txt
```

### Dashboard Not Loading
- Check if Flask is running: `curl http://localhost:5000/`
- Check browser console for JavaScript errors
- Clear browser cache and refresh

## 📝 Configuration

Edit `config.json` to customize:
- Agent name
- Default timezone list
- Memory limits
- Conversation history size
- Feature toggles

## 🚀 Performance

- **CLI Mode**: Minimal resource usage (< 50MB RAM)
- **API Mode**: Low overhead REST server (< 100MB RAM)
- **Dashboard**: Lightweight web interface with 2s refresh rate
- **Metrics**: Tracks up to 100 samples for visualization

## 📚 Learning & Development

### Extending with Custom Commands
1. Add method in `AdvancedJarvisAgent` class
2. Map command in `process_command()` method
3. Add API endpoint in `create_flask_app()` function

### Adding New Features
1. Create feature class (e.g., `CustomFeature`)
2. Integrate with main agent
3. Add REST endpoint
4. Update dashboard display

## 📄 License

MIT License - See LICENSE file for details

## 👨‍💻 Author

Created with ❤️ for advanced AI-powered agent systems

## 🤝 Contributing

Contributions welcome! Please feel free to submit issues and enhancement requests.

## 📞 Support

For issues and questions:
- Check the documentation above
- Review API examples
- Check console logs for error messages

---

**JARVIS v3.0** - Advanced AI Agent System with REST API, Web Dashboard, and Real-time Monitoring
