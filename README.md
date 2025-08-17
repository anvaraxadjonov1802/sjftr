# 🎓 O'zbekcha Onlayn Ta'lim Platformasi

Bu loyiha — o‘zbek tilida yaratilgan zamonaviy va interaktiv onlayn ta’lim platformasidir. Platforma orqali foydalanuvchilar nazariy bilimlar, amaliy mashg‘ulotlar, testlar, video darslar va topshiriqlar orqali mustaqil o‘rganish imkoniyatiga ega bo‘ladilar.

## 🚀 Asosiy Funksiyalar

* 📚 **Nazariy bo‘lim** — Har bir dars maqola va kod misollari bilan.
* 💻 **Amaliy mashqlar** — VBA, Python, Excel va boshqa yo‘nalishlarda real topshiriqlar.
* 📹 **Video darslar** — YouTube yoki Google Drive orqali ulangan video kontentlar.
* 🧐 **Test moduli** — Har bir mavzuga mos avtomatlashtirilgan testlar.
* 📂 **Topshiriqlar** — Foydalanuvchi topshiriqni yuklab oladi, bajargan faylini yuklaydi.
* ✅ **Foydalanuvchi autentifikatsiyasi** — Ro'yxatdan o'tish, email orqali tasdiqlash, login/logout.
* ⚙️ **Admin panel** — To‘liq boshqaruv: foydalanuvchilar, darslar, videolar, testlar, topshiriqlar.
* 🌐 **Responsive dizayn** — Mobil qurilmalar uchun moslashtirilgan interfeys.

## 🛠 Texnologiyalar

* **Backend:** Django (Python)
* **Frontend:** HTML, CSS, Bootstrap (va JS imkoniyatlari)
* **Database:** PostgreSQL / SQLite
* **Storage:** Google Drive (video fayllar uchun)
* **Email xizmati:** Django email backend orqali OTP / ro'yxatdan o'tish
* **PDF generator:** WeasyPrint

## 🖼 Dizayn

* 💡 Professional UI/UX dizayn
* 📱 Popup login/signup holatlari
* ⚠️ Maxsus 404/500 xatolik sahifalari

## ⚙️ O‘rnatish (Local)

```bash
# 1. GitHub'dan klon qilish
git clone https://github.com/yourusername/talim-platformasi.git
cd talim-platformasi

# 2. Virtual muhit yaratish va aktivlashtirish
python -m venv venv
source venv/bin/activate  # Windows uchun: venv\Scripts\activate

# 3. Talab qilinadigan kutubxonalarni o‘rnatish
pip install -r requirements.txt

# 4. Migratsiyalarni bajarish
python manage.py migrate

# 5. Superuser yaratish
python manage.py createsuperuser

# 6. Serverni ishga tushurish
python manage.py runserver
```

## 📁 Fayl Tuzilishi

```
talim-platformasi/
│
├── accounts/           
├── main/            
├── media/             
├── sjftr/           
├── static/          
└── template/
```

## 🔒 Xavfsizlik

* OTP (email orqali) ro'yxatdan o'tish
* Parolni tiklash uchun 6 xonali kod
* Xavfsiz fayl yuklash va to‘lovsiz testlar

## 🧑‍💻 Muallif

**Ismingiz**
💼 [LinkedIn](https://linkedin.com/in/axadjonovanvar)
📧 Email: [axadjonov@gmail.com](mailto:axadjonov123@gmail.com)


