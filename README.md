# 🩺 medagg-search

Мини-проект: поиск по медицинским датасетам (русские и английские запросы).  
На вход — строка запроса, на выход — топ-K датасетов и JSON-теги для внешнего API (например, Kaggle).

---

## 🚀 Запуск

```bash
# установка окружения
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# пример поиска
python -m medsearch.search "КТ легких пневмония классификация" --k 3
python -m medsearch.search "МРТ мозга глиома сегментация" --k 3
python -m medsearch.search "глазное дно диабетическая ретинопатия классификация" --k 3
```

---

## ⚙️ Что внутри

```
medagg-search/
├─ medsearch/
│  ├─ data.py              # синтетические карточки датасетов
│  ├─ scoring.py           # TF-IDF + бонусы за совпадение тегов
│  ├─ parsing.py           # парсинг запроса (через YAML-таксономию)
│  ├─ config_loader.py     # загрузка и компиляция YAML
│  └─ config/
│     └─ taxonomy.yaml     # редактируемые паттерны и стоп-слова (RU/EN)
├─ main.py                 # точка входа (CLI)
├─ requirements.txt
└─ README.md
```

---

## 🧩 Пример вывода

```
Parsed slots: {'modality': ['CT'], 'tasks': ['classification'], 'organs': ['lung'], 'diseases': ['pneumonia']}
API tags: {'modality': ['CT'], 'organ': ['lung'], 'disease': ['pneumonia'], 'task': ['classification'], 'keywords': ['кт','легких','пневмония','классификация']}

Top-3 results:
[1] Lung CT for Pneumonia Classification (score=4.47)
[2] Chest CT Lung Cancer Screening
[3] Chest X-Ray COVID-19 Detection
```

---

## 🛠 Как редактировать теги

Файл: `medsearch/config/taxonomy.yaml`

Пример добавления болезни:
```yaml
diseases:
  - label: hepatitis
    patterns:
      - "\\bhepatitis\\b"
      - "гепатит"
```

После правки просто перезапусти скрипт.

---

Респект и уважуха, братуха нубяра! 😎✌️
