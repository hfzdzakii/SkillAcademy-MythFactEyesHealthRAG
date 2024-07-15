Nama : Muhammad Hafizh Dzaki

# Fakta Mitos Kesehatan Mata

Projek ini dibuat untuk memenuhi syarat kelulusan dalam Bootcamp - Artificial Intelligence Skill Academy Pro, Ruang Guru.
Website Fakta Mitos Kesehatan Mata adalah website berbasis AI yang digunakan untuk mengecek semua hal terkait kesehatan
mata. Namun, ada beberapa **disclaimer** yang wajib diperhatikan!

# Disclaimer

1. Pencipta berlatar belakang IT, bukanlah Kesehatan atau Kedokteran.
2. Pencipta tidak memiliki seorang yang benar-benar ahli untuk memverifikasi seluruh informasi terkait kesehatan mata.
3. Pencipta menggunakan dataset yang dibuat pribadi yang di-*generate* menggunakan tools AI populer seperti OpenAI ChatGPT 3.5 dan Google Gemini.
4. Validasi kebenaran data menggunakan tools AI dengan syarat kedua tools memiliki 1 suara, baik itu mitos atau fakta.

Oleh karena itu, ada kemungkinan AI **memberikan jawaban yang tidak relevan**. Sehingga, mohon **kebijakan pengguna** dalam 
bermain dan mencoba! Selain itu, mohon bertanya saja langsung kepada Dokter yang ahli apabila memiliki masalah dalam penglihatan Anda.

# Syarat Install

1. Python versi 3.9.x atau diatasnya.
2. Virtual Environtment, misal miniconda (opsional)
3. Git

# Cara Install

1. Clone repository ini dengan menggunakan code dibawah di dalam CMD / Terminal:

   ```
   git clone https://github.com/hfzdzakii/fakta-mitos-kesehatan-mata.git
   ```

3. Masuk ke dalam folder:

   ```
   cd fakta-mitos-kesehatan-mata
   ```
   
5. Install semua library yang dibutuhkan:

   ```
   pip install -r requirements.txt
   ```
   
7. Copy file .env.example, ubah nama menjadi .env

   Jika Anda menggunakan Windows, gunakan *command* berikut:
   
   ```
   copy .env.example .env
   ```

   Jika Anda menggunakan Linux / MacOs:

   ```
   cp .env.example .env
   ```
  
9. Isi GOOGLE_API_KEY sesuai API Key yang dibuat di [sini](https://console.cloud.google.com/apis/credentials), lali klik **Create Credentials -> Api Key**

    Jika Anda menggunakan Windows bisa dilakukan dengan manual, masuk ke text editor, copy dan paste API Key

    Jika Anda menggunakan Linux, gunakan command berikut:

    ```
    nano .env
    ```

    Lalu **paste API Key -> Ctrl+V -> X -> Enter**

10. Jalankan projek dengan command berikut:

    ```
    uvicorn main:app --reload
    ```
