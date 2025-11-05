# 🩺 medagg-search

Мини-проект: поиск по медицинским датасетам (русские и английские запросы).

Ветка для работы с модулями git.

---

## Создание модуля

```bash
# добавление модуля в директорию с названием medsearch
git submodule add -b submodule -- https://github.com/ESBehtev/medagg-search.git ./medsearch
```

---

## ⚙️ Что внутри

```
medsearch/
├─ data.py              # синтетические карточки датасетов
├─ scoring.py           # TF-IDF + бонусы за совпадение тегов
├─ parsing.py           # парсинг запроса (через YAML-таксономию)
├─ config_loader.py     # загрузка и компиляция YAML
├─ config_loader/
│  └─ taxonomy.yaml     # редактируемые паттерны и стоп-слова (RU/EN)
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

Файл: `config/taxonomy.yaml`

Пример добавления болезни:
```yaml
diseases:
  - label: hepatitis
    patterns:
      - "\\bhepatitis\\b"
      - "гепатит"
```

---

Респект и уважуха, братуха нубяра! 😎✌️
