# Ted-AI Enhanced - Next Generation Security Assessment Copilot

A sophisticated, production-grade evolution of the Ted-AI penetration testing copilot with advanced architecture, intelligent reasoning, and comprehensive feature set.

## 🎯 What's New in This Enhancement

This enhanced version introduces significant architectural improvements and sophisticated features:

### **Architecture Improvements**

#### 1. **Advanced ORM Data Models** (`models.py`)
- SQLAlchemy ORM with proper relationships and constraints
- Comprehensive data validation
- Support for complex queries and aggregations
- Automatic timestamp management
- Enum-based status tracking for type safety

#### 2. **Sophisticated Database Layer** (`database.py`)
- Connection pooling with optimized settings
- Transaction management with automatic rollback
- Context managers for safe session handling
- Query optimization with indexing
- Comprehensive statistics and aggregation methods
- Efficient batch operations

#### 3. **Multi-Agent Reasoning Engine** (`reasoning_engine.py`)
- Specialized analysis agents (Evidence, Hypothesis, Priority)
- Intelligent recommendation generation
- Hypothesis validation based on supporting evidence
- Priority management and focus optimization
- Session tracking and audit trails
- Extensible agent framework for custom analysis

#### 4. **Rich CLI Interface** (`cli.py`)
- Beautiful terminal output with Rich library
- Interactive prompt-based commands
- Real-time table formatting
- Progress indicators and spinner animations
- Context-aware help system
- Comprehensive error handling

#### 5. **Scalable Application Architecture** (`app.py`)
- Configuration management (environment + file-based)
- Logging infrastructure with file persistence
- Health check system for monitoring
- Extensible design for API server integration
- Clean separation of concerns

## 🚀 Key Features

### **Engagement Management**
- Create and manage multiple engagements
- Track target information and technology stacks
- Monitor engagement status and progress
- Support for scope definition and out-of-scope tracking

### **Testing Objectives**
- Define multiple testing objectives per engagement
- Priority-based ordering
- Progress tracking
- Reject/accept hypotheses per objective
- Automatic completion tracking

### **Evidence Collection**
- Multiple evidence types (HTTP requests, responses, reconnaissance, etc.)
- Confidence-level tracking
- Endpoint-specific evidence
- Raw data storage and artifact linking
- Evidence clustering and analysis

### **Hypothesis Management**
- Create testable theories about vulnerabilities
- Link hypotheses to supporting evidence
- Status tracking (pending, in_progress, validated, rejected)
- Confidence scoring based on evidence
- Attack vector and component tracking

### **Finding Management**
- Confirm vulnerabilities as findings
- Severity classification (Critical, High, Medium, Low, Info)
- CVSS scoring support
- CWE/CVE tracking
- Remediation guidance
- Proof-of-concept documentation

### **Intelligent Analysis**
- **Evidence Analysis Agent**: Identifies patterns, gaps, and coverage
- **Hypothesis Validation Agent**: Evaluates hypothesis likelihood
- **Priority Agent**: Determines optimal testing focus
- Automated recommendation generation
- Session logging and feedback tracking

## 📊 Data Model

### Core Entities
```
Engagement
├── Objectives
├── Evidence
│   └── Related Hypotheses
├── Hypotheses
│   └── Supporting Evidence
├── Findings
│   ├── Related Evidence
│   └── Validated Hypotheses
└── Session Logs
    └── Reasoning Outputs
```

### Key Relationships
- Engagements contain multiple Objectives, Evidence, Findings, and Hypotheses
- Evidence can be related to multiple Hypotheses
- Hypotheses are validated by supporting Evidence
- Findings are derived from Hypotheses and Evidence
- All operations are logged in Session Logs for audit trails

## 🛠️ Installation

### Prerequisites
- Python 3.9+
- SQLite3
- Local Ollama/Qwen (for AI models) or API key for remote models

### Setup

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Configure Environment**
```bash
cp .env.example .env
# Edit .env with your settings
```

3. **Initialize Application**
```bash
python app.py health
```

## 💻 Usage

### Starting the CLI
```bash
python app.py cli
```

### Available Commands

#### Engagement Management
```
new          - Create new engagement
list         - List all engagements
select       - Select current engagement
status       - Show current engagement status
```

#### Testing Objectives
```
obj-add      - Add testing objective
obj-list     - List objectives for current engagement
```

#### Evidence Collection
```
ev-add       - Add evidence item
ev-list      - List all evidence
```

#### Finding Management
```
find-list    - List findings for engagement
```

#### Analysis and Intelligence
```
analyze      - Run comprehensive analysis
stats        - Display engagement statistics
```

#### Utility
```
help         - Show help information
exit         - Exit application
```

## 📋 Example Workflow

```bash
# Start application
python app.py cli

# Create engagement
> new
  Target Name: api.example.com
  Target Type: api
  ...

# Add testing objective
> obj-add
  Title: Identify Authorization Flaws
  ...

# Collect evidence
> ev-add
  Type: HTTP_REQUEST
  Title: Unauthorized user endpoint access
  Confidence: 0.8
  ...

# Analyze engagement
> analyze
  [Running Evidence Analysis]
  [Running Hypothesis Validation]
  [Generating Recommendations]
  ✓ 5 recommended actions identified

# View statistics
> stats
  Progress: 45%
  Findings: Critical=1, High=3
  Evidence: 24 items collected
```

## 🧠 Reasoning Engine Details

### Evidence Analysis Agent
- Analyzes confidence distribution
- Identifies evidence gaps
- Evaluates endpoint coverage
- Clusters evidence by type
- Detects contradictions

### Hypothesis Validation Agent
- Scores hypotheses based on evidence
- Ranks by validation likelihood
- Assesses readiness for testing
- Tracks evidence relationships
- Identifies contradicted theories

### Priority Agent
- Determines objective priorities
- Calculates testing efficiency
- Identifies critical findings
- Recommends focus areas
- Optimizes resource allocation

## 🔐 Security Features

- Foreign key constraints for data integrity
- Transaction rollback on errors
- Secure session management
- Audit logging of all operations
- No sensitive data in logs
- Configuration isolation

## 📈 Database Schema

### Tables
- `engagements` - Main engagement records
- `objectives` - Testing objectives
- `evidence` - Collected evidence items
- `hypotheses` - Testable theories
- `findings` - Confirmed vulnerabilities
- `session_logs` - AI reasoning sessions
- `evidence_hypothesis` - M2M relationship

### Indexes
- Fast lookups by engagement
- Quick status filtering
- Efficient date range queries
- Severity-based sorting

## 🔧 Configuration

### Environment Variables
```bash
TED_DB_PATH=ted_ai.db
TED_ECHO_SQL=false
TED_AI_MODEL=local/qwen
TED_DEBUG=false
TED_LOG_LEVEL=INFO
```

### Configuration File (config.json)
```json
{
  "database_path": "ted_ai.db",
  "ai_model": "local/qwen",
  "enable_research_layer": true,
  "enable_auto_analysis": true,
  "debug_mode": false
}
```

## 📊 Statistics and Reporting

### Engagement Metrics
- Overall progress percentage
- Objective completion rate
- Finding severity distribution
- Evidence collection progress
- Hypothesis validation status

### Analysis Output
- Confidence distributions
- Evidence gaps and recommendations
- Hypothesis rankings
- Priority recommendations
- Time efficiency metrics

## 🚀 Advanced Features (Roadmap)

- **API Server**: FastAPI-based REST API for programmatic access
- **Research Layer**: Autonomous security intelligence gathering
- **Report Generation**: Automated penetration test report creation
- **Collaboration**: Multi-user engagement tracking
- **Integration**: Custom tool integration framework
- **Webhooks**: Real-time event notifications
- **ML Training**: Learn from past engagements

## 🐛 Debugging

### Enable Debug Mode
```bash
TED_DEBUG=true python app.py cli
```

### View Logs
```bash
tail -f ted_ai_data/ted_ai.log
```

### Database Inspection
```bash
sqlite3 ted_ai.db
sqlite> .tables
sqlite> SELECT * FROM engagements;
```

## 📚 Architecture Diagram

```
┌──────────────────────────────────────┐
│      Interactive CLI Interface      │
│      (Rich Formatting)              │
└────────────────┬─────────────────────┘
                 │
        ┌────────▼────────┐
        │   Application   │
        │   Controller    │
        └────────┬────────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
┌───▼──┐   ┌────▼─────┐   ┌──▼────────┐
│ DB   │   │ Reasoning│   │ Config    │
│Layer │   │ Engine   │   │ Mgmt      │
└───┬──┘   └────┬─────┘   └───────────┘
    │           │
┌───▼────────────▼──┐
│  SQLAlchemy ORM   │
│   + SQLite3       │
└───────────────────┘
```

## 🤝 Contributing

To add custom analysis agents:

1. Extend `ReasoningAgent` base class
2. Implement `analyze()` and `generate_recommendations()`
3. Register in `ReasoningEngine.agents` dict
4. Add CLI command if user-facing

## 📝 License

MIT License - See LICENSE file

## 🙏 Acknowledgments

This enhanced version builds upon the original Ted-AI architecture with significant improvements to:
- Code organization and maintainability
- Database design and optimization
- User interface and experience
- Reasoning capabilities
- Extensibility and scalability

## 📞 Support

For issues, questions, or suggestions:
1. Check logs in `ted_ai_data/ted_ai.log`
2. Run health check: `python app.py health`
3. Review this documentation
4. Submit detailed bug reports with context

## 🎓 Learning Resources

- SQLAlchemy ORM: https://docs.sqlalchemy.org
- Rich Library: https://rich.readthedocs.io
- Penetration Testing Methodology: https://owasp.org/www-project-web-security-testing-guide/
- CVSS Scoring: https://www.first.org/cvss/

---

**Version**: 2.0 Enhanced  
**Last Updated**: 2024  
**Status**: Production Ready