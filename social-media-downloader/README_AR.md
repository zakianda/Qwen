# Social Media Downloader - Educational Edition

## 📚 وصف التطبيق

هذا تطبيق تعليمي شامل لتحميل الوسائط من منصات التواصل الاجتماعي المختلفة. تم تصميمه لأغراض تعليمية فقط.

### ⚠️ تحذير مهم

**هذا التطبيق مخصص للأغراض التعليمية فقط!**
- استخدمه فقط للمحتوى الذي تملكه
- أو المحتوى الذي لديك إذن صريح بتحميله
- أو المحتوى العام (Public Domain)
- أو المحتوى المرخص برخص Creative Commons المناسبة

## 🎯 المميزات

### 1. دعم منصات متعددة
- YouTube
- Vimeo
- TikTok
- Instagram
- Twitter/X
- Facebook
- Pinterest
- Reddit
- Tumblr

### 2. أنواع الوسائط المدعومة
- 🎬 فيديوهات
- 🖼️ صور
- 🎵 ملفات صوتية
- 📄 مستندات

### 3. أدوات تعليمية
- تحليل خصائص الصور
- تحليل خصائص الصوت
- توليد Hash للتحقق من سلامة الملفات
- إحصائيات التحميل

## 🚀 التثبيت

### المتطلبات
- Python 3.8 أو أحدث
- pip

### خطوات التثبيت

```bash
# إنشاء بيئة افتراضية
python -m venv venv

# تفعيل البيئة الافتراضية
# على Windows:
venv\Scripts\activate
# على Linux/Mac:
source venv/bin/activate

# تثبيت المكتبات المطلوبة
pip install yt-dlp requests beautifulsoup4 lxml pillow mutagen
```

## 📖 الاستخدام

### التشغيل

```bash
python downloader.py
```

### القائمة الرئيسية

بعد تشغيل التطبيق، ستظهر قائمة تفاعلية:

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

### أمثلة على الاستخدام

#### 1. تحميل فيديو
```
Enter your choice (1-9): 1
Enter video URL: https://www.youtube.com/watch?v=example
Enter title (optional): My Educational Video
```

#### 2. تحميل صورة
```
Enter your choice (1-9): 2
Enter image URL: https://example.com/image.jpg
Enter title (optional): Educational Image
```

#### 3. تحميل ملف صوتي
```
Enter your choice (1-9): 3
Enter audio URL: https://example.com/audio.mp3
Enter title (optional): Lecture Audio
```

#### 4. الحصول على معلومات الوسائط
```
Enter your choice (1-9): 4
Enter media URL: https://www.youtube.com/watch?v=example
```

#### 5. التحميل الجماعي
```
Enter your choice (1-9): 5
Enter URLs (one per line, empty line to finish):
https://example.com/video1.mp4
https://example.com/video2.mp4
https://example.com/image.jpg

Media type (video/image/audio/auto): auto
```

#### 6. تحليل الملفات المحملة
```
Enter your choice (1-9): 6
Enter file path to analyze: downloads/video/my_video.mp4

Choose analysis type:
1. Image Analysis
2. Audio Analysis
3. Generate File Hash
```

## 📁 هيكل المجلدات

بعد التشغيل الأول، سيتم إنشاء الهيكل التالي:

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

## 🔧 البرمجة والتطوير

### استخدام الكود كـ Module

```python
from downloader import MediaDownloader, DownloadConfig, EducationalTools

# إعداد التكوين
config = DownloadConfig()
config.output_dir = "my_downloads"
config.max_file_size = 1024 * 1024 * 1024  # 1 GB

# إنشاء مثيل للتطبيق
downloader = MediaDownloader(config)

# تحميل فيديو
result = downloader.download_video("https://youtube.com/watch?v=example")
if result:
    print(f"Downloaded: {result.download_path}")

# تحميل صورة
result = downloader.download_image("https://example.com/image.jpg")

# تحميل صوتي
result = downloader.download_audio("https://youtube.com/watch?v=audio")

# الحصول على معلومات
info = downloader.get_media_info("https://youtube.com/watch?v=example")
print(info)

# التحميل الجماعي
urls = ["url1", "url2", "url3"]
results = downloader.download_batch(urls, media_type="video")

# تصدير السجل
downloader.export_history("my_history.json")

# الحصول على الإحصائيات
stats = downloader.get_statistics()
print(stats)

# أدوات تعليمية
edutools = EducationalTools()
image_info = edutools.analyze_image("path/to/image.jpg")
audio_info = edutools.analyze_audio("path/to/audio.mp3")
file_hash = edutools.generate_hash("path/to/file.mp4")
```

### فئات التطبيق الرئيسية

#### 1. `MediaType` (Enum)
تعداد لأنواع الوسائط المدعومة.

#### 2. `MediaInfo` (Dataclass)
تخزين معلومات الوسائط المحملة.

#### 3. `DownloadConfig`
إعدادات التكوين للتحميل.

#### 4. `MediaDownloader`
الفئة الرئيسية لإدارة عمليات التحميل.

#### 5. `EducationalTools`
أدوات مساعدة للأغراض التعليمية.

## 🎓 الأهداف التعليمية

### 1. تعلم شبكات الحاسوب
- فهم بروتوكول HTTP/HTTPS
- التعامل مع Headers
- إدارة Sessions
- التحقق من SSL/TLS

### 2. تعلم معالجة الملفات
- قراءة وكتابة الملفات الثنائية
- التحقق من صحة الملفات
- تحليل خصائص الوسائط
- توليد Hashes

### 3. تعلم البرمجة الكائنية
- تصميم الفئات
- الوراثة وتعدد الأشكال
- استخدام Dataclasses
- التعامل مع Exceptions

### 4. تعلم الأخلاقيات الرقمية
- احترام حقوق النشر
- شروط الاستخدام
- الخصوصية والأمان
- الاستخدام المسؤول

## 🔐 الأمان والخصوصية

### ميزات الأمان المضمنة
1. **التحقق من SSL**: التحقق من شهادات الأمان
2. **حد أقصى لحجم الملف**: منع تحميل ملفات ضخمة
3. **مهلة زمنية**: تجنب الانتظار اللانهائي
4. **تنظيف الأسماء**: منع أحرف غير آمنة في أسماء الملفات
5. **سجل التحميلات**: تتبع جميع العمليات

### أفضل الممارسات
- لا تخزن بيانات اعتماد المستخدمين
- استخدم اتصالات HTTPS المشفرة
- تحقق من محتوى الملفات المحملة
- احترم robots.txt للمواقع

## 📊 الإحصائيات والتقارير

يمكنك عرض إحصائيات مفصلة عن التحميلات:

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

## 🛠️ استكشاف الأخطاء

### المشاكل الشائعة وحلولها

#### 1. خطأ في الاتصال
```
Error: Connection timeout
```
**الحل**: تحقق من اتصال الإنترنت وزيادة مهلة الوقت في الإعدادات.

#### 2. ملف كبير جداً
```
File too large: X bytes
```
**الحل**: قم بزيادة `max_file_size` في الإعدادات أو اختر ملفاً أصغر.

#### 3. رابط غير صالح
```
Invalid URL
```
**الحل**: تأكد من صحة الرابط وأنه يبدأ بـ http:// أو https://

#### 4. منصة غير مدعومة
```
Detected platform: generic
```
**الحل**: بعض المنصات قد تتطلب أدوات خاصة. حاول التحميل المباشر.

## 📝 الترخيص

MIT License - للاستخدام التعليمي فقط

## 🤝 المساهمة

نرحب بالمساهمات التعليمية:
- تحسين الوثائق
- إضافة منصات جديدة
- تحسين الأدوات التعليمية
- إصلاح الأخطاء

## 📞 الدعم

للأسئلة التعليمية والاستفسارات حول الكود:
- راجع التعليقات في الكود
- ادرس الأمثلة المرفقة
- جرب التعديلات البسيطة لفهم الآلية

## ⭐ نصائح للحصول على أفضل جودة

انظر ملف `TIPS.md` للحصول على نصائح مفصلة.

---

**تذكر**: هذا التطبيق أداة تعليمية. استخدمه بمسؤولية واحترم حقوق الآخرين.
