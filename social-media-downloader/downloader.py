#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Social Media Downloader - Educational Application
A comprehensive tool for downloading videos, images, and files from various social media platforms.

This application is designed for educational purposes to teach:
- Web scraping ethics
- API usage
- Media processing
- File management
- Network programming

IMPORTANT: This tool should only be used for:
1. Educational purposes
2. Content you own
3. Content with explicit permission
4. Public domain content
5. Content under appropriate Creative Commons licenses

Author: Educational Development Team
License: MIT License (for educational use)
"""

import os
import sys
import json
import re
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

# Third-party imports
import requests
from bs4 import BeautifulSoup
import yt_dlp
from PIL import Image
import mutagen
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4


class MediaType(Enum):
    """Enumeration of supported media types"""
    VIDEO = "video"
    IMAGE = "image"
    AUDIO = "audio"
    DOCUMENT = "document"
    UNKNOWN = "unknown"


@dataclass
class MediaInfo:
    """Data class to store media information"""
    url: str
    title: str
    media_type: str
    platform: str
    file_size: Optional[int] = None
    duration: Optional[float] = None
    resolution: Optional[str] = None
    thumbnail: Optional[str] = None
    description: Optional[str] = None
    upload_date: Optional[str] = None
    uploader: Optional[str] = None
    download_path: Optional[str] = None
    timestamp: str = ""
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()


class DownloadConfig:
    """Configuration class for download settings"""
    
    def __init__(self):
        self.output_dir: str = "downloads"
        self.max_file_size: int = 500 * 1024 * 1024  # 500 MB default
        self.timeout: int = 30
        self.retry_count: int = 3
        self.verify_ssl: bool = True
        self.user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        self.supported_platforms: List[str] = [
            "youtube", "vimeo", "tiktok", "instagram", "twitter", 
            "facebook", "pinterest", "reddit", "tumblr"
        ]
        
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class MediaDownloader:
    """Main class for handling media downloads from various platforms"""
    
    def __init__(self, config: Optional[DownloadConfig] = None):
        self.config = config or DownloadConfig()
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": self.config.user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        })
        self.download_history: List[MediaInfo] = []
        self._setup_output_directory()
        
    def _setup_output_directory(self):
        """Create output directory structure"""
        base_path = Path(self.config.output_dir)
        base_path.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories for different media types
        for media_type in MediaType:
            (base_path / media_type.value).mkdir(exist_ok=True)
            
        # Create platform-specific directories
        for platform in self.config.supported_platforms:
            (base_path / platform).mkdir(exist_ok=True)
    
    def _generate_filename(self, title: str, media_type: str, extension: str) -> str:
        """Generate a safe filename"""
        # Remove invalid characters
        safe_title = re.sub(r'[<>:"/\\|?*]', '_', title)
        safe_title = safe_title[:100]  # Limit length
        
        # Add timestamp to avoid duplicates
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{safe_title}_{timestamp}.{extension}"
        
        return filename
    
    def _get_file_size(self, url: str) -> Optional[int]:
        """Get file size from URL headers"""
        try:
            response = self.session.head(url, timeout=self.config.timeout, 
                                        allow_redirects=True)
            return int(response.headers.get('content-length', 0))
        except Exception:
            return None
    
    def _validate_url(self, url: str) -> bool:
        """Validate URL format"""
        pattern = re.compile(
            r'^https?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return pattern.match(url) is not None
    
    def _detect_platform(self, url: str) -> str:
        """Detect the social media platform from URL"""
        url_lower = url.lower()
        
        platform_mapping = {
            'youtube': ['youtube.com', 'youtu.be'],
            'vimeo': ['vimeo.com'],
            'tiktok': ['tiktok.com'],
            'instagram': ['instagram.com'],
            'twitter': ['twitter.com', 'x.com'],
            'facebook': ['facebook.com', 'fb.watch'],
            'pinterest': ['pinterest.com'],
            'reddit': ['reddit.com'],
            'tumblr': ['tumblr.com'],
        }
        
        for platform, domains in platform_mapping.items():
            if any(domain in url_lower for domain in domains):
                return platform
        
        return "generic"
    
    def download_with_ytdlp(self, url: str, output_path: str) -> Optional[Dict[str, Any]]:
        """Download using yt-dlp for supported platforms"""
        
        ydl_opts = {
            'outtmpl': output_path,
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'ignoreerrors': True,
            'socket_timeout': self.config.timeout,
            'retries': self.config.retry_count,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                if info:
                    return {
                        'title': info.get('title', 'Unknown'),
                        'duration': info.get('duration'),
                        'filesize': info.get('filesize'),
                        'resolution': info.get('resolution'),
                        'thumbnail': info.get('thumbnail'),
                        'uploader': info.get('uploader'),
                        'upload_date': info.get('upload_date'),
                        'description': info.get('description'),
                    }
        except Exception as e:
            print(f"yt-dlp error: {str(e)}")
        
        return None
    
    def download_direct_file(self, url: str, save_path: str) -> bool:
        """Download file directly from URL"""
        try:
            response = self.session.get(url, stream=True, timeout=self.config.timeout,
                                       verify=self.config.verify_ssl)
            response.raise_for_status()
            
            # Check file size
            content_length = int(response.headers.get('content-length', 0))
            if content_length > self.config.max_file_size:
                print(f"File too large: {content_length} bytes")
                return False
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            return True
            
        except Exception as e:
            print(f"Direct download error: {str(e)}")
            return False
    
    def download_video(self, url: str, title: Optional[str] = None) -> Optional[MediaInfo]:
        """Download video from supported platforms"""
        if not self._validate_url(url):
            print("Invalid URL")
            return None
        
        platform = self._detect_platform(url)
        print(f"Detected platform: {platform}")
        
        if title is None:
            title = f"video_{platform}"
        
        # Try yt-dlp first for supported platforms
        if platform in self.config.supported_platforms:
            output_template = str(Path(self.config.output_dir) / platform / f"{title}.%(ext)s")
            result = self.download_with_ytdlp(url, output_template)
            
            if result:
                # Find the downloaded file
                download_dir = Path(self.config.output_dir) / platform
                files = list(download_dir.glob(f"{title}.*"))
                
                if files:
                    downloaded_file = str(files[0])
                    media_info = MediaInfo(
                        url=url,
                        title=title,
                        media_type=MediaType.VIDEO.value,
                        platform=platform,
                        file_size=result.get('filesize'),
                        duration=result.get('duration'),
                        resolution=result.get('resolution'),
                        thumbnail=result.get('thumbnail'),
                        description=result.get('description'),
                        upload_date=result.get('upload_date'),
                        uploader=result.get('uploader'),
                        download_path=downloaded_file
                    )
                    self.download_history.append(media_info)
                    return media_info
        
        # Fallback: try direct download
        filename = self._generate_filename(title, MediaType.VIDEO.value, "mp4")
        save_path = str(Path(self.config.output_dir) / MediaType.VIDEO.value / filename)
        
        if self.download_direct_file(url, save_path):
            media_info = MediaInfo(
                url=url,
                title=title,
                media_type=MediaType.VIDEO.value,
                platform=platform,
                download_path=save_path
            )
            self.download_history.append(media_info)
            return media_info
        
        return None
    
    def download_image(self, url: str, title: Optional[str] = None) -> Optional[MediaInfo]:
        """Download image from URL"""
        if not self._validate_url(url):
            print("Invalid URL")
            return None
        
        platform = self._detect_platform(url)
        
        if title is None:
            title = f"image_{platform}"
        
        # Determine file extension from URL or content type
        extension = "jpg"
        if url.lower().endswith(('.png', '.gif', '.webp', '.bmp')):
            extension = url.split('.')[-1].lower()
        
        filename = self._generate_filename(title, MediaType.IMAGE.value, extension)
        save_path = str(Path(self.config.output_dir) / MediaType.IMAGE.value / filename)
        
        if self.download_direct_file(url, save_path):
            # Validate image
            try:
                with Image.open(save_path) as img:
                    img.verify()
                print(f"Image validated: {save_path}")
            except Exception as e:
                print(f"Image validation warning: {str(e)}")
            
            media_info = MediaInfo(
                url=url,
                title=title,
                media_type=MediaType.IMAGE.value,
                platform=platform,
                download_path=save_path
            )
            self.download_history.append(media_info)
            return media_info
        
        return None
    
    def download_audio(self, url: str, title: Optional[str] = None) -> Optional[MediaInfo]:
        """Download audio from supported platforms"""
        if not self._validate_url(url):
            print("Invalid URL")
            return None
        
        platform = self._detect_platform(url)
        
        if title is None:
            title = f"audio_{platform}"
        
        # Use yt-dlp for audio extraction
        if platform in self.config.supported_platforms:
            output_template = str(Path(self.config.output_dir) / platform / f"{title}.%(ext)s")
            
            ydl_opts = {
                'outtmpl': output_template,
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'quiet': True,
                'no_warnings': True,
            }
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    if info:
                        download_dir = Path(self.config.output_dir) / platform
                        files = list(download_dir.glob(f"{title}.*"))
                        
                        if files:
                            media_info = MediaInfo(
                                url=url,
                                title=title,
                                media_type=MediaType.AUDIO.value,
                                platform=platform,
                                duration=info.get('duration'),
                                download_path=str(files[0])
                            )
                            self.download_history.append(media_info)
                            return media_info
            except Exception as e:
                print(f"Audio download error: {str(e)}")
        
        # Fallback: direct download
        filename = self._generate_filename(title, MediaType.AUDIO.value, "mp3")
        save_path = str(Path(self.config.output_dir) / MediaType.AUDIO.value / filename)
        
        if self.download_direct_file(url, save_path):
            media_info = MediaInfo(
                url=url,
                title=title,
                media_type=MediaType.AUDIO.value,
                platform=platform,
                download_path=save_path
            )
            self.download_history.append(media_info)
            return media_info
        
        return None
    
    def get_media_info(self, url: str) -> Optional[Dict[str, Any]]:
        """Get media information without downloading"""
        if not self._validate_url(url):
            return None
        
        platform = self._detect_platform(url)
        
        if platform in self.config.supported_platforms:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
                'ignoreerrors': True,
            }
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    if info:
                        return {
                            'platform': platform,
                            'title': info.get('title'),
                            'duration': info.get('duration'),
                            'filesize': info.get('filesize'),
                            'resolution': info.get('resolution'),
                            'thumbnail': info.get('thumbnail'),
                            'description': info.get('description'),
                            'uploader': info.get('uploader'),
                            'upload_date': info.get('upload_date'),
                            'formats': len(info.get('formats', [])),
                        }
            except Exception as e:
                print(f"Info extraction error: {str(e)}")
        
        return None
    
    def download_batch(self, urls: List[str], media_type: str = "auto") -> List[MediaInfo]:
        """Download multiple URLs"""
        results = []
        
        for i, url in enumerate(urls, 1):
            print(f"\n[{i}/{len(urls)}] Processing: {url}")
            
            if media_type == "auto":
                # Auto-detect media type from URL
                if any(ext in url.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
                    media_type = "image"
                elif any(ext in url.lower() for ext in ['.mp3', '.wav', '.ogg', '.flac']):
                    media_type = "audio"
                else:
                    media_type = "video"
            
            if media_type == "video":
                result = self.download_video(url)
            elif media_type == "image":
                result = self.download_image(url)
            elif media_type == "audio":
                result = self.download_audio(url)
            else:
                result = None
            
            if result:
                results.append(result)
                print(f"✓ Downloaded: {result.download_path}")
            else:
                print(f"✗ Failed to download: {url}")
        
        return results
    
    def export_history(self, filename: str = "download_history.json"):
        """Export download history to JSON file"""
        history_data = [asdict(item) for item in self.download_history]
        
        save_path = Path(self.config.output_dir) / filename
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, indent=2, ensure_ascii=False)
        
        print(f"History exported to: {save_path}")
        return str(save_path)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get download statistics"""
        total_downloads = len(self.download_history)
        
        by_type = {}
        by_platform = {}
        total_size = 0
        
        for item in self.download_history:
            # Count by type
            media_type = item.media_type
            by_type[media_type] = by_type.get(media_type, 0) + 1
            
            # Count by platform
            platform = item.platform
            by_platform[platform] = by_platform.get(platform, 0) + 1
            
            # Sum file sizes
            if item.file_size:
                total_size += item.file_size
        
        return {
            'total_downloads': total_downloads,
            'by_type': by_type,
            'by_platform': by_platform,
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2)
        }


class EducationalTools:
    """Educational utilities for learning about media processing"""
    
    @staticmethod
    def analyze_image(filepath: str) -> Dict[str, Any]:
        """Analyze image properties for educational purposes"""
        try:
            with Image.open(filepath) as img:
                return {
                    'format': img.format,
                    'mode': img.mode,
                    'size': img.size,
                    'width': img.width,
                    'height': img.height,
                    'aspect_ratio': round(img.width / img.height, 2) if img.height > 0 else 0,
                    'has_transparency': img.mode in ('RGBA', 'LA', 'P'),
                }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def analyze_audio(filepath: str) -> Dict[str, Any]:
        """Analyze audio properties for educational purposes"""
        try:
            if filepath.lower().endswith('.mp3'):
                audio = MP3(filepath)
                return {
                    'duration': audio.info.length,
                    'bitrate': audio.info.bitrate,
                    'sample_rate': audio.info.sample_rate,
                    'channels': audio.info.channels,
                }
            elif filepath.lower().endswith('.mp4'):
                audio = MP4(filepath)
                return {
                    'duration': audio.info.length,
                    'bitrate': audio.info.bitrate,
                    'sample_rate': audio.info.sample_rate,
                    'channels': audio.info.channels,
                }
        except Exception as e:
            return {'error': str(e)}
        
        return {'error': 'Unsupported format'}
    
    @staticmethod
    def generate_hash(filepath: str) -> str:
        """Generate SHA-256 hash of file for integrity verification"""
        sha256_hash = hashlib.sha256()
        
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        return sha256_hash.hexdigest()


def create_cli_interface():
    """Create command-line interface"""
    print("=" * 70)
    print("SOCIAL MEDIA DOWNLOADER - EDUCATIONAL EDITION")
    print("=" * 70)
    print("\n⚠️  IMPORTANT: This tool is for EDUCATIONAL PURPOSES ONLY!")
    print("Only download content you own or have permission to download.\n")
    
    downloader = MediaDownloader()
    edutools = EducationalTools()
    
    while True:
        print("\n" + "-" * 70)
        print("MENU:")
        print("1. Download Video")
        print("2. Download Image")
        print("3. Download Audio")
        print("4. Get Media Info (without downloading)")
        print("5. Batch Download")
        print("6. Analyze Downloaded File")
        print("7. View Statistics")
        print("8. Export History")
        print("9. Exit")
        print("-" * 70)
        
        choice = input("\nEnter your choice (1-9): ").strip()
        
        if choice == '1':
            url = input("Enter video URL: ").strip()
            title = input("Enter title (optional, press Enter to skip): ").strip() or None
            result = downloader.download_video(url, title)
            if result:
                print(f"\n✓ Downloaded successfully: {result.download_path}")
        
        elif choice == '2':
            url = input("Enter image URL: ").strip()
            title = input("Enter title (optional, press Enter to skip): ").strip() or None
            result = downloader.download_image(url, title)
            if result:
                print(f"\n✓ Downloaded successfully: {result.download_path}")
        
        elif choice == '3':
            url = input("Enter audio URL: ").strip()
            title = input("Enter title (optional, press Enter to skip): ").strip() or None
            result = downloader.download_audio(url, title)
            if result:
                print(f"\n✓ Downloaded successfully: {result.download_path}")
        
        elif choice == '4':
            url = input("Enter media URL: ").strip()
            info = downloader.get_media_info(url)
            if info:
                print("\n" + "=" * 50)
                print("MEDIA INFORMATION:")
                print("=" * 50)
                for key, value in info.items():
                    print(f"{key}: {value}")
            else:
                print("Could not retrieve media information.")
        
        elif choice == '5':
            print("\nEnter URLs (one per line, empty line to finish):")
            urls = []
            while True:
                url = input().strip()
                if not url:
                    break
                urls.append(url)
            
            media_type = input("Media type (video/image/audio/auto): ").strip() or "auto"
            results = downloader.download_batch(urls, media_type)
            print(f"\n✓ Successfully downloaded {len(results)} of {len(urls)} items")
        
        elif choice == '6':
            filepath = input("Enter file path to analyze: ").strip()
            if not os.path.exists(filepath):
                print("File not found!")
                continue
            
            print("\nChoose analysis type:")
            print("1. Image Analysis")
            print("2. Audio Analysis")
            print("3. Generate File Hash")
            
            analysis_choice = input("Enter choice (1-3): ").strip()
            
            if analysis_choice == '1':
                result = edutools.analyze_image(filepath)
                print("\nIMAGE ANALYSIS:")
                for key, value in result.items():
                    print(f"  {key}: {value}")
            
            elif analysis_choice == '2':
                result = edutools.analyze_audio(filepath)
                print("\nAUDIO ANALYSIS:")
                for key, value in result.items():
                    print(f"  {key}: {value}")
            
            elif analysis_choice == '3':
                file_hash = edutools.generate_hash(filepath)
                print(f"\nSHA-256 Hash: {file_hash}")
        
        elif choice == '7':
            stats = downloader.get_statistics()
            print("\n" + "=" * 50)
            print("DOWNLOAD STATISTICS:")
            print("=" * 50)
            print(f"Total Downloads: {stats['total_downloads']}")
            print(f"Total Size: {stats['total_size_mb']} MB")
            print("\nBy Type:")
            for media_type, count in stats['by_type'].items():
                print(f"  {media_type}: {count}")
            print("\nBy Platform:")
            for platform, count in stats['by_platform'].items():
                print(f"  {platform}: {count}")
        
        elif choice == '8':
            filename = input("Enter filename (default: download_history.json): ").strip() or "download_history.json"
            downloader.export_history(filename)
        
        elif choice == '9':
            print("\nThank you for using the Educational Social Media Downloader!")
            print("Remember: Always respect copyright and terms of service.")
            break
        
        else:
            print("Invalid choice. Please try again.")


def main():
    """Main entry point"""
    try:
        create_cli_interface()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user.")
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
