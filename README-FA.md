
[<img src="https://img.shields.io/badge/Telegram-%40Me-orange">](https://t.me/SudoLite)

![img1](.github/images/demo.png)


## قابلیت‌ها
| قابلیت‌ها                                                    | پشتیبانی شده |
|---------------------------------------------------------------|:------------:|
| چند رشته‌ای (Multithreading)                                  |      ✅      |
| اتصال یک پروکسی به جلسه                                       |      ✅      |
| دریافت خودکار همه وظایف به جز وظایف تلگرام                     |      ✅      |
| ارتقاء خودکار سطح برای فارمینگ سریع‌تر                        |      ✅      |
| دریافت خودکار پاداش روزانه                                     |      ✅      |
| شروع و پایان خودکار فارمینگ                                     |      ✅      |
| دریافت خودکار پاداش ماه                                         |      ✅      |
| پشتیبانی از tdata / pyrogram .session / telethon .session      |      ✅      |

## [تنظیمات](https://github.com/SudoLite/MMProBumpBot/blob/main/.env-example)
| تنظیمات                      | توضیحات                                                                         |
|------------------------------|---------------------------------------------------------------------------------|
| **API_ID / API_HASH**        | داده‌های پلتفرم برای راه‌اندازی جلسه تلگرام (پیش‌فرض - اندروید)               |
| **AUTO_BUY_BOOST**           | آیا باید تقویت‌کننده برای فارمینگ بخرم _(True / False)_                         |
| **AUTO_CLAIM_TASKS**         | آیا باید وظایف را دریافت کنم _(True / False)_                                   |
| **AUTO_CLAIM_MOON_BOUNS**    | آیا باید پاداش ماه را دریافت کنم _(True / False)_                              |
| **SLEEP_BETWEEN_CLAIM**      | تأخیر تصادفی بین **دریافت ها** بر حسب ثانیه _(مثال [3600,5000])_                   |
| **TAPS_COUNT**               | تعداد تصادفی کلیک‌ها _(مثال [45000,99000])_                                    |
| **DEFAULT_BOOST**            | نام پیش‌فرض تقویت‌کننده برای خرید _(مثال x3)_                                   |
| **USE_PROXY_FROM_FILE**      | آیا باید از پروکسی فایل `bot/config/proxies.txt` استفاده کنم _(True / False)_ |

## نصب
می‌توانید [**مخزن**](https://github.com/SudoLite/MMProBumpBot) را با کلون کردن به سیستم خود دانلود کرده و وابستگی‌های لازم را نصب کنید:
```shell
~ >>> git clone https://github.com/SudoLite/MMProBumpBot.git
~ >>> cd MMProBumpBot

# اگر از جلسات Telethon استفاده می‌کنید، شاخه "converter" را کلون کنید
~ >>> git clone https://github.com/SudoLite/MMProBumpBot.git -b converter
~ >>> cd MMProBumpBot

#لینوکس
~/MMProBumpBot >>> python3 -m venv venv
~/MMProBumpBot >>> source venv/bin/activate
~/MMProBumpBot >>> pip3 install -r requirements.txt
~/MMProBumpBot >>> cp .env-example .env
~/MMProBumpBot >>> nano .env # در اینجا باید API_ID و API_HASH خود را مشخص کنید، بقیه به صورت پیش‌فرض گرفته می‌شوند
~/MMProBumpBot >>> python3 main.py

#ویندوز
~/MMProBumpBot >>> python -m venv venv
~/MMProBumpBot >>> venv\Scripts\activate
~/MMProBumpBot >>> pip install -r requirements.txt
~/MMProBumpBot >>> copy .env-example .env
~/MMProBumpBot >>> # API_ID و API_HASH خود را مشخص کنید، بقیه به صورت پیش‌فرض گرفته می‌شوند
~/MMProBumpBot >>> python main.py
```

همچنین، برای راه‌اندازی سریع، می‌توانید از آرگومان‌ها استفاده کنید، به عنوان مثال:
```shell
~/MMProBumpBot >>> python3 main.py --action (1/2)
# یا
~/MMProBumpBot >>> python3 main.py -a (1/2)

#1 - ایجاد جلسه
#2 - اجرای کلیکر
```
