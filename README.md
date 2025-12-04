# py-works

Python 開発環境のコンテナ

<!-- TOC -->

- [1. Features](#1-features)
  - [1.1. 基本機能](#11-基本機能)
- [2. Getting Started](#2-getting-started)
  - [2.1. Prerequisites](#21-prerequisites)
    - [2.1.1. ソフトウェア要件](#211-ソフトウェア要件)
- [3. Usage](#3-usage)
  - [3.1. Redmine REST API の使用時](#31-redmine-rest-api-の使用時)
- [4. Author](#4-author)

<!-- /TOC -->

## 1. Features

### 1.1. 基本機能

- Visual Studio Code の Dev Containers 対応開発コンテナ
- Python 開発環境
- ユニットテスト環境 (pytest)

## 2. Getting Started

### 2.1. Prerequisites

#### 2.1.1. ソフトウェア要件

CPU アーキテクチャが x86_64 (amd64) で、以下のソフトウェアがインストールされていること

- Visual Studio Code + Remote Development 拡張機能 (※)
- Git クライアント (※※)
- Docker Compose V2 (※※)

※ ホスト OS にインストールする
※※ ホスト OS が Windows の場合は、WSL2 上の Linux にインストールする

## 3. Usage

### 3.1. Redmine REST API の使用時

- `/workspace/.env.local` を作成して以下の例のように環境変数を定義する
- `API_KEY` の値は Redmine の個人設定 ＞ APIアクセスキー で作成する
- `API_URL` の値は `プロトコル://ホスト[:ポート]`

```shell
API_KEY=0123456789abcdef0123456789abcdef01234567
API_URL=http://redmine.wk.aruze.co.jp:3000
```

```shell
API_KEY=0123456789abcdef0123456789abcdef01234567
API_URL=http://localhost
```

## 4. Author

ishida
