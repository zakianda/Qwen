#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick Start Script - Social Media Downloader
تشغيل سريع للتطبيق مع أمثلة توضيحية
"""

from downloader import MediaDownloader, DownloadConfig, EducationalTools
import os


def demonstrate_features():
    """عرض مميزات التطبيق"""
    
    print("=" * 70)
    print("SOCIAL MEDIA DOWNLOADER - EDUCATIONAL EDITION")
    print("تطبيق تعليمي لتحميل الوسائط من منصات التواصل الاجتماعي")
    print("=" * 70)
    print()
    
    # إعداد التكوين
    config = DownloadConfig()
    config.output_dir = "downloads"
    
    # إنشاء المثيل
    downloader = MediaDownloader(config)
    edutools = EducationalTools()
    
    print("✓ تم تهيئة التطبيق بنجاح")
    print()
    
    # عرض المميزات
    print("📋 المميزات المتاحة:")
    print("-" * 50)
    print("1. تحميل الفيديوهات من منصات متعددة")
    print("2. تحميل الصور بجودة عالية")
    print("3. تحميل الملفات الصوتية")
    print("4. الحصول على معلومات الوسائط بدون تحميل")
    print("5. التحميل الجماعي (Batch Download)")
    print("6. تحليل الملفات المحملة")
    print("7. إحصائيات التحميلات")
    print("8. تصدير سجل التحميلات")
    print()
    
    # عرض المنصات المدعومة
    print("🌐 المنصات المدعومة:")
    print("-" * 50)
    for platform in config.supported_platforms:
        print(f"  • {platform.capitalize()}")
    print()
    
    # عرض هيكل المجلدات
    print("📁 هيكل المجلدات:")
    print("-" * 50)
    base_path = config.output_dir
    print(f"  {base_path}/")
    print("  ├── video/")
    print("  ├── image/")
    print("  ├── audio/")
    print("  ├── youtube/")
    print("  ├── vimeo/")
    print("  ├── tiktok/")
    print("  └── ...")
    print()
    
    # مثال على استخدام الكود كـ API
    print("💻 مثال على الاستخدام البرمجي:")
    print("-" * 50)
    print("""
from downloader import MediaDownloader, DownloadConfig

# إعداد التكوين
config = DownloadConfig()
config.output_dir = "my_downloads"

# إنشاء المثيل
downloader = MediaDownloader(config)

# تحميل فيديو
result = downloader.download_video("URL_HERE")

# تحميل صورة
result = downloader.download_image("URL_HERE")

# تحميل صوتي
result = downloader.download_audio("URL_HERE")

# الحصول على معلومات
info = downloader.get_media_info("URL_HERE")

# التحميل الجماعي
urls = ["url1", "url2", "url3"]
results = downloader.download_batch(urls)

# تصدير السجل
downloader.export_history("history.json")

# الإحصائيات
stats = downloader.get_statistics()
print(stats)
    """)
    
    # نصائح سريعة
    print("⭐ نصائح سريعة للحصول على أفضل جودة:")
    print("-" * 50)
    print("1. استخدم اتصال إنترنت مستقر وسريع")
    print("2. اختر الجودة المناسبة لاحتياجك")
    print("3. تحقق من مساحة التخزين قبل التحميل")
    print("4. استخدم صيغ عالية الجودة للفيديو (MP4, MKV)")
    print("5. للصوت، استخدم 320 kbps لأفضل جودة MP3")
    print("6. للصور، استخدم PNG للجودة الأعلى")
    print("7. احتفظ بنسخ احتياطية من الملفات المهمة")
    print("8. وثق جميع عمليات التحميل في السجل")
    print()
    
    # تحذير مهم
    print("⚠️  تحذير مهم:")
    print("-" * 50)
    print("هذا التطبيق للأغراض التعليمية فقط!")
    print("- حمل فقط المحتوى الذي تملكه")
    print("- أو المحتوى الذي لديك إذن بتحميله")
    print("- احترم حقوق النشر وشروط الاستخدام")
    print()
    
    print("=" * 70)
    print("للبدء، شغل الملف الرئيسي: python downloader.py")
    print("للمزيد من النصائح، اقرأ ملف: TIPS_AR.md")
    print("=" * 70)


if __name__ == "__main__":
    demonstrate_features()
