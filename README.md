# micro-billing [![Build Status](https://app.travis-ci.com/izumimatsuo/micro-billing.svg?branch=main)](https://app.travis-ci.com/izumimatsuo/micro-billing)

環境構築

```
$ python3 -m venv .venv
$ source .venv/bin/activate
(.venv) $ pip install --upgrade pip
(.venv) $ pip install -r requirements.txt
```

実行

```
(.venv) $ FLASK_ENV=development flask run
```

テスト
```
(.venv) $ pytest
(.venv) $ coverage run -m pytest
(.venv) $ coverage report
```

開発環境 venv
静的チェック flake8
PEP8準拠コードフォーマット black
type hintをチェック mypy
自動テスト pytest

