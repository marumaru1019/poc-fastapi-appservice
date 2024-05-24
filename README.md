# FastAPI アプリケーションのAzure App Serviceへのデプロイ手順

## 構成手順
以下を構成、実装する事でAzure App Service上にFastAPIアプリケーションをデプロイします。

### 事前準備
#### GitHubからアプリケーションをクローン
1. GitHubからアプリケーションをクローンします。

```bash
git clone https://github.com/marumaru1019/poc-fastapi-appservice.git
cd poc-fastapi-appservice
```

#### ローカルでの動作確認
1. `requirements.txt` ファイルの内容をインストールします。

```bash
pip install -r requirements.txt
```

2. 以下のコマンドでローカルサーバーを起動し、アプリケーションが正しく動作するか確認します。

```bash
uvicorn app.main:app --reload
```


ブラウザで `http://127.0.0.1:8000/docs` にアクセスし、アプリケーションが正常に動作していることを確認します。
下記のような画面が出力されれば成功です。

![image](https://github.com/marumaru1019/github-image/assets/70362624/94e1790a-9aa2-4779-8726-9b08af6e546f)

### アプリケーションのデプロイ
#### Azure CLIでのログイン
1. Azure CLIを使用してAzureにログインします。

```bash
az login
```

ブラウザが開き、Azureアカウントへのログインを求められます。ログインが完了すると、ターミナルにサインイン成功のメッセージが表示されます。

#### リソースグループの作成 (Optional)
1. Azureにリソースグループを作成します。<br>※既に作成済の場合はスキップしてください。

```bash
az group create --name <リソースグループ> --location japaneast
```

| パラメータ       | 説明                                             |
|------------------|--------------------------------------------------|
| リソースグループ | 任意のリソースグループ名。|

#### App Serviceプランの作成
1. 次に、App Serviceプランを作成します。

```bash
az appservice plan create --name <AppServiceプラン> --resource-group <リソースグループ> --sku <SKU> --is-linux
```

##### 補足説明
| パラメータ        | 説明                                         |
|-------------------|----------------------------------------------|
| AppServiceプラン  | 任意のApp Serviceプラン名。                  |
| リソースグループ  | 作成したリソースグループ名。                  |
| SKU        | 使用する価格プランです。[価格オプション](https://azure.microsoft.com/ja-jp/pricing/details/app-service/linux/)についてはこちらをご覧ください。指定できる値は[こちら](https://learn.microsoft.com/ja-jp/cli/azure/appservice/plan?view=azure-cli-latest)の `--sku` の説明をご覧ください。      |

#### Webアプリケーションの作成
1. Webアプリケーションを作成します。

```bash
az webapp create --resource-group <リソースグループ> --plan <AppServiceプラン> --name <Webアプリケーション名> --runtime "PYTHON:3.x"
```

##### 補足説明
| パラメータ          | 説明                                         |
|---------------------|----------------------------------------------|
| リソースグループ    | 作成したリソースグループ名。                  |
| AppServiceプラン    | 作成したApp Serviceプラン名。                |
| Webアプリケーション名 | 任意のWebアプリケーション名。                 |
| "PYTHON:3.x" | Python 3.x ランタイムを指定。        |

#### スタートアップコマンドの設定
1. スタートアップコマンドを設定します。

```bash
az webapp config set --resource-group <リソースグループ名> --name <Webアプリケーション名> --startup-file "./startup.sh"
```

##### 補足説明
| パラメータ          | 説明                                         |
|---------------------|----------------------------------------------|
| リソースグループ    | 作成したリソースグループ名。                  |
| Webアプリケーション名      | 作成したWebアプリケーション名。                       |


#### アプリケーションのデプロイ
1. デプロイの準備として、クローンしたリポジトリのディレクトリに移動し、以下のコマンドを実行します(このコマンドは、必ずプロジェクトのルートディレクトリから行ってください)。<br>※ アプリケーションの変更を行ってアップデートする際にも、このコマンドを実行してください。

```bash
az webapp up --resource-group <リソースグループ> --name <Webアプリケーション名> --sku <SKU> --runtime "PYTHON:3.x"
```

##### 補足説明
| パラメータ          | 説明                                         |
|---------------------|----------------------------------------------|
| リソースグループ    | 作成したリソースグループ名。                  |
| Webアプリケーション名 | 作成したWebアプリケーション名。                 |
| SKU         | 作成した App Service Plan の SKU を指定。        |
| "PYTHON:3.x" | Python 3.x ランタイムを指定。        |

### アプリケーションの確認
1. ブラウザで`https://<Webアプリケーション名>.azurewebsites.net/docs`にアクセスし、アプリケーションが正しく動作していることを確認します。<br>
下記のように、APIドキュメントが表示されれば成功です。
![image](https://github.com/marumaru1019/github-image/assets/70362624/925988cc-a97c-4676-8896-2cf0c030dd5f)


## 動作確認
1. ブラウザで `https://<Webアプリケーション名>.azurewebsites.net/docs` にアクセスし、APIドキュメントが表示されることを確認します。
2. APIドキュメントの `GET /embed` の `Try it out` ボタンをクリックし、`sentence` パラメータに任意の文字列を入力し、`Execute` ボタンをクリックします。
3. レスポンスが返却され、embddingされたベクトルが表示されれば成功です。
![image](https://github.com/marumaru1019/github-image/assets/70362624/8dfe6025-3fa2-4891-a958-d67486e9a320)
