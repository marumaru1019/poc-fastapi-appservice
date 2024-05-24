## FastAPIアプリケーションをAzure App Serviceにコンテナとしてデプロイする手順

### ローカルでの動作確認

Azureにデプロイする前に、ローカルでFastAPIアプリケーションが正常に動作することを確認します。

#### 1. Dockerイメージのビルド

ターミナルで以下のコマンドを実行し、Dockerイメージをビルドします。

```bash
docker build -t <Dockerイメージ名>:<タグ> .
```

##### 補足説明
| パラメータ         | 説明                      |
|--------------------|---------------------------|
| Dockerイメージ名   | 任意のDockerイメージの名前(半角英数字で作成する必要があります)      |
| タグ               | 任意のDockerイメージのタグ (v1, v2 等の識別子)      |

#### 2. Dockerコンテナの起動

ビルドしたDockerイメージを使用して、ローカルでコンテナを起動します。

```bash
docker run -d -p 8000:8000 <Dockerイメージ名>:<タグ>
```

##### 補足説明
| パラメータ         | 説明                      |
|--------------------|---------------------------|
| Dockerイメージ名   | 作成したDockerイメージの名前      |
| タグ               | 作成したDockerイメージのタグ      |

#### 3. アプリケーションの動作確認

ブラウザで `http://localhost:8000` にアクセスし、FastAPIアプリケーションが正常に動作していることを確認します。また、FastAPIの自動生成されたAPIドキュメントにアクセスするには、`http://localhost:8000/docs` にアクセスします。<br>
正しくFastAPIアプリケーションが動作している場合、以下のような画面が表示されます。

![image](https://github.com/marumaru1019/poc-fastapi-appservice/assets/70362624/0680e920-2126-43b7-9f06-4bd54d73db9b)


##### `app.main:app` の部分の補足説明

- `app` は FastAPIアプリケーションのディレクトリです。
- `main` はアプリケーションを定義しているPythonファイルの名前です（`.py` 拡張子を除く）。
- `app` は FastAPI インスタンスの名前です。

例：ディレクトリ構造が以下のようになっている場合

```
/app
  ├── app
  │    ├── __init__.py
  │    ├── main.py  # ここに FastAPI インスタンスを定義
  └── Dockerfile
```

`main.py` の内容が以下のようであるとします：

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
```

この場合、`app.main:app` は `app` ディレクトリの `main.py` ファイル内の `app` という名前の FastAPI インスタンスを指します。
別のケースで`app/api/main.py`というパスにFastAPIインスタンスがある場合、`app.api.main:app`と指定します。

### Azure App Serviceへのデプロイ手順

#### 1. **ACRの作成**
下記のコマンドで Azure Container Registry (ACR) を作成します。

   ```bash
   az acr create --resource-group <リソースグループ名> --name <ACR名> --sku <SKU> --admin-enabled true
   ```

##### 補足説明
| パラメータ         | 説明                       |
|--------------------|----------------------------|
| リソースグループ名 | 作成したリソースグループ名 |
| ACR名              | 任意のACRの名前          |
| SKU              | ACRのSKU（Basic, Premium, Standard の 3 種類）     |

#### 2. **ACRにログイン**
下記のコマンドで ACR にログインします。ログインが成功すると、`Login Succeeded` と表示されます。

   ```bash
   az acr login --name <ACR名>
   ```

##### 補足説明
| パラメータ | 説明                  |
|------------|-----------------------|
| ACR名      | 作成したACRの名前     |

3. **Dockerイメージをプッシュ**

   ```bash
   docker tag <Dockerイメージ名>:<タグ> <ACR名>.azurecr.io/<Dockerイメージ名>:<タグ>
   docker push <ACR名>.azurecr.io/<Dockerイメージ名>:<タグ>
   ```

##### 補足説明
| パラメータ         | 説明                      |
|--------------------|---------------------------|
| Dockerイメージ名   | Dockerイメージの名前      |
| タグ               | Dockerイメージのタグ      |
| ACR名.azurecr.io   | ACRのドメイン名           |

#### 3. **App Serviceプランを作成**

   ```bash
   az appservice plan create --name <プラン名> --resource-group <リソースグループ名> --is-linux --sku <SKU>
   ```

##### 補足説明
| パラメータ         | 説明                           |
|--------------------|--------------------------------|
| プラン名           | 作成するApp Serviceプランの名前 |
| リソースグループ名 | 作成したリソースグループ名     |
| SKU                 | App ServiceプランのSKU |

#### 3. **Webアプリケーションを作成**

   ```bash
   az webapp create --resource-group <リソースグループ名> --plan <プラン名> --name <App Service名> --deployment-container-image-name <レジストリ>/<Dockerイメージ名>:<タグ>
   ```

   例：

   ```bash
   az webapp create --resource-group myResourceGroup --plan myAppServicePlan --name myFastAPIApp --deployment-container-image-name myacr.azurecr.io/myfastapiapp:latest
   ```

##### 補足説明
| パラメータ                    | 説明                                    |
|-------------------------------|-----------------------------------------|
| リソースグループ名            | 作成したリソースグループ名              |
| プラン名                      | 作成したApp Serviceプランの名前         |
| App Service名                 | 作成するWebアプリケーションの名前       |
| レジストリ/Dockerイメージ名:タグ | デプロイするDockerイメージの名前とタグ |

#### 5. 環境変数の設定（必要な場合）

環境変数を設定するには、以下のコマンドを使用します。

```bash
az webapp config appsettings set --resource-group <リソースグループ名> --name <App Service名> --settings KEY=VALUE
```

##### 補足説明
| パラメータ         | 説明                              |
|--------------------|-----------------------------------|
| リソースグループ名 | 作成したリソースグループ名         |
| App Service名      | 作成したWebアプリケーションの名前  |
| KEY                | 設定する環境変数のキー             |
| VALUE              | 設定する環境変数の値               |

#### 6. アプリケーションの起動確認

ブラウザで `https://<App Service名>.azurewebsites.net/docs` にアクセスして、FastAPIアプリケーションが正常に動作していることを確認します。
正しくFastAPIアプリケーションが動作している場合、以下のような画面が表示されます。

![image](https://github.com/marumaru1019/poc-fastapi-appservice/assets/70362624/93f25e07-9ef8-432c-a152-5f4a23d69ac3)
