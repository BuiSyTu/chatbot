# Chatbot

[![Build Status](https://travis-ci.org/archiverjs/node-archiver.svg?branch=master)](https://www.tandan.com.vn/)
[More info](https://www.tandan.com.vn/)

## Prerequisites

- Cài ODBC Driver 13

    - `https://www.microsoft.com/en-us/download/details.aspx?id=50420`

- Cài Visual C++ 14.0

    - `https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=BuildTools&rel=16`

## Quick start
- Tạo database như sau
```sql
    CREATE DATABASE chatbot
```

- Cài đặt một số thư viện
```Python
  > pip install -r requirements.txt
```

- Di chuyển đến thư mục chương trình
```Python
  > cd tdai
```

- Migration
```Python
  > python manage.py makemigrations
  > python manage.py migrate
```

- Chạy chương trình

```Python
  > python manage.py runserver
```

## Contributors
