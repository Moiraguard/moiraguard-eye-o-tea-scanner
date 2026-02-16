# MOIRAGUARD - Eye O Tea (IoT) Scanner

<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-Moiraguard-181717?style=for-the-badge&logo=github)](https://github.com/Moiraguard/moiraguard-eye-o-tea-scanner)
[![Python](https://img.shields.io/badge/Python-3.7%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Research%20Only-red?style=for-the-badge)](https://github.com/Moiraguard/moiraguard-eye-o-tea-scanner)
[![DEFCON](https://img.shields.io/badge/DEFCON-GROUP%20CASABLANCA-00FF88?style=for-the-badge)](https://www.linkedin.com/company/defcon-group-casablanca)

</div>

<div align="center">
  <img src="examples/MoiraGuard-Eye-O-Tea-logo.png" alt="MOIRAGUARD Eye-O-Tea Logo" width="600">

  ### 👁️ Global IoT/IIoT Infrastructure Reconnaissance
  **Monitoring IoT Reconnaissance & Guard**
</div>

## 📖 Overview

**MOIRAGUARD** (Eye-O-Tea) is an advanced IoT/IIoT security reconnaissance framework designed for security research and educational purposes. Built for DEFCON GROUP CASABLANCA 2026, this tool performs passive reconnaissance on global IoT infrastructure using the Shodan API.

### Author
**Mohammed Amine Moulay (@MLY)**
DEFCON GROUP CASABLANCA 2026 | Security Research

### 🔗 Quick Links
- **Repository**: https://github.com/Moiraguard/moiraguard-eye-o-tea-scanner
- **Issues & Bug Reports**: https://github.com/Moiraguard/moiraguard-eye-o-tea-scanner/issues
- **Pull Requests**: https://github.com/Moiraguard/moiraguard-eye-o-tea-scanner/pulls
- **Releases**: https://github.com/Moiraguard/moiraguard-eye-o-tea-scanner/releases

## 📸 Example Output

<div align="center">
  <img src="examples/moiraguard_report_20260216_185544.png" alt="MOIRAGUARD HTML Report Example" width="850">
  <br><br>
  <em>🎯 Example Report: United States IoT Infrastructure Scan - 283,882 Devices Discovered</em>
  <br>
  <sub>HTML Report with Cyberpunk Neon Theme | Interactive Charts | Risk Analysis | Country-Targeted Reconnaissance</sub>
</div>

**Report Highlights:**
- 👁️ **Cyberpunk Neon Emerald Design** - Dark theme with glowing accents and glassmorphic UI
- 📊 **Interactive Visualizations** - Pie charts, bar graphs, and risk level doughnuts
- 🎯 **Multi-Category Analysis** - Smart Home (10) | Cameras (278K) | SCADA (1.2K) | Building (4K) | MQTT (9)
- 🚨 **Risk Classification** - Real-time CRITICAL/HIGH/MEDIUM indicators
- 🌍 **Country-Specific Targeting** - 50+ countries supported
- 💾 **Multiple Export Formats** - JSON, CSV, HTML, PNG screenshots

## ⚠️ LEGAL DISCLAIMER

```
╔═══════════════════════════════════════════════════════════════╗
║                      ⚠️  LEGAL WARNING ⚠️                     ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  This tool is for SECURITY RESEARCH and EDUCATION ONLY        ║
║                                                               ║
║  • Unauthorized access to computer systems is ILLEGAL         ║
║  • This tool performs PASSIVE reconnaissance only             ║
║  • Do NOT attempt to access systems without authorization     ║
║  • Use RESPONSIBLY and ETHICALLY                              ║
║  • The author is NOT responsible for misuse                   ║
║                                                               ║
║  By using this tool, you agree to comply with all applicable  ║
║  laws and regulations. The user assumes all responsibility.   ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

**Legal Use Cases:**
- Security research and vulnerability assessment
- Educational purposes and IoT security training
- Defensive security operations
- Authorized penetration testing
- Academic research

**Illegal Use Cases:**
- Unauthorized access to systems
- Exploitation of discovered vulnerabilities
- Any malicious activity

## 🎯 Features

### Current Features (v1.1)

- **Multi-Category IoT Scanning**
  - Smart Home Appliances & Consumer IoT
  - IoT Cameras & Surveillance Systems (RTSP)
  - SCADA/Industrial Control Systems (Modbus)
  - Building Automation Systems (BACnet)
  - IoT MQTT Messaging Brokers
  - Industrial IoT Gateways & Automation

- **Country-Specific Targeting**
  - Select from 50+ predefined countries
  - Custom country code input option
  - Global scan mode (no country filter)
  - Configurable via `countries.json`

- **Dual Verbosity Modes**
  - **Metrics Mode**: Fast scans collecting only counts and totals
  - **Verbose Mode**: Detailed scans including IP addresses, organizations, and device details

- **Advanced Export & Reporting**
  - **JSON Export**: Structured data for API integration
  - **CSV Export**: Spreadsheet-friendly format
  - **HTML Reports with Interactive Charts**:
    - Beautiful pie charts showing device distribution
    - Bar charts for category comparison
    - Risk level doughnut charts
    - Responsive design with Chart.js
    - Optional detailed device tables in verbose mode
  - **PNG Charts Export** (NEW!):
    - High-resolution pie chart (300 DPI)
    - Bar chart with value labels
    - Risk level doughnut chart
    - Combined summary chart
    - Perfect for presentations and reports
  - Export all formats at once
  - Organized in `Moiraguard-Eye-O-Tea-Exports/` directory

- **Advanced Reconnaissance**
  - Geographic distribution analysis
  - Vendor identification
  - Risk level assessment
  - Sample device enumeration
  - Real-time statistics

- **Rich CLI Interface**
  - Colorized output
  - Typewriter effects
  - Loading animations
  - Progress indicators
  - Beautiful ASCII art banner

- **Security Features**
  - API key stored in separate file
  - `.gitignore` protection for credentials
  - Passive reconnaissance only
  - Legal warnings and reminders

## 📁 Project Structure

```
moiraguard-eye-o-tea-scanner/
├── moiraguard_iot_scanner.py    # Main scanner application
├── check_setup.py                # Setup verification tool
├── requirements.txt              # Python dependencies
├── countries.json                # Country code mappings (50+ countries)
├── targets.json                  # Scan profile configurations
├── shodan_api.key               # Your Shodan API key (create this)
├── examples/                     # Example files (tracked in git)
│   ├── MoiraGuard-Eye-O-Tea-logo.png
│   ├── moiraguard_report_20260216_185544.png
│   └── README.md
├── Moiraguard-Eye-O-Tea-Exports/ # Scan outputs (git ignored)
│   ├── *.json                   # JSON exports
│   ├── *.csv                    # CSV exports
│   ├── *.html                   # HTML reports
│   └── *.png                    # Chart/screenshot exports
└── README.md                     # This file
```

**Note:**
- The `examples/` folder contains sample files for documentation (included in git)
- The `Moiraguard-Eye-O-Tea-Exports/` folder is created automatically and excluded from git (sensitive data)
- Your API key file (`shodan_api.key`) is protected by `.gitignore`

## 🚀 Installation

### Prerequisites

- **Python 3.7 or higher**
- **Shodan API account** (Membership recommended)
- **Internet connection**

### Step-by-Step Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/Moiraguard/moiraguard-eye-o-tea-scanner.git
cd moiraguard-eye-o-tea-scanner
```

#### 2. Install Python Dependencies
```bash
# Using pip
pip install -r requirements.txt

# Or using pip3
pip3 install -r requirements.txt

# Or install manually
pip install shodan matplotlib
```

#### 3. Get Your Shodan API Key

1. Go to: https://account.shodan.io/
2. Register for an account or login
3. Navigate to "My Account" section
4. Copy your API key

**Shodan Membership Required:**

This tool requires a **Shodan Membership** ($59/month or $899/lifetime) for optimal functionality:
- **Query Credits**: 10,000+ per month (vs 100 on free)
- **Results**: Full result sets (vs 1 page on free)
- **Filters**: Advanced country and protocol filters
- **Historical Data**: Access to historical scan data
- **API Features**: Full API capabilities needed for this tool

**Note:** Free accounts are very limited and may not provide enough data for meaningful scans. Consider the membership as an investment in your security research capabilities.

#### 4. Configure Your API Key

**Option A: Create the key file manually**
```bash
# Linux/Mac
echo "YOUR_API_KEY_HERE" > shodan_api.key

# Windows (Command Prompt)
echo YOUR_API_KEY_HERE > shodan_api.key

# Windows (PowerShell)
"YOUR_API_KEY_HERE" | Out-File -FilePath shodan_api.key -NoNewline
```

**Option B: Use a text editor**
1. Create a new file named `shodan_api.key` in the tools directory
2. Paste your API key (single line, no spaces or quotes)
3. Save the file

**Example file content:**
```
Ab1Cd2Ef3Gh4Ij5Kl6Mn7Op8Qr9St0Uv
```

#### 5. Verify Installation

**Quick Verification (Automated):**
```bash
# Run the setup checker (recommended)
python3 check_setup.py
```

This will verify:
- ✓ Python version compatibility
- ✓ Shodan module installation
- ✓ API key file exists and valid
- ✓ Configuration files present
- ✓ Main scanner script ready
- ✓ API connection working

**Manual Verification:**
```bash
# Check Python version
python3 --version  # Should be 3.7 or higher

# Check Shodan installation
python3 -c "import shodan; print('Shodan installed successfully')"

# Verify API key file exists
ls -l shodan_api.key  # Linux/Mac
dir shodan_api.key    # Windows
```

#### 6. Customize Configuration (Optional)

**Edit `countries.json`** to add/remove countries:
```json
{
  "countries": {
    "Your Country": "YC",
    "Morocco": "MA",
    "United States": "US"
  }
}
```

**Edit `targets.json`** for custom scan profiles:
- Pre-configured regional profiles
- Custom query templates
- Sector-specific scans

## 📝 Usage

### Quick Start

```bash
# Navigate to tools directory
cd DEFCON-GROUP-CASA/tools

# Run the scanner
python3 moiraguard_iot_scanner.py
```

### Complete Usage Walkthrough

#### Step 1: Launch the Scanner

```bash
python3 moiraguard_iot_scanner.py
```

You'll see the MOIRAGUARD banner and initialization:

```
╔═══════════════════════════════════════════════════════════════════════╗
║                     MOIRAGUARD Eye-O-Tea                              ║
╚═══════════════════════════════════════════════════════════════════════╝

[✓] API key loaded from shodan_api.key
[i] Key length: 32 characters
```

#### Step 2: Select Target Country

When launched, you'll see a menu:

```
╔═══════════════════════════════════════════════════════════╗
║            SELECT TARGET COUNTRY              ║
╚═══════════════════════════════════════════════════════════╝

[0] GLOBAL (All countries - no filter)

[1] Morocco                  (MA)
[2] United States            (US)
[3] China                    (CN)
...

[C] Custom country code

Select option:
```

**Options:**
- Enter `0` for global scan (all countries)
- Enter a number (1-N) to select a specific country
- Enter `C` to input a custom 2-letter country code

#### Step 3: Choose Verbosity Level

Select how much detail you want to collect:

```
Scan Verbosity:
  [1] Metrics Only (Fast - counts and totals only)
  [2] Verbose Mode (Detailed - includes IPs and device info)

Select mode [1/2]:
```

**When to use Metrics Mode (1):**
- Quick overview scans
- Conserving API credits
- Only need statistics
- Faster processing

**When to use Verbose Mode (2):**
- Detailed security assessments
- Need specific IP addresses
- Creating comprehensive reports
- Investigating specific devices

#### Step 4: Scan Execution

The scanner will now:
1. Connect to Shodan API
2. Verify your credentials
3. Run 6 category scans sequentially
4. Display results in real-time

```
[✓] Shodan API connection established
[✓] API verified - Query credits: 100

[SCAN 1/6] ► SMART HOME APPLIANCES & CONSUMER IoT
Risk Level: HIGH ⚠️⚠️
[◆] Discovered 45,231 exposed smart home devices globally

[SCAN 2/6] ► IoT CAMERAS & SURVEILLANCE SYSTEMS (RTSP)
Risk Level: CRITICAL ⚠️⚠️⚠️
[!!!] Found 12,847 exposed camera streams
...
```

**Scan Duration:** Approximately 1-2 minutes per category (6-12 minutes total)

#### Step 5: Review Summary

After all scans complete, you'll see:
- Total devices discovered
- Category breakdown with percentages
- Risk level analysis
- Geographic distribution (if applicable)

#### Step 6: Export Results (Post-Scan Menu)

Choose how to export your findings:

```
╔═══════════════════════════════════════════════════════════╗
║            POST-SCAN OPTIONS                    ║
╚═══════════════════════════════════════════════════════════╝

[1] Export to JSON (Metrics Only)
[2] Export to JSON (Verbose - with IP addresses)
[3] Export to CSV (Metrics Only)
[4] Export to CSV (Verbose - with device details)
[5] Export to HTML with Charts (Metrics Only)
[6] Export to HTML with Charts (Verbose - with device table)
[7] Export Charts as PNG (4 chart images)
[8] Export ALL formats (Metrics Only)
[9] Export ALL formats + PNG (Verbose)
[0] Exit

Select option:
```

**Export Recommendations:**

| Use Case | Recommended Option |
|----------|-------------------|
| PowerPoint presentation | Option 7 (PNG charts) |
| Quick web report | Option 5 (HTML - Metrics) |
| Detailed security report | Option 6 (HTML - Verbose) |
| Data analysis in Excel | Option 4 (CSV - Verbose) |
| API integration | Option 2 (JSON - Verbose) |
| Complete documentation | Option 9 (All formats + PNG) |

**After exporting:**
```
[✓] JSON exported to: Moiraguard-Eye-O-Tea-Exports/moiraguard_scan_20260216_163045.json
[✓] CSV exported to: Moiraguard-Eye-O-Tea-Exports/moiraguard_scan_20260216_163045.csv
[✓] HTML report exported to: Moiraguard-Eye-O-Tea-Exports/moiraguard_scan_20260216_163045.html
[✓] Pie chart exported: moiraguard_pie_chart_20260216_163045.png
[✓] Bar chart exported: moiraguard_bar_chart_20260216_163045.png
[✓] Risk chart exported: moiraguard_risk_chart_20260216_163045.png
[✓] Summary chart exported: moiraguard_summary_20260216_163045.png
[✓] All formats exported successfully!
```

#### Step 7: View Reports

**Open HTML Report:**
```bash
# Linux
xdg-open Moiraguard-Eye-O-Tea-Exports/moiraguard_scan_*.html

# Mac
open Moiraguard-Eye-O-Tea-Exports/moiraguard_scan_*.html

# Windows
start Moiraguard-Eye-O-Tea-Exports\moiraguard_scan_*.html

# Or just double-click the file
```

**View PNG Charts:**
```bash
# Linux
xdg-open Moiraguard-Eye-O-Tea-Exports/moiraguard_summary_*.png

# Mac
open Moiraguard-Eye-O-Tea-Exports/moiraguard_summary_*.png

# Windows
start Moiraguard-Eye-O-Tea-Exports\moiraguard_summary_*.png

# Or view all charts at once
ls Moiraguard-Eye-O-Tea-Exports/*.png
```

**View JSON:**
```bash
cat Moiraguard-Eye-O-Tea-Exports/moiraguard_scan_*.json | jq .
```

**Open CSV in Excel:**
- Double-click the .csv file
- Or open in Excel/LibreOffice Calc/Google Sheets

### Usage Examples

#### Example 1: Quick Global Scan (Metrics Only)
```bash
python3 moiraguard_iot_scanner.py
# Select: [0] Global
# Select: [1] Metrics Only
# After scan: [5] Export to HTML with Charts
# Result: Fast overview with nice visuals
```

#### Example 2: Detailed Country Scan (Verbose)
```bash
python3 moiraguard_iot_scanner.py
# Select: [1] Morocco (or your country)
# Select: [2] Verbose Mode
# After scan: [6] Export to HTML with device table
# Result: Comprehensive report with all device details
```

#### Example 3: Custom Country Code
```bash
python3 moiraguard_iot_scanner.py
# Select: [C] Custom country code
# Enter: DE (for Germany)
# Select: [2] Verbose Mode
# After scan: [8] Export ALL formats
# Result: Complete documentation in all formats
```

#### Example 4: Multiple Exports
```bash
# Run scan once, export multiple times
python3 moiraguard_iot_scanner.py
# ... complete scan ...
# From post-scan menu:
# [5] HTML Metrics → for presentation
# [2] JSON Verbose → for analysis
# [4] CSV Verbose → for spreadsheet
# [0] Exit
```

## 📁 Project Structure

```
tools/
├── moiraguard_iot_scanner.py          # Main scanner script (1,635 lines)
├── requirements.txt                   # Python dependencies
├── check_setup.py                     # Setup verification script
├── countries.json                     # Country configuration (50+ countries)
├── targets.json                       # Target profiles and custom queries
├── shodan_api.key                     # Your Shodan API key (not in repo)
├── .gitignore                         # Git ignore patterns
├── README.md                          # This documentation
├── MoiraGuard-Eye-O-Tea-logo.png      # Project logo
└── Moiraguard-Eye-O-Tea-Exports/      # Export directory (auto-created)
    ├── moiraguard_scan_YYYYMMDD_HHMMSS.json        # JSON data
    ├── moiraguard_scan_YYYYMMDD_HHMMSS.csv         # CSV spreadsheet
    ├── moiraguard_scan_YYYYMMDD_HHMMSS.html        # HTML report
    ├── moiraguard_pie_chart_YYYYMMDD_HHMMSS.png    # Pie chart
    ├── moiraguard_bar_chart_YYYYMMDD_HHMMSS.png    # Bar chart
    ├── moiraguard_risk_chart_YYYYMMDD_HHMMSS.png   # Risk chart
    └── moiraguard_summary_YYYYMMDD_HHMMSS.png      # Combined summary
```

## ⚙️ Configuration

### countries.json

Customize the country list by editing `countries.json`:

```json
{
  "countries": {
    "Morocco": "MA",
    "United States": "US",
    "France": "FR",
    ...
  }
}
```

### Shodan API Key

The tool reads your API key from `shodan_api.key`. Keep this file secure and never commit it to version control (it's already in `.gitignore`).

## 🎨 Scan Categories

| Category | Protocol/Port | Risk Level | Description |
|----------|--------------|------------|-------------|
| Smart Home | 80, 8080, 443 | HIGH ⚠️⚠️ | Consumer IoT devices, smart appliances |
| Cameras | 554 (RTSP) | CRITICAL ⚠️⚠️⚠️ | Surveillance systems, IP cameras |
| SCADA/ICS | 502 (Modbus) | CRITICAL ⚠️⚠️⚠️ | Industrial control systems |
| Building Automation | 47808 (BACnet) | HIGH ⚠️⚠️ | HVAC, lighting, access control |
| MQTT Brokers | 1883 | HIGH ⚠️⚠️ | IoT messaging infrastructure |
| Industrial IoT | Various | CRITICAL ⚠️⚠️⚠️ | IIoT gateways, PLCs, industrial systems |

## 🔮 Upcoming Features (Roadmap)

### Version 1.1 ✅ (COMPLETED)
- [x] **Export Functionality**
  - CSV export of scan results
  - JSON report generation
  - HTML reports with interactive charts (Chart.js)
  - Dual verbosity modes (Metrics vs Verbose)

- [ ] **Multi-Target Scanning** (In Progress)
  - Select multiple countries in one scan
  - Create target profiles/presets (targets.json ready)
  - Save and load scan configurations

- [ ] **Enhanced Filtering** (Planned)
  - Filter by ISP/Organization
  - Filter by specific vendors
  - Custom Shodan query builder

### Version 1.2 (Planned)
- [ ] **Advanced Analytics**
  - Historical data tracking
  - Trend analysis over time
  - Vulnerability scoring

- [ ] **Integration Features**
  - Webhook notifications
  - Slack/Discord alerts
  - API for programmatic access

- [ ] **Database Support**
  - SQLite/PostgreSQL storage
  - Query historical scans
  - Compare scans over time

### Version 2.0 (Future)
- [ ] **Web Dashboard**
  - Real-time monitoring interface
  - Interactive maps
  - Visualization charts

- [ ] **Automated Scanning**
  - Scheduled scans
  - Continuous monitoring mode
  - Change detection alerts

- [ ] **Extended Protocol Support**
  - CoAP (Constrained Application Protocol)
  - AMQP (Advanced Message Queuing Protocol)
  - Additional industrial protocols

- [ ] **Threat Intelligence Integration**
  - CVE database integration
  - Known vulnerability matching
  - Risk scoring algorithms

## 🛡️ Security Best Practices

1. **API Key Protection**
   - Never share your API key
   - Never commit `shodan_api.key` to version control
   - Rotate keys regularly

2. **Ethical Usage**
   - Only scan systems you're authorized to test
   - Respect rate limits and API quotas
   - Follow responsible disclosure practices

3. **Data Handling**
   - Be careful with collected reconnaissance data
   - Don't publish sensitive findings publicly
   - Follow coordinated disclosure timelines

## 🐛 Troubleshooting

### Common Issues & Solutions

#### 1. API Key Not Found
```
[✗] API key file not found: shodan_api.key
```
**Solution:**
```bash
# Create the key file
echo "YOUR_ACTUAL_API_KEY" > shodan_api.key

# Verify it was created
cat shodan_api.key
```

#### 2. API Key Invalid
```
[✗] Shodan API Error: Invalid API key
```
**Solutions:**
- Check for extra spaces or newlines in `shodan_api.key`
- Verify key is correct at https://account.shodan.io/
- Regenerate a new key if necessary

#### 3. API Credits Exhausted
```
[✗] Shodan API Error: API rate limit exceeded
```
**Solutions:**
- Wait for monthly quota reset (1st of each month)
- Use more targeted country searches instead of global scans
- Space out your scans over multiple days
- Monitor your credit usage at https://account.shodan.io/

#### 4. No Results for Country
```
[◆] Discovered 0 exposed devices
```
**Possible Reasons:**
- Country has very few IoT devices
- Country code might be wrong (check ISO 3166-1 alpha-2)
- Network connectivity issues
- Shodan hasn't indexed that region recently

**Solutions:**
- Try global scan ([0] Global option)
- Verify country code is correct
- Try a different country

#### 5. Import Error
```
ModuleNotFoundError: No module named 'shodan'
```
**Solution:**
```bash
pip3 install -r requirements.txt
# or
pip3 install shodan
```

#### 6. Permission Denied (Linux/Mac)
```
Permission denied: shodan_api.key
```
**Solution:**
```bash
chmod 600 shodan_api.key
```

#### 7. Network Connection Error
```
[✗] Error: Connection timeout
```
**Solutions:**
- Check internet connection
- Verify firewall isn't blocking Python
- Try using a VPN if Shodan is blocked in your region
- Check if proxy settings are needed

#### 8. Export Directory Error
```
[✗] Error: Permission denied creating moiraguard_reports/
```
**Solution:**
```bash
# Manually create the directory
mkdir moiraguard_reports
chmod 755 moiraguard_reports
```

### Getting Help

If you encounter issues not listed here:

1. **Check Shodan Status**: https://status.shodan.io/
2. **Verify API Key**: https://account.shodan.io/
3. **Review Logs**: Look at the error message carefully
4. **Report Issues**: https://github.com/Moiraguard/moiraguard-eye-o-tea-scanner/issues

### Performance Tips

- **Use Metrics Mode** for faster scans and less data processing
- **Target specific countries** instead of global to conserve API credits
- **Run during off-peak hours** for better API response times
- **Wait between scans** to avoid rate limiting
- **Monitor your credits** regularly at https://account.shodan.io/

### API Credit Usage

Each scan category uses **1 query credit**:
- Smart Home Devices: 1 credit
- IoT Cameras: 1 credit
- SCADA/ICS: 1 credit
- Building Automation: 1 credit
- MQTT Brokers: 1 credit
- Industrial IoT: 1 credit

**Total per scan: 6 credits**

With Shodan Membership (10,000 credits/month), you can run approximately **1,666 full scans per month**.

## 📊 Export Formats

### JSON Export
Structured data format perfect for:
- API integration
- Data analysis with Python/R
- Feeding into security tools

**Example:**
```json
{
  "scan_timestamp": "2026-02-16T16:30:45",
  "target_country": "Morocco",
  "total_devices": 12345,
  "categories": {
    "Smart Home Devices": {
      "count": 5000,
      "devices": []
    }
  }
}
```

### CSV Export
Spreadsheet-friendly format for:
- Excel/Google Sheets analysis
- Database imports
- Quick data review

**Includes:**
- Scan metadata (date, time, target)
- Category summaries with risk levels
- Detailed device table (verbose mode)

### HTML Reports
Beautiful visual reports featuring:
- **Responsive web design**
- **Interactive charts** (Chart.js)
  - Pie chart: Device distribution
  - Bar chart: Category comparison
  - Doughnut chart: Risk levels
- **Professional styling**
- **Exportable to PDF** (browser print)
- **Shareable with stakeholders**

### PNG Charts Export (NEW!)
High-quality image files perfect for:
- PowerPoint/Keynote presentations
- Research papers and reports
- Social media sharing
- Documentation

**4 Charts Generated:**
1. **Pie Chart** - Device distribution by category
2. **Bar Chart** - Category comparison with counts
3. **Risk Chart** - Risk level breakdown (Critical/High/Medium)
4. **Summary Chart** - Combined view with both distributions

**Features:**
- **300 DPI resolution** - Print-quality images
- **Professional styling** - Clean, modern design
- **Color-coded** - Risk levels clearly visible
- **Labeled** - All values and percentages shown
- **Branded** - MOIRAGUARD footer on summary chart

## 📚 Resources

### Official Documentation
- **Shodan:** https://www.shodan.io/
- **Shodan API Docs:** https://developer.shodan.io/api
- **Chart.js:** https://www.chartjs.org/
- **Python Shodan Library:** https://shodan.readthedocs.io/

### IoT Security Resources
- **OWASP IoT Top 10:** https://owasp.org/www-project-internet-of-things/
- **NIST IoT Security:** https://www.nist.gov/programs-projects/nist-cybersecurity-iot-program
- **ICS-CERT:** https://www.cisa.gov/topics/industrial-control-systems

### Learning Materials
- **Shodan Cheat Sheet:** https://www.osintme.com/index.php/2021/01/16/ultimate-osint-with-shodan-100-great-shodan-queries/
- **IoT Pentesting Guide:** Various online resources
- **DEFCON GROUP CASABLANCA:** https://www.linkedin.com/company/defcon-group-casablanca/

## 🤝 Contributing

Contributions are welcome for legitimate security research purposes! We appreciate your help in making MOIRAGUARD better.

### How to Contribute

1. **Fork the repository**: https://github.com/Moiraguard/moiraguard-eye-o-tea-scanner/fork
2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/moiraguard-eye-o-tea-scanner.git
   cd moiraguard-eye-o-tea-scanner
   ```
3. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes** and commit them:
   ```bash
   git add .
   git commit -m "Add: your feature description"
   ```
5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Submit a Pull Request**: https://github.com/Moiraguard/moiraguard-eye-o-tea-scanner/pulls

### Contribution Guidelines

- All contributions must align with ethical security research practices
- Follow existing code style and conventions
- Add appropriate documentation for new features
- Test your changes thoroughly
- Ensure no sensitive information (API keys, credentials) is committed

**Note:** Contributions that facilitate malicious activities will be rejected.

## 📄 License

This tool is released under the **Research & Educational Use Only** license.

```
Copyright (c) 2026 Mohammed Amine Moulay (@MLY)

Permission is granted for research and educational purposes only.
Commercial use, malicious activities, and unauthorized system access
are strictly prohibited.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
```

## 👤 Author

**Mohammed Amine Moulay (@MLY)**
Security Engineer 
DEFCON GROUP CASABLANCA 2026

## 🙏 Acknowledgments

- **Shodan.io** for providing the comprehensive IoT search engine API
- **DEFCON GROUP CASABLANCA** community for supporting security research
- **Open source security research community** for continuous innovation
- All contributors who help improve this tool

## ⭐ Support the Project

If you find this tool useful for your security research:
- ⭐ Star the repository: https://github.com/Moiraguard/moiraguard-eye-o-tea-scanner
- 🐛 Report bugs or suggest features via Issues
- 🤝 Contribute code improvements
- 📢 Share with the security research community

---

<div align="center">

**Remember:** With great power comes great responsibility. Use this tool ethically and legally.

```
       👁️  Eye-O-Tea  👁️
    Stay curious, stay ethical
```

**[⬆ Back to Top](#moiraguard---eye-o-tea-iot-scanner)**

Made with 💚 by [Mohammed Amine Moulay](https://github.com/Moiraguard) | DEFCON GROUP CASABLANCA 2026

</div>
