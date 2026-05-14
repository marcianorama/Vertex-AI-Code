# Vertex AI Chatbot Project

Project ini adalah contoh implementasi chatbot berbasis **Google Vertex AI Reasoning Engine** dengan antarmuka web menggunakan **Flask**. Di dalam repository ini juga tersedia contoh service API pihak ketiga sederhana yang dapat digunakan sebagai mock/proxy API saat pengembangan agent.

## Ringkasan Fitur

- Web chatbot dengan UI sederhana berbasis HTML, CSS, dan JavaScript.
- Integrasi ke Google Vertex AI Reasoning Engine.
- Session ID unik untuk setiap percakapan.
- Proteksi endpoint chat menggunakan header `x-api-key`.
- Dukungan input teks pada UI chatbot.
- Tersedia tombol voice recording pada UI. Catatan: endpoint backend `/process_audio` belum tersedia di implementasi saat ini.
- Contoh service API pihak ketiga menggunakan Flask dan `requests`.
- Catatan command untuk deploy ke Google Cloud Run.

## Struktur Project

```text
.
├── README.md
├── .gitignore
├── vertext_ai.ipynb
├── api_third_party/
│   ├── app.py
│   └── requirements.txt
├── chatbot_app/
│   ├── app.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── config/
│   │   └── settings.py
│   ├── templates/
│   │   └── index.html
│   └── utils/
│       └── utils.py
└── catatan/
    ├── create_data_store.txt
    ├── gcloud run command.txt
    ├── link gcloud.txt
    └── tutorial setup gcloud untuk agent engine.txt
```

## Komponen Utama

### 1. `chatbot_app`

Aplikasi utama chatbot berbasis Flask.

Endpoint yang tersedia:

| Method | Endpoint | Deskripsi | Auth |
|---|---|---|---|
| `GET` | `/` | Menampilkan halaman chatbot | Tidak |
| `GET` | `/new_session` | Membuat session ID baru | Tidak |
| `POST` | `/chat` | Mengirim pesan user ke Vertex AI Reasoning Engine | Ya, `x-api-key` |

Contoh request ke endpoint chat:

```bash
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_APP_API_KEY" \
  -d "{\"query\": \"Halo\", \"session_id\": \"default\"}"
```

### 2. `api_third_party`

Service Flask sederhana untuk contoh API pihak ketiga.

Endpoint yang tersedia:

| Method | Endpoint | Deskripsi |
|---|---|---|
| `GET` | `/locations` | Melakukan request ke upstream API dan mengembalikan response JSON |

Contoh request:

```bash
curl "http://localhost:8080/locations?q=Coffee&location=Austin"
```

### 3. `vertext_ai.ipynb`

Notebook untuk eksperimen/setup Vertex AI Agent atau Reasoning Engine.

### 4. `catatan`

Folder berisi catatan command dan referensi untuk setup Google Cloud, data store, serta deployment.

## Prasyarat

Pastikan sudah terinstall:

- Python 3.10 atau lebih baru.
- `pip`.
- Google Cloud CLI (`gcloud`) jika ingin deploy ke Google Cloud Run.
- Project Google Cloud dengan Vertex AI API aktif.
- Service account JSON dengan permission yang sesuai.
- Reasoning Engine yang sudah dibuat di Vertex AI.

## Setup Environment Chatbot App

Masuk ke folder aplikasi chatbot:

```bash
cd chatbot_app
```

Buat virtual environment:

```bash
python -m venv .venv
```

Aktifkan virtual environment.

Windows CMD:

```cmd
.venv\Scripts\activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Install dependency:

```bash
pip install -r requirements.txt
```

Copy file environment example:

```bash
copy .env.example .env
```

Untuk Linux/macOS:

```bash
cp .env.example .env
```

Isi file `.env`:

```env
ENGINE_NAME=projects/YOUR_PROJECT_NUMBER/locations/YOUR_LOCATION/reasoningEngines/YOUR_ENGINE_ID
API_KEY=YOUR_APP_API_KEY
PROJECT_ID=YOUR_PROJECT_ID
LOCATION=YOUR_LOCATION
STAGING_BUCKET=gs://YOUR_STAGING_BUCKET
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account.json
```

Keterangan variable:

| Variable | Deskripsi |
|---|---|
| `ENGINE_NAME` | Resource name dari Vertex AI Reasoning Engine. |
| `API_KEY` | API key internal untuk proteksi endpoint `/chat`. |
| `PROJECT_ID` | ID project Google Cloud. |
| `LOCATION` | Region Vertex AI, contoh `asia-southeast1` atau `us-central1`. |
| `STAGING_BUCKET` | Cloud Storage bucket untuk staging Vertex AI. |
| `GOOGLE_APPLICATION_CREDENTIALS` | Path file service account JSON. |

Jalankan aplikasi:

```bash
python app.py
```

Aplikasi akan berjalan di:

```text
http://localhost:8080
```

## Setup API Third Party

Masuk ke folder service API:

```bash
cd api_third_party
```

Buat dan aktifkan virtual environment jika belum:

```bash
python -m venv .venv
```

Windows CMD:

```cmd
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Install dependency:

```bash
pip install -r requirements.txt
```

Jalankan service:

```bash
python app.py
```

Jika ingin menjalankan dengan Gunicorn saat production:

```bash
gunicorn -b 0.0.0.0:8080 app:app
```

## Deploy ke Google Cloud Run

Login ke Google Cloud:

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

Set credential lokal jika diperlukan:

Windows CMD:

```cmd
set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\your\service-account.json
```

Linux/macOS:

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account.json
```

Tambahkan IAM role yang diperlukan untuk service account:

```bash
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:YOUR_SERVICE_ACCOUNT@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:YOUR_SERVICE_ACCOUNT@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/cloudbuild.builds.builder"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:YOUR_SERVICE_ACCOUNT@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.admin"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:YOUR_SERVICE_ACCOUNT@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.writer"
```

Deploy `api_third_party`:

```bash
cd api_third_party

gcloud run deploy third-party-api-service \
  --source . \
  --region asia-southeast2 \
  --allow-unauthenticated \
  --build-service-account=projects/YOUR_PROJECT_ID/serviceAccounts/YOUR_SERVICE_ACCOUNT@YOUR_PROJECT_ID.iam.gserviceaccount.com \
  --service-account=YOUR_SERVICE_ACCOUNT@YOUR_PROJECT_ID.iam.gserviceaccount.com
```

Deploy `chatbot_app`:

```bash
cd chatbot_app

gcloud run deploy chatbot-app-service \
  --source . \
  --region asia-southeast2 \
  --allow-unauthenticated \
  --build-service-account=projects/YOUR_PROJECT_ID/serviceAccounts/YOUR_SERVICE_ACCOUNT@YOUR_PROJECT_ID.iam.gserviceaccount.com \
  --service-account=YOUR_SERVICE_ACCOUNT@YOUR_PROJECT_ID.iam.gserviceaccount.com
```

> Catatan: untuk production, sebaiknya environment variable seperti `API_KEY`, `ENGINE_NAME`, dan credential disimpan menggunakan Cloud Run environment variables atau Secret Manager, bukan hardcoded di source code.

## Contoh Konfigurasi Environment di Cloud Run

Saat deploy, variable environment dapat ditambahkan dengan flag `--set-env-vars`:

```bash
gcloud run deploy chatbot-app-service \
  --source . \
  --region asia-southeast2 \
  --allow-unauthenticated \
  --set-env-vars PROJECT_ID=YOUR_PROJECT_ID,LOCATION=YOUR_LOCATION,STAGING_BUCKET=gs://YOUR_STAGING_BUCKET,ENGINE_NAME=projects/YOUR_PROJECT_NUMBER/locations/YOUR_LOCATION/reasoningEngines/YOUR_ENGINE_ID,API_KEY=YOUR_APP_API_KEY
```

## Testing

### Test session baru

```bash
curl http://localhost:8080/new_session
```

Response contoh:

```json
{
  "session_id": "generated-uuid",
  "message": "Halo! Saya Eca. Saya di sini untuk membantu Anda."
}
```

### Test chat

```bash
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_APP_API_KEY" \
  -d "{\"query\": \"Apa kabar?\", \"session_id\": \"generated-uuid\"}"
```

Response contoh:

```json
{
  "response": "..."
}
```

## Catatan Keamanan

- Jangan commit file `.env` ke repository.
- Jangan commit file service account JSON ke repository.
- Gunakan Secret Manager untuk menyimpan credential di production.
- Pastikan `API_KEY` diganti dengan value yang kuat dan rahasia.
- Batasi IAM role service account sesuai kebutuhan minimum.

## Troubleshooting

### Error `Unauthorized` saat akses `/chat`

Pastikan header berikut dikirim:

```text
x-api-key: YOUR_APP_API_KEY
```

Value harus sama dengan `API_KEY` di file `.env`.

### Error credential Google Cloud

Pastikan variable berikut sudah benar:

```env
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account.json
```

Pastikan juga service account memiliki permission untuk menggunakan Vertex AI Reasoning Engine.

### Error Reasoning Engine tidak ditemukan

Periksa kembali format `ENGINE_NAME`:

```text
projects/YOUR_PROJECT_NUMBER/locations/YOUR_LOCATION/reasoningEngines/YOUR_ENGINE_ID
```

Pastikan location dan project number sesuai dengan engine yang dibuat.

### Tombol voice recording error

UI sudah memiliki fungsi recording, tetapi backend endpoint `/process_audio` belum tersedia pada `chatbot_app/app.py`. Jika ingin mengaktifkan fitur audio, tambahkan endpoint untuk menerima file audio, transkripsi audio, lalu kirim hasil transkripsi ke Reasoning Engine.

## Lisensi

Belum ada lisensi publik yang ditentukan untuk project ini.
