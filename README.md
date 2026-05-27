# 💿 SSPECTRA AUDIO LAB v1.0

<p align="center">
  <a href="#-sspectra-audio-lab-v10-en">English Edition</a> •
  <a href="#-sspectra-audio-lab-v10-ru">Русская версия</a>
</p>

---

# 💿 SSPECTRA AUDIO LAB v1.0 [EN]

> Developed & Secured by **PHANT044M // SSPECTRA MUSIC**

**SSPECTRA AUDIO LAB** is an integrated desktop studio environment (audio workstation companion) designed for sound designers, beatmakers, music producers, and loop creators. It provides comprehensive mass-editing of audio metadata, recursive file analysis, and intelligent library deconstruction with high cross-platform compatibility.

---

## ⚡ Core Systems

### 🏷️ Tag Studio (Metadata Forge)
Designed for bulk-editing metadata tags and embedding cover art (Artist, Album, Year, Genre, Composer, Title, Cover Art).

- **RIFF LIST INFO Dual-Tagging:** Solves the classic WAV metadata issue. The application simultaneously injects tags into a modern `id3` chunk (ID3v2.3 format for VLC, Telegram, mobile players) and a classic RIFF `LIST INFO` chunk (for Windows Explorer, FL Studio, Ableton Live, and other DAWs).
- **Stable FLAC & MP3 Sync:** Rebuilds Vorbis Comment blocks (FLAC) and ID3v2.3 tags (MP3) securely, preventing byte offsets or metadata corruption.
- **DPI-Aware Preview & Dropzone:** Supports Drag & Drop of cover art files. Transparent PNG images (RGBA/LA) are automatically converted onto a clean white JPEG background before being embedded into the audio payload.
- **Smart Mass Renaming Mask:** Rename hundreds of files simultaneously using templates (e.g., `808 - {n} [PHANT044M]`), with a toggle to automatically strip promo clutter, usernames (`@...`), and hashtags.
- **macOS Formats Support:** Full tagging compatibility for `.aif` and `.aiff` files.

### 📦 Deconstructor (Archive Sorter)
An intelligent sorting engine to reorganize messy sample packs, one-shots, and loops.

- **Hybrid Target Queue:** Scan loose directory folders and packaged `.zip` archives at the same time.
- **Deep Recursive Walk:** Traverses directory chains to any depth, applying rapid regular-expression categories (`808`, `Kick`, `Clap`, `Snare`, `Hi Hat`, `Open Hat`, `Percs` (with Rims, Bells, Shakers subfolders), `Vox`, `FX`, `Riser`, `Tag`, and `Loops & Melodies`).
- **MD5 Cryptographic Duplicate Filter:** Computes MD5 file hashes on the fly. If identical samples are present across different folders or archives (even under different names), the duplicates are automatically filtered out.
- **Move/Cut Action Mode:** Physically moves original assets instead of copying, followed by an automatic cleanup of leftover empty directories.
- **Content Inventory:** Generates a clean text ledger `[Pack_Name]_Inventory.txt` with statistics on exactly how many elements were sorted into each category.

---

## ⚙️ Unified Control Center (Settings)
- **Secure Bug Reporting:** A dedicated bug-report wizard securely packages a subject, text, and up to 10 screenshots (base64-encoded) and sends them to a serverless Google Apps Script proxy. It forwards the report to the developer's Gmail. Your credentials and email tokens remain 100% hidden on the server, ensuring client-side security.
- **Custom Output Paths:** Define a permanent Deconstructor save folder in the settings. If left blank, it defaults to the active script directory.
- **Automatic Folder Increment:** If the name is left blank, it defaults to `SOUND PACK`. When running subsequent deconstructions, the engine merges files into existing categories within the same directory instead of creating duplicate folders.
- **Auto-Update Agent:** Quietly queries the GitHub API on startup. If a newer tag is found, it prompts the user with a download window redirecting to the latest release page.

---

## 🚀 How to Use

### Working in Tag Studio:
1. Navigate to the **TAG STUDIO** tab.
2. Click **Browse Directory** or drag-and-drop an audio folder from Windows Explorer directly into the left listbox.
3. Select files in the list (use `Ctrl+A` or standard `Shift` / `Ctrl` click).
4. Fill in the metadata fields on the right panel (Artist, Album, Year, etc.).
5. Drag-and-drop a cover image over the **`[ DROP HERE ]`** box, or load it via **Load Image**.
6. Set up your renaming pattern (e.g., `808 - {n} [PHANT044M]`).
7. Click **SAVE METADATA**.

### Working in Deconstructor:
1. Navigate to the **DECONSTRUCTOR** tab.
2. In the **Output folder name** field, write the name of your new organized pack.
3. Click **+ Add Target** (select directories/ZIPs), or drag-and-drop folders and archives into the queue.
4. Toggle **Cut/Move Files** and **Skip Dupes** depending on your needs.
5. Click **INITIATE DECONSTRUCTION**.
6. Once processed, your sorted directory will automatically open along with the generated inventory log.

---

## 🛠️ Installation & Compilation

### Standalone Portable EXE (Recommended)
Download the precompiled `SSPECTRA AUDIO LAB.exe` directly from the [Releases](https://github.com/PHANT044M/SSPECTRA-AUDIO-LAB/releases) section. The program is fully portable—simply launch it on your Windows PC.

### Running from Source
Requires Python **3.11** or higher.

1. Clone the repository and install dependencies:
```bash
pip install -r requirements.txt
```
2. Launch the lab:
```bash
python "SSPECTRA AUDIO LAB v1.0.py"
```

### Compiling manually
To compile a single, zero-dependency executable with full Drag & Drop support, place your `icon.ico` in the directory and run:
```bash
pyinstaller --onefile --noconsole --collect-all tkinterdnd2 --add-data "icon.ico;." --icon=icon.ico "SSPECTRA AUDIO LAB v1.0.py"
```

---

## 🌐 Community & Networks

Join the **PHANTOM NETWORK** ecosystem, share layouts, and stay up to date:

* **Telegram:** [t.me/phant044m_network](https://t.me/spectracore)
* **Instagram:** [@phant044m](https://instagram.com/phant044m)

---

# 💿 SSPECTRA AUDIO LAB v1.0 [RU]

> Разработано и защищено: **PHANT044M // SSPECTRA MUSIC**

**SSPECTRA AUDIO LAB** — это интегрированная рабочая среда (звуковой комбайн) для саунд-дизайнеров, битмейкеров, музыкальных продюсеров и loop-мейкеров. Программа создана для профессионального массового управления метаданными аудиофайлов, рекурсивного анализа и интеллектуальной сортировки звуковых библиотек с высокой кросс-платформенной совместимостью.

---

## ⚡ Описание ключевых систем

### 🏷️ Tag Studio (Лаборатория метаданных)
Модуль предназначен для пакетного редактирования аудио-тегов и вшивания обложек (Artist, Album, Year, Genre, Composer, Title, Cover Art).

* **Решение конфликта WAV-контейнеров:** Реализован гибридный метод двойной записи тегов в WAV-файлы. Программа одновременно записывает данные в современный чанк `id3` (в формате ID3v2.3 для корректного отображения обложек и текстов в VLC, Telegram, смартфонах) и в классический системный чанк RIFF `LIST INFO` (для мгновенного отображения авторов и названий в Проводнике Windows, FL Studio, Ableton Live и других DAW).
* **Стабильная синхронизация FLAC и MP3:** Полностью пересобирает структуру Vorbis Comment во FLAC и ID3v2.3 в MP3 без риска смещения байтов или повреждения структуры аудиоданных.
* **Безопасная конвертация графики (PNG Alpha):** При импорте обложек программа автоматически выявляет изображения формата PNG с прозрачным альфа-каналом (RGBA/LA) и бесшовно переносит их на белую подложку JPG перед вшиванием в аудио. Это предотвращает падение библиотек и искажение графики.
* **Smart-маска переименования:** Позволяет переименовывать сотни файлов за раз по шаблонам (например, `808 - {n} [PHANT044M]`), вычищая при этом рекламный мусор, хэштеги и сторонние никнеймы из названий.
* **Поддержка macOS форматов:** Полная совместимость и поддержка тегирования файлов форматов `.aif` и `.aiff`.

### 📦 Deconstructor (Деконструктор и Сортировщик)
Интеллектуальный сортировщик сэмплов, ван-шотов и петель, способный наводить порядок в хаотичных папках и архивах.

* **Гибридное сканирование целей:** Вы можете добавлять в список на сортировку как обычные папки любой вложенности, так и упакованные `.zip` архивы одновременно.
* **Рекурсивный анализ и авто-категоризация:** Движок сканирует папки на любую глубину, анализирует имена файлов по регулярным выражениям и автоматически распределяет их по папкам (`808`, `Kick`, `Clap`, `Snare`, `Hi Hat`, `Open Hat`, `Percs` (с подкатегориями Rims, Bells, Shakers), `Vox`, `FX`, `Riser`, `Tag` и `Loops & Melodies`).
* **Криптографический фильтр дубликатов (MD5):** Программа на лету вычисляет MD5-хэши файлов. Если в разных архивах или папках лежат абсолютно одинаковые сэмплы (даже под разными именами), дубликаты будут пропущены.
* **Режим умного перемещения (Move/Cut):** При активации режима переноса программа физически перемещает оригиналы файлов (вместо копирования) и автоматически удаляет за собой пустые папки.
* **Инвентарный лист (Content Inventory):** По окончании работы автоматически генерирует текстовый отчет `[Имя_Пака]_Inventory.txt` со статистикой: сколько сэмплов каждой категории было успешно отсортировано в ваш новый пак.

---

## ⚙️ Единый центр управления (Настройки)
* **Защищенный шлюз баг-репортов:** В настройки интегрирована безопасная форма отправки багов и обратной связи. Данные (тема, текст и до 10 скриншотов) упаковываются в Base64 и передаются на зашифрованный серверный шлюз Google Apps Script, откуда мгновенно пересылаются на почту разработчика. Ваши личные данные, пароли от почты и API-ключи полностью скрыты на стороне сервера и отсутствуют в коде клиента.
* **Выбор папки сохранения:** Возможность зафиксировать дефолтную папку, куда Деконструктор всегда будет складывать отсортированные паки. Если путь не указан, сохранение происходит в папку с программой.
* **Автоинкремент паков:** Если пользователь не указал имя для нового пака, программа назовет его `SOUND PACK`. При повторной сортировке в ту же папку Деконструктор не будет создавать копии, а аккуратно сольет новые сэмплы в уже существующие категории.
* **Автоматические обновления:** При старте программа незаметно обращается к официальному GitHub API репозитория. Если версия на сервере новее текущей, пользователю будет предложено скачать обновление.

---

## 🚀 Инструкция по использованию

### Работа в Tag Studio:
1. Перейдите на вкладку **TAG STUDIO**.
2. Нажмите **Browse Directory** (Обзор папки) или просто перетащите папку с аудиофайлами из Проводника в левое окно списка.
3. Выберите файлы в списке (используйте `Ctrl+A` или русскую `Ctrl+Ф` для выделения всех, либо `Shift` / `Ctrl` для выборочного выделения).
4. В правой панели заполните нужные текстовые поля (Артист, Альбом, Год и т.д.).
5. Перетащите картинку обложки прямо на область превью **`[ DROP HERE ]`** или загрузите её вручную кнопкой **Load Image**.
6. При необходимости настройте маску переименования (например, `808 - {n} [PHANT044M]`).
7. Нажмите **SAVE METADATA** (Сохранить метаданные).

### Работа в Deconstructor:
1. Перейдите на вкладку **DECONSTRUCTOR**.
2. В поле **Output folder name** напишите желаемое имя для вашего нового пака (например, `My Premium Drumkit`).
3. Нажмите кнопку **+ Add Target** и выберите папки или `.zip` архивы, либо просто перетащите их мышкой в список сканирования.
4. Настройте флаги: **Cut/Move Files** (физическое перемещение файлов вместо копирования) и **Skip Dupes** (пропуск дубликатов по MD5).
5. Нажмите **INITIATE DECONSTRUCTION** (Начать деконструкцию).
6. По завершении процесса автоматически откроется папка с вашим готовым, рассортированным паком и текстовым инвентарным файлом.

---

## 🛠️ Установка, запуск и компиляция

### Портативный запуск (Рекомендуется)
Скачайте готовый скомпилированный файл `SSPECTRA AUDIO LAB.exe` в разделе [Releases](https://github.com/PHANT044M/SSPECTRA-AUDIO-LAB/releases) репозитория. Программа является полностью портативной — просто запустите её на вашем ПК с Windows без установки дополнительных библиотек.

### Запуск из исходного кода
Для запуска программы из исходников вам понадобится Python версии **3.11** или выше.

1. Склонируйте репозиторий и установите все необходимые зависимости:
```bash
pip install -r requirements.txt
```
2. Запустите лабораторный стенд:
```bash
python "SSPECTRA AUDIO LAB v1.0.py"
```

### Компиляция в автономный `.exe`
Если вы хотите скомпилировать собственный портативный исполняемый файл с кастомной иконкой и полной поддержкой Drag & Drop, установите PyInstaller:
```bash
pip install pyinstaller
```
Положите ваш файл иконки `icon.ico` в папку со скриптом и выполните команду сборки:
```bash
pyinstaller --onefile --noconsole --collect-all tkinterdnd2 --add-data "icon.ico;." --icon=icon.ico "SSPECTRA AUDIO LAB v1.0.py"
```
*Результат компиляции будет находиться в созданной папке `dist/`.*

---

## 🌐 Сообщество и Социальные сети

Присоединяйтесь к экосистеме **PHANTOM NETWORK**, делитесь пресетами, сообщайте о багах и следите за обновлениями ядра:

* **Telegram:** [t.me/phant044m_network](https://t.me/spectracore)
* **Instagram:** [@phant044m](https://instagram.com/phant044m)

---
```
