# Persian Reel Captions — مثال: ریل فارسی با کپشن کلمه‌ای

ریل عمودی ۹:۱۶ (۱۰۸۰×۱۹۲۰) با کپشن فارسی همگام با گفتار: کلمه‌ی فعال نارنجی
(`#D97757`)، بقیه‌ی کلمات سفید، داخل باکس تیره‌ی گرد، چیدمان RTL، فونت نمایشی Lalezar.

- فایل: `persian-reel-captions.html` — تک‌فایل (فونت‌ها از `assets/fonts/` لود می‌شوند).
- کپشن‌ها از جدول `WORDS` در فایل خوانده می‌شوند (متن + زمان شروع/پایان هر کلمه).
  در استفاده‌ی واقعی این جدول را با خروجی `faster-whisper` با تایم‌استمپ کلمه‌ای جایگزین کنید
  (رجوع به `scripts/transcribe.py`).
- قرارداد رندر: `seek(t)` تابع خالص زمان است؛ کلمه‌ی فعال با `scale(1.12)` پاپ می‌شود.

## تله‌های فارسی رعایت‌شده (از persian-reel)

- `letter-spacing` منفی روی متن فارسی تنظیم نشده (فاصله‌ی کلمات را می‌بندد).
- عدد فارسی «۰» در این مثال استفاده نشده؛ اگر لازم شد، رندر نهایی را چک کنید.
- زیرنویس با libass سوزانده نمی‌شود چون کپشن داخل HTML است — اگر خروجی ASS لازم بود،
  از `scripts/captions.py` استفاده کنید، نه `ffmpeg drawtext`.

## رندر — ✅ رندر شده و تأیید شده (۲۰۲۶-۱۱-۱۱)

رندر نمونه با `capture.mjs` + Chrome هدلس + ffmpeg روی همین ماشین انجام شد:
`persian-reel-captions.mp4` — ۸ ثانیه، ۱۰۸۰×۱۹۲۰، ۲۴ فریم، h264، QC: PASS (۰ فریم
سیاه، ۸ فریم متمایز). فریم‌ها دیده و تأیید شدند: عنوان «سپاریک» با فونت Lalezar،
کپشن فارسی در باکس تیره‌ی گرد با کلمه‌ی فعال نارنجی (`#D97757`)، حروف متصل و RTL
درست. فایل MP4 در همین پوشه است.

```bash
# از ریشه‌ی اسکیل:
cd motion-studio

# ۱) (اختیاری) اگر فایل صوتی نریشن دارید، تایم‌استمپ کلمه‌ای بگیرید و جدول WORDS را به‌روز کنید:
python scripts/transcribe.py --audio narration.mp3 --lang fa --word-timestamps

# ۲) کپچر فریم‌به‌فریم + اسمبل به MP4 (۲۴ فریم بر ثانیه، ۸ ثانیه = ۱۹۲ فریم)
# capture.mjs خودش فریم‌ها را می‌گیرد و با ffmpeg به MP4 تبدیل می‌کند.
MOTION_STUDIO_TMPDIR=./.frames-tmp node scripts/capture.mjs \
  --input examples/persian-reel-captions/persian-reel-captions.html \
  --output examples/persian-reel-captions/persian-reel-captions.mp4 \
  --fps 24 --duration 8 --width 1080 --height 1920

# ۳) (اختیاری) میکس با نریشن + موزیک و مستر ‎−۱۴ LUFS
ffmpeg -y -i examples/persian-reel-captions/persian-reel-captions.mp4 -i narration.mp3 \
  -c:v copy -c:a aac -shortest examples/persian-reel-captions/persian-reel-captions-with-audio.mp4
# برای مستر دقیق ‎−۱۴ LUFS از scripts/mix.py استفاده کنید.
```

نکته: `capture.mjs` باید پیش از شروع، `document.fonts.ready` را صبر کند تا فونت‌های
Lalezar و Vazirmatn کامل لود شوند.
