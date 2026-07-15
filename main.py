import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
from steam.client import SteamClient
from steam.enums import EResult

class SteamIdlerApp(App):
    def build(self):
        self.title = "Kendi Steam Idler Uygulamam"
        self.client = SteamClient()
        
        # Ana dikey hizalama
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Başlık
        layout.add_widget(Label(text="STEAM KART / SAAT KASICI", font_size=20, size_hint_y=None, height=40))
        
        # Kullanıcı Adı Girişi
        layout.add_widget(Label(text="Steam Kullanıcı Adı:", size_hint_y=None, height=20))
        self.username_input = TextInput(multiline=False, text="")
        layout.add_widget(self.username_input)
        
        # Şifre Girişi
        layout.add_widget(Label(text="Steam Şifresi:", size_hint_y=None, height=20))
        self.password_input = TextInput(multiline=False, password=True, text="")
        layout.add_widget(self.password_input)
        
        # Oyun ID Girişi
        layout.add_widget(Label(text="Oyun ID'leri (Virgülle ayırabilirsiniz. Örn: 730, 381210):", size_hint_y=None, height=20))
        self.games_input = TextInput(multiline=False, text="381210") # Varsayılan Dead by Daylight
        layout.add_widget(self.games_input)
        
        # Durum Bilgisi Ekranı
        self.status_label = Label(text="Durum: Bekleniyor...", size_hint_y=None, height=40)
        layout.add_widget(self.status_label)
        
        # Başlat Butonu
        self.start_btn = Button(text="BOTU BAŞLAT", background_color=(0, 0.7, 0, 1), size_hint_y=None, height=50)
        self.start_btn.bind(on_press=self.start_idler_thread)
        layout.add_widget(self.start_btn)
        
        return layout

    def update_status(self, text):
        # Arayüzü güvenli şekilde güncellemek için Clock kullanıyoruz
        Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', f"Durum: {text}"))

    def start_idler_thread(self, instance):
        # Steam bağlantısı arayüzü dondurmasın diye arka planda (Thread) çalıştırıyoruz
        self.update_status("Bağlanıyor...")
        threading.Thread(target=self.run_steam_bot, daemon=True).start()

    def run_steam_bot(self):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        
        # Oyun ID'lerini listeye çevir
        try:
            game_ids = [int(x.strip()) for x in self.games_input.text.split(",") if x.strip().isdigit()]
        except Exception:
            self.update_status("Hata: Geçersiz Oyun ID'leri!")
            return

        if not username or not password:
            self.update_status("Hata: Kullanıcı adı veya şifre boş!")
            return

        # Steam'e bağlanmayı dene
        result = self.client.login(username, password)
        
        if result == EResult.OK:
            self.update_status("Giriş Başarılı! Oyunlar başlatılıyor...")
            # Belirtilen oyunları oynamaya başla
            self.client.games_played(game_ids)
            self.update_status(f"Aktif! Şu an oynanıyor: {game_ids}")
            
            # Bağlantıyı canlı tutmak için döngü
            self.client.run_forever()
            
        elif result == EResult.TwoFactorCodeRequired:
            self.update_status("Hata: Steam Guard 2FA Kodu gerekiyor!")
            # İlerleyen aşamada buraya 2FA kodu için girdi ekranı ekleyebiliriz.
        else:
            self.update_status(f"Giriş Başarısız! Hata Kodu: {result}")

if __name__ == '__main__':
    SteamIdlerApp().run()
