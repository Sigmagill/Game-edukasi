Project ini dibuat menggunakan bahasa pemrograman Python sebagai bagian dari pembelajaran/penugasan.
Tujuannya adalah untuk mengedukasi anak" tk sejak dini untuk semangat belajar.

__________________________________________________________
| -- Langkah-langkah Menjalankan Project --              |
|                                                        |
| git clone https://github.com/Sigmagill/Game-edukas.git |
|________________________________________________________|


   
# 🎮 Game Edukatif Anak TK - Petualangan Belajar

Project game edukatif interaktif untuk anak TK dengan Pygame dan PyCairo sebagai tugas Grafika Komputer.

## 🎯 Fitur Utama

- **Level Belajar Angka**: Puzzle drag & drop untuk mengurutkan angka 1-5
- **Level Belajar Huruf**: Menyusun kata sederhana (BOLA, KUCING, MAMA, dll)
- **UI Interaktif**: Button animasi, drag & drop smooth, efek hover
- **Sistem Reward**: Tracking progress dengan bintang
- **Animasi Canggih**: Menggunakan PyCairo untuk rendering grafis vektor

## 🛠️ Teknologi

- **Pygame**: Game engine dan event handling
- **PyCairo**: Rendering grafis vektor berkualitas tinggi
- **Python 3.7+**: Bahasa pemrograman

## 📦 Instalasi

### 1. Install Dependencies

```bash
pip install pygame
pip install pycairo
pip install numpy
```

**Catatan untuk Windows:**
- Jika PyCairo error, install wheel dari: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pycairo
- Download file `.whl` sesuai Python version Anda
- Install dengan: `pip install nama_file.whl`

### 2. Struktur Folder

Buat struktur folder seperti ini:

```
game-edukatif-tk/
│
├── main.py                 # File utama
├── game_engine.py          # Core engine
│
├── scenes/
│   ├── __init__.py
│   ├── menu.py            # Menu utama
│   ├── level_angka.py     # Level angka
│   └── level_huruf.py     # Level huruf
│
├── components/
│   ├── __init__.py
│   ├── button.py          # UI Button
│   └── draggable.py       # Drag & drop
│
└── README.md
```

### 3. Buat File `__init__.py`

Buat file kosong `__init__.py` di folder `scenes/` dan `components/`:

```bash
# Linux/Mac
touch scenes/__init__.py
touch components/__init__.py

# Windows
type nul > scenes\__init__.py
type nul > components\__init__.py
```

## 🚀 Cara Menjalankan

```bash
python main.py
```

## 🎮 Cara Bermain

### Level Angka
1. Tarik kotak angka dari bawah
2. Letakkan ke kotak target sesuai urutan (1, 2, 3, 4, 5)
3. Selesaikan 3 puzzle untuk mendapat bintang

### Level Huruf
1. Tarik kotak huruf dari bawah
2. Susun huruf membentuk kata yang benar
3. Selesaikan 3 kata untuk mendapat bintang

## 🎨 Fitur Grafika Komputer

### PyCairo Features:
- ✅ Gradient backgrounds
- ✅ Rounded rectangles dengan smooth edges
- ✅ Shadow effects
- ✅ Custom text rendering
- ✅ Alpha blending/transparency
- ✅ Transformasi (scale, rotate, translate)

### Animasi:
- ✅ Button hover dengan scale animation
- ✅ Drag & drop dengan rotation effect
- ✅ Pulsating celebration text
- ✅ Smooth particle background
- ✅ Easing functions untuk natural movement

## 📚 Penjelasan Kode

### 1. Game Engine (`game_engine.py`)
- Mengelola scene management
- Cairo surface untuk rendering
- Main game loop
- Event handling

### 2. Components
- **Button**: Tombol interaktif dengan animasi hover
- **Draggable**: Object yang bisa di-drag dengan snap detection

### 3. Scenes
- **MenuScene**: Menu utama dengan animated particles
- **LevelAngkaScene**: Puzzle mengurutkan angka
- **LevelHurufScene**: Puzzle menyusun kata

## 🔧 Pengembangan Lebih Lanjut

### Fitur yang Bisa Ditambahkan:

1. **Level Tambahan**:
   - Menghitung benda
   - Mengenali bentuk
   - Puzzle gambar

2. **Sound Effects**:
   ```python
   import pygame.mixer
   
   # Di dalam handle_event button
   click_sound = pygame.mixer.Sound("assets/sounds/click.wav")
   click_sound.play()
   ```

3. **Particle Effects**:
   - Confetti saat menang
   - Sparkle pada hover
   - Trail saat drag

4. **Difficulty Levels**:
   - Mudah: 3 angka/huruf
   - Sedang: 5 angka/huruf
   - Sulit: 7+ angka/huruf

5. **Leaderboard**:
   - Simpan high score
   - Timer untuk speedrun

## 📊 Konsep Grafika Komputer yang Diterapkan

### 1. **2D Transformations**
- Translation (x, y movement)
- Scaling (zoom in/out effect)
- Rotation (dragging effect)

### 2. **Color Theory**
- Gradient fills (linear gradient)
- Color interpolation
- Alpha blending untuk transparency

### 3. **Anti-aliasing**
- PyCairo secara default menggunakan anti-aliasing
- Hasil rendering lebih smooth dibanding Pygame biasa

### 4. **Bezier Curves**
- Rounded rectangles menggunakan arc/bezier
- Smooth corner transitions

### 5. **Coordinate Systems**
- World coordinates vs screen coordinates
- Transform matrices untuk animasi

## 🐛 Troubleshooting

### Error: `No module named 'cairo'`
**Solusi**: Install PyCairo dengan benar (lihat bagian Instalasi)

### Error: `ModuleNotFoundError: No module named 'scenes'`
**Solusi**: Pastikan file `__init__.py` ada di folder `scenes/` dan `components/`

### Game lag/slow
**Solusi**: 
- Kurangi jumlah particles di menu
- Turunkan FPS dari 60 ke 30
- Optimalkan rendering (gunakan dirty rect)

### Font tidak muncul
**Solusi**: Ganti font name di code:
```python
ctx.select_font_face("Arial", ...)  # Ganti "Arial" dengan font lain
```

## 📝 Lisensi

Project ini dibuat untuk tugas Grafika Komputer. Bebas digunakan untuk keperluan pendidikan.

## 👨‍💻 Pengembang

Dibuat dengan ❤️ untuk pembelajaran anak-anak Indonesia

## 🙏 Kontribusi

Silakan fork dan improve! Beberapa ide:
- Tambah level baru
- Improve animasi
- Tambah sound effects
- Buat tutorial mode

---

**Happy Coding! 🚀**
