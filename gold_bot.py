import yfinance as yf
import pandas_ta as ta
import time
import requests

# إعدادات التلجرام (المأخوذة من مشروعك السابق)
TOKEN = "8686248913:AAFzhrlUnswNuE_Kta3ZNutbYOfgt6HGd9U"
CHAT_ID = "1053985097"

def send_msg(text):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": text}, timeout=10)
    except Exception as e:
        print(f"Error sending telegram: {e}")

print("🚀 البوت انطلق على السيرفر الجديد المفتوح...")
send_msg("✅ البوت اشتغل رسمياً من السيرفر الجديد المفتوح!")

while True:
    try:
        # جلب بيانات الذهب (هنا ستعمل لأن السيرفر الجديد غير محجوب)
        df = yf.download(tickers="GC=F", period="2d", interval="5m", progress=False)
        
        if not df.empty:
            # تنظيف وتجهيز الأعمدة
            df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
            # حساب مؤشر RSI
            df['RSI'] = ta.rsi(df['Close'], length=14)
            
            last_price = float(df['Close'].iloc[-1])
            last_rsi = float(df['RSI'].iloc[-1])
            
            print(f"💰 السعر الحالي: {last_price:.2f} | RSI: {last_rsi:.2f}")

            # منطق إرسال التنبيهات
            if last_rsi < 30:
                send_msg(f"🔔 فرصة شراء (RSI تشبع بيعي)!\nالسعر: {last_price:.2f}\nRSI: {last_rsi:.2f}")
            elif last_rsi > 70:
                send_msg(f"🔔 فرصة بيع (RSI تشبع شرائي)!\nالسعر: {last_price:.2f}\nRSI: {last_rsi:.2f}")
        
        time.sleep(300) # فحص كل 5 دقائق
    except Exception as e:
        print(f"خطأ في التنفيذ: {e}")
        time.sleep(60)
      
