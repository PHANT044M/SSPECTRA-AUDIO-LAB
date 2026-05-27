import os
import re
import json
import io
import shutil
import zipfile
import hashlib
import threading
import struct
import base64
import urllib.request
import webbrowser
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image

try:
    import mutagen
    import mutagen.wave
    import mutagen.mp3
    import mutagen.flac
    import mutagen.aiff
    from mutagen.wave import WAVE
    from mutagen.mp3 import MP3
    from mutagen.flac import FLAC, Picture
    from mutagen.aiff import AIFF
    from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, TYER, TCON, TCOM, TDRC
    MUTAGEN_AVAILABLE = True
except ImportError:
    MUTAGEN_AVAILABLE = False

# Попытка инициализации Drag & Drop
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    HAS_DND = True
except ImportError:
    HAS_DND = False

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

CONFIG_FILE = "spectra_config.json"
APP_VERSION = "v1.0"  

LANGUAGES = {
    'en': {
        'title': f"SSPECTRA AUDIO LAB {APP_VERSION}",
        'header': "SSPECTRA AUDIO LAB",
        'settings_btn': "⚙ Settings",
        'processing_btn': "PROCESSING...",
        'home_tab': "HOME",
        'tag_tab': "TAG STUDIO",
        'decomp_tab': "DECONSTRUCTOR",
        'win_set_bug_btn': "🐛 Report a Bug",
        'bug_win_title': "Report a Bug / Spectra Feedback",
        'bug_win_subject': "Subject / Theme:",
        'bug_win_desc': "Detailed Description of the Bug:",
        'bug_win_attach': "Attach Screenshot (PNG/JPG)",
        'bug_win_submit': "SUBMIT BUG REPORT",
        'bug_win_sending': "SENDING REPORT...",
        'bug_win_success': "Bug report successfully transmitted! Thank you.",
        'bug_win_fail': "Failed to send report. Check internet connection.",
        'bug_win_limit': "Attached: {} / 10",
        'msg_update_title': "Update Available",
        'msg_update_avail': "A new update ({}) is available! Would you like to open the download page?",
        
        # Home UI Dashboard Cards
        'home_welcome': "WELCOME TO SPECTRA CORE",
        'home_subtitle': "AUDIO LAB // INTEGRATED METADATA & DECONSTRUCTION ENGINE",
        'home_guide_hdr': "   System Quick Start Guide",
        'home_guide_1': "● TAG STUDIO: Bulk-edit metadata and embed cover arts into WAV, MP3, FLAC, AIF, AIFF.",
        'home_guide_2': "● DECONSTRUCTOR: Recursively scan folders or unpack ZIPs, filter duplicate audio files using MD5 hashes, and auto-categorize sounds.",
        'home_links_hdr': "   External Networks",
        'home_link_tg': "● Join PHANT044M Telegram channel",
        'home_link_docs': "● Documentation & Audio Layout Manuals",
        'home_status_hdr': "   Engine Core Diagnostic",
        'home_status_mutagen': "● Mutagen Audio Library: ACTIVE",
        'home_status_mutagen_no': "● Mutagen Audio Library: OFFLINE",
        'home_status_dnd': "● Drag & Drop Engine: ACTIVE",
        'home_status_dnd_no': "● Drag & Drop Engine: OFFLINE (Run 'pip install tkinterdnd2')",
        
        # Tag Studio UI
        'tag_folder_lbl': "Target Folder Sector:",
        'tag_browse_btn': "Browse Directory",
        'tag_meta_hdr': " ID3 / Vorbis Metadata Inspector ",
        'tag_title': "Track Title (Manual Input):",
        'tag_artist': "Artist / Producer:",
        'tag_album': "Album / Kit Name:",
        'tag_year': "Release Year:",
        'tag_genre': "Genre / Style:",
        'tag_composer': "Composer Tag:",
        'tag_btn_author': "Set Artist Profile",
        'tag_btn_title': "Insert Filename as Title",
        'tag_cover_hdr': " Cover Art Laboratory ",
        'tag_cover_load': "Load Image",
        'tag_cover_del': "Delete Art",
        'tag_rename_hdr': " Smart Mass Renaming Mask ",
        'tag_rename_lbl': "Pattern (use {n} for number positioning):",
        'tag_clean_cb': "Auto-clean tags if mask is empty",
        'tag_execute_btn': "SAVE METADATA",
        'tag_wipe_btn': "TOTAL WIPE METADATA",
        'log_tag_ready': "Tag Studio active. Select target folder.",
        'log_tag_err_path': "[!] Error: Target directory does not exist.",
        'log_tag_start': "Initiating metadata injection thread...",
        'log_tag_renamed': "Renamed: {} -> {}",
        'log_tag_finish': "   TAG INJECTION COMPLETED!\n   Total assets customized: {}",
        'log_wipe_start': "Initiating total tag deletion stream...",
        'log_wiped': "Wiped tags from: {}",
        'log_wipe_finish': "   TOTAL WIPE COMPLETED! Clean files: {}",
        'log_lang_change': "Language switched to: English",
        'msg_success_title': "Success v1.0",
        'msg_success_body': "Operation complete!\nProcessed files: {}",
        
        # Deconstructor UI
        'decomp_header': "SSPECTRA CORE // DECONSTRUCTOR",
        'pack_label': "Output folder name:",
        'folder_frame': " Directories & archives for scanning",
        'current_folder': "Current folder",
        'add_target_btn': "+ Add Target",
        'add_folder_btn': "📁 Add Folder",
        'add_zip_btn': "📦 Add ZIP Archive",
        'remove_btn': "- Remove Selected",
        'clear_btn': "Clear All",
        'log_frame': " Data stream monitoring",
        'start_btn': "INITIATE DECONSTRUCTION",
        'move_cb': "Cut/Move Files",
        'dupe_cb': "Skip Dupes",
        'err_empty': "[!] Error: Scan paths list is empty.",
        'err_no_items': "[!] Error: No valid files or folders found to process.",
        'log_analysing': "Total targets queued for analysis: {}. Processing...",
        'log_unpacking': "Unpacking archive: {}",
        'log_scanning_folder': "[+] Scanning directory: {}",
        'log_success_hdr': "   DECONSTRUCTION COMPLETED SUCCESSFULLY!",
        'log_success_ext': "   Audio categorized & structured: {}",
        'log_success_trsh': "   Unsorted files: {}",
        'log_success_dupes': "   Duplicate files skipped: {}",
        'log_added': "Added target: {}",
        'log_removed': "Removed target: {}",
        'log_cleared': "All paths cleared.",
        
        # Settings Win UI 
        'win_set_title': "--- SPECTRA CORE SETTINGS ---",
        'win_set_lang': "Application Interface Language:",
        'win_set_prof_btn': "Add Artist Profile Preset",
        'win_set_dest_lbl': "Default Deconstructor Destination:",
        'win_set_dest_browse': "Browse",
        'win_set_save_btn': "SAVE CORE CONFIGURATION",
        'win_sub_title': "Artist Profile Configuration",
        'win_sub_art': "Default Artist Name:",
        'win_sub_alb': "Default Album / Kit Name:",
        'win_sub_yr': "Default Release Year:",
        'win_sub_gen': "Default Genre / Style:",
        'win_sub_comp': "Default Composer / Tag:",
        
        # Status Bar & Tooltips
        'status_ready': "● System Ready",
        'tip_move_cb': "CUT/MOVE: Moves original files to sorted folders instead of copying (cleans up empty folders).",
        'tip_dupe_cb': "SKIP DUPES: Computes MD5 file hashes to automatically ignore identical duplicates.",
        'tip_clean_cb': "AUTO-CLEAN: Strips promo clutter, usernames (@...) and hashtags from filenames if mask is empty.",
        'tip_tag_wipe': "TOTAL WIPE: Permanently removes all ID3/Vorbis tags and pictures from selected items.",
        'tip_tag_execute': "COMPILE: Initiates mass metadata injection, cover art rendering and mass renaming mask.",
        'tip_decomp_start': "DECONSTRUCT: Unpacks archives, scans folders, filters duplicate sounds and builds category hierarchy.",
        'tip_auto_title_hint': "Auto-uses the filename (excluding ext) as the title tag."
    },
    'ru': {
        'title': f"SSPECTRA AUDIO LAB {APP_VERSION}",
        'header': "SSPECTRA CORE // AUDIO LAB",
        'settings_btn': "⚙ Настройки",
        'processing_btn': "ОБРАБОТКА...",
        'home_tab': "HOME",
        'tag_tab': "TAG STUDIO",
        'decomp_tab': "DECONSTRUCTOR",
        'win_set_bug_btn': "🐛 Сообщить о баге",
        'bug_win_title': "Сообщить о баге / Обратная связь",
        'bug_win_subject': "Тема бага:",
        'bug_win_desc': "Подробное описание проблемы:",
        'bug_win_attach': "Прикрепить скриншот (PNG/JPG)",
        'bug_win_submit': "ОТПРАВИТЬ ОТЧЕТ",
        'bug_win_sending': "ОТПРАВКА ОТЧЕТА...",
        'bug_win_success': "Отчет успешно отправлен! Спасибо за помощь.",
        'bug_win_fail': "Не удалось отправить отчет. Проверьте интернет.",
        'bug_win_limit': "Прикреплено: {} из 10",
        'msg_update_title': "Доступно обновление",
        'msg_update_avail': "Доступна новая версия ({})! Хотите открыть страницу скачивания?",
        
        # Home UI Dashboard Cards
        'home_welcome': "ДОБРО ПОЖАЛОВАТЬ В SPECTRA CORE",
        'home_subtitle': "AUDIO LAB // ИНТЕГРИРОВАННЫЙ ДВИЖОК МЕТАДАННЫХ И СОРТИРОВКИ",
        'home_guide_hdr': "   Руководство быстрого старта",
        'home_guide_1': "● TAG STUDIO: Массовое редактирование тегов и внедрение обложек в WAV, MP3, FLAC, AIF и AIFF.",
        'home_guide_2': "● DECONSTRUCTOR: Рекурсивный поиск в папках и распаковка ZIP, отсев дубликатов по MD5 и авто-сортировка звуков.",
        'home_links_hdr': "   Внешние ресурсы",
        'home_link_tg': "● Присоединиться к Telegram-каналу PHANT044M",
        'home_link_docs': "● Документация и стандарты звуковых макетов",
        'home_status_hdr': "   Диагностика системных модулей",
        'home_status_mutagen': "● Звуковая библиотека Mutagen: АКТИВНА",
        'home_status_mutagen_no': "● Звуковая библиотека Mutagen: ОФФЛАЙН",
        'home_status_dnd': "● Движок Drag & Drop: АКТИВЕН",
        'home_status_dnd_no': "● Движок Drag & Drop: ОФФЛАЙН (Выполните 'pip install tkinterdnd2')",
        
        # Tag Studio UI
        'tag_folder_lbl': "Целевой сектор папки:",
        'tag_browse_btn': "Обзор папки",
        'tag_meta_hdr': " Инспектор метаданных ID3 / Vorbis ",
        'tag_title': "Название трека (Вручную):",
        'tag_artist': "Артист / Продюсер:",
        'tag_album': "Альбом / Название кита:",
        'tag_year': "Год релиза:",
        'tag_genre': "Жанр / Вайб:",
        'tag_composer': "Тег Композитора:",
        'tag_btn_author': "Установить артист профиль",
        'tag_btn_title': "Вставить имя файла как название",
        'tag_cover_hdr': " Лаборатория обложек пака ",
        'tag_cover_load': "Загрузить фото",
        'tag_cover_del': "Удалить фото",
        'tag_rename_hdr': " Умный конвейер имен (Маска) ",
        'tag_rename_lbl': "Шаблон (используй {n} для позиции цифры):",
        'tag_clean_cb': "Авто-очистка тегов если маска пустая",
        'tag_execute_btn': "СОХРАНИТЬ МЕТАДАННЫЕ",
        'tag_wipe_btn': "ПОЛНАЯ ОЧИСТКА МЕТАДАННЫХ",
        'log_tag_ready': "Студия Тегов готова. Выберите тему папки.",
        'log_tag_err_path': "[!] Ошибка: Указанная папка не существует.",
        'log_tag_start': "Запуск потока инжекции тегов в аудиофайлы...",
        'log_tag_renamed': "Переименовано: {} -> {}",
        'log_tag_finish': "   МАССОВЫЙ ТЕГИНГ ЗАВЕРШЕН!\n   Всего файлов модифицировано: {}",
        'log_wipe_start': "Запуск потока полного уничтожения метаданных...",
        'log_wiped': "Теги полностью стерты в: {}",
        'log_wipe_finish': "   ПОЛНАЯ ОЧИСТКА ЗАВЕРШЕНА! Чистых файлов: {}",
        'log_lang_change': "Язык переключен на: Русский",
        'msg_success_title': "Готово v1.0",
        'msg_success_body': "Операция успешно завершена!\nОбработано файлов: {}",
        
        # Deconstructor UI
        'decomp_header': "SSPECTRA CORE // ДЕКОНСТРУКТОР",
        'pack_label': "Название выходной папки:",
        'folder_frame': " Директории и архивы для сканирования",
        'current_folder': "Текущая папка",
        'add_target_btn': "+ Добавить цель",
        'add_folder_btn': "📁 Добавить папку",
        'add_zip_btn': "📦 Добавить ZIP-архив",
        'remove_btn': "- Удалить выбранное",
        'clear_btn': "Очистить список",
        'log_frame': " Мониторинг потока данных",
        'start_btn': "ИНИЦИИРОВАТЬ ДЕКОНСТРУКЦИЮ",
        'move_cb': "Перемещать файлы",
        'dupe_cb': "Без дубликатов",
        'err_empty': "[!] Ошибка: Список путей пуст.",
        'err_no_items': "[!] Ошибка: Не найдено подходящих папок или ZIP-архивов.",
        'log_analysing': "Всего целей поставлено в очередь: {}. Анализ...",
        'log_unpacking': "Распаковка архива: {}",
        'log_scanning_folder': "[+] Сканирование папки: {}",
        'log_success_hdr': "   ДЕКОНСТРУКЦИЯ ЗАВЕРШЕНА С УСПЕХОМ!",
        'log_success_ext': "   Успешно отсортировано аудио: {}",
        'log_success_trsh': "   Нераспознанных файлов: {}",
        'log_success_dupes': "   Пропущено файлов-дубликатов: {}",
        'log_added': "Добавлена цель: {}",
        'log_removed': "Удалена цель: {}",
        'log_cleared': "Список путей очищен.",
        
        # Settings Win UI
        'win_set_title': "--- НАСТРОЙКИ ЯДРА SPECTRA ---",
        'win_set_lang': "Язык интерфейса приложения:",
        'win_set_prof_btn': "Добавить профиль артиста",
        'win_set_dest_lbl': "Папка сохранения Деконструктора:",
        'win_set_dest_browse': "Обзор",
        'win_set_save_btn': "СОХРАНИТЬ КОНФИГУРАЦИЮ ЯДРА",
        'win_sub_title': "Конфигуратор профиля артиста",
        'win_sub_art': "Имя артиста по умолчанию:",
        'win_sub_alb': "Альбом / Кит по умолчанию:",
        'win_sub_yr': "Год релиза по умолчанию:",
        'win_sub_gen': "Жанр / Вайб по умолчанию:",
        'win_sub_comp': "Тег композитора / копирайт:",
        
        # Status Bar & Tooltips
        'status_ready': "● Система готова",
        'tip_move_cb': "ПЕРЕМЕЩЕНИЕ: Физически переносит файлы в отсортированные папки вместо копирования (очищая пустые папки).",
        'tip_dupe_cb': "БЕЗ ДУБЛИКАТОВ: Вычисляет MD5-хэши для автоматического исключения одинаковых файлов-копий.",
        'tip_clean_cb': "АВТО-ОЧИСТКА: Вырезает рекламный мусор, никнеймы (@...) и хэштеги из имен файлов, если маска пуста.",
        'tip_tag_wipe': "ПОЛНАЯ ОЧИСТКА: Навсегда стирает все метатеги ID3/Vorbis и обложки из выбранных аудиофайлов.",
        'tip_tag_execute': "ЗАПЕЧАТАТЬ: Запускает процесс инжекции метаданных, генерации обложек и маски переименования.",
        'tip_decomp_start': "ДЕКОНСТРУКЦИЯ: Распаковывает архивы, сканирует папки, фильтрует дубликаты и строит иерархию категорий.",
        'tip_auto_title_hint': "Автоматически вставляет имя файла без расширения в тег названия."
    }
}

CATEGORIES = {
    '808': ['808', 'bass', 'sub', '808s', 'бас'],
    'CLAP': ['clap', 'claps', 'snclap', 'snclaps', 'клэп'],
    'SNARE': ['snare', 'snares', 'снейр'],
    'KICK': ['kick', 'kicks', 'кик', 'бочка'],
    'OPEN HAT': ['openhat', 'oh', 'open_hat', 'ophat'],
    'HI HAT': ['hihat', 'hh', 'hat', 'хэт'],
    'VOX': ['vox', 'vocal', 'vocals', 'chant', 'chants', 'вокс', 'вокал'],
    'TAG': ['tag', 'tags'], 
    'RISER': ['riser', 'risers'],
    'FX': ['fx', 'foley', 'glitch', 'ambient', 'rise', 'drop', 'hit', 'эффект']
}

def resize_to_square(pil_img, size=110):
    w, h = pil_img.size
    min_side = min(w, h)
    left = int((w - min_side) / 2)
    top = int((h - min_side) / 2)
    right = int(left + min_side)
    bottom = int(top + min_side)
    
    img_cropped = pil_img.crop((left, top, right, bottom))
    return img_cropped.resize((size, size), Image.Resampling.LANCZOS)

def convert_to_jpeg_bytes(pil_img, size=800):
    pil_square = resize_to_square(pil_img, size)
    if pil_square.mode in ('RGBA', 'LA') or (pil_square.mode == 'P' and 'transparency' in pil_square.info):
        background = Image.new("RGB", pil_square.size, (255, 255, 255))
        alpha = pil_square.split()[3] if pil_square.mode == 'RGBA' else pil_square.convert('RGBA').split()[3]
        background.paste(pil_square, mask=alpha)
        pil_square = background
    elif pil_square.mode != 'RGB':
        pil_square = pil_square.convert('RGB')
        
    img_byte_arr = io.BytesIO()
    pil_square.save(img_byte_arr, format='JPEG', quality=96, subsampling=0)
    return img_byte_arr.getvalue()

def write_wav_riff_info_tags(file_path, tags_dict):
    try:
        with open(file_path, 'rb') as f:
            header = f.read(12)
            if len(header) < 12 or header[:4] != b'RIFF' or header[8:] != b'WAVE':
                return
            
            chunks = []
            while True:
                chunk_id = f.read(4)
                if len(chunk_id) < 4:
                    break
                size_bytes = f.read(4)
                if len(size_bytes) < 4:
                    break
                size = struct.unpack('<I', size_bytes)[0]
                
                read_size = size + (size % 2)
                chunk_data = f.read(read_size)
                
                chunks.append({
                    'id': chunk_id,
                    'size': size,
                    'data': chunk_data[:size]
                })
        
        info_data = b'INFO'
        has_tags = False
        for tag, val in tags_dict.items():
            if not val:
                continue
            has_tags = True
            val_bytes = val.encode('utf-8') + b'\x00'
            val_len = len(val_bytes)
            info_data += tag + struct.pack('<I', val_len) + val_bytes
            if val_len % 2 != 0:
                info_data += b'\x00'
                
        fmt_chunks = []
        data_chunks = []
        id3_chunks = []
        other_chunks = []
        
        for c in chunks:
            if c['id'] == b'fmt ':
                fmt_chunks.append(c)
            elif c['id'] == b'data':
                data_chunks.append(c)
            elif c['id'] in (b'id3 ', b'ID3 '):
                id3_chunks.append(c)
            elif c['id'] == b'LIST' and len(c['data']) >= 4 and c['data'][:4] == b'INFO':
                continue
            else:
                other_chunks.append(c)
                
        new_chunks = fmt_chunks + other_chunks + data_chunks
        if has_tags:
            new_chunks.append({
                'id': b'LIST',
                'size': len(info_data),
                'data': info_data
            })
        new_chunks.extend(id3_chunks)
        
        total_riff_size = 4
        for c in new_chunks:
            total_riff_size += 8 + c['size'] + (c['size'] % 2)
            
        with open(file_path, 'wb') as f:
            f.write(b'RIFF')
            f.write(struct.pack('<I', total_riff_size))
            f.write(b'WAVE')
            for c in new_chunks:
                f.write(c['id'])
                f.write(struct.pack('<I', c['size']))
                f.write(c['data'])
                if c['size'] % 2 != 0:
                    f.write(b'\x00')
    except Exception:
        pass

class SplashWindow(ctk.CTkToplevel):
    """Класс заставки (Splash Screen) без рамок, открывающийся строго по центру."""
    def __init__(self, parent):
        super().__init__(parent)
        self.overrideredirect(True)
        self.configure(fg_color="#0a0a0a")
        
        self.geometry("500x320")
        self.update_idletasks()
        self.tk.eval(f'tk::PlaceWindow {self._w} center')
        
        self.logo_lbl = ctk.CTkLabel(
            self, 
            text="SSPECTRA\nAUDIO LAB", 
            font=("Segoe UI", 32, "bold"), 
            text_color="#bb86fc"
        )
        self.logo_lbl.pack(expand=True, pady=(40, 0))
        
        self.status_lbl = ctk.CTkLabel(
            self, 
            text="INITIALIZING SYSTEM MATRIX...", 
            font=("Consolas", 10), 
            text_color="#888888"
        )
        self.status_lbl.pack(pady=5)
        
        self.progress = ctk.CTkProgressBar(
            self, 
            width=400, 
            fg_color="#161616", 
            progress_color="#00ff66", 
            height=4
        )
        self.progress.pack(pady=(0, 40))
        self.progress.set(0)
        
        self.load_step(0.0)
        
    def load_step(self, val):
        if val <= 1.0:
            self.progress.set(val)
            if val < 0.3:
                self.status_lbl.configure(text="LOADING INJECTOR CORES...")
            elif val < 0.6:
                self.status_lbl.configure(text="PREPARING DECONSTRUCTION MATRICES...")
            elif val < 0.9:
                self.status_lbl.configure(text="ESTABLISHING DND CHANNELS...")
            else:
                self.status_lbl.configure(text="SYSTEM DIAGNOSTIC: READY")
                
            self.update()
            self.after(20, lambda: self.load_step(val + 0.015))
        else:
            self.destroy()


class SpectraAudioLabApp:
    def __init__(self, root):
        self.root = root
        self.current_lang = 'en'
        self.is_processing = False
        
        # Параметры Tag Studio
        self.staged_cover_bytes = None  
        self.loaded_file_cover_bytes = None  
        self.current_cover_image = None  
        self.cover_action = "keep"  
        
        self.def_artist = "PHANT044M"
        self.def_album = ""
        self.def_year = ""
        self.def_genre = ""
        self.def_composer = "PHANT044M // ANTIWORLD"
        self.def_auto_title = True  
        
        # Параметры Deconstructor
        self.scan_paths = [os.getcwd()]
        self.dest_dir = ""
        
        self.root.geometry("1100x780")
        self.root.minsize(1100, 760)
        self.root.configure(fg_color="#0a0a0a")
        
        self.create_layouts()
        self.load_config()
        self.update_ui_text()
        
        # Автоматическая проверка обновлений при старте
        self.check_for_updates()
        
        # Привязка всплывающих подсказок (Способ Б)
        self.register_hover_hints()

        if HAS_DND:
            try:
                self.root.drop_target_register(DND_FILES)
                
                self.tag_file_listbox.drop_target_register(DND_FILES)
                self.tag_file_listbox.dnd_bind('<<Drop>>', self.on_drop_tag_files)
                
                self.paths_listbox.drop_target_register(DND_FILES)
                self.paths_listbox.dnd_bind('<<Drop>>', self.on_drop_sorter_paths)
                
                self.cover_preview_box.drop_target_register(DND_FILES)
                self.cover_preview_box.dnd_bind('<<DragEnter>>', self.on_dnd_enter)
                self.cover_preview_box.dnd_bind('<<DragLeave>>', self.on_dnd_leave)
                self.cover_preview_box.dnd_bind('<<Drop>>', self.on_drop_cover)
            except:
                pass

    def on_dnd_enter(self, event):
        self.cover_border_frame.configure(border_color="#00ff66")

    def on_dnd_leave(self, event):
        self.cover_border_frame.configure(border_color="#bb86fc")

    def center_window(self, win, width, height):
        win.update_idletasks()
        parent_x = self.root.winfo_x()
        parent_y = self.root.winfo_y()
        parent_w = self.root.winfo_width()
        parent_h = self.root.winfo_height()
        
        x = parent_x + (parent_w - width) // 2
        y = parent_y + (parent_h - height) // 2
        win.geometry(f"{width}x{height}+{x}+{y}")

    def check_for_updates(self):
        """Запуск фоновой проверки обновлений через GitHub API"""
        t = threading.Thread(target=self._perform_update_check)
        t.daemon = True
        t.start()
        
    def _perform_update_check(self):
        try:
            import urllib.request
            import json
            
            # Укажите здесь путь к вашему будущему репозиторию на GitHub:
            github_repo = "PHANT044M/SSPECTRA-AUDIO-LAB"
            url = f"https://api.github.com/repos/{github_repo}/releases/latest"
            
            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'Spectra-Audio-Lab-Updater'}
            )
            
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode('utf-8'))
                latest_version = data.get("tag_name", APP_VERSION)
                release_url = data.get("html_url", "")
                
                # Если версия на сервере отличается от текущей константы APP_VERSION
                if latest_version != APP_VERSION:
                    self.root.after(0, lambda: self.show_update_notification(latest_version, release_url))
        except Exception:
            pass

    def show_update_notification(self, latest_version, release_url):
        lang = LANGUAGES[self.current_lang]
        msg = lang['msg_update_avail'].format(latest_version)
        if messagebox.askyesno(lang['msg_update_title'], msg):
            webbrowser.open_new_tab(release_url)
        
    def bind_select_all(self, widget):
        """Мультиязычный бинд для Ctrl+A (без падений из-за русских литер)"""
        def select_all(event):
            # 65 — это физический код клавиши 'A'/'Ф' на Windows, Cyrillic_ef — имя в X11
            if event.keycode == 65 or event.keysym.lower() in ('a', 'cyrillic_ef'):
                widget.select_set(0, tk.END)
                widget.event_generate("<<ListboxSelect>>")
                return "break"
        widget.bind("<Control-Key>", select_all)

    def create_layouts(self):
        top_header_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        top_header_frame.pack(fill="x", padx=25, pady=(15, 5))
        top_header_frame.grid_columnconfigure(0, weight=1, uniform="header")
        top_header_frame.grid_columnconfigure(1, weight=1, uniform="header")
        top_header_frame.grid_columnconfigure(2, weight=1, uniform="header")
        
        self.title_lbl = ctk.CTkLabel(top_header_frame, text="", font=("Segoe UI", 16, "bold"), text_color="#bb86fc")
        self.title_lbl.grid(row=0, column=0, sticky="w")
        
        self.tabs_btn_frame = ctk.CTkFrame(top_header_frame, fg_color="transparent")
        self.tabs_btn_frame.grid(row=0, column=1)
        
        self.btn_home = ctk.CTkButton(
            self.tabs_btn_frame, 
            text="HOME", 
            width=90, 
            height=30, 
            corner_radius=6,
            command=lambda: self.switch_tab("HOME")
        )
        self.btn_home.pack(side="left", padx=3)
        
        self.btn_tag = ctk.CTkButton(
            self.tabs_btn_frame, 
            text="TAG STUDIO", 
            width=110, 
            height=30, 
            corner_radius=6,
            command=lambda: self.switch_tab("TAG STUDIO")
        )
        self.btn_tag.pack(side="left", padx=3)
        
        self.btn_decomp = ctk.CTkButton(
            self.tabs_btn_frame, 
            text="DECONSTRUCTOR", 
            width=135, 
            height=30, 
            corner_radius=6,
            command=lambda: self.switch_tab("DECONSTRUCTOR")
        )
        self.btn_decomp.pack(side="left", padx=3)
        
        self.settings_btn = ctk.CTkButton(
            top_header_frame, 
            text="", 
            font=("Segoe UI", 11, "bold"), 
            fg_color="#1a1a1a", 
            hover_color="#2b2b2b", 
            text_color="#bb86fc", 
            width=110, 
            height=28, 
            corner_radius=6, 
            command=self.open_settings_window
        )
        self.settings_btn.grid(row=0, column=2, sticky="e")
        
        self.tab_container = ctk.CTkFrame(self.root, fg_color="transparent")
        self.tab_container.pack(fill="both", expand=True)
        
        self.frame_home = ctk.CTkFrame(self.tab_container, fg_color="transparent")
        self.frame_tag = ctk.CTkFrame(self.tab_container, fg_color="transparent")
        self.frame_decomp = ctk.CTkFrame(self.tab_container, fg_color="transparent")
        
        self.init_home_tab()
        self.init_tag_tab()
        self.init_decomp_tab()
        
        self.status_bar_frame = ctk.CTkFrame(self.root, fg_color="#111111", height=24, border_color="#222222", border_width=1)
        self.status_bar_frame.pack(side="bottom", fill="x", padx=20, pady=(5, 10))
        self.status_bar_frame.pack_propagate(False)
        
        self.status_lbl = ctk.CTkLabel(self.status_bar_frame, text="", font=("Segoe UI", 10, "bold"), text_color="#00ff66")
        self.status_lbl.pack(side="left", padx=15)
        
        self.current_active_tab = None

    def switch_tab(self, tab_name):
        self.frame_home.pack_forget()
        self.frame_tag.pack_forget()
        self.frame_decomp.pack_forget()
        
        inactive_bg = "#161616"
        inactive_text = "#bb86fc"
        inactive_hover = "#333333"  
        
        active_bg = "#bb86fc"
        active_text = "#0a0a0a"     
        active_hover = "#cda3ff"    
        
        self.btn_home.configure(fg_color=inactive_bg, text_color=inactive_text, hover_color=inactive_hover)
        self.btn_tag.configure(fg_color=inactive_bg, text_color=inactive_text, hover_color=inactive_hover)
        self.btn_decomp.configure(fg_color=inactive_bg, text_color=inactive_text, hover_color=inactive_hover)
        
        if tab_name == "HOME":
            self.frame_home.pack(fill="both", expand=True, padx=20, pady=5)
            self.btn_home.configure(fg_color=active_bg, text_color=active_text, hover_color=active_hover)
            self.current_active_tab = "HOME"
        elif tab_name == "TAG STUDIO":
            self.frame_tag.pack(fill="both", expand=True, padx=20, pady=5)
            self.btn_tag.configure(fg_color=active_bg, text_color=active_text, hover_color=active_hover)
            self.current_active_tab = "TAG STUDIO"
        elif tab_name == "DECONSTRUCTOR":
            self.frame_decomp.pack(fill="both", expand=True, padx=20, pady=5)
            self.btn_decomp.configure(fg_color=active_bg, text_color=active_text, hover_color=active_hover)
            self.current_active_tab = "DECONSTRUCTOR"
            
    def set_status(self, text, color="#00ff66"):
        self.status_lbl.configure(text=text, text_color=color)

    def reset_status(self):
        lang = LANGUAGES[self.current_lang]
        self.set_status(lang['status_ready'], "#00ff66")

    def register_hover_hints(self):
        widgets_with_hints = [
            (self.tag_wipe_btn, 'tip_tag_wipe'),
            (self.tag_execute_btn, 'tip_tag_execute'),
            (self.tag_clean_cb, 'tip_clean_cb'),
            (self.move_cb, 'tip_move_cb'),
            (self.dupe_cb, 'tip_dupe_cb'),
            (self.start_btn, 'tip_decomp_start')
        ]
        for widget, tip_key in widgets_with_hints:
            self.bind_hint(widget, tip_key)

    def bind_hint(self, widget, tip_key):
        def on_enter(event):
            lang = LANGUAGES[self.current_lang]
            self.set_status(lang[tip_key], "#bb86fc")
        def on_leave(event):
            self.reset_status()
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def init_home_tab(self):
        welcome_frame = ctk.CTkFrame(self.frame_home, fg_color="#111111", border_color="#222222", border_width=1, corner_radius=8)
        welcome_frame.pack(fill="both", expand=True, padx=25, pady=25)
        
        self.home_welcome_lbl = ctk.CTkLabel(welcome_frame, text="", font=("Segoe UI", 24, "bold"), text_color="#bb86fc")
        self.home_welcome_lbl.pack(pady=(40, 5))
        
        self.home_subtitle_lbl = ctk.CTkLabel(welcome_frame, text="", font=("Segoe UI", 11, "bold"), text_color="#aaaaaa")
        self.home_subtitle_lbl.pack(pady=(0, 10)) # Немного уменьшили отступ снизу
        
        # Информационная строка создателя (PHANT044M)
        self.home_creator_lbl = ctk.CTkLabel(welcome_frame, text="SYSTEM DEVELOPER: PHANT044M // SSPECTRA MUSIC", font=("Consolas", 10, "bold"), text_color="#00ff66")
        self.home_creator_lbl.pack(pady=(0, 25))
        
        guide_card = ctk.CTkFrame(welcome_frame, fg_color="#141416", border_color="#bb86fc", border_width=1, corner_radius=6)
        guide_card.pack(fill="x", padx=60, pady=6)
        self.home_guide_title = ctk.CTkLabel(guide_card, text="", font=("Segoe UI", 12, "bold"), text_color="#00ff66")
        self.home_guide_title.pack(anchor="w", padx=15, pady=(8, 2))
        self.home_guide_1_lbl = ctk.CTkLabel(guide_card, text="", font=("Segoe UI", 10), text_color="#ffffff", justify="left")
        self.home_guide_1_lbl.pack(anchor="w", padx=20, pady=2)
        self.home_guide_2_lbl = ctk.CTkLabel(guide_card, text="", font=("Segoe UI", 10), text_color="#ffffff", justify="left")
        self.home_guide_2_lbl.pack(anchor="w", padx=20, pady=(2, 8))
        
        links_card = ctk.CTkFrame(welcome_frame, fg_color="#141416", border_color="#bb86fc", border_width=1, corner_radius=6)
        links_card.pack(fill="x", padx=60, pady=6)
        self.home_links_title = ctk.CTkLabel(links_card, text="", font=("Segoe UI", 12, "bold"), text_color="#00ff66")
        self.home_links_title.pack(anchor="w", padx=15, pady=(8, 2))
        self.home_link_tg_lbl = ctk.CTkLabel(links_card, text="", font=("Segoe UI", 10, "underline"), text_color="#38bdf8", cursor="hand2")
        self.home_link_tg_lbl.pack(anchor="w", padx=20, pady=2)
        self.home_link_tg_lbl.bind("<Button-1>", lambda e: webbrowser.open_new_tab("https://t.me/phant044"))
        self.home_link_docs_lbl = ctk.CTkLabel(links_card, text="", font=("Segoe UI", 10, "underline"), text_color="#38bdf8", cursor="hand2")
        self.home_link_docs_lbl.pack(anchor="w", padx=20, pady=(2, 8))
        self.home_link_docs_lbl.bind("<Button-1>", lambda e: webbrowser.open_new_tab("https://github.com/PHANT044M/SSPECTRA-AUDIO-LAB"))
        
        status_card = ctk.CTkFrame(welcome_frame, fg_color="#141416", border_color="#bb86fc", border_width=1, corner_radius=6)
        status_card.pack(fill="x", padx=60, pady=6)
        self.home_status_title = ctk.CTkLabel(status_card, text="", font=("Segoe UI", 12, "bold"), text_color="#00ff66")
        self.home_status_title.pack(anchor="w", padx=15, pady=(8, 2))
        self.home_status_mutagen_lbl = ctk.CTkLabel(status_card, text="", font=("Segoe UI", 10), text_color="#ffffff")
        self.home_status_mutagen_lbl.pack(anchor="w", padx=20, pady=2)
        self.home_status_dnd_lbl = ctk.CTkLabel(status_card, text="", font=("Segoe UI", 10), text_color="#ffffff")
        self.home_status_dnd_lbl.pack(anchor="w", padx=20, pady=(2, 8))

    def init_tag_tab(self):
        main_grid = ctk.CTkFrame(self.frame_tag, fg_color="transparent")
        main_grid.pack(fill="both", expand=True)
        
        left_panel = ctk.CTkFrame(main_grid, fg_color="transparent")
        left_panel.pack(side="left", fill="both", expand=True, padx=(5, 10))
        
        self.tag_folder_lbl = ctk.CTkLabel(left_panel, text="", font=("Segoe UI", 11), text_color="#ffffff")
        self.tag_folder_lbl.pack(anchor="w", pady=2)
        
        path_search_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        path_search_frame.pack(fill="x")
        self.tag_path_entry = ctk.CTkEntry(path_search_frame, font=("Segoe UI", 11), fg_color="#141414", border_color="#2d2d2d", height=30, corner_radius=6)
        self.tag_path_entry.pack(side="left", fill="x", expand=True)
        self.tag_browse_btn = ctk.CTkButton(path_search_frame, text="", font=("Segoe UI", 11), fg_color="#1a1a1a", hover_color="#2b2b2b", width=120, height=30, corner_radius=6, command=self.browse_tag_folder)
        self.tag_browse_btn.pack(side="right", padx=(10, 0))
        
        self.tag_file_listbox = tk.Listbox(left_panel, font=("Consolas", 12), bg="#141414", fg="#ffffff", selectbackground="#bb86fc", selectforeground="#000000", bd=0, highlightthickness=0, selectmode=tk.EXTENDED, exportselection=False)
        self.tag_file_listbox.pack(fill="both", expand=True, pady=10)
        self.tag_file_listbox.bind("<<ListboxSelect>>", self.on_file_selected)
        self.bind_select_all(self.tag_file_listbox)
        
        self.tag_log_frame = ctk.CTkFrame(left_panel, fg_color="#111111", border_color="#222222", border_width=1, corner_radius=8, height=110)
        self.tag_log_frame.pack(fill="x")
        self.tag_log_frame.pack_propagate(False)
        self.tag_log_area = tk.Text(self.tag_log_frame, font=("Consolas", 9), bg="#161616", fg="#00ff66", bd=0, highlightthickness=0)
        self.tag_log_area.pack(fill="both", expand=True, padx=12, pady=10)
        
        self.tag_log_area.tag_config("success", foreground="#00ff66")
        self.tag_log_area.tag_config("error", foreground="#ff5555")
        self.tag_log_area.tag_config("info", foreground="#bb86fc")

        right_panel = ctk.CTkFrame(main_grid, fg_color="#111111", border_color="#222222", border_width=1, corner_radius=8, width=480)
        right_panel.pack(side="right", fill="both", padx=(10, 5))
        right_panel.pack_propagate(False)
        
        self.meta_frame_lbl = ctk.CTkLabel(right_panel, text="", font=("Segoe UI", 11, "bold"), text_color="#bb86fc")
        self.meta_frame_lbl.pack(anchor="w", padx=15, pady=(12, 2))
        
        meta_grid = ctk.CTkFrame(right_panel, fg_color="transparent")
        meta_grid.pack(fill="x", padx=15)
        
        self.lbl_title = ctk.CTkLabel(meta_grid, text="", font=("Segoe UI", 10), text_color="#aaaaaa"); self.lbl_title.grid(row=0, column=0, sticky="w", pady=2)
        self.ent_title = ctk.CTkEntry(meta_grid, font=("Segoe UI", 10), fg_color="#141414", border_color="#2d2d2d", height=24, width=250, corner_radius=5); self.ent_title.grid(row=0, column=1, pady=2, sticky="w", padx=15)
        
        self.lbl_art = ctk.CTkLabel(meta_grid, text="", font=("Segoe UI", 10), text_color="#aaaaaa"); self.lbl_art.grid(row=1, column=0, sticky="w", pady=2)
        self.ent_artist = ctk.CTkEntry(meta_grid, font=("Segoe UI", 10), fg_color="#141414", border_color="#2d2d2d", height=24, width=250, corner_radius=5); self.ent_artist.grid(row=1, column=1, pady=2, sticky="w", padx=15)
        
        self.lbl_alb = ctk.CTkLabel(meta_grid, text="", font=("Segoe UI", 10), text_color="#aaaaaa"); self.lbl_alb.grid(row=2, column=0, sticky="w", pady=2)
        self.ent_album = ctk.CTkEntry(meta_grid, font=("Segoe UI", 10), fg_color="#141414", border_color="#2d2d2d", height=24, width=250, corner_radius=5); self.ent_album.grid(row=2, column=1, pady=2, sticky="w", padx=15)
        
        self.lbl_yr = ctk.CTkLabel(meta_grid, text="", font=("Segoe UI", 10), text_color="#aaaaaa"); self.lbl_yr.grid(row=3, column=0, sticky="w", pady=2)
        self.ent_year = ctk.CTkEntry(meta_grid, font=("Segoe UI", 10), fg_color="#141414", border_color="#2d2d2d", height=24, width=250, corner_radius=5); self.ent_year.grid(row=3, column=1, pady=2, sticky="w", padx=15)
        
        self.lbl_gen = ctk.CTkLabel(meta_grid, text="", font=("Segoe UI", 10), text_color="#aaaaaa"); self.lbl_gen.grid(row=4, column=0, sticky="w", pady=2)
        self.ent_genre = ctk.CTkEntry(meta_grid, font=("Segoe UI", 10), fg_color="#141414", border_color="#2d2d2d", height=24, width=250, corner_radius=5); self.ent_genre.grid(row=4, column=1, pady=2, sticky="w", padx=15)
        
        self.lbl_comp = ctk.CTkLabel(meta_grid, text="", font=("Segoe UI", 10), text_color="#aaaaaa"); self.lbl_comp.grid(row=5, column=0, sticky="w", pady=2)
        self.ent_composer = ctk.CTkEntry(meta_grid, font=("Segoe UI", 10), fg_color="#141414", border_color="#2d2d2d", height=24, width=250, corner_radius=5); self.ent_composer.grid(row=5, column=1, pady=2, sticky="w", padx=15)
        
        hack_btn_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        hack_btn_frame.pack(fill="x", padx=15, pady=6)
        
        self.btn_def_author = ctk.CTkButton(hack_btn_frame, text="", font=("Segoe UI", 10), fg_color="#1a1a1a", hover_color="#2b2b2b", height=26, corner_radius=5, command=self.fill_default_author)
        self.btn_def_author.pack(side="left", fill="x", expand=True, padx=(0, 2))
        
        self.btn_file_title = ctk.CTkButton(hack_btn_frame, text="", font=("Segoe UI", 10), fg_color="#1a1a1a", hover_color="#2b2b2b", height=26, corner_radius=5, command=self.fill_filename_as_title)
        self.btn_file_title.pack(side="right", fill="x", expand=True, padx=(2, 0))

        self.cover_frame_lbl = ctk.CTkLabel(right_panel, text="", font=("Segoe UI", 11, "bold"), text_color="#bb86fc")
        self.cover_frame_lbl.pack(anchor="w", padx=15, pady=(4, 2))
        
        cover_work_area = ctk.CTkFrame(right_panel, fg_color="transparent")
        cover_work_area.pack(fill="x", padx=15)
        
        self.cover_border_frame = ctk.CTkFrame(cover_work_area, fg_color="#1c1c1e", border_color="#bb86fc", border_width=1, width=114, height=114, corner_radius=8)
        self.cover_border_frame.pack_propagate(False)
        self.cover_border_frame.pack(side="left")
        
        self.cover_preview_box = ctk.CTkLabel(self.cover_border_frame, text="[ DROP HERE ]\n[ NO ART ]", font=("Consolas", 10), fg_color="#141414", width=110, height=110, corner_radius=6, text_color="#555555", padx=0, pady=0)
        self.cover_preview_box.pack(padx=1, pady=1)
        
        cover_ctrls = ctk.CTkFrame(cover_work_area, fg_color="transparent")
        cover_ctrls.pack(side="right", fill="both", expand=True, padx=(15, 0))
        
        self.cover_type_menu = ctk.CTkOptionMenu(cover_ctrls, values=["Front Cover", "Artist", "Icon", "Illustration"], font=("Segoe UI", 10), fg_color="#141414", button_color="#1a1a1a", button_hover_color="#2b2b2b", dropdown_fg_color="#141414", height=26)
        self.cover_type_menu.pack(fill="x", pady=(2, 5))
        
        self.btn_load_art = ctk.CTkButton(cover_ctrls, text="", font=("Segoe UI", 10), fg_color="#1a1a1a", hover_color="#2b2b2b", height=26, command=self.load_cover_art_file)
        self.btn_load_art.pack(fill="x", pady=2)
        
        self.btn_del_art = ctk.CTkButton(cover_ctrls, text="", font=("Segoe UI", 10), fg_color="#1a1a1a", hover_color="#2b2b2b", height=26, command=self.delete_cover_art_buffer)
        self.btn_del_art.pack(fill="x", pady=2)

        self.rename_frame_lbl = ctk.CTkLabel(right_panel, text="", font=("Segoe UI", 11, "bold"), text_color="#bb86fc")
        self.rename_frame_lbl.pack(anchor="w", padx=15, pady=(6, 2))
        
        self.tag_rename_lbl = ctk.CTkLabel(right_panel, text="", font=("Segoe UI", 9), text_color="#aaaaaa")
        self.tag_rename_lbl.pack(anchor="w", padx=15)
        
        self.tag_mask_entry = ctk.CTkEntry(right_panel, font=("Segoe UI", 11), fg_color="#141414", border_color="#2d2d2d", placeholder_text="808 - {n} [NICKNAME]", height=28, corner_radius=5)
        self.tag_mask_entry.pack(fill="x", padx=15, pady=4)
        
        self.tag_clean_var = tk.BooleanVar(value=True)
        self.tag_clean_cb = ctk.CTkCheckBox(right_panel, text="", variable=self.tag_clean_var, font=("Segoe UI", 10), text_color="#00ff66", fg_color="#141414", border_color="#2d2d2d", hover_color="#1f1f1f", height=20)
        self.tag_clean_cb.pack(anchor="w", padx=15, pady=2)

        action_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        action_frame.pack(fill="x", padx=15, pady=(15, 10))
        
        self.tag_execute_btn = ctk.CTkButton(action_frame, text="", font=("Segoe UI", 12, "bold"), fg_color="#bb86fc", hover_color="#cda3ff", text_color="#000000", height=40, corner_radius=6, command=self.trigger_tag_thread)
        self.tag_execute_btn.pack(fill="x", pady=(0, 6))
        
        self.tag_wipe_btn = ctk.CTkButton(action_frame, text="", font=("Segoe UI", 11, "bold"), fg_color="#222222", hover_color="#3a1010", text_color="#ff5555", height=40, corner_radius=6, command=self.trigger_wipe_thread)
        self.tag_wipe_btn.pack(fill="x")

    def init_decomp_tab(self):
        main_layout = ctk.CTkFrame(self.frame_decomp, fg_color="transparent")
        main_layout.pack(fill="both", expand=True)
        
        config_frame = ctk.CTkFrame(main_layout, fg_color="transparent")
        config_frame.pack(fill="x", padx=15, pady=5)
        
        self.pack_lbl = ctk.CTkLabel(config_frame, text="", font=("Segoe UI", 11), text_color="#ffffff")
        self.pack_lbl.pack(side="left")
        
        self.kit_name_entry = ctk.CTkEntry(config_frame, font=("Segoe UI", 11), fg_color="#141414", border_color="#2d2d2d", text_color="#ffffff", placeholder_text="SOUND PACK", width=200, height=30, corner_radius=6)
        self.kit_name_entry.pack(side="left", padx=10)

        self.move_mode_var = tk.BooleanVar(value=False)
        self.move_cb = ctk.CTkCheckBox(config_frame, text="", variable=self.move_mode_var, font=("Segoe UI", 10), text_color="#ffaa00", fg_color="#141414", border_color="#2d2d2d", hover_color="#1f1f1f")
        self.move_cb.pack(side="left", padx=10)

        self.dupe_filter_var = tk.BooleanVar(value=True)
        self.dupe_cb = ctk.CTkCheckBox(config_frame, text="", variable=self.dupe_filter_var, font=("Segoe UI", 10), text_color="#00ff66", fg_color="#141414", border_color="#2d2d2d", hover_color="#1f1f1f")
        self.dupe_cb.pack(side="left", padx=10)

        self.folder_frame = ctk.CTkFrame(main_layout, fg_color="#111111", border_color="#222222", border_width=1, corner_radius=8)
        self.folder_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        self.folder_title = ctk.CTkLabel(self.folder_frame, text="", font=("Segoe UI", 11, "bold"), text_color="#bb86fc")
        self.folder_title.pack(anchor="w", padx=15, pady=(10, 0))
        
        self.paths_listbox = tk.Listbox(self.folder_frame, font=("Consolas", 12), bg="#161616", fg="#e0e0e0", selectbackground="#bb86fc", selectforeground="#000000", bd=0, highlightthickness=0, height=5)
        self.paths_listbox.pack(side="left", fill="both", expand=True, padx=15, pady=10)
        self.bind_select_all(self.paths_listbox)
        
        btn_frame = ctk.CTkFrame(self.folder_frame, fg_color="transparent")
        btn_frame.pack(side="right", fill="y", padx=(0, 15), pady=10)
        
        self.add_target_btn = ctk.CTkButton(btn_frame, text="", font=("Segoe UI", 11, "bold"), fg_color="#bb86fc", hover_color="#cda3ff", text_color="#000000", height=32, corner_radius=6, command=self.show_add_target_menu)
        self.add_target_btn.pack(fill="x", pady=2)
        
        self.remove_btn = ctk.CTkButton(btn_frame, text="", font=("Segoe UI", 11), fg_color="#1e1e1e", hover_color="#2b2b2b", text_color="#ffaa00", height=28, corner_radius=6, command=self.remove_selected_folder)
        self.remove_btn.pack(fill="x", pady=2)
        
        self.clear_btn = ctk.CTkButton(btn_frame, text="", font=("Segoe UI", 11), fg_color="#1e1e1e", hover_color="#2b2b2b", text_color="#ff5555", height=28, corner_radius=6, command=self.clear_folders)
        self.clear_btn.pack(fill="x", pady=2)

        self.log_frame = ctk.CTkFrame(main_layout, fg_color="#111111", border_color="#222222", border_width=1, corner_radius=8)
        self.log_frame.pack(fill="both", expand=True, padx=15, pady=5)
        
        self.monitor_title = ctk.CTkLabel(self.log_frame, text="", font=("Segoe UI", 11, "bold"), text_color="#bb86fc")
        self.monitor_title.pack(anchor="w", padx=15, pady=(10, 0))
        
        self.log_area_decomp = tk.Text(self.log_frame, font=("Consolas", 10), bg="#161616", fg="#00ff66", bd=0, highlightthickness=0, height=6)
        self.log_area_decomp.pack(fill="both", expand=True, padx=15, pady=10)
        
        self.log_area_decomp.tag_config("success", foreground="#00ff66")
        self.log_area_decomp.tag_config("error", foreground="#ff5555")
        self.log_area_decomp.tag_config("info", foreground="#bb86fc")

        self.progress = ctk.CTkProgressBar(main_layout, fg_color="#1e1e1e", progress_color="#bb86fc", height=6, corner_radius=3)
        self.progress.set(0)

        self.start_btn = ctk.CTkButton(main_layout, text="", font=("Segoe UI", 12, "bold"), fg_color="#00ff66", hover_color="#26ff7d", text_color="#000000", height=42, corner_radius=8, command=self.trigger_sorting_thread)
        self.start_btn.pack(fill="x", padx=15, pady=(10, 15))

    def update_ui_text(self):
        lang = LANGUAGES[self.current_lang]
        self.root.title(f"SSPECTRA AUDIO LAB {APP_VERSION}")
        self.title_lbl.configure(text=lang['header'])
        self.settings_btn.configure(text=lang['settings_btn'])
        self.reset_status()
        
        if self.current_active_tab is None:
            self.switch_tab("HOME")
            self.current_active_tab = "HOME"
        else:
            self.switch_tab(self.current_active_tab)
            
        self.home_welcome_lbl.configure(text=lang['home_welcome'])
        self.home_subtitle_lbl.configure(text=lang['home_subtitle'])
        self.home_guide_title.configure(text=lang['home_guide_hdr'])
        self.home_guide_1_lbl.configure(text=lang['home_guide_1'])
        self.home_guide_2_lbl.configure(text=lang['home_guide_2'])
        self.home_links_title.configure(text=lang['home_links_hdr'])
        self.home_link_tg_lbl.configure(text=lang['home_link_tg'])
        self.home_link_docs_lbl.configure(text=lang['home_link_docs'])
        self.home_status_title.configure(text=lang['home_status_hdr'])
        
        if MUTAGEN_AVAILABLE:
            self.home_status_mutagen_lbl.configure(text=lang['home_status_mutagen'], text_color="#00ff66")
        else:
            self.home_status_mutagen_lbl.configure(text=lang['home_status_mutagen_no'], text_color="#ff5555")
            
        if HAS_DND:
            self.home_status_dnd_lbl.configure(text=lang['home_status_dnd'], text_color="#00ff66")
        else:
            self.home_status_dnd_lbl.configure(text=lang['home_status_dnd_no'], text_color="#ff5555")
            
        self.tag_folder_lbl.configure(text=lang['tag_folder_lbl'])
        self.tag_browse_btn.configure(text=lang['tag_browse_btn'])
        self.meta_frame_lbl.configure(text=lang['tag_meta_hdr'])
        self.lbl_title.configure(text=lang['tag_title'])
        self.lbl_art.configure(text=lang['tag_artist'])
        self.lbl_alb.configure(text=lang['tag_album'])
        self.lbl_yr.configure(text=lang['tag_year'])
        self.lbl_gen.configure(text=lang['tag_genre'])
        self.lbl_comp.configure(text=lang['tag_composer'])
        self.btn_def_author.configure(text=lang['tag_btn_author'])
        self.btn_file_title.configure(text=lang['tag_btn_title'])
        self.cover_frame_lbl.configure(text=lang['tag_cover_hdr'])
        self.btn_load_art.configure(text=lang['tag_cover_load'])
        self.btn_del_art.configure(text=lang['tag_cover_del'])
        self.rename_frame_lbl.configure(text=lang['tag_rename_hdr'])
        self.tag_rename_lbl.configure(text=lang['tag_rename_lbl'])
        self.tag_clean_cb.configure(text=lang['tag_clean_cb'])
        self.tag_wipe_btn.configure(text=lang['tag_wipe_btn'])
        
        self.pack_lbl.configure(text=lang['pack_label'])
        self.move_cb.configure(text=lang['move_cb'])
        self.dupe_cb.configure(text=lang['dupe_cb'])
        self.folder_title.configure(text=lang['folder_frame'])
        self.add_target_btn.configure(text=lang['add_target_btn'])
        self.remove_btn.configure(text=lang['remove_btn'])
        self.clear_btn.configure(text=lang['clear_btn'])
        self.monitor_title.configure(text=lang['log_frame'])
        
        if not self.is_processing:
            self.tag_execute_btn.configure(text=lang['tag_execute_btn'], fg_color="#bb86fc", state="normal")
            self.tag_wipe_btn.configure(state="normal")
            self.start_btn.configure(text=lang['start_btn'], fg_color="#00ff66", state="normal")
        else:
            self.tag_execute_btn.configure(text=lang['processing_btn'], fg_color="#333333", state="disabled")
            self.tag_wipe_btn.configure(state="disabled")
            self.start_btn.configure(text=lang['processing_btn'], fg_color="#333333", state="disabled")

        self.paths_listbox.delete(0, tk.END)
        for idx, path in enumerate(self.scan_paths):
            if idx == 0 and path == os.getcwd():
                self.paths_listbox.insert(tk.END, f"[{lang['current_folder']}] -> {path}")
            else:
                self.paths_listbox.insert(tk.END, path)

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    self.current_lang = config.get("lang", "en")
                    self.def_artist = config.get("artist", "PHANT044M")
                    self.def_album = config.get("album", "")
                    self.def_year = config.get("year", "")
                    self.def_genre = config.get("genre", "")
                    self.def_composer = config.get("composer", "PHANT044M // ANTIWORLD")
                    self.def_auto_title = config.get("auto_title", True)
                    self.dest_dir = config.get("dest_dir", "")  
            except: pass

    def open_settings_window(self):
        lang = LANGUAGES[self.current_lang]
        settings_win = ctk.CTkToplevel(self.root)
        settings_win.title(lang['settings_btn'])
        
        # Центрирование настроек
        self.center_window(settings_win, 440, 465)
        
        settings_win.resizable(False, False)
        settings_win.configure(fg_color="#0c0c0c")
        settings_win.transient(self.root)
        settings_win.grab_set()

        ctk.CTkLabel(settings_win, text=lang['win_set_title'], font=("Segoe UI", 12, "bold"), text_color="#bb86fc").pack(pady=12)
        
        ctk.CTkLabel(settings_win, text=lang['win_set_lang'], font=("Segoe UI", 10), text_color="#aaaaaa").pack(anchor="w", padx=30)
        
        # Плоские кнопки выбора языков
        lang_frame = ctk.CTkFrame(settings_win, fg_color="transparent")
        lang_frame.pack(pady=6)
        
        self.btn_en = ctk.CTkButton(lang_frame, text="EN", width=180, height=30, corner_radius=6, command=lambda: switch_lang("en"))
        self.btn_en.pack(side="left", padx=5)
        
        self.btn_ru = ctk.CTkButton(lang_frame, text="RU", width=180, height=30, corner_radius=6, command=lambda: switch_lang("ru"))
        self.btn_ru.pack(side="left", padx=5)
        
        def switch_lang(lang_code):
            self.current_lang = lang_code
            update_lang_btns()
            
        def update_lang_btns():
            inactive_bg, inactive_text, inactive_hover = "#161616", "#bb86fc", "#333333"
            active_bg, active_text, active_hover = "#bb86fc", "#0a0a0a", "#cda3ff"
            
            self.btn_en.configure(fg_color=active_bg if self.current_lang == 'en' else inactive_bg,
                                  text_color=active_text if self.current_lang == 'en' else inactive_text,
                                  hover_color=active_hover if self.current_lang == 'en' else inactive_hover)
            self.btn_ru.configure(fg_color=active_bg if self.current_lang == 'ru' else inactive_bg,
                                  text_color=active_text if self.current_lang == 'ru' else inactive_text,
                                  hover_color=active_hover if self.current_lang == 'ru' else inactive_hover)
        update_lang_btns()

        # Функция открытия подменю (строго ДО создания кнопки prof_btn)
        def open_profile_setup():
            self.open_artist_profile_submenu(settings_win)

        prof_btn = ctk.CTkButton(settings_win, text=lang['win_set_prof_btn'], font=("Segoe UI", 11), fg_color="#1a1a1a", hover_color="#2b2b2b", text_color="#bb86fc", height=34, command=open_profile_setup)
        prof_btn.pack(pady=10, fill="x", padx=30)
        
        # Кнопка отправки баг-репорта
        bug_btn = ctk.CTkButton(
            settings_win, 
            text=lang['win_set_bug_btn'], 
            font=("Segoe UI", 11, "bold"), 
            fg_color="#1a1a1a", 
            hover_color="#2b2b2b", 
            text_color="#ff5555",
            height=34, 
            command=self.open_bug_report_window
        )
        bug_btn.pack(pady=10, fill="x", padx=30)
        
        ctk.CTkLabel(settings_win, text=lang['win_set_dest_lbl'], font=("Segoe UI", 10), text_color="#aaaaaa").pack(anchor="w", padx=30, pady=(5, 0))
        dest_frame = ctk.CTkFrame(settings_win, fg_color="transparent")
        dest_frame.pack(fill="x", padx=30, pady=2)
        
        self.dest_entry = ctk.CTkEntry(dest_frame, font=("Segoe UI", 10), fg_color="#141414", border_color="#2d2d2d", height=26)
        self.dest_entry.pack(side="left", fill="x", expand=True)
        self.dest_entry.insert(0, self.dest_dir)
        
        def browse_dest():
            folder = filedialog.askdirectory()
            if folder:
                self.dest_entry.delete(0, tk.END)
                self.dest_entry.insert(0, os.path.normpath(folder))
                
        dest_browse_btn = ctk.CTkButton(dest_frame, text=lang['win_set_dest_browse'], font=("Segoe UI", 10), fg_color="#1a1a1a", hover_color="#2b2b2b", text_color="#bb86fc", width=80, height=26, command=browse_dest)
        dest_browse_btn.pack(side="right", padx=(5, 0))
        
        cb_var = tk.BooleanVar(value=self.def_auto_title)
        cb_frame = ctk.CTkFrame(settings_win, fg_color="transparent")
        cb_frame.pack(pady=10, anchor="w", padx=30)
        
        cb = ctk.CTkCheckBox(cb_frame, text=lang['tag_btn_title'], variable=cb_var, font=("Segoe UI", 10), text_color="#ffffff", fg_color="#141414", border_color="#2d2d2d", hover_color="#1f1f1f")
        cb.pack(side="left")
        
        info_sign = ctk.CTkLabel(cb_frame, text="ⓘ", font=("Segoe UI", 12, "bold"), text_color="#bb86fc", cursor="hand2")
        info_sign.pack(side="left", padx=8)
        
        info_help_lbl = ctk.CTkLabel(settings_win, text="", font=("Segoe UI", 10), text_color="#00ff66", justify="center")
        info_help_lbl.pack(side="bottom", pady=5)
        
        info_sign.bind("<Enter>", lambda e: info_help_lbl.configure(text=lang['tip_auto_title_hint']))
        info_sign.bind("<Leave>", lambda e: info_help_lbl.configure(text=""))

        def save_settings():
            self.def_auto_title = cb_var.get()
            self.dest_dir = self.dest_entry.get().strip()
            try:
                with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                    json.dump({
                        "lang": self.current_lang,
                        "artist": self.def_artist,
                        "album": self.def_album,
                        "year": self.def_year,
                        "genre": self.def_genre,
                        "composer": self.def_composer,
                        "auto_title": self.def_auto_title,
                        "dest_dir": self.dest_dir
                    }, f, indent=4, ensure_ascii=False)
                self.current_active_tab = None
                self.update_ui_text()
                settings_win.destroy()
            except: pass

        ctk.CTkButton(settings_win, text=lang['win_set_save_btn'], font=("Segoe UI", 11, "bold"), fg_color="#bb86fc", hover_color="#cda3ff", text_color="#000000", height=40, command=save_settings).pack(pady=10, fill="x", padx=30)

    def open_artist_profile_submenu(self, parent_win):
        lang = LANGUAGES[self.current_lang]
        sub_win = ctk.CTkToplevel(parent_win)
        sub_win.title(lang['win_sub_title'])
        
        self.center_window(sub_win, 400, 420)
        
        sub_win.resizable(False, False)
        sub_win.configure(fg_color="#111111")
        sub_win.transient(parent_win)
        sub_win.grab_set()

        ctk.CTkLabel(sub_win, text=lang['win_sub_title'], font=("Segoe UI", 12, "bold"), text_color="#00ff66").pack(pady=10)
        
        ctk.CTkLabel(sub_win, text=lang['win_sub_art'], font=("Segoe UI", 9), text_color="#aaaaaa").pack(anchor="w", padx=35)
        art_ent = ctk.CTkEntry(sub_win, width=330, height=24, fg_color="#161616"); art_ent.pack(pady=2); art_ent.insert(0, self.def_artist)
        
        ctk.CTkLabel(sub_win, text=lang['tag_album'], font=("Segoe UI", 9), text_color="#aaaaaa").pack(anchor="w", padx=35)
        alb_ent = ctk.CTkEntry(sub_win, width=330, height=24, fg_color="#161616"); alb_ent.pack(pady=2); alb_ent.insert(0, self.def_album)
        
        ctk.CTkLabel(sub_win, text=lang['tag_year'], font=("Segoe UI", 9), text_color="#aaaaaa").pack(anchor="w", padx=35)
        yr_ent = ctk.CTkEntry(sub_win, width=330, height=24, fg_color="#161616"); yr_ent.pack(pady=2); yr_ent.insert(0, self.def_year)
        
        ctk.CTkLabel(sub_win, text=lang['tag_genre'], font=("Segoe UI", 9), text_color="#aaaaaa").pack(anchor="w", padx=35)
        gen_ent = ctk.CTkEntry(sub_win, width=330, height=24, fg_color="#161616"); gen_ent.pack(pady=2); gen_ent.insert(0, self.def_genre)
        
        ctk.CTkLabel(sub_win, text=lang['win_sub_comp'], font=("Segoe UI", 9), text_color="#aaaaaa").pack(anchor="w", padx=35)
        comp_ent = ctk.CTkEntry(sub_win, width=330, height=24, fg_color="#161616"); comp_ent.pack(pady=2); comp_ent.insert(0, self.def_composer)

        def apply_profile():
            self.def_artist = art_ent.get().strip()
            self.def_album = alb_ent.get().strip()
            self.def_year = yr_ent.get().strip()
            self.def_genre = gen_ent.get().strip()
            self.def_composer = comp_ent.get().strip()
            sub_win.destroy()

        ctk.CTkButton(sub_win, text="OK", font=("Segoe UI", 11, "bold"), fg_color="#00ff66", hover_color="#26ff7d", text_color="#000000", width=140, height=32, command=apply_profile).pack(pady=15)

    def log_tag(self, message):
        tag = None
        msg_lower = message.lower()
        if any(x in msg_lower for x in ["[+]", "success", "renamed", "wiped", "ready"]):
            tag = "success"
        elif any(x in msg_lower for x in ["[!]", "error", "fail"]):
            tag = "error"
        elif any(x in msg_lower for x in ["[i]", "info", "initiating", "wipe"]):
            tag = "info"
            
        self.tag_log_area.insert(tk.END, message + "\n", tag)
        self.tag_log_area.see(tk.END)

    def fill_default_author(self):
        self.ent_artist.delete(0, tk.END); self.ent_artist.insert(0, self.def_artist)
        self.ent_album.delete(0, tk.END); self.ent_album.insert(0, self.def_album)
        self.ent_year.delete(0, tk.END); self.ent_year.insert(0, self.def_year)
        self.ent_genre.delete(0, tk.END); self.ent_genre.insert(0, self.def_genre)
        self.ent_composer.delete(0, tk.END); self.ent_composer.insert(0, self.def_composer)

    def fill_filename_as_title(self):
        selected_indices = self.tag_file_listbox.curselection()
        if len(selected_indices) == 1:
            filename = self.tag_file_listbox.get(selected_indices[0])
            name_part, _ = os.path.splitext(filename)
            self.ent_title.delete(0, tk.END)
            self.ent_title.insert(0, name_part)

    def browse_tag_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            norm_path = os.path.normpath(folder)
            self.tag_path_entry.delete(0, tk.END)
            self.tag_path_entry.insert(0, norm_path)
            self.refresh_tag_listbox(norm_path)
            self.log_tag(LANGUAGES[self.current_lang]['log_tag_ready'])

    def refresh_tag_listbox(self, path):
        self.tag_file_listbox.delete(0, tk.END)
        try:
            audio_files = sorted([f for f in os.listdir(path) if f.endswith(('.wav', '.mp3', '.flac', '.aif', '.aiff'))])
            for f in audio_files:
                self.tag_file_listbox.insert(tk.END, f)
        except Exception as e:
            self.log_tag(f"[!] Error reading dir: {e}")

    def safe_reset_cover(self, text_msg="[ NO ART ]", color="#444444"):
        self.current_cover_image = None  
        try:
            self.cover_preview_box._label.configure(image="")
        except: pass
        try:
            self.cover_preview_box.configure(image=None)
            self.cover_preview_box.configure(text=text_msg, text_color=color)
            self.cover_preview_box._current_img = None
        except: pass

    def on_file_selected(self, event):
        if not MUTAGEN_AVAILABLE: return
        selected_indices = self.tag_file_listbox.curselection()
        if not selected_indices: return
        
        self.staged_cover_bytes = None
        self.cover_action = "keep"
        
        if len(selected_indices) == 1:
            filename = self.tag_file_listbox.get(selected_indices[0])
            file_path = os.path.join(self.tag_path_entry.get(), filename)
            
            self.ent_title.delete(0, tk.END)
            self.ent_artist.delete(0, tk.END)
            self.ent_album.delete(0, tk.END)
            self.ent_year.delete(0, tk.END)
            self.ent_genre.delete(0, tk.END)
            self.ent_composer.delete(0, tk.END)
            
            self.loaded_file_cover_bytes = None  
            self.safe_reset_cover("[ NO ART ]", "#444444")
            
            try:
                if filename.lower().endswith(('.wav', '.mp3', '.aif', '.aiff')):
                    if filename.lower().endswith('.wav'): audio = WAVE(file_path)
                    elif filename.lower().endswith('.mp3'): audio = MP3(file_path)
                    else: audio = AIFF(file_path)
                    
                    tags = audio.tags
                    if tags:
                        if 'TIT2' in tags and tags['TIT2'].text: self.ent_title.insert(0, str(tags['TIT2'].text[0]))
                        if 'TPE1' in tags and tags['TPE1'].text: self.ent_artist.insert(0, str(tags['TPE1'].text[0]))
                        if 'TALB' in tags and tags['TALB'].text: self.ent_album.insert(0, str(tags['TALB'].text[0]))
                        
                        if 'TYER' in tags and tags['TYER'].text:
                            self.ent_year.insert(0, str(tags['TYER'].text[0]))
                        elif 'TDRC' in tags and tags['TDRC'].text:
                            self.ent_year.insert(0, str(tags['TDRC'].text[0]))
                            
                        if 'TCON' in tags and tags['TCON'].text: self.ent_genre.insert(0, str(tags['TCON'].text[0]))
                        if 'TCOM' in tags and tags['TCOM'].text: self.ent_composer.insert(0, str(tags['TCOM'].text[0]))
                        
                        apic_frames = tags.getall("APIC")
                        if apic_frames and apic_frames[0].data:
                            self.loaded_file_cover_bytes = apic_frames[0].data
                            pil_img = Image.open(io.BytesIO(self.loaded_file_cover_bytes))
                            pil_square = resize_to_square(pil_img, 110)
                            ctk_img = ctk.CTkImage(light_image=pil_square, dark_image=pil_square, size=(110, 110))
                            self.current_cover_image = ctk_img  
                            self.cover_preview_box.configure(image=ctk_img, text="", compound="center", fg_color="transparent")
                            self.cover_preview_box._current_img = ctk_img
                                
                elif filename.lower().endswith('.flac'):
                    audio = FLAC(file_path)
                    if audio:
                        if 'title' in audio and audio['title']: self.ent_title.insert(0, audio['title'][0])
                        if 'artist' in audio and audio['artist']: self.ent_artist.insert(0, audio['artist'][0])
                        if 'album' in audio and audio['album']: self.ent_album.insert(0, audio['album'][0])
                        if 'date' in audio and audio['date']: self.ent_year.insert(0, audio['date'][0])
                        if 'genre' in audio and audio['genre']: self.ent_genre.insert(0, audio['genre'][0])
                        if 'composer' in audio and audio['composer']: self.ent_composer.insert(0, audio['composer'][0])
                        
                        if audio.pictures and audio.pictures[0].data:
                            self.loaded_file_cover_bytes = audio.pictures[0].data
                            pil_img = Image.open(io.BytesIO(self.loaded_file_cover_bytes))
                            pil_square = resize_to_square(pil_img, 110)
                            ctk_img = ctk.CTkImage(light_image=pil_square, dark_image=pil_square, size=(110, 110))
                            self.current_cover_image = ctk_img  
                            self.cover_preview_box.configure(image=ctk_img, text="", compound="center", fg_color="transparent")
                            self.cover_preview_box._current_img = ctk_img
            except: pass
        else:
            self.safe_reset_cover("[ MULTIPLE\nFILES ]", "#bb86fc")

    def load_cover_art_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if file_path:
            self.loaded_cover_path = os.path.normpath(file_path)
            try:
                pil_img = Image.open(self.loaded_cover_path)
                
                pil_square_ui = resize_to_square(pil_img, 220)
                ctk_img = ctk.CTkImage(light_image=pil_square_ui, dark_image=pil_square_ui, size=(110, 110))
                self.current_cover_image = ctk_img  
                self.cover_preview_box.configure(image=ctk_img, text="", compound="center", fg_color="transparent")
                self.cover_preview_box._current_img = ctk_img
                
                self.staged_cover_bytes = convert_to_jpeg_bytes(pil_img, 800)
                self.cover_action = "set"
            except Exception as e:
                self.log_tag(f"[!] Error loading preview art: {e}")

    def delete_cover_art_buffer(self):
        self.loaded_cover_path = None
        self.staged_cover_bytes = None
        self.loaded_file_cover_bytes = None
        self.cover_action = "delete"
        self.safe_reset_cover("[ NO ART ]", "#444444")

    def on_drop_tag_files(self, event):
        data = event.data
        paths = []
        if data:
            for p in re.findall(r'\{([^}]+)\}|(\S+)', data):
                path = p[0] if p[0] else p[1]
                paths.append(os.path.normpath(path))
        if paths:
            first_path = paths[0]
            target_folder = first_path if os.path.isdir(first_path) else os.path.dirname(first_path)
            self.tag_path_entry.delete(0, tk.END)
            self.tag_path_entry.insert(0, target_folder)
            self.refresh_tag_listbox(target_folder)
            self.log_tag(LANGUAGES[self.current_lang]['log_tag_ready'])
            
            self.root.after(100, lambda: self.select_files_in_listbox(paths))

    def select_files_in_listbox(self, file_paths):
        filenames = [os.path.basename(p) for p in file_paths]
        self.tag_file_listbox.selection_clear(0, tk.END)
        for i in range(self.tag_file_listbox.size()):
            item = self.tag_file_listbox.get(i)
            if item in filenames:
                self.tag_file_listbox.selection_set(i)
        self.on_file_selected(None)

    def on_drop_cover(self, event):
        data = event.data
        paths = []
        if data:
            for p in re.findall(r'\{([^}]+)\}|(\S+)', data):
                path = p[0] if p[0] else p[1]
                paths.append(os.path.normpath(path))
        if paths:
            file_path = paths[0]
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                self.loaded_cover_path = file_path
                try:
                    pil_img = Image.open(self.loaded_cover_path)
                    
                    pil_square_ui = resize_to_square(pil_img, 220)
                    ctk_img = ctk.CTkImage(light_image=pil_square_ui, dark_image=pil_square_ui, size=(110, 110))
                    self.current_cover_image = ctk_img
                    self.cover_preview_box.configure(image=ctk_img, text="", compound="center", fg_color="transparent")
                    self.cover_preview_box._current_img = ctk_img
                    
                    self.staged_cover_bytes = convert_to_jpeg_bytes(pil_img, 800)
                    self.cover_action = "set"
                    self.log_tag("[+] Cover art loaded via Drag & Drop.")
                    self.cover_border_frame.configure(border_color="#bb86fc") 
                except Exception as e:
                    self.log_tag(f"[!] Error loading cover art DND: {e}")

    def trigger_tag_thread(self):
        if self.is_processing: return
        t = threading.Thread(target=self.start_tagging_process)
        t.daemon = True
        t.start()

    def start_tagging_process(self):
        self.is_processing = True
        lang = LANGUAGES[self.current_lang]
        self.tag_execute_btn.configure(state="disabled", fg_color="#333333", text=lang['processing_btn'])
        self.tag_log_area.delete("1.0", tk.END)
        
        target_dir = self.tag_path_entry.get().strip()
        if not target_dir or not os.path.exists(target_dir):
            self.log_tag(lang['log_tag_err_path'])
            self.end_process()
            return
            
        manual_title = self.ent_title.get().strip()
        artist = self.ent_artist.get().strip()
        album = self.ent_album.get().strip()
        year = self.ent_year.get().strip()
        genre = self.ent_genre.get().strip()
        composer = self.ent_composer.get().strip()
        mask = self.tag_mask_entry.get().strip()
        auto_clean = self.tag_clean_var.get()
        cover_type_str = self.cover_type_menu.get()
        
        type_mapping = {"Front Cover": 3, "Artist": 8, "Icon": 1, "Illustration": 11}
        selected_cover_type_code = type_mapping.get(cover_type_str, 3)
        
        self.log_tag(lang['log_tag_start'].format(target_dir))
        mime_type = "image/jpeg"

        selected_indices = self.tag_file_listbox.curselection()
        if selected_indices:
            files_to_process = [self.tag_file_listbox.get(i) for i in selected_indices]
        else:
            files_to_process = sorted([f for f in os.listdir(target_dir) if f.endswith(('.wav', '.mp3', '.flac', '.aif', '.aiff'))])

        modified_files = 0
        
        for index, file in enumerate(files_to_process, 1):
            old_path = os.path.join(target_dir, file)
            name_part, ext_part = os.path.splitext(file)
            
            new_name = name_part
            if mask:
                if "{n}" in mask: new_name = mask.replace("{n}", str(index))
                else: new_name = f"{mask} {index}"
            
            if auto_clean and not mask:
                new_name = re.sub(r'@[A-Za-z0-9_.]+', '', new_name)
                new_name = re.sub(r'[#\$]+[A-Za-z0-9]+', '', new_name)
                new_name = re.sub(r'[-_\s]+$', '', new_name)
                new_name = re.sub(r'^[-_\s]+', '', new_name)
                new_name = re.sub(r'\s+', ' ', new_name).strip()
            
            if not new_name: new_name = name_part
            final_filename = f"{new_name}{ext_part}"
            new_path = os.path.join(target_dir, final_filename)
            
            if final_filename != file:
                try:
                    os.rename(old_path, new_path)
                    current_working_path = new_path
                    self.log_tag(lang['log_tag_renamed'].format(file, final_filename))
                except Exception as e:
                    self.log_tag(f" -> [RENAME FAIL] {file}: {e}")
                    current_working_path = old_path
            else:
                current_working_path = old_path

            final_title_tag = new_name
            if manual_title and len(files_to_process) == 1:
                final_title_tag = manual_title  
            elif not self.def_auto_title and not manual_title and not mask:
                final_title_tag = ""  

            if MUTAGEN_AVAILABLE:
                try:
                    if current_working_path.lower().endswith(('.wav', '.mp3', '.aif', '.aiff')):
                        if current_working_path.lower().endswith('.wav'):
                            try: mutagen.wave.delete(current_working_path)
                            except: pass
                            audio = WAVE(current_working_path)
                        elif current_working_path.lower().endswith('.mp3'): 
                            audio = MP3(current_working_path)
                        else: 
                            audio = AIFF(current_working_path)
                        
                        if audio.tags is None: audio.add_tags()
                        id3_tags = audio.tags

                        if id3_tags is not None:
                            if final_title_tag: id3_tags.add(TIT2(encoding=1, text=final_title_tag))
                            if artist: id3_tags.add(TPE1(encoding=1, text=artist))
                            if album: id3_tags.add(TALB(encoding=1, text=album))
                            
                            if year: 
                                id3_tags.add(TYER(encoding=1, text=year))
                                id3_tags.add(TDRC(encoding=1, text=year))
                                
                            if genre: id3_tags.add(TCON(encoding=1, text=genre))
                            if composer: id3_tags.add(TCOM(encoding=1, text=composer))
                            
                            if self.cover_action == "set" and self.staged_cover_bytes:
                                id3_tags.delall("APIC")
                                id3_tags.add(APIC(
                                    encoding=1, 
                                    mime=mime_type, 
                                    type=selected_cover_type_code, 
                                    desc='Cover', 
                                    data=self.staged_cover_bytes
                                ))
                            elif self.cover_action == "delete":
                                id3_tags.delall("APIC")
                            
                            try: id3_tags.update_to_v23()
                            except: pass
                            
                            if current_working_path.lower().endswith(('.mp3', '.wav', '.aif', '.aiff')):
                                audio.save(v2_version=3)
                            else:
                                audio.save()  

                        if current_working_path.lower().endswith('.wav'):
                            riff_tags = {
                                b'INAM': final_title_tag,
                                b'IART': artist,
                                b'IPRD': album,
                                b'ICRD': year,
                                b'IGNR': genre,
                                b'ICMT': composer
                            }
                            write_wav_riff_info_tags(current_working_path, riff_tags)
                            
                        modified_files += 1
                        
                    elif current_working_path.lower().endswith('.flac'):
                        audio = FLAC(current_working_path)
                        try: audio.add_tags()
                        except Exception: pass
                            
                        if final_title_tag: audio["title"] = final_title_tag
                        if artist: audio["artist"] = artist
                        if album: audio["album"] = album
                        if year: audio["date"] = year
                        if genre: audio["genre"] = genre
                        if composer: audio["composer"] = composer
                        
                        if self.cover_action == "set" and self.staged_cover_bytes:
                            pic = Picture()
                            pic.data = self.staged_cover_bytes
                            pic.type = selected_cover_type_code
                            pic.mime = mime_type
                            pic.desc = "Cover"
                            audio.clear_pictures()
                            audio.add_picture(pic)
                        elif self.cover_action == "delete":
                            audio.clear_pictures()
                            
                        audio.save(deleteid3=True)
                        modified_files += 1
                except Exception as e:
                    self.log_tag(f" -> [TAG FAIL] {final_filename}: {e}")
            else:
                modified_files += 1

        self.log_tag("\n" + "="*50)
        self.log_tag(lang['log_tag_finish'].format(modified_files))
        self.log_tag("="*50)
        
        self.staged_cover_bytes = None
        self.cover_action = "keep"
        
        self.root.after(0, lambda: self.refresh_tag_listbox(target_dir))
        messagebox.showinfo(lang['msg_success_title'], lang['msg_success_body'].format(modified_files))
        self.end_process()

    def trigger_wipe_thread(self):
        if self.is_processing: return
        t = threading.Thread(target=self.start_wipe_process)
        t.daemon = True
        t.start()

    def start_wipe_process(self):
        self.is_processing = True
        lang = LANGUAGES[self.current_lang]
        self.tag_wipe_btn.configure(state="disabled", fg_color="#333333")
        self.tag_log_area.delete("1.0", tk.END)
        self.log_tag(lang['log_wipe_start'])
        
        target_dir = self.tag_path_entry.get().strip()
        selected_indices = self.tag_file_listbox.curselection()
        if selected_indices:
            files_to_process = [self.tag_file_listbox.get(i) for i in selected_indices]
        else:
            files_to_process = sorted([f for f in os.listdir(target_dir) if f.endswith(('.wav', '.mp3', '.flac', '.aif', '.aiff'))])
            
        wiped_count = 0
        for file in files_to_process:
            file_path = os.path.join(target_dir, file)
            try:
                if file.lower().endswith('.mp3'):
                    mutagen.mp3.delete(file_path)
                    wiped_count += 1
                    self.log_tag(lang['log_wiped'].format(file))
                elif file.lower().endswith('.wav'):
                    try: mutagen.wave.delete(file_path)
                    except: pass
                    write_wav_riff_info_tags(file_path, {})  
                    wiped_count += 1
                    self.log_tag(lang['log_wiped'].format(file))
                elif file.lower().endswith('.flac'):
                    try:
                        audio = FLAC(file_path)
                        audio.clear_pictures()  
                        try: audio.delete()     
                        except: pass
                        audio.save(deleteid3=True)
                    except:
                        pass
                    wiped_count += 1
                    self.log_tag(lang['log_wiped'].format(file))
                elif file.lower().endswith(('.aif', '.aiff')):
                    mutagen.aiff.delete(file_path)
                    wiped_count += 1
                    self.log_tag(lang['log_wiped'].format(file))
            except: pass
            
        self.log_tag("\n" + "="*50)
        self.log_tag(lang['log_wipe_finish'].format(wiped_count))
        self.log_tag("="*50)
        
        self.root.after(0, self.delete_cover_art_buffer)
        self.root.after(0, lambda: self.refresh_tag_listbox(target_dir))
        
        messagebox.showinfo(lang['msg_success_title'], lang['msg_success_body'].format(wiped_count))
        self.end_process()

    # --- ЛОГИКА DECONSTRUCTOR ---
    def log_decomp(self, message):
        tag = None
        msg_lower = message.lower()
        if any(x in msg_lower for x in ["[+]", "success", "unpacking", "scanning", "active"]):
            tag = "success"
        elif any(x in msg_lower for x in ["[!]", "error", "fail"]):
            tag = "error"
        elif any(x in msg_lower for x in ["[i]", "info", "analysing"]):
            tag = "info"
            
        self.log_area_decomp.insert(tk.END, message + "\n", tag)
        self.log_area_decomp.see(tk.END)

    def add_folder(self):
        if self.is_processing: return
        folder = filedialog.askdirectory()
        if folder:
            norm = os.path.normpath(folder)
            if norm not in self.scan_paths:
                self.scan_paths.append(norm)
                self.update_ui_text()
                self.log_decomp(LANGUAGES[self.current_lang]['log_added'].format(norm))

    def add_zip_file(self):
        if self.is_processing: return
        zip_file = filedialog.askopenfilename(filetypes=[("ZIP Archives", "*.zip")])
        if zip_file:
            norm = os.path.normpath(zip_file)
            if norm not in self.scan_paths:
                self.scan_paths.append(norm)
                self.update_ui_text()
                self.log_decomp(LANGUAGES[self.current_lang]['log_added'].format(norm))

    def show_add_target_menu(self):
        menu = tk.Menu(self.root, tearoff=0, bg="#111111", fg="#ffffff", activebackground="#bb86fc", activeforeground="#000000", bd=1, font=("Segoe UI", 12, "bold"))
        lang = LANGUAGES[self.current_lang]
        menu.add_command(label=lang['add_folder_btn'], command=self.add_folder)
        menu.add_command(label=lang['add_zip_btn'], command=self.add_zip_file)
        
        x = self.add_target_btn.winfo_rootx()
        y = self.add_target_btn.winfo_rooty() + self.add_target_btn.winfo_height()
        menu.post(x, y)

    def remove_selected_folder(self):
        if self.is_processing: return
        try:
            selected_idx = self.paths_listbox.curselection()[0]
            removed_folder = self.scan_paths[selected_idx]
            self.scan_paths.pop(selected_idx)
            self.update_ui_text()
            self.log_decomp(LANGUAGES[self.current_lang]['log_removed'].format(removed_folder))
        except IndexError:
            pass

    def clear_folders(self):
        if self.is_processing: return
        self.scan_paths = []
        self.update_ui_text()
        self.log_decomp(LANGUAGES[self.current_lang]['log_cleared'])

    def on_drop_sorter_paths(self, event):
        data = event.data
        paths = []
        if data:
            for p in re.findall(r'\{([^}]+)\}|(\S+)', data):
                path = p[0] if p[0] else p[1]
                paths.append(os.path.normpath(path))
        for p in paths:
            if os.path.exists(p) and (os.path.isdir(p) or p.lower().endswith('.zip')):
                if p not in self.scan_paths:
                    self.scan_paths.append(p)
                    self.log_decomp(LANGUAGES[self.current_lang]['log_added'].format(p))
        self.update_ui_text()

    def get_category_and_sub(self, filename):
        fn = filename.lower()
        tokens = re.findall(r'[a-z0-9#]+', fn)
        tokens_set = set(tokens)
        
        if 'tag' in tokens_set or 'tags' in tokens_set: return 'TAG', None
        if 'riser' in tokens_set or 'risers' in tokens_set or 'riser' in fn: return 'RISER', None
        if 'fx' in tokens_set or 'foley' in tokens_set or 'glitch' in tokens_set or 'ambient' in tokens_set or 'effect' in tokens_set or 'effects' in tokens_set: return 'FX', None
        if '808' in fn or 'bass' in tokens_set or 'sub' in tokens_set: return '808', None
        if 'openhat' in fn or 'ophat' in fn or 'oh' in tokens_set or (('open' in tokens_set or 'op' in tokens_set) and ('hat' in tokens_set or 'hats' in tokens_set)): return 'OPEN HAT', None
        if 'hihat' in fn or 'hh' in tokens_set or 'hat' in tokens_set or 'hats' in tokens_set: return 'HI HAT', None
        if 'clap' in tokens_set or 'claps' in tokens_set or 'snclap' in tokens_set or 'snclaps' in tokens_set: return 'CLAP', None
        if 'snare' in tokens_set or 'snares' in tokens_set: return 'SNARE', None
        if 'kick' in tokens_set or 'kicks' in tokens_set: return 'KICK', None
        
        perc_keywords = {'perc', 'percs', 'percussion', 'rim', 'rimshot', 'cowbell', 'bell', 'bells', 'triangle', 'stomp', 'shaker', 'snap', 'tom', 'cabasa', 'maraca', 'gunshot'}
        if any(t in perc_keywords for t in tokens_set) or 'perc' in fn or 'gunshot' in fn or 'bell' in fn:
            if 'rim' in tokens_set or 'rimshot' in tokens_set: return 'PERC', 'Rims'
            elif 'cowbell' in tokens_set or 'bell' in tokens_set or 'bells' in tokens_set: return 'PERC', 'Bells'
            elif 'shaker' in tokens_set: return 'PERC', 'Shakers'
            return 'PERC', 'Other_Percs'

        loop_keywords = {
            'loop', 'loops', 'bpm', 'key', 'waveloop', 'consolidated', 'melody', 'melodies',
            'adlib', 'adlibs', 'atmos', 'atmosphere', 'temper', 'cuts', 'sample', 'samples', 'pattern', 'patterns',
            'zenology', 'omnisphere', 'serum', 'kontakt', 'sylenth', 'nexus', 'vital'
        }
        has_strict_key = any(re.match(r'^[a-g](?:#|b)?(min|maj|minor|major)$', t) for t in tokens)
        has_split_key = any(t in {'maj', 'min', 'major', 'minor'} for t in tokens) and any(re.match(r'^[a-g]#?$', t) for t in tokens)
        has_bpm_number = any(t.isdigit() and 50 <= int(t) <= 195 for t in tokens)
        
        if (any(k in fn for k in loop_keywords) or any(t in loop_keywords for t in tokens_set) or 
            'track' in tokens_set or has_strict_key or has_split_key or has_bpm_number or re.search(r'\d+\s*bpm', fn)):
            return 'LOOPS & MELODIES', None

        if 'vox' in tokens_set or 'vocal' in tokens_set or 'chant' in tokens_set or 'vocals' in tokens_set: return 'VOX', None
        return None, None

    def get_file_md5(self, file_path):
        hasher = hashlib.md5()
        try:
            with open(file_path, 'rb') as f:
                buf = f.read(65536)
                while len(buf) > 0:
                    hasher.update(buf)
                    buf = f.read(65536)
            return hasher.hexdigest()
        except:
            return None

    def trigger_sorting_thread(self):
        if self.is_processing: return
        t = threading.Thread(target=self.start_sorting_process)
        t.daemon = True
        t.start()

    def start_sorting_process(self):
        self.is_processing = True
        lang = LANGUAGES[self.current_lang]
        self.start_btn.configure(state="disabled", fg_color="#333333", text=lang['processing_btn'])
        self.log_area_decomp.delete("1.0", tk.END)
        
        self.progress.pack(fill="x", padx=15, pady=5, before=self.start_btn)
        self.progress.set(0)
        
        kit_name = self.kit_name_entry.get().strip()
        base_dest = self.dest_dir if (self.dest_dir and os.path.exists(self.dest_dir)) else os.getcwd()
        
        if not kit_name:
            kit_name = "SOUND PACK"
        
        if not self.scan_paths:
            self.log_decomp(lang['err_empty'])
            self.end_process()
            return
            
        output_dir = os.path.join(base_dest, kit_name)
        os.makedirs(output_dir, exist_ok=True)
        
        zips_to_process = []
        folders_to_process = []
        
        for p in self.scan_paths:
            if os.path.exists(p):
                if os.path.isdir(p):
                    folders_to_process.append(p)
                elif p.lower().endswith('.zip'):
                    zips_to_process.append(p)
                    
        total_items = len(zips_to_process) + len(folders_to_process)
        if total_items == 0:
            self.log_decomp(lang['err_no_items'])
            self.end_process()
            return
            
        self.log_decomp(lang['log_analysing'].format(total_items))
        
        extracted_count = 0
        unsorted_count = 0
        duplicate_count = 0
        processed_count = 0
        
        seen_hashes = set()
        
        for zip_path in zips_to_process:
            zip_name = os.path.basename(zip_path)
            self.log_decomp("\n" + lang['log_unpacking'].format(zip_name))
            
            try:
                with zipfile.ZipFile(zip_path, 'r') as archive:
                    for member in archive.namelist():
                        if member.endswith('/') or member.lower().endswith('.flp'):
                            continue
                        
                        base_filename = os.path.basename(member)
                        if not base_filename.endswith(('.wav', '.mp3', '.flac')):
                            continue
                            
                        if self.dupe_filter_var.get():
                            with archive.open(member) as f_mem:
                                file_data = f_mem.read()
                                file_hash = hashlib.md5(file_data).hexdigest()
                                if file_hash in seen_hashes:
                                    duplicate_count += 1
                                    continue
                                seen_hashes.add(file_hash)
                        
                        cat, subcat = self.get_category_and_sub(base_filename)
                        
                        if cat:
                            if subcat: final_folder = os.path.join(output_dir, cat, subcat)
                            else: final_folder = os.path.join(output_dir, cat)
                            extracted_count += 1
                        else:
                            final_folder = os.path.join(output_dir, 'Unsorted_Trash')
                            unsorted_count += 1
                            
                        new_name = base_filename
                        target_path = os.path.join(final_folder, new_name)
                        
                        if os.path.exists(target_path):
                            name_part, ext_part = os.path.splitext(new_name)
                            counter = 1
                            while os.path.exists(os.path.join(final_folder, f"{name_part}_{counter}{ext_part}")):
                                counter += 1
                            target_path = os.path.join(final_folder, f"{name_part}_{counter}{ext_part}")
                        
                        os.makedirs(final_folder, exist_ok=True)
                        
                        with archive.open(member) as source, open(target_path, 'wb') as target:
                            shutil.copyfileobj(source, target)
                            
            except Exception as e:
                self.log_decomp(f"[!] {zip_name}: {e}")
                
            processed_count += 1
            self.progress.set(processed_count / total_items)
            self.root.update_idletasks()

        for folder_path in folders_to_process:
            folder_name = os.path.basename(folder_path)
            self.log_decomp("\n" + lang['log_scanning_folder'].format(folder_name))
            
            for root_dir, dirs, files in os.walk(folder_path):
                if os.path.abspath(root_dir).startswith(os.path.abspath(output_dir)):
                    continue
                    
                for file in files:
                    if file.lower().endswith(('.wav', '.mp3', '.flac')):
                        file_src_path = os.path.join(root_dir, file)
                        
                        if self.dupe_filter_var.get():
                            file_hash = self.get_file_md5(file_src_path)
                            if file_hash:
                                if file_hash in seen_hashes:
                                    duplicate_count += 1
                                    if self.move_mode_var.get():
                                        try: os.remove(file_src_path)
                                        except: pass
                                    continue
                                seen_hashes.add(file_hash)
                        
                        cat, subcat = self.get_category_and_sub(file)
                        if cat:
                            if subcat: final_folder = os.path.join(output_dir, cat, subcat)
                            else: final_folder = os.path.join(output_dir, cat)
                            extracted_count += 1
                        else:
                            final_folder = os.path.join(output_dir, 'Unsorted_Trash')
                            unsorted_count += 1
                            
                        target_path = os.path.join(final_folder, file)
                        
                        if os.path.exists(target_path):
                            name_part, ext_part = os.path.splitext(file)
                            counter = 1
                            while os.path.exists(os.path.join(final_folder, f"{name_part}_{counter}{ext_part}")):
                                counter += 1
                            target_path = os.path.join(final_folder, f"{name_part}_{counter}{ext_part}")
                            
                        os.makedirs(final_folder, exist_ok=True)
                        
                        try:
                            if self.move_mode_var.get():
                                shutil.move(file_src_path, target_path)
                            else:
                                shutil.copy2(file_src_path, target_path)
                        except Exception as e:
                            self.log_decomp(f" -> [FAIL] {file}: {e}")
            
            if self.move_mode_var.get():
                for root_dir, dirs, files in os.walk(folder_path, topdown=False):
                    if not os.listdir(root_dir):
                        try: os.rmdir(root_dir)
                        except: pass
                        
            processed_count += 1
            self.progress.set(processed_count / total_items)
            self.root.update_idletasks()
                
        self.log_decomp("\n" + "="*50)
        self.log_decomp(lang['log_success_hdr'])
        self.log_decomp(lang['log_success_ext'].format(extracted_count))
        self.log_decomp(lang['log_success_trsh'].format(unsorted_count))
        self.log_decomp(lang['log_success_dupes'].format(duplicate_count))
        self.log_decomp("="*50)
        
        # ГЕНЕРАЦИЯ TXT ИНВЕНТАРЯ (ЧЕК-ЛИСТ ПАКА)
        try:
            inventory_path = os.path.join(output_dir, f"{kit_name}_Inventory.txt")
            with open(inventory_path, "w", encoding="utf-8") as inv_file:
                inv_file.write(f"=== {kit_name.upper()} | CONTENT INVENTORY ===\n\n")
                total_in_pack = 0
                for item in sorted(os.listdir(output_dir)):
                    item_path = os.path.join(output_dir, item)
                    if os.path.isdir(item_path):
                        count = sum(len(f) for r, d, f in os.walk(item_path))
                        inv_file.write(f" ► {item}: {count} files\n")
                        total_in_pack += count
                inv_file.write(f"\nTotal Audio Elements: {total_in_pack}\n")
                inv_file.write("=======================================\n")
                inv_file.write(f"Generated by SSPECTRA AUDIO LAB {APP_VERSION}\n")
        except Exception as e:
            self.log_decomp(f"[!] Inventory gen error: {e}")
        
        try: os.startfile(output_dir)
        except: pass
            
        messagebox.showinfo(lang['msg_success_title'], lang['msg_success_body'].format(extracted_count, duplicate_count))
        self.end_process()

    def end_process(self):
        self.is_processing = False
        self.staged_cover_bytes = None
        self.cover_action = "keep"
        try: self.progress.pack_forget()
        except: pass
        self.update_ui_text()

    def open_bug_report_window(self):
        lang = LANGUAGES[self.current_lang]
        bug_win = ctk.CTkToplevel(self.root)
        bug_win.title(lang['bug_win_title'])
        self.center_window(bug_win, 500, 500)
        bug_win.resizable(False, False)
        bug_win.configure(fg_color="#0a0a0a")
        bug_win.transient(self.root)
        bug_win.grab_set()
        
        # Динамический список путей прикрепленных картинок
        attached_image_paths = []
        
        # Поле "Тема"
        ctk.CTkLabel(bug_win, text=lang['bug_win_subject'], font=("Segoe UI", 11, "bold"), text_color="#bb86fc").pack(anchor="w", padx=30, pady=(20, 2))
        subject_entry = ctk.CTkEntry(bug_win, font=("Segoe UI", 11), fg_color="#141414", border_color="#2d2d2d", height=30)
        subject_entry.pack(fill="x", padx=30)
        
        # Поле "Описание"
        ctk.CTkLabel(bug_win, text=lang['bug_win_desc'], font=("Segoe UI", 11, "bold"), text_color="#bb86fc").pack(anchor="w", padx=30, pady=(15, 2))
        desc_text = tk.Text(bug_win, font=("Segoe UI", 10), bg="#141414", fg="#ffffff", insertbackground="white", bd=1, relief="flat", highlightbackground="#2d2d2d", highlightthickness=1, height=8)
        desc_text.pack(fill="x", padx=30)
        
        # Панель аттачментов
        attach_frame = ctk.CTkFrame(bug_win, fg_color="transparent")
        attach_frame.pack(fill="x", padx=30, pady=15)
        
        limit_lbl = ctk.CTkLabel(attach_frame, text=lang['bug_win_limit'].format(0), font=("Segoe UI", 11), text_color="#aaaaaa")
        limit_lbl.pack(side="right")
        
        def attach_photos():
            if len(attached_image_paths) >= 10:
                return
            files = filedialog.askopenfilenames(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
            if files:
                for f in files:
                    if len(attached_image_paths) < 10 and f not in attached_image_paths:
                        attached_image_paths.append(os.path.normpath(f))
                limit_lbl.configure(text=lang['bug_win_limit'].format(len(attached_image_paths)))
                
        attach_btn = ctk.CTkButton(attach_frame, text=lang['bug_win_attach'], font=("Segoe UI", 11), fg_color="#1a1a1a", hover_color="#2d2d2d", text_color="#bb86fc", width=200, height=28, command=attach_photos)
        attach_btn.pack(side="left")
        
        def send_report():
            subject = subject_entry.get().strip()
            description = desc_text.get("1.0", tk.END).strip()
            if not subject or not description:
                return
                
            # Блокируем интерфейс на время отправки
            submit_btn.configure(state="disabled", text=lang['bug_win_sending'], fg_color="#333333")
            attach_btn.configure(state="disabled")
            
            # Запускаем отправку в фоновом потоке, чтобы окно интерфейса не зависало
            t = threading.Thread(target=perform_send, args=(subject, description, list(attached_image_paths)))
            t.daemon = True
            t.start()
            
        def perform_send(subject, description, image_paths):
            try:
                images_payload = []
                for p in image_paths:
                    name = os.path.basename(p)
                    with open(p, "rb") as img_file:
                        b64_data = base64.b64encode(img_file.read()).decode('utf-8')
                    images_payload.append({
                        "name": name,
                        "base64": b64_data
                    })
                    
                payload = {
                    "subject": subject,
                    "description": description,
                    "images": images_payload
                }
                
                json_bytes = json.dumps(payload).encode('utf-8')
                
                # Вставьте сюда скопированный URL-адрес вашего веб-приложения Google Script:
                url = "https://script.google.com/macros/s/AKfycbxwOkbfYnXd-VRdBcV-oZKpeDMN9FJpUN0VPHKaRg9ZnAwyryvpACthCsj9WvZePVyJ/exec"
                
                req = urllib.request.Request(
                    url,
                    data=json_bytes,
                    headers={'Content-Type': 'application/json'}
                )
                
                with urllib.request.urlopen(req) as response:
                    res_body = response.read().decode('utf-8')
                    res_json = json.loads(res_body)
                    
                if res_json.get("status") == "success":
                    bug_win.after(0, lambda: messagebox.showinfo(lang['msg_success_title'], lang['bug_win_success']))
                    bug_win.after(0, bug_win.destroy)
                else:
                    raise Exception(res_json.get("message", "Unknown script error"))
            except Exception as e:
                # В случае ошибки разблокируем кнопки
                bug_win.after(0, lambda: messagebox.showerror("Error", f"{lang['bug_win_fail']}\nDetails: {e}"))
                bug_win.after(0, lambda: submit_btn.configure(state="normal", text=lang['bug_win_submit'], fg_color="#bb86fc"))
                bug_win.after(0, lambda: attach_btn.configure(state="normal"))
                
        submit_btn = ctk.CTkButton(bug_win, text=lang['bug_win_submit'], font=("Segoe UI", 12, "bold"), fg_color="#bb86fc", hover_color="#cda3ff", text_color="#000000", height=40, command=send_report)
        submit_btn.pack(fill="x", padx=30, pady=(10, 20))

if __name__ == "__main__":
    if HAS_DND:
        class CTkDND(ctk.CTk, TkinterDnD.DnDWrapper):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                try:
                    self.TkdndVersion = TkinterDnD._require(self)
                except Exception:
                    pass
        root = CTkDND()
    else:
        root = ctk.CTk()
        
    app = SpectraAudioLabApp(root)
    
    try:
        if os.path.exists("icon.ico"):
            root.iconbitmap("icon.ico")
        elif os.path.exists("icon.png"):
            img = tk.PhotoImage(file="icon.png")
            root.tk.call('wm', 'iconphoto', root._w, img)
    except Exception:
        pass
        
    root.withdraw()
    splash = SplashWindow(root)
    
    def launch_main_app():
        if splash.winfo_exists():
            root.after(100, launch_main_app)
        else:
            root.update_idletasks()
            w_width, w_height = 1000, 760
            s_width = root.winfo_screenwidth()
            s_height = root.winfo_screenheight()
            x = (s_width - w_width) // 2
            y = (s_height - w_height) // 2
            root.geometry(f"{w_width}x{w_height}+{x}+{y}")
            root.deiconify()  
            
    root.after(100, launch_main_app)
    root.mainloop()

