Python SDK for blastengine

Python向けのblastengine用SDKです。

## 使い方

### インポート

```py
from blastengine.Client import Blastengine
from blastengine.Transaction import Transaction
```

### 初期化

```py
Blastengine('USER_NAME', 'API_KEY')
```

### トランザクション（即時発送）メール

```py
transaction = Transaction()
transaction.subject('test mail')
transaction.text_part('mail body')
transaction.fromAddress('info@opendata.jp')
transaction.to('atsushi@moongift.jp')
```

#### 送信

```py
try:
	delivery_id = transaction.send()
	print(delivery_id)
except Exception as e:
	print(e)
```

## License

MIT License



print(res)