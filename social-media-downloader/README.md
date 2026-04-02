# Social Media Downloader - Educational Edition

## 📚 Application Description

A comprehensive educational application for downloading media from various social media platforms. Designed for educational purposes only.

### ⚠️ Important Warning

**This application is for EDUCATIONAL PURPOSES ONLY!**
- Use it only for content you own
- Or content you have explicit permission to download
- Or Public Domain content
- Or content licensed under appropriate Creative Commons licenses

## 🎯 Features

### 1. Multi-Platform Support
- YouTube
- Vimeo
- TikTok
- Instagram
- Twitter/X
- Facebook
- Pinterest
- Reddit
- Tumblr

### 2. Supported Media Types
- 🎬 Videos
- 🖼️ Images
- 🎵 Audio Files
- 📄 Documents

### 3. Educational Tools
- Image properties analysis
- Audio properties analysis
- File hash generation for integrity verification
- Download statistics

## 🚀 Installation

### Requirements
- Python 3.8 or later
- pip

### Installation Steps

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install required packages
pip install yt-dlp requests beautifulsoup4 lxml pillow mutagen
```

## 📖 Usage

### Run the Application

```bash
python downloader.py
```

### Main Menu

After running the application, an interactive menu will appear:

```
======================================================================
SOCIAL MEDIA DOWNLOADER - EDUCATIONAL EDITION
======================================================================

⚠️  IMPORTANT: This tool is for EDUCATIONAL PURPOSES ONLY!
Only download content you own or have permission to download.

----------------------------------------------------------------------
MENU:
1. Download Video
2. Download Image
3. Download Audio
4. Get Media Info (without downloading)
5. Batch Download
6. Analyze Downloaded File
7. View Statistics
8. Export History
9. Exit
----------------------------------------------------------------------
```

### Quick Start Demo

```bash
python quick_start.py
```

## 📁 Directory Structure

After first run, the following structure will be created:

```
downloads/
├── video/
├── image/
├── audio/
├── document/
├── youtube/
├── vimeo/
├── tiktok/
├── instagram/
├── twitter/
├── facebook/
├── pinterest/
├── reddit/
└── tumblr/
```

## 🔧 Programming & Development

### Using as a Module

```python
from downloader import MediaDownloader, DownloadConfig, EducationalTools

# Configure settings
config = DownloadConfig()
config.output_dir = "my_downloads"
config.max_file_size = 1024 * 1024 * 1024  # 1 GB

# Create instance
downloader = MediaDownloader(config)

# Download video
result = downloader.download_video("https://youtube.com/watch?v=example")
if result:
    print(f"Downloaded: {result.download_path}")

# Download image
result = downloader.download_image("https://example.com/image.jpg")

# Download audio
result = downloader.download_audio("https://youtube.com/watch?v=audio")

# Get info
info = downloader.get_media_info("https://youtube.com/watch?v=example")
print(info)

# Batch download
urls = ["url1", "url2", "url3"]
results = downloader.download_batch(urls, media_type="video")

# Export history
downloader.export_history("my_history.json")

# Get statistics
stats = downloader.get_statistics()
print(stats)

# Educational tools
edutools = EducationalTools()
image_info = edutools.analyze_image("path/to/image.jpg")
audio_info = edutools.analyze_audio("path/to/audio.mp3")
file_hash = edutools.generate_hash("path/to/file.mp4")
```

### Main Application Classes

#### 1. `MediaType` (Enum)
Enumeration of supported media types.

#### 2. `MediaInfo` (Dataclass)
Store downloaded media information.

#### 3. `DownloadConfig`
Configuration settings for downloads.

#### 4. `MediaDownloader`
Main class for managing download operations.

#### 5. `EducationalTools`
Helper tools for educational purposes.

## 🎓 Educational Objectives

### 1. Computer Networks Learning
- Understanding HTTP/HTTPS protocols
- Working with Headers
- Managing Sessions
- SSL/TLS verification

### 2. File Processing Learning
- Reading and writing binary files
- File validation
- Media properties analysis
- Hash generation

### 3. Object-Oriented Programming
- Class design
- Inheritance and polymorphism
- Using Dataclasses
- Exception handling

### 4. Digital Ethics
- Copyright respect
- Terms of service
- Privacy and security
- Responsible use

## 🔐 Security & Privacy

### Built-in Security Features
1. **SSL Verification**: Verify security certificates
2. **Max File Size Limit**: Prevent huge file downloads
3. **Timeout**: Avoid infinite waiting
4. **Filename Sanitization**: Prevent unsafe characters
5. **Download Log**: Track all operations

### Best Practices
- Don't store user credentials
- Use encrypted HTTPS connections
- Verify downloaded file content
- Respect website robots.txt

## 📊 Statistics & Reports

View detailed download statistics:

```
==================================================
DOWNLOAD STATISTICS:
==================================================
Total Downloads: 15
Total Size: 245.67 MB

By Type:
  video: 10
  image: 4
  audio: 1

By Platform:
  youtube: 8
  vimeo: 3
  instagram: 2
  tiktok: 2
```

## 🛠️ Troubleshooting

### Common Issues & Solutions

#### 1. Connection Error
```
Error: Connection timeout
```
**Solution**: Check internet connection and increase timeout in settings.

#### 2. File Too Large
```
File too large: X bytes
```
**Solution**: Increase `max_file_size` in settings or choose smaller file.

#### 3. Invalid URL
```
Invalid URL
```
**Solution**: Ensure URL is valid and starts with http:// or https://

#### 4. Unsupported Platform
```
Detected platform: generic
```
**Solution**: Some platforms may require special tools. Try direct download.

## 📝 License

MIT License - For educational use only

## 🤝 Contributing

Educational contributions welcome:
- Improve documentation
- Add new platforms
- Enhance educational tools
- Fix bugs

## 📞 Support

For educational questions and code inquiries:
- Review code comments
- Study provided examples
- Try simple modifications to understand mechanisms

## ⭐ Tips for Best Quality

See `TIPS_AR.md` file (Arabic) for detailed tips.

### Quick Tips:
1. Use stable and fast internet connection
2. Choose appropriate quality for your needs
3. Check storage space before downloading
4. Use high-quality formats for video (MP4, MKV)
5. For audio, use 320 kbps for best MP3 quality
6. For images, use PNG for highest quality
7. Keep backups of important files
8. Document all downloads in logs

---

**Remember**: This is an educational tool. Use it responsibly and respect others' rights.
