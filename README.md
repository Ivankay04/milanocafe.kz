# Сайт кафе «Милано» — milanocafe.kz (GitHub Pages)

- `index.html` — русская версия, `kz/index.html` — казахская. Вручную не править: обе собираются из `src/template.html` командой `python3 src/build.py` (правки делает Claude).
- `assets/img/`, `assets/video/` — фото и видео, имена файлов — в `ФОТО-И-ВИДЕО.md`.
- `CNAME` — домен для GitHub Pages, не удалять.
- Заказы, брони, обед дня и стоп-лист обрабатывает отдельный сервер на Railway (репозиторий `milano-bot`). Его адрес вписан в `src/build.py` → `API_URL`.
