import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# ---------- تنظیمات ----------
ADMIN_ID = id number telegram
API_TOKEN = "token telegram"
CARD_NUMBER = "1234-5678-9012-3456" شماره کارت

# زبان‌ها با پرچم
LANGUAGES = {
    'fa': '🇮🇷 فارسی',
    'en': '🇬🇧 English',
    'ar': '🇸🇦 العربية',
    'tr': '🇹🇷 Türkçe',
    'fr': '🇫🇷 Français',
    'uk': '🇺🇦 Українська'
}
DEFAULT_LANG = 'fa'

# دسته‌بندی‌ها و محصولات (فقط نمونه، بقیه رو خودت کامل کن)
CATEGORIES = {
    'fa': {
        '🎼 موسیقی': {
            'اسپاتیفای_Spotify': {'price': '10$', 'duration': 'ماهانه'},
            'اپل موزیک_Apple Music': {'price': '12$', 'duration': 'ماهانه'},
            'تیدال_Tidal': {'price': '15$', 'duration': 'ماهانه'},
            'دیزر_Deezer': {'price': '8$', 'duration': 'ماهانه'},
            'ساندکلاود_Sound Cloud': {'price': '9$', 'duration': 'ماهانه'}
        },
        '🎞 استریم': {
            'یوتوب پرمیوم_Youtube Premium': {'price': '15$', 'duration': 'ماهانه'},
            'نتفلیکس_Netflix': {'price': '20$', 'duration': 'ماهانه'},
            'دیزنی پلاس_Disney Plus': {'price': '18$', 'duration': 'ماهانه'},
            'اچ بی او مکس_HBO MAX': {'price': '22$', 'duration': 'ماهانه'},
            'هولو_Hulu': {'price': '17$', 'duration': 'ماهانه'},
            'دازن_Dazen': {'price': '25$', 'duration': 'سالانه'},
            'اسلینگ_Sling': {'price': '30$', 'duration': 'سالانه'},
            'پیورفلیکس_Purflix': {'price': '12$', 'duration': 'ماهانه'}
        },
        '💡 آموزش زبان': {
            'دولینگو_Duolingo': {'price': '10$', 'duration': 'سالانه'},
            'ماندلی_Mondly': {'price': '8$', 'duration': 'سالانه'},
            'رزتا استون_Rosetta Stone': {'price': '50$', 'duration': 'سالانه'},
            'ممرایز_Memrise': {'price': '9$', 'duration': 'سالانه'},
            'بوسو_Busu': {'price': '12$', 'duration': 'سالانه'},
            'السا اسپیک_Elsa Speak': {'price': '15$', 'duration': 'سالانه'}
        },
        '📚 آموزش': {
            'بلینکیست_Blinkist': {'price': '20$', 'duration': 'سالانه'},
            'کدکدمی_Codecademy': {'price': '30$', 'duration': 'سالانه'},
            'سولولرن_Sololearn': {'price': '15$', 'duration': 'سالانه'},
            'التیمیت گیتار_Ultimate Guitar': {'price': '10$', 'duration': 'سالانه'},
            'گرمرلی_Grammarly': {'price': '25$', 'duration': 'سالانه'},
            'کویل بات_Quillbot': {'price': '15$', 'duration': 'سالانه'},
            'یودمی_Udemy': {'price': '50$', 'duration': 'سالانه'},
            'اسکریبد_Scribd': {'price': '12$', 'duration': 'سالانه'},
            'ریدلی_Readly': {'price': '18$', 'duration': 'سالانه'},
            'اسکیل شیر_Skillshare': {'price': '20$', 'duration': 'سالانه'},
            'چِس_Chess': {'price': '10$', 'duration': 'سالانه'}
        },
        '🧘🏻‍♂️ مدیتیشن': {
            'کالم_Calm': {'price': '15$', 'duration': 'سالانه'},
            'هداسپیس_Head Space': {'price': '18$', 'duration': 'سالانه'}
        },
        '🖍 ادیت و گرافیک': {
            'کانوا_Canva': {'price': '12$', 'duration': 'سالانه'},
            'کپ کات_Capcut Pro': {'price': '10$', 'duration': 'ماهانه'},
            'پیکس‌آرت_Picsart': {'price': '8$', 'duration': 'ماهانه'},
            'کپشنر_Captions': {'price': '15$', 'duration': 'ماهانه'}
        },
        '💰 معامله (Trade)': {
            'تریدینگ ویو_Tradingview': {'price': '30$', 'duration': 'سالانه'},
            'وریفای حساب بایننس': {'price': '50$', 'duration': 'یکبار'},
            'وایز_Wise': {'price': '20$', 'duration': 'یکبار'},
            'پرفکت مانی_Perfect Money': {'price': '15$', 'duration': 'یکبار'},
            'فوپس بانک_FUPS Bank': {'price': '25$', 'duration': 'یکبار'},
            'پی پل_Paypal': {'price': '30$', 'duration': 'یکبار'}
        },
        '🗂 لایسنس (License)': {
            'کسپرسکی_Kaspersky': {'price': '20$', 'duration': 'سالانه'},
            'آفیس ۳۶۵_Office 365': {'price': '50$', 'duration': 'سالانه'},
            'ویندوز اورجینال_Windows': {'price': '100$', 'duration': 'یکبار'},
            'لایسنس نود 32': {'price': '15$', 'duration': 'سالانه'}
        },
        '📲 کاربردی': {
            'تلگرام پرمیوم_Telegram Premium': {'price': '5$', 'duration': 'ماهانه'},
            'لایف سل_Lifecell': {'price': '10$', 'duration': 'ماهانه'},
            'دیسکورد_Discord': {'price': '8$', 'duration': 'ماهانه'},
            'استیم_Steam': {'price': '20$', 'duration': 'یکبار'},
            'بیتدفندر_Bitdefender': {'price': '25$', 'duration': 'سالانه'},
            'ماز_Moz': {'price': '30$', 'duration': 'سالانه'},
            'گوگل وویس_Google Voice': {'price': '15$', 'duration': 'یکبار'},
            'چت جی پی تی_ChatGPT': {'price': '20$', 'duration': 'ماهانه'},
            'فانی تل_Funytel': {'price': '10$', 'duration': 'ماهانه'},
            'اپل ایدی': {'price': '5$', 'duration': 'یکبار'},
            'رجیستر موبایل': {'price': '10$', 'duration': 'یکبار'},
            'اکانت IPTV': {'price': '15$', 'duration': 'ماهانه'},
            'افزونه‌های نال شده وردپرس': {'price': '20$', 'duration': 'یکبار'},
            'قالب نال شده وردپرس': {'price': '15$', 'duration': 'یکبار'}
        }
    },
    'en': {
        '🎼 Music': {
            'Spotify': {'price': '10$', 'duration': 'Monthly'},
            'Apple Music': {'price': '12$', 'duration': 'Monthly'},
            'Tidal': {'price': '15$', 'duration': 'Monthly'},
            'Deezer': {'price': '8$', 'duration': 'Monthly'},
            'Sound Cloud': {'price': '9$', 'duration': 'Monthly'}
        },
        '🎞 Streaming': {
            'Youtube Premium': {'price': '15$', 'duration': 'Monthly'},
            'Netflix': {'price': '20$', 'duration': 'Monthly'},
            'Disney Plus': {'price': '18$', 'duration': 'Monthly'},
            'HBO MAX': {'price': '22$', 'duration': 'Monthly'},
            'Hulu': {'price': '17$', 'duration': 'Monthly'},
            'Dazen': {'price': '25$', 'duration': 'Yearly'},
            'Sling': {'price': '30$', 'duration': 'Yearly'},
            'Purflix': {'price': '12$', 'duration': 'Monthly'}
        },
        '💡 Language Learning': {
            'Duolingo': {'price': '10$', 'duration': 'Yearly'},
            'Mondly': {'price': '8$', 'duration': 'Yearly'},
            'Rosetta Stone': {'price': '50$', 'duration': 'Yearly'},
            'Memrise': {'price': '9$', 'duration': 'Yearly'},
            'Busuu': {'price': '12$', 'duration': 'Yearly'},
            'Elsa Speak': {'price': '15$', 'duration': 'Yearly'}
        },
        '📚 Education': {
            'Blinkist': {'price': '20$', 'duration': 'Yearly'},
            'Codecademy': {'price': '30$', 'duration': 'Yearly'},
            'Sololearn': {'price': '15$', 'duration': 'Yearly'},
            'Ultimate Guitar': {'price': '10$', 'duration': 'Yearly'},
            'Grammarly': {'price': '25$', 'duration': 'Yearly'},
            'Quillbot': {'price': '15$', 'duration': 'Yearly'},
            'Udemy': {'price': '50$', 'duration': 'Yearly'},
            'Scribd': {'price': '12$', 'duration': 'Yearly'},
            'Readly': {'price': '18$', 'duration': 'Yearly'},
            'Skillshare': {'price': '20$', 'duration': 'Yearly'},
            'Chess': {'price': '10$', 'duration': 'Yearly'}
        },
        '🧘🏻‍♂️ Meditation': {
            'Calm': {'price': '15$', 'duration': 'Yearly'},
            'Head Space': {'price': '18$', 'duration': 'Yearly'}
        },
        '🖍 Editing & Graphics': {
            'Canva': {'price': '12$', 'duration': 'Yearly'},
            'Capcut Pro': {'price': '10$', 'duration': 'Monthly'},
            'Picsart': {'price': '8$', 'duration': 'Monthly'},
            'Captions': {'price': '15$', 'duration': 'Monthly'}
        },
        '💰 Trading': {
            'Tradingview': {'price': '30$', 'duration': 'Yearly'},
            'Binance Verification': {'price': '50$', 'duration': 'One-time'},
            'Wise': {'price': '20$', 'duration': 'One-time'},
            'Perfect Money': {'price': '15$', 'duration': 'One-time'},
            'FUPS Bank': {'price': '25$', 'duration': 'One-time'},
            'Paypal': {'price': '30$', 'duration': 'One-time'}
        },
        '🗂 Licenses': {
            'Kaspersky': {'price': '20$', 'duration': 'Yearly'},
            'Office 365': {'price': '50$', 'duration': 'Yearly'},
            'Windows Original': {'price': '100$', 'duration': 'One-time'},
            'NOD32 License': {'price': '15$', 'duration': 'Yearly'}
        },
        '📲 Utilities': {
            'Telegram Premium': {'price': '5$', 'duration': 'Monthly'},
            'Lifecell': {'price': '10$', 'duration': 'Monthly'},
            'Discord': {'price': '8$', 'duration': 'Monthly'},
            'Steam': {'price': '20$', 'duration': 'One-time'},
            'Bitdefender': {'price': '25$', 'duration': 'Yearly'},
            'Moz': {'price': '30$', 'duration': 'Yearly'},
            'Google Voice': {'price': '15$', 'duration': 'One-time'},
            'ChatGPT': {'price': '20$', 'duration': 'Monthly'},
            'Funytel': {'price': '10$', 'duration': 'Monthly'},
            'Apple ID': {'price': '5$', 'duration': 'One-time'},
            'Mobile Registration': {'price': '10$', 'duration': 'One-time'},
            'IPTV Account': {'price': '15$', 'duration': 'Monthly'},
            'WordPress Nulled Plugins': {'price': '20$', 'duration': 'One-time'},
            'WordPress Nulled Themes': {'price': '15$', 'duration': 'One-time'}
        }
    },
    'ar': {
        '🎼 الموسيقى': {
            'سبوتيفاي_Spotify': {'price': '10$', 'duration': 'شهري'},
            'أبل ميوزك_Apple Music': {'price': '12$', 'duration': 'شهري'},
            'تايدل_Tidal': {'price': '15$', 'duration': 'شهري'},
            'ديزر_Deezer': {'price': '8$', 'duration': 'شهري'},
            'ساوند كلاود_Sound Cloud': {'price': '9$', 'duration': 'شهري'}
        },
        '🎞 البث': {
            'يوتيوب بريميوم_Youtube Premium': {'price': '15$', 'duration': 'شهري'},
            'نتفليكس_Netflix': {'price': '20$', 'duration': 'شهري'},
            'ديزني بلس_Disney Plus': {'price': '18$', 'duration': 'شهري'},
            'إتش بي أو ماكس_HBO MAX': {'price': '22$', 'duration': 'شهري'},
            'هولو_Hulu': {'price': '17$', 'duration': 'شهري'},
            'دازن_Dazen': {'price': '25$', 'duration': 'سنوي'},
            'سلينغ_Sling': {'price': '30$', 'duration': 'سنوي'},
            'بورفليكس_Purflix': {'price': '12$', 'duration': 'شهري'}
        },
        '💡 تعلم اللغة': {
            'دولينغو_Duolingo': {'price': '10$', 'duration': 'سنوي'},
            'موندلي_Mondly': {'price': '8$', 'duration': 'سنوي'},
            'روزيتا ستون_Rosetta Stone': {'price': '50$', 'duration': 'سنوي'},
            'ميمريز_Memrise': {'price': '9$', 'duration': 'سنوي'},
            'بوسو_Busuu': {'price': '12$', 'duration': 'سنوي'},
            'إلسا سبيك_Elsa Speak': {'price': '15$', 'duration': 'سنوي'}
        },
        '📚 التعليم': {
            'بلينكست_Blinkist': {'price': '20$', 'duration': 'سنوي'},
            'كودكاديمي_Codecademy': {'price': '30$', 'duration': 'سنوي'},
            'سولوليرن_Sololearn': {'price': '15$', 'duration': 'سنوي'},
            'ألتيميت غيتار_Ultimate Guitar': {'price': '10$', 'duration': 'سنوي'},
            'غرامرلي_Grammarly': {'price': '25$', 'duration': 'سنوي'},
            'كويل بوت_Quillbot': {'price': '15$', 'duration': 'سنوي'},
            'يوديمي_Udemy': {'price': '50$', 'duration': 'سنوي'},
            'سكريبد_Scribd': {'price': '12$', 'duration': 'سنوي'},
            'ريدلي_Readly': {'price': '18$', 'duration': 'سنوي'},
            'سكيل شير_Skillshare': {'price': '20$', 'duration': 'سنوي'},
            'شطرنج_Chess': {'price': '10$', 'duration': 'سنوي'}
        },
        '🧘🏻‍♂️ التأمل': {
            'كالم_Calm': {'price': '15$', 'duration': 'سنوي'},
            'هيد سبيس_Head Space': {'price': '18$', 'duration': 'سنوي'}
        },
        '🖍 التحرير والرسومات': {
            'كانفا_Canva': {'price': '12$', 'duration': 'سنوي'},
            'كاب كات_Capcut Pro': {'price': '10$', 'duration': 'شهري'},
            'بيكس آرت_Picsart': {'price': '8$', 'duration': 'شهري'},
            'كابشنز_Captions': {'price': '15$', 'duration': 'شهري'}
        },
        '💰 التداول': {
            'تريدينغ فيو_Tradingview': {'price': '30$', 'duration': 'سنوي'},
            'توثيق حساب بينانس': {'price': '50$', 'duration': 'مرة واحدة'},
            'وايز_Wise': {'price': '20$', 'duration': 'مرة واحدة'},
            'بيرفكت موني_Perfect Money': {'price': '15$', 'duration': 'مرة واحدة'},
            'فوبس بنك_FUPS Bank': {'price': '25$', 'duration': 'مرة واحدة'},
            'باي بال_Paypal': {'price': '30$', 'duration': 'مرة واحدة'}
        },
        '🗂 التراخيص': {
            'كاسبرسكي_Kaspersky': {'price': '20$', 'duration': 'سنوي'},
            'أوفيس 365_Office 365': {'price': '50$', 'duration': 'سنوي'},
            'ويندوز أصلي_Windows': {'price': '100$', 'duration': 'مرة واحدة'},
            'ترخيص نود 32': {'price': '15$', 'duration': 'سنوي'}
        },
        '📲 الأدوات': {
            'تلغرام بريميوم_Telegram Premium': {'price': '5$', 'duration': 'شهري'},
            'لايف سل_Lifecell': {'price': '10$', 'duration': 'شهري'},
            'ديسكورد_Discord': {'price': '8$', 'duration': 'شهري'},
            'ستيم_Steam': {'price': '20$', 'duration': 'مرة واحدة'},
            'بتدفندر_Bitdefender': {'price': '25$', 'duration': 'سنوي'},
            'ماز_Moz': {'price': '30$', 'duration': 'سنوي'},
            'غوغل فويس_Google Voice': {'price': '15$', 'duration': 'مرة واحدة'},
            'تشات جي بي تي_ChatGPT': {'price': '20$', 'duration': 'شهري'},
            'فونيتل_Funytel': {'price': '10$', 'duration': 'شهري'},
            'أبل آي دي': {'price': '5$', 'duration': 'مرة واحدة'},
            'تسجيل موبايل': {'price': '10$', 'duration': 'مرة واحدة'},
            'حساب IPTV': {'price': '15$', 'duration': 'شهري'},
            'إضافات ووردبريس معطلة': {'price': '20$', 'duration': 'مرة واحدة'},
            'قوالب ووردبريس معطلة': {'price': '15$', 'duration': 'مرة واحدة'}
        }
    },
    'tr': {
        '🎼 Müzik': {
            'Spotify': {'price': '10$', 'duration': 'Aylık'},
            'Apple Music': {'price': '12$', 'duration': 'Aylık'},
            'Tidal': {'price': '15$', 'duration': 'Aylık'},
            'Deezer': {'price': '8$', 'duration': 'Aylık'},
            'Sound Cloud': {'price': '9$', 'duration': 'Aylık'}
        },
        '🎞 Yayın': {
            'Youtube Premium': {'price': '15$', 'duration': 'Aylık'},
            'Netflix': {'price': '20$', 'duration': 'Aylık'},
            'Disney Plus': {'price': '18$', 'duration': 'Aylık'},
            'HBO MAX': {'price': '22$', 'duration': 'Aylık'},
            'Hulu': {'price': '17$', 'duration': 'Aylık'},
            'Dazen': {'price': '25$', 'duration': 'Yıllık'},
            'Sling': {'price': '30$', 'duration': 'Yıllık'},
            'Purflix': {'price': '12$', 'duration': 'Aylık'}
        },
        '💡 Dil Öğrenimi': {
            'Duolingo': {'price': '10$', 'duration': 'Yıllık'},
            'Mondly': {'price': '8$', 'duration': 'Yıllık'},
            'Rosetta Stone': {'price': '50$', 'duration': 'Yıllık'},
            'Memrise': {'price': '9$', 'duration': 'Yıllık'},
            'Busuu': {'price': '12$', 'duration': 'Yıllık'},
            'Elsa Speak': {'price': '15$', 'duration': 'Yıllık'}
        },
        '📚 Eğitim': {
            'Blinkist': {'price': '20$', 'duration': 'Yıllık'},
            'Codecademy': {'price': '30$', 'duration': 'Yıllık'},
            'Sololearn': {'price': '15$', 'duration': 'Yıllık'},
            'Ultimate Guitar': {'price': '10$', 'duration': 'Yıllık'},
            'Grammarly': {'price': '25$', 'duration': 'Yıllık'},
            'Quillbot': {'price': '15$', 'duration': 'Yıllık'},
            'Udemy': {'price': '50$', 'duration': 'Yıllık'},
            'Scribd': {'price': '12$', 'duration': 'Yıllık'},
            'Readly': {'price': '18$', 'duration': 'Yıllık'},
            'Skillshare': {'price': '20$', 'duration': 'Yıllık'},
            'Satranç_Chess': {'price': '10$', 'duration': 'Yıllık'}
        },
        '🧘🏻‍♂️ Meditasyon': {
            'Calm': {'price': '15$', 'duration': 'Yıllık'},
            'Head Space': {'price': '18$', 'duration': 'Yıllık'}
        },
        '🖍 Düzenleme ve Grafik': {
            'Canva': {'price': '12$', 'duration': 'Yıllık'},
            'Capcut Pro': {'price': '10$', 'duration': 'Aylık'},
            'Picsart': {'price': '8$', 'duration': 'Aylık'},
            'Captions': {'price': '15$', 'duration': 'Aylık'}
        },
        '💰 Ticaret': {
            'Tradingview': {'price': '30$', 'duration': 'Yıllık'},
            'Binance Doğrulama': {'price': '50$', 'duration': 'Tek Sefer'},
            'Wise': {'price': '20$', 'duration': 'Tek Sefer'},
            'Perfect Money': {'price': '15$', 'duration': 'Tek Sefer'},
            'FUPS Bank': {'price': '25$', 'duration': 'Tek Sefer'},
            'Paypal': {'price': '30$', 'duration': 'Tek Sefer'}
        },
        '🗂 Lisanslar': {
            'Kaspersky': {'price': '20$', 'duration': 'Yıllık'},
            'Office 365': {'price': '50$', 'duration': 'Yıllık'},
            'Orijinal Windows': {'price': '100$', 'duration': 'Tek Sefer'},
            'NOD32 Lisansı': {'price': '15$', 'duration': 'Yıllık'}
        },
        '📲 Yardımcı Araçlar': {
            'Telegram Premium': {'price': '5$', 'duration': 'Aylık'},
            'Lifecell': {'price': '10$', 'duration': 'Aylık'},
            'Discord': {'price': '8$', 'duration': 'Aylık'},
            'Steam': {'price': '20$', 'duration': 'Tek Sefer'},
            'Bitdefender': {'price': '25$', 'duration': 'Yıllık'},
            'Moz': {'price': '30$', 'duration': 'Yıllık'},
            'Google Voice': {'price': '15$', 'duration': 'Tek Sefer'},
            'ChatGPT': {'price': '20$', 'duration': 'Aylık'},
            'Funytel': {'price': '10$', 'duration': 'Aylık'},
            'Apple ID': {'price': '5$', 'duration': 'Tek Sefer'},
            'Mobil Kayıt': {'price': '10$', 'duration': 'Tek Sefer'},
            'IPTV Hesabı': {'price': '15$', 'duration': 'Aylık'},
            'WordPress Nulled Eklentiler': {'price': '20$', 'duration': 'Tek Sefer'},
            'WordPress Nulled Temalar': {'price': '15$', 'duration': 'Tek Sefer'}
        }
    },
    'fr': {
        '🎼 Musique': {
            'Spotify': {'price': '10$', 'duration': 'Mensuel'},
            'Apple Music': {'price': '12$', 'duration': 'Mensuel'},
            'Tidal': {'price': '15$', 'duration': 'Mensuel'},
            'Deezer': {'price': '8$', 'duration': 'Mensuel'},
            'Sound Cloud': {'price': '9$', 'duration': 'Mensuel'}
        },
        '🎞 Streaming': {
            'Youtube Premium': {'price': '15$', 'duration': 'Mensuel'},
            'Netflix': {'price': '20$', 'duration': 'Mensuel'},
            'Disney Plus': {'price': '18$', 'duration': 'Mensuel'},
            'HBO MAX': {'price': '22$', 'duration': 'Mensuel'},
            'Hulu': {'price': '17$', 'duration': 'Mensuel'},
            'Dazen': {'price': '25$', 'duration': 'Annuel'},
            'Sling': {'price': '30$', 'duration': 'Annuel'},
            'Purflix': {'price': '12$', 'duration': 'Mensuel'}
        },
        '💡 Apprentissage des langues': {
            'Duolingo': {'price': '10$', 'duration': 'Annuel'},
            'Mondly': {'price': '8$', 'duration': 'Annuel'},
            'Rosetta Stone': {'price': '50$', 'duration': 'Annuel'},
            'Memrise': {'price': '9$', 'duration': 'Annuel'},
            'Busuu': {'price': '12$', 'duration': 'Annuel'},
            'Elsa Speak': {'price': '15$', 'duration': 'Annuel'}
        },
        '📚 Éducation': {
            'Blinkist': {'price': '20$', 'duration': 'Annuel'},
            'Codecademy': {'price': '30$', 'duration': 'Annuel'},
            'Sololearn': {'price': '15$', 'duration': 'Annuel'},
            'Ultimate Guitar': {'price': '10$', 'duration': 'Annuel'},
            'Grammarly': {'price': '25$', 'duration': 'Annuel'},
            'Quillbot': {'price': '15$', 'duration': 'Annuel'},
            'Udemy': {'price': '50$', 'duration': 'Annuel'},
            'Scribd': {'price': '12$', 'duration': 'Annuel'},
            'Readly': {'price': '18$', 'duration': 'Annuel'},
            'Skillshare': {'price': '20$', 'duration': 'Annuel'},
            'Échecs_Chess': {'price': '10$', 'duration': 'Annuel'}
        },
        '🧘🏻‍♂️ Méditation': {
            'Calm': {'price': '15$', 'duration': 'Annuel'},
            'Head Space': {'price': '18$', 'duration': 'Annuel'}
        },
        '🖍 Édition et Graphisme': {
            'Canva': {'price': '12$', 'duration': 'Annuel'},
            'Capcut Pro': {'price': '10$', 'duration': 'Mensuel'},
            'Picsart': {'price': '8$', 'duration': 'Mensuel'},
            'Captions': {'price': '15$', 'duration': 'Mensuel'}
        },
        '💰 Trading': {
            'Tradingview': {'price': '30$', 'duration': 'Annuel'},
            'Vérification Binance': {'price': '50$', 'duration': 'Unique'},
            'Wise': {'price': '20$', 'duration': 'Unique'},
            'Perfect Money': {'price': '15$', 'duration': 'Unique'},
            'FUPS Bank': {'price': '25$', 'duration': 'Unique'},
            'Paypal': {'price': '30$', 'duration': 'Unique'}
        },
        '🗂 Licences': {
            'Kaspersky': {'price': '20$', 'duration': 'Annuel'},
            'Office 365': {'price': '50$', 'duration': 'Annuel'},
            'Windows Original': {'price': '100$', 'duration': 'Unique'},
            'Licence NOD32': {'price': '15$', 'duration': 'Annuel'}
        },
        '📲 Utilitaires': {
            'Telegram Premium': {'price': '5$', 'duration': 'Mensuel'},
            'Lifecell': {'price': '10$', 'duration': 'Mensuel'},
            'Discord': {'price': '8$', 'duration': 'Mensuel'},
            'Steam': {'price': '20$', 'duration': 'Unique'},
            'Bitdefender': {'price': '25$', 'duration': 'Annuel'},
            'Moz': {'price': '30$', 'duration': 'Annuel'},
            'Google Voice': {'price': '15$', 'duration': 'Unique'},
            'ChatGPT': {'price': '20$', 'duration': 'Mensuel'},
            'Funytel': {'price': '10$', 'duration': 'Mensuel'},
            'Apple ID': {'price': '5$', 'duration': 'Unique'},
            'Enregistrement Mobile': {'price': '10$', 'duration': 'Unique'},
            'Compte IPTV': {'price': '15$', 'duration': 'Mensuel'},
            'Plugins WordPress Nulled': {'price': '20$', 'duration': 'Unique'},
            'Thèmes WordPress Nulled': {'price': '15$', 'duration': 'Unique'}
        }
    },
    'uk': {
        '🎼 Музика': {
            'Spotify': {'price': '10$', 'duration': 'Щомісяця'},
            'Apple Music': {'price': '12$', 'duration': 'Щомісяця'},
            'Tidal': {'price': '15$', 'duration': 'Щомісяця'},
            'Deezer': {'price': '8$', 'duration': 'Щомісяця'},
            'Sound Cloud': {'price': '9$', 'duration': 'Щомісяця'}
        },
        '🎞 Стрімінг': {
            'Youtube Premium': {'price': '15$', 'duration': 'Щомісяця'},
            'Netflix': {'price': '20$', 'duration': 'Щомісяця'},
            'Disney Plus': {'price': '18$', 'duration': 'Щомісяця'},
            'HBO MAX': {'price': '22$', 'duration': 'Щомісяця'},
            'Hulu': {'price': '17$', 'duration': 'Щомісяця'},
            'Dazen': {'price': '25$', 'duration': 'Щорічно'},
            'Sling': {'price': '30$', 'duration': 'Щорічно'},
            'Purflix': {'price': '12$', 'duration': 'Щомісяця'}
        },
        '💡 Вивчення мов': {
            'Duolingo': {'price': '10$', 'duration': 'Щорічно'},
            'Mondly': {'price': '8$', 'duration': 'Щорічно'},
            'Rosetta Stone': {'price': '50$', 'duration': 'Щорічно'},
            'Memrise': {'price': '9$', 'duration': 'Щорічно'},
            'Busuu': {'price': '12$', 'duration': 'Щорічно'},
            'Elsa Speak': {'price': '15$', 'duration': 'Щорічно'}
        },
        '📚 Освіта': {
            'Blinkist': {'price': '20$', 'duration': 'Щорічно'},
            'Codecademy': {'price': '30$', 'duration': 'Щорічно'},
            'Sololearn': {'price': '15$', 'duration': 'Щорічно'},
            'Ultimate Guitar': {'price': '10$', 'duration': 'Щорічно'},
            'Grammarly': {'price': '25$', 'duration': 'Щорічно'},
            'Quillbot': {'price': '15$', 'duration': 'Щорічно'},
            'Udemy': {'price': '50$', 'duration': 'Щорічно'},
            'Scribd': {'price': '12$', 'duration': 'Щорічно'},
            'Readly': {'price': '18$', 'duration': 'Щورічно'},
            'Skillshare': {'price': '20$', 'duration': 'Щорічно'},
            'Шахи_Chess': {'price': '10$', 'duration': 'Щорічно'}
        },
        '🧘🏻‍♂️ Медитація': {
            'Calm': {'price': '15$', 'duration': 'Щорічно'},
            'Head Space': {'price': '18$', 'duration': 'Щорічно'}
        },
        '🖍 Редагування та графіка': {
            'Canva': {'price': '12$', 'duration': 'Щорічно'},
            'Capcut Pro': {'price': '10$', 'duration': 'Щомісяця'},
            'Picsart': {'price': '8$', 'duration': 'Щомісяця'},
            'Captions': {'price': '15$', 'duration': 'Щомісяця'}
        },
        '💰 Трейдинг': {
            'Tradingview': {'price': '30$', 'duration': 'Щорічно'},
            'Верифікація Binance': {'price': '50$', 'duration': 'Одноразово'},
            'Wise': {'price': '20$', 'duration': 'Одноразово'},
            'Perfect Money': {'price': '15$', 'duration': 'Одноразово'},
            'FUPS Bank': {'price': '25$', 'duration': 'Одноразово'},
            'Paypal': {'price': '30$', 'duration': 'Одноразово'}
        },
        '🗂 Ліцензії': {
            'Kaspersky': {'price': '20$', 'duration': 'Щорічно'},
            'Office 365': {'price': '50$', 'duration': 'Щорічно'},
            'Оригінальний Windows': {'price': '100$', 'duration': 'Одноразово'},
            'Ліцензія NOD32': {'price': '15$', 'duration': 'Щорічно'}
        },
        '📲 Утиліти': {
            'Telegram Premium': {'price': '5$', 'duration': 'Щомісяця'},
            'Lifecell': {'price': '10$', 'duration': 'Щомісяця'},
            'Discord': {'price': '8$', 'duration': 'Щомісяця'},
            'Steam': {'price': '20$', 'duration': 'Одноразово'},
            'Bitdefender': {'price': '25$', 'duration': 'Щорічно'},
            'Moz': {'price': '30$', 'duration': 'Щорічно'},
            'Google Voice': {'price': '15$', 'duration': 'Одноразово'},
            'ChatGPT': {'price': '20$', 'duration': 'Щомісяця'},
            'Funytel': {'price': '10$', 'duration': 'Щомісяця'},
            'Apple ID': {'price': '5$', 'duration': 'Одноразово'},
            'Реєстрація мобільного': {'price': '10$', 'duration': 'Одноразово'},
            'Обліковий запис IPTV': {'price': '15$', 'duration': 'Щомісяця'},
            'Нульовані плагіни WordPress': {'price': '20$', 'duration': 'Одноразово'},
            'Нульовані теми WordPress': {'price': '15$', 'duration': 'Одноразово'}
        }
    }
}

# ---------- راه‌اندازی ----------
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

# ---------- حالت‌ها ----------
class OrderState(StatesGroup):
    waiting_for_lang = State()
    waiting_for_category = State()
    waiting_for_service = State()
    waiting_for_email = State()
    waiting_for_payment = State()
    waiting_for_help = State()

# ---------- پیام‌ها ----------
MESSAGES = {
    'fa': {
        'start': 'سلام! لطفاً زبان خود را انتخاب کنید یا از راهنما استفاده کنید:',
        'lang_changed': 'زبان به {lang} تغییر کرد.',
        'choose_category': 'لطفاً دسته‌بندی مورد نظر را انتخاب کنید:',
        'choose_service': 'لطفاً سرویس مورد نظر را انتخاب کنید:',
        'service_details': 'سرویس: {service}\n💰 قیمت: {price}\n⏳ مدت: {duration}\nبرای ادامه، ایمیل یا یوزرنیم خود را وارد کنید:',
        'enter_email': 'لطفاً ایمیل یا یوزرنیم خود را وارد کنید:',
        'send_payment': 'لطفاً مبلغ {price} را به شماره کارت زیر واریز کنید و رسید را ارسال کنید:\n{CARD_NUMBER}\nاکانت شما طی 24 تا 48 ساعت تحویل داده خواهد شد.',
        'thank_you': 'سفارش شما ثبت شد. اکانت طی 24 تا 48 ساعت تحویل داده خواهد شد.',
        'invalid': 'ورودی نامعتبر است، لطفاً دوباره تلاش کنید.',
        'back_to_menu': 'بازگشت به منو',
        'help': 'از گرک بپرس! سوال خود را بنویسید:'
    },
    'en': {
        'start': 'Hello! Please choose your language or use the guide:',
        'lang_changed': 'Language changed to {lang}.',
        'choose_category': 'Please select a category:',
        'choose_service': 'Please select a service:',
        'service_details': 'Service: {service}\n💰 Price: {price}\n⏳ Duration: {duration}\nTo proceed, enter your email or username:',
        'enter_email': 'Please enter your email or username:',
        'send_payment': 'Please send {price} to the following card number and upload the receipt:\n{CARD_NUMBER}\nYour account will be delivered within 24-48 hours.',
        'thank_you': 'Your order has been received. The account will be delivered within 24-48 hours.',
        'invalid': 'Invalid input, please try again.',
        'back_to_menu': 'Back to Menu',
        'help': 'Ask Grok! Write your question:'
    },
    'ar': {
        'start': 'مرحبًا! يرجى اختيار لغتك أو استخدام الدليل:',
        'lang_changed': 'تم تغيير اللغة إلى {lang}.',
        'choose_category': 'يرجى اختيار الفئة:',
        'choose_service': 'يرجى اختيار الخدمة:',
        'service_details': 'الخدمة: {service}\n💰 السعر: {price}\n⏳ المدة: {duration}\nللمتابعة، أدخل بريدك الإلكتروني أو اسم المستخدم:',
        'enter_email': 'يرجى إدخال بريدك الإلكتروني أو اسم المستخدم:',
        'send_payment': 'يرجى إرسال {price} إلى رقم البطاقة التالي ورفع الإيصال:\n{CARD_NUMBER}\nسيتم تسليم حسابك خلال 24-48 ساعة.',
        'thank_you': 'تم استلام طلبك. سيتم تسليم الحساب خلال 24-48 ساعة.',
        'invalid': 'إدخال غير صالح، حاول مرة أخرى.',
        'back_to_menu': 'العودة إلى القائمة',
        'help': 'اسأل گروك! اكتب سؤالك:'
    },
    'tr': {
        'start': 'Merhaba! Lütfen dilinizi seçin veya rehberi kullanın:',
        'lang_changed': 'Dil {lang} olarak değiştirildi.',
        'choose_category': 'Lütfen bir kategori seçin:',
        'choose_service': 'Lütfen bir hizmet seçin:',
        'service_details': 'Hizmet: {service}\n💰 Fiyat: {price}\n⏳ Süre: {duration}\nDevam etmek için e-posta veya kullanıcı adınızı girin:',
        'enter_email': 'Lütfen e-posta adresinizi veya kullanıcı adınızı girin:',
        'send_payment': 'Lütfen {price} tutarını aşağıdaki kart numarasına gönderin ve makbuzu yükleyin:\n{CARD_NUMBER}\nHesabınız 24-48 saat içinde teslim edilecek.',
        'thank_you': 'Siparişiniz alındı. Hesap 24-48 saat içinde teslim edilecek.',
        'invalid': 'Geçersiz giriş, lütfen tekrar deneyin.',
        'back_to_menu': 'Menüye Geri Dön',
        'help': 'Grok’a sor! Sorunu yaz:'
    },
    'fr': {
        'start': 'Bonjour ! Veuillez choisir votre langue ou utiliser le guide :',
        'lang_changed': 'Langue changée en {lang}.',
        'choose_category': 'Veuillez sélectionner une catégorie :',
        'choose_service': 'Veuillez sélectionner un service :',
        'service_details': 'Service : {service}\n💰 Prix : {price}\n⏳ Durée : {duration}\nPour continuer, entrez votre email ou nom d’utilisateur :',
        'enter_email': 'Veuillez entrer votre email ou nom d’utilisateur :',
        'send_payment': 'Veuillez envoyer {price} au numéro de carte suivant et téléverser le reçu :\n{CARD_NUMBER}\nVotre compte sera livré sous 24 à 48 heures.',
        'thank_you': 'Votre commande a été reçue. Le compte sera livré sous 24 à 48 heures.',
        'invalid': 'Entrée invalide, veuillez réessayer.',
        'back_to_menu': 'Retour au menu',
        'help': 'Demandez à Grok ! Écrivez votre question :'
    },
    'uk': {
        'start': 'Привіт! Будь ласка, виберіть мову або скористайтеся гідом:',
        'lang_changed': 'Мову змінено на {lang}.',
        'choose_category': 'Будь ласка, виберіть категорію:',
        'choose_service': 'Будь ласка, виберіть послугу:',
        'service_details': 'Послуга: {service}\n💰 Ціна: {price}\n⏳ Тривалість: {duration}\nЩоб продовжити, введіть вашу електронну пошту або ім’я користувача:',
        'enter_email': 'Будь лاسка, введіть свою електронну пошту або ім’я користувача:',
        'send_payment': 'Будь лاسка, надішліть {price} на наступний номер картки та завантажте квитанцію:\n{CARD_NUMBER}\nВаш акаунт буде доставлено протягом 24-48 годин.',
        'thank_you': 'Ваше замовлення отримано. Акаунт буде доставлено протягом 24-48 годин.',
        'invalid': 'Невірне введення, спробуйте ще раз.',
        'back_to_menu': 'Повернутися до меню',
        'help': 'Запитайте у Grok! Напишіть своє запитання:'
    }
}

# ---------- کیبوردهای پویا ----------
def get_language_keyboard():
    builder = ReplyKeyboardBuilder()
    for code, name in LANGUAGES.items():
        builder.button(text=name)  # پرچم توی LANGUAGES هست
    builder.button(text="❓ راهنما" if DEFAULT_LANG == 'fa' else "❓ Guide")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def get_category_keyboard(lang):
    builder = ReplyKeyboardBuilder()
    for category in CATEGORIES.get(lang, {}).keys():
        builder.button(text=category)
    builder.button(text=f"⬅️ {MESSAGES[lang]['back_to_menu']}")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def get_service_keyboard(lang, category):
    builder = ReplyKeyboardBuilder()
    services = CATEGORIES.get(lang, {}).get(category, {})
    for service in services.keys():
        emoji = "🎵" if "موسیقی" in category or "Music" in category else "📺" if "استریم" in category or "Streaming" in category else "⭐️"
        builder.button(text=f"{emoji} {service.split('_')[0]}")  # فقط اسم اصلی بدون پسوند
    builder.button(text=f"⬅️ {MESSAGES[lang]['back_to_menu']}")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def get_back_keyboard(lang):
    builder = ReplyKeyboardBuilder()
    builder.button(text=f"⬅️ {MESSAGES[lang]['back_to_menu']}")
    return builder.as_markup(resize_keyboard=True)

# ---------- شبیه‌سازی Grok ----------
async def ask_grok(question: str, lang: str) -> str:
    if lang == 'fa':
        return f"سلام! من گرک هستم، ساخته‌شده توسط xAI. سوالت این بود: '{question}'. جواب ساده‌م اینه: بستگی داره! اگه توضیح بیشتر می‌خوای، بگو."
    else:
        return f"Hi! I'm Grok, created by xAI. Your question was: '{question}'. My simple answer: It depends! Let me know if you want more details."

# ---------- هندلرها ----------
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(OrderState.waiting_for_lang)
    await message.answer(MESSAGES[DEFAULT_LANG]['start'], reply_markup=get_language_keyboard())

@dp.message(OrderState.waiting_for_lang)
async def process_language_or_help(message: types.Message, state: FSMContext):
    if message.text in ["❓ راهنما", "❓ Guide"]:
        await state.set_state(OrderState.waiting_for_help)
        await message.answer(MESSAGES[DEFAULT_LANG]['help'])
        return
    selected_lang = next((code for code, name in LANGUAGES.items() if name == message.text), None)
    if not selected_lang:
        await message.answer(MESSAGES[DEFAULT_LANG]['invalid'])
        return
    await state.update_data(lang=selected_lang)
    await state.set_state(OrderState.waiting_for_category)
    await message.answer(
        MESSAGES[selected_lang]['lang_changed'].format(lang=LANGUAGES[selected_lang].split(' ')[1]),  # بدون پرچم
        reply_markup=types.ReplyKeyboardRemove()
    )
    await message.answer(MESSAGES[selected_lang]['choose_category'], reply_markup=get_category_keyboard(selected_lang))

@dp.message(OrderState.waiting_for_help)
async def process_help(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get('lang', DEFAULT_LANG)
    answer = await ask_grok(message.text, lang)
    await message.answer(answer)
    await message.answer(MESSAGES[lang]['start'], reply_markup=get_language_keyboard())
    await state.set_state(OrderState.waiting_for_lang)

@dp.message(OrderState.waiting_for_category)
async def process_category(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get('lang', DEFAULT_LANG)
    if message.text == f"⬅️ {MESSAGES[lang]['back_to_menu']}":
        await state.set_state(OrderState.waiting_for_lang)
        await message.answer(MESSAGES[lang]['start'], reply_markup=get_language_keyboard())
        return
    if message.text not in CATEGORIES.get(lang, {}):
        await message.answer(MESSAGES[lang]['invalid'])
        return
    await state.update_data(category=message.text)
    await state.set_state(OrderState.waiting_for_service)
    await message.answer(MESSAGES[lang]['choose_service'], reply_markup=get_service_keyboard(lang, message.text))

@dp.message(OrderState.waiting_for_service)
async def process_service(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get('lang', DEFAULT_LANG)
    category = data.get('category', '')
    if message.text == f"⬅️ {MESSAGES[lang]['back_to_menu']}":
        await state.set_state(OrderState.waiting_for_category)
        await message.answer(MESSAGES[lang]['choose_category'], reply_markup=get_category_keyboard(lang))
        return
    selected_service = None
    emoji = "🎵" if "موسیقی" in category or "Music" in category else "📺" if "استریم" in category or "Streaming" in category else "⭐️"
    for service in CATEGORIES[lang][category].keys():
        if message.text == f"{emoji} {service.split('_')[0]}":
            selected_service = service
            break
    if not selected_service:
        await message.answer(MESSAGES[lang]['invalid'])
        return
    price = CATEGORIES[lang][category][selected_service]['price']
    duration = CATEGORIES[lang][category][selected_service]['duration']
    await state.update_data(service=selected_service, price=price)
    await state.set_state(OrderState.waiting_for_email)
    await message.answer(
        MESSAGES[lang]['service_details'].format(service=selected_service.split('_')[0], price=price, duration=duration),
        reply_markup=get_back_keyboard(lang)
    )

@dp.message(OrderState.waiting_for_email)
async def process_email(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get('lang', DEFAULT_LANG)
    if message.text == f"⬅️ {MESSAGES[lang]['back_to_menu']}":
        await state.set_state(OrderState.waiting_for_service)
        await message.answer(MESSAGES[lang]['choose_service'], reply_markup=get_service_keyboard(lang, data['category']))
        return
    price = data.get('price', 'نامشخص')
    await state.update_data(email=message.text)
    await state.set_state(OrderState.waiting_for_payment)
    await message.answer(
        MESSAGES[lang]['send_payment'].format(price=price, CARD_NUMBER=CARD_NUMBER),
        reply_markup=get_back_keyboard(lang)
    )

@dp.message(OrderState.waiting_for_payment)
async def process_payment(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get('lang', DEFAULT_LANG)
    if message.text == f"⬅️ {MESSAGES[lang]['back_to_menu']}":
        await state.set_state(OrderState.waiting_for_email)
        await message.answer(MESSAGES[lang]['enter_email'], reply_markup=get_back_keyboard(lang))
        return
    category = data.get('category', 'نامشخص')
    service = data.get('service', 'نامشخص')
    email = data.get('email', 'نامشخص')
    price = data.get('price', 'نامشخص')
    user_id = message.from_user.id
    user_name = getattr(message.from_user, 'full_name', 'بدون نام')

    await message.answer(MESSAGES[lang]['thank_you'])
    try:
        await bot.send_message(
            ADMIN_ID,
            f"سفارش جدید:\nکاربر: {user_name} (ID: {user_id})\nدسته‌بندی: {category}\nسرویس: {service}\nقیمت: {price}\nایمیل: {email}"
        )
    except Exception as e:
        logging.error(f"Failed to send order to admin: {e}")
        await message.answer(MESSAGES[lang]['thank_you'] + " (مشکل در اطلاع به ادمین)")
    finally:
        await state.clear()
        await message.answer(MESSAGES[lang]['choose_category'], reply_markup=get_category_keyboard(lang))

# ---------- اجرا ----------
async def main():
    try:
        logging.info("Bot is starting...")
        await dp.start_polling(bot, skip_updates=True)
    except Exception as e:
        logging.error(f"Bot crashed: {e}")
        try:
            await bot.send_message(ADMIN_ID, f"❌ خطا در ربات: {str(e)}")
        except:
            pass

if __name__ == "__main__":
    asyncio.run(main())