Sure! Here's the English translation of your `README.md`:

---

# TikTok Automation with Python + Playwright

🤖 Automate interactions with TikTok for viewing and analyzing videos based on search queries.

## 📋 Overview

The script performs the following tasks:
- ✅ Login to TikTok via browser
- ✅ Search for videos based on a specified query  
- ✅ Watch videos in the search results feed
- ✅ Randomly skip some videos (12% by default)
- ✅ Log all actions to the console and a log file

## 🛠 Technologies

- **Python 3.10+**
- **Playwright** – for browser automation
- **python-dotenv** – to manage environment variables

## 📦 Project Structure

```
tiktok-automation/
├── main.py               # Main script
├── requirements.txt      # Dependencies
├── .env.example          # Configuration template
├── .env                  # Your custom settings (to create)
├── README.md             # Documentation
└── tiktok_automation.log # Log file (generated automatically)
```

## 🚀 Installation & Run

### 1. Clone the repository
```bash
git clone <repository-url>
cd tiktok-automation
```

### 2. Create a virtual environment
```bash
python3 -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
# venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

### 4. Configure settings
```bash
cp .env.example .env
nano .env   # or edit manually
```

### 5. Run the script
```bash
python main.py
```

## ⚙️ Configuration

You can configure settings in `.env`:

```env
# Percentage of videos to skip (default is 12%)
SKIP_PERCENT=12

# Max number of videos to process
MAX_VIDEOS=20

# Default search query
SEARCH_QUERY=dance
```

## 📊 Logging

The script logs details both to console and to a file:

### Console example:
```
ID: 7123456789 | URL: https://tiktok.com/video/7123456789 | Status: WATCHED FULLY
ID: 7123456790 | URL: https://tiktok.com/video/7123456790 | Status: SKIPPED
```

### Log file:
- `tiktok_automation.log` contains detailed logs of execution

### Statistics:
```
=== STATISTICS ===
Total videos processed: 20
Fully watched: 18
Skipped: 2
Skip rate: 10.0%
```

## 🔧 Implementation Highlights

### Login
- Opens a real browser window for manual login
- Supports different login methods
- Verifies successful login

### Video Search
- Automatically searches for specified query
- Adapts to interface elements
- Works across TikTok language/region variants

### Video Viewing
- Random watch duration (15–45 seconds)
- Simulates human behavior
- Smooth transition between videos

### Error Handling
- Detailed error logging
- Graceful handling of missing elements
- Auto-recovery from failures

## 🎯 Workflow Logic

1. **Initialization**: Browser launches with realistic settings  
2. **Login**: Go to TikTok and log in manually  
3. **Search**: Enter query and navigate to results  
4. **Process Videos**:  
   - Get video info  
   - Randomly decide to skip or watch (12% skip rate)  
   - View or skip  
   - Log outcome  
5. **Summary Stats**: Output final report

## ⚠️ Notes

### Security
- Use a real TikTok account
- Don't run too frequently (risk of account blocks)
- Follow TikTok's terms of use

### Limitations
- Requires manual login on first run
- May need updated selectors if TikTok UI changes
- Only works with publicly available videos

### Performance
- Uses full browser (not headless) to bypass bot detection
- Adds delays to mimic human activity
- Adaptive watch times

## 🐛 Troubleshooting

### Playwright installation issues
```bash
playwright install --force chromium
```

### Missing elements
- Check selector accuracy
- TikTok's layout might’ve changed
- Try updating Playwright

### Login problems
- Use a stable internet connection
- Try different login methods (email/phone)
- Check if your account is blocked

## 📈 Potential Improvements

- [ ] Automatic login via API  
- [ ] Session persistence between runs  
- [ ] Video content analysis  
- [ ] Data export to CSV/JSON  
- [ ] Multiple search queries support  
- [ ] GUI interface  
- [ ] Docker containerization  

## 📄 License

MIT License – use freely for learning and testing purposes.

## 🤝 Contributing

1. Fork the repository  
2. Create a new feature branch  
3. Make changes  
4. Submit a Pull Request

---

**⚠️ Disclaimer**: Use responsibly and in accordance with TikTok’s terms. The author is not responsible for account suspensions or violations of ToS.