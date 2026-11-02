# Ringkasan Tesis: Ekstraksi Entitas pada Keluhan Penipuan Online Berbahasa Indonesia Menggunakan IndoBERTweet, CharCNN, Leksikon Toleran, dan Efficient GlobalPointer

**Program Studi**: Teknik Informatika S2, Universitas Hasanuddin
**Versi**: rev8.2 | **Tanggal**: Oktober 2026

---

## Daftar Isi

- **[1. Topik dan Judul](#1-topik-dan-judul)**
- **[2. Mengapa Topik Ini Penting](#2-mengapa-topik-ini-penting)**
- **[3. Temuan Prapenelitian](#3-temuan-prapenelitian)**
- **[4. Rumusan Masalah dan Tujuan Penelitian](#4-rumusan-masalah-dan-tujuan-penelitian)**
- **[5. Metode yang Sudah Ada dan Keterbatasannya](#5-metode-yang-sudah-ada-dan-keterbatasannya)**
- **[6. Baseline: MGBERT-Pointer dan Kekurangannya](#6-baseline-mgbert-pointer-dan-kekurangannya)**
- **[7. Arsitektur Usulan](#7-arsitektur-usulan)**
- **[8. Rencana Uji Coba](#8-rencana-uji-coba)**
- **[9. Kebaruan dan Karya Terdekat](#9-kebaruan-dan-karya-terdekat)**
- **[10. Kontribusi Penelitian](#10-kontribusi-penelitian)**
- **[11. Antisipasi Pertanyaan Sidang](#11-antisipasi-pertanyaan-sidang)**
- **[12. State of The Art](#12-state-of-the-art)**
- **[13. Daftar Pustaka](#13-daftar-pustaka)**
- **[Lampiran A. Data dan Metode Prapenelitian](#lampiran-a-data-dan-metode-prapenelitian)**

---

## 1. Topik dan Judul

**Bidang**: Natural Language Processing (NLP) > Information Extraction > Named Entity Recognition (NER)

**Judul Tesis**:
> *Ekstraksi Entitas pada Keluhan Penipuan Online Berbahasa Indonesia Menggunakan IndoBERTweet, CharCNN, Leksikon Toleran, dan Efficient GlobalPointer*

**Judul Publikasi (Inggris, kerja)**:
> *Entity Extraction in Indonesian Online Fraud Complaints Using IndoBERTweet, CharCNN, Tolerant Lexicon, and Efficient GlobalPointer*

> **Catatan judul.** Struktur judul mengikuti pola penelitian NER *hybrid* di Unhas (Zainuddin, Mudassir & Tahir, 2025, TWBiL), dalam versi ringkas tanpa frasa "dengan Metode Hibrida". Bila ablasi menunjukkan CharCNN atau Leksikon Toleran tidak menambah nilai, judul disesuaikan dengan komponen yang tersisa.

**Task**: mengekstrak entitas penting dari keluhan korban penipuan online secara otomatis, dengan 5 tipe entitas: **PELAKU, NOMINAL, PLATFORM, MODUS, OBJEK**. Entitas bertumpuk diizinkan secara terbatas: PLATFORM di dalam PELAKU, dan NOMINAL di dalam MODUS.

---

## 2. Mengapa Topik Ini Penting

### Skala Masalah di Indonesia

Penipuan online adalah ancaman siber teratas yang dirasakan pengguna internet Indonesia:

| Sumber | Data | Periode |
|--------|------|---------|
| APJII, Survei Penetrasi Internet (8.720 responden) | 32,5% responden menyebut penipuan online sebagai permasalahan tertinggi kejahatan siber, naik 22,2 poin persentase dari 10,3% | 2024 |
| Kemenkominfo (kanal cekrekening.id) | 572.185 aduan penipuan online: 528.415 jual beli online dan 43.770 investasi fiktif. Angka ini jumlah aduan, bukan kasus yang terbukti | 2017 sampai 2 September 2024 |
| OJK dan IASC | Kerugian dana yang dilaporkan Rp2,6 triliun dari 128.281 laporan penipuan | Hingga 23 Mei 2025 |

Sumber: APJII 2024 (dikutip CNN Indonesia, 1 Februari 2024), Kemenkominfo 2024 (dikutip Bisnis.com, 3 September 2024), OJK 2025 (dikutip Katadata, 25 Mei 2025). Angka OJK dicocokkan dengan tiga media (Katadata, Investortrust, Kontan), belum dengan siaran pers OJK.

### Dari Fenomena ke Masalah Informatika

**Fenomena.** Sebagian besar korban tidak berakhir di jalur hukum. Survei GASA dan Mastercard (2025, 358 korban) menemukan hanya 13% korban yang melapor ke polisi dan 34% ke otoritas mana pun; laporan lain tersebar ke platform media sosial (53%) dan situs ulasan (15%); di antara 144 korban yang kehilangan uang, 74% melapor ke penyedia pembayaran. Di sisi lain, banyak korban menuliskan pengalamannya secara terbuka di ulasan aplikasi dan media sosial. Teks itu memuat informasi forensik yang berguna (pelaku, platform, nominal, modus), tetapi tersebar dan tidak terstruktur.

**Solusi.** Ekstraksi entitas bernama (*named entity recognition*, NER) dapat mengubah teks korban menjadi data terstruktur. Sepengetahuan penulis, berdasarkan penelusuran literatur, belum ada dataset NER untuk domain ini dalam bahasa Indonesia; karena itu penelitian ini juga membangun datasetnya.

**Masalah informatika.** NER saja belum tentu cukup, karena teks korban ditulis bebas dan tidak formal, dengan empat ciri yang diukur pada prapenelitian: kata tidak baku, ejaan nama yang bervariasi, nominal tidak baku, dan entitas bertumpuk (Bagian 3). Apakah model NER standar mampu menanganinya adalah **pertanyaan penelitian**, diuji dengan membandingkan IndoBERTweet + Efficient GlobalPointer (tanpa adaptor) dengan arsitektur usulan.

**Pemilihan arsitektur.** MGBERT-Pointer (Zhang et al., 2024) dipakai sebagai kerangka rujukan karena Efficient GlobalPointer menangani entitas bertumpuk dan adaptornya modular. Namun komponennya hanya dievaluasi pada teks Tionghoa, sehingga komponen itu diuji dan disesuaikan untuk teks Indonesia (Bagian 6 dan 7).

> **Catatan sumber data.** Korpus dibangun dari keluhan korban yang terbuka: ulasan Play Store bintang 1 dan 2 serta unggahan X. Kanal pelaporan resmi tidak menyediakan teksnya untuk umum dan hanya dipakai sebagai gambaran skala. Teks publik dapat memuat data pribadi (nomor rekening, telepon, nama), sehingga penanganannya mengikuti prinsip minimisasi dan anonimisasi. Perbedaan genre antara ulasan, X, dan laporan resmi berdampak nyata pada skema entitas (lihat Lampiran A.4).

---

## 3. Temuan Prapenelitian

Bagian 2 menyebut satu kekosongan dan empat ciri teks korban. Bagian ini menunjukkan buktinya satu per satu dengan penomoran yang sama (M1, lalu 01 sampai 04). Semua angka prapenelitian berlaku untuk **kandidat** keluhan korban dan perbandingannya dengan teks pembanding; korpus, definisi kelompok, dan risiko sirkularitas dijelaskan di Lampiran A. Apakah model standar gagal pada keempat ciri ini **belum diuji**; itu pertanyaan eksperimen (Bagian 8), bukan premis.

### 3.1 Ringkasan

| No | Masalah | Contoh | Bukti dari data | Status bukti |
|---|---|---|---|---|
| M1 | **Belum ada dataset** NER keluhan penipuan online berbahasa Indonesia | skema PELAKU, NOMINAL, PLATFORM, MODUS, OBJEK | Tinjauan literatur; korpus kandidat 6.032 dokumen | Didukung (berdasarkan penelusuran terbatas) |
| 01 | **Kata tidak baku** | *gak*, *udh*, *tf* | 74,9% dokumen Play Store dan 92,9% dokumen X | Didukung kuat, tetapi sifat ragam platform, bukan khas penipuan |
| 02 | **Ejaan nama bervariasi** | *buka lapak*, *tokped*, *shoppe* | 15,3% dari 3.059 sebutan 13 nama platform | Didukung (pemindaian pola, batas bawah) |
| 03 | **Nominal tidak baku** | *2jt*, *500rb*, *100k*, *sejuta* | 81 sampai 85% ungkapan nominal; Rp baku hanya 5 sampai 10% | Didukung secara deskriptif; perbandingan dengan pembanding sirkular |
| 04 | **Entitas bertumpuk** | "tf dulu **100k**" (NOMINAL di dalam MODUS) | 107 pasangan pada 1.000 dokumen X (pra-anotasi); heuristik Play Store 15,5% (batas atas) | Deskriptif dan heuristik; tingkat sejati menunggu pilot anotasi ganda |

### 3.2 M1: Belum ada dataset

Tinjauan Budi & Suryono (2023, *Bulletin of EEI* 12(2)) atas NER pada dataset berbahasa Indonesia mencakup ekstraksi berita, pemantauan banjir, dan lalu lintas; domain penipuan tidak termasuk di antaranya. (241 dokumen awal disaring menjadi 20 paper terpilih.) Dave & Chowanda (2024) mengakui: *"There is minimal research focusing on applications of Indonesian NER in a specific domain."* (Scopus Q1, DOI: 10.1186/s40537-024-00987-6)

Selain bukti literatur tersebut, tidak ditemukan dataset NER publik berbahasa Indonesia dengan skema entitas forensik (PELAKU, NOMINAL, PLATFORM, MODUS, OBJEK). Korpus kandidat 6.032 dokumen (Lampiran A.1) adalah bahan awal dataset tersebut. Sebaran kategori modus untuk korpus v1.4 dihitung dari `catatan_proses.json`.

Dave & Chowanda (2024) melaporkan bahwa NER finansial Indonesia mencapai F1 0,73 pada dataset kecil dan justru turun 0,04 poin (sekitar 0,69) saat 552 kalimat ditambahkan ke data latih, sehingga penambahan data saja tidak menjamin representasi entitas domain membaik.

### 3.3 Ciri 01: Kata tidak baku

Korban menulis keluhan dengan bahasa sehari-hari. Koto et al. (2021) menunjukkan bahwa model yang dilatih lanjut pada teks Twitter (IndoBERTweet) mengungguli IndoBERT pada tugas teks media sosial Indonesia (EMNLP 2021). Data prapenelitian mengonfirmasi bahwa 74,9% keluhan korban Play Store dan 92,9% keluhan korban X memuat kata tidak baku, dibanding 2,4% paragraf Wikipedia. Catatan penting: ketidakbakuan ini adalah sifat ragam platform, bukan khas penipuan, karena teks pembanding dari platform yang sama hampir sama informalnya.

| Indikator | Korban Play Store | Pembanding Play Store | Korban X | Pembanding X | Wikipedia |
|---|---|---|---|---|---|
| Dokumen memuat kata tidak baku | 74,9% | 67,8% | 92,9% | 90,0% | 2,4% |
| Token tidak baku | 7,8% | 10,1% | 9,8% | 8,4% | 0,1% |
| Dokumen memuat gabungan angka dan huruf (*2jt*, *hati2*) | 32,9% | 14,5% | 38,0% | 31,8% | 4,2% |
| Dokumen memuat huruf berulang (*bangettt*) | 3,8% | 5,1% | 12,4% | 11,1% | 1,6% |
| Dokumen dominan huruf kapital | 2,7% | 2,3% | 4,8% | 3,5% | 0,0% |
| Dokumen campur kode bahasa Inggris | 0,1% | 0,1% | 2,8% | 2,5% | 5,4% |
| Median panjang (kata) | 34 | 15 | 41 | 40 | 40 |

Kata tidak baku diukur dengan kamus *colloquial-indonesian-lexicon* (Salsabila et al., 2018), sehingga angkanya adalah batas bawah. Ciri 01 **didukung kuat** terhadap rujukan formal. Gabungan angka dan huruf tercatat 32,9% pada kandidat korban Play Store dan 14,5% pada pembanding, tetapi selisih ini ikut dipengaruhi seleksi nominal dan panjang teks, sehingga tidak ditafsirkan sebagai ciri khas korban. Per token, kandidat korban tidak lebih informal daripada pembanding (7,8% berbanding 10,1% token tidak baku). Campur kode bahasa Inggris hampir tidak ada, sehingga istilah "campur kode" pada rumusan awal dibatasi pada X dan tidak dijadikan ciri utama.

**Jarak dari ragam pralatih.** *Pseudo-perplexity* (Salazar et al., 2020) median IndoBERTweet adalah 31,3 pada kandidat korban Play Store, 40,5 pada pembanding Play Store, 32,7 pada kandidat korban X, 36,9 pada pembanding X, dan 17,7 pada Wikipedia. Teks korban sekitar 1,8 kali lebih "asing" daripada Wikipedia (rasio 1,76; IK 95% 1,39 sampai 2,14), tetapi **tidak berbeda** dari teks pembanding platform yang sama (rasio 0,77, IK 95% 0,65 sampai 1,02 pada Play Store; 0,89, IK 95% 0,74 sampai 1,09 pada X). Pada anggaran 50.000 token, 31,4% token kandidat korban Play Store tidak muncul di separuh sampel Wikipedia, dibanding 35,4% pada pembanding (batas dasar akibat ukuran sampel 10,8%). Jadi jarak dari ragam formal berasal dari **ragam platform**, bukan dari domain penipuan. *Pseudo-perplexity* IndoBERT belum tersedia karena *checkpoint* `indobenchmark/indobert-base-p1` tidak menyimpan bobot kepala MLM; perlu dihitung ulang dengan *checkpoint* lain.

### 3.4 Ciri 02: Ejaan nama bervariasi

Nama platform dan *fintech* (*kredivo*, *adakami*, *carousell*) menjadi kata khas keluhan korban, dan satu entitas sering ditulis dalam beberapa bentuk. Dari 3.059 sebutan 13 merek, 468 (15,3%) ditulis tidak baku: dipisah spasi 287 (sekitar 61%; *buka lapak* 122, *link aja* 42, *toko pedia* 31), singkatan 102 (*tokped* 73, *toped* 29), dan salah ketik 79 (*shoppe* 34, *carousel* 22). Varian spasi hampir seluruhnya dari Play Store; pada X yang dominan singkatan media sosial (*wa* 254 berbanding *whatsapp* 49, *ig* 117 berbanding *instagram* 17). Hanya 13 merek yang dipindai, sehingga angka bisa lebih tinggi. Bentuk berspasi (*buka lapak*) tidak terjangkau pembacaan per kata dan menjadi alasan terkuat menambahkan leksikon toleran (Bagian 7). Hasil negatif terkait fragmentasi *subword* ada di 3.7.

### 3.5 Ciri 03: Nominal tidak baku

Entitas pada keluhan korban penipuan tidak ditulis dalam bentuk baku. Sebanyak 23,2% kandidat korban Play Store dan 35,4% kandidat korban X memuat ungkapan nominal, dan 81 sampai 85% ungkapan itu ditulis dalam format singkat atau terbilang (*2jt*, *500rb*, *50k*, *sejuta*), bukan pola Rp baku. Format informal ini juga ditemukan pada teks pembanding, sehingga yang khas domain adalah **kehadiran** entitas nominal dan pelaku dalam narasi kerugian, bukan bentuk penulisannya. Nama platform dan *fintech* (*kredivo*, *adakami*, *carousell*) menjadi kata khas keluhan korban, dan pelaku sering disebut lewat frasa penyamar (*cs shopee*, *oknum yang mengaku kurir*).

| Indikator | Korban Play Store | Pembanding Play Store | Korban X | Pembanding X |
|---|---|---|---|---|
| Dokumen memuat ungkapan nominal | 23,2% | 4,4% | 35,4% | 18,0% |
| Ungkapan nominal berformat singkat atau terbilang | 80,7% | 80,4% | 85,3% | 78,5% |

Rincian format nominal pada kandidat korban Play Store: angka + *rb/ribu/k* 47,9%, angka + *jt/juta* 30,0%, angka berpemisah ribuan 14,1%, Rp + angka 5,3%, terbilang 2,7%. Pada kandidat korban X: angka + *jt/juta* 46,9%, angka + *rb/ribu/k* 29,9%, Rp + angka 9,9%, terbilang 8,5%, angka berpemisah ribuan 4,8%.

Hanya 5 sampai 10% ungkapan nominal pada kandidat korban memakai pola Rp baku. Proporsi format informal hampir sama pada kandidat korban dan pembanding (80,7% berbanding 80,4% di Play Store), jadi bentuk penulisan nominal adalah sifat ragam platform. Selisih prevalensi nominal (23,2% berbanding 4,4%) **tidak** dijadikan bukti karena sebagian dibuat oleh aturan seleksi dan oleh perbedaan panjang teks (lihat Lampiran A.3). Yang dapat diklaim: entitas NOMINAL pada korpus ini mayoritas berformat informal, sehingga model perlu mengenali batas NOMINAL di luar pola Rp baku.

Rincian jenis ungkapan pada 6.032 dokumen: singkatan *rb/ribu* 566, angka + *juta* 513, *jt* 454, *k* 342, angka bertitik tanpa Rp 233, kata (*sejuta*) 161; Rp + angka baku hanya 73.

Apakah IndoBERT tanpa pengetahuan domain gagal mengenali pola entitas ini **belum diuji**; itu adalah pertanyaan eksperimen (susunan B-Indo, B-Tweet, dan Usulan di Bagian 8), bukan premis.

### 3.6 Ciri 04: Entitas bertumpuk

Frasa *"CS Shopee"* bisa ditafsirkan berbeda: apakah *Shopee* adalah PLATFORM terpisah atau bagian dari PELAKU? Liu et al. (2024) mengidentifikasi masalah ini sebagai *"lexical conflict"*, yaitu kelemahan kritis model NER berbasis leksikon. (PeerJ CS, Scopus Q1, DOI: 10.7717/peerj-cs.2344). Estimasi heuristik prapenelitian menunjukkan 30,4% kandidat korban Play Store memuat minimal tiga tipe entitas dan sekitar 15,5% memuat kandidat entitas bertumpuk (batas atas kasar).

| Indikator (deteksi pola, bukan anotasi) | Korban Play Store | Pembanding Play Store | Korban X | Pembanding X |
|---|---|---|---|---|
| Dokumen memuat minimal 2 tipe entitas | 62,4% | 18,6% | 46,0% | 50,5% |
| Dokumen memuat minimal 3 tipe entitas | 30,4% | 3,0% | 21,3% | 21,7% |
| Kandidat bertumpuk (platform di dalam frasa pelaku) | 15,5% | 3,4% | 6,6% | 13,1% |

Contoh konkret dari data (Shopee, IMPERSONATION_EXTORTION):

> *"Saya kena tipu dari chat aplikasi Shopee yg mengatasnamakan CS Shopee dengan kedok akun kena blokir sehingga perlu pemulihan akun..."*
>
> Token `shopee` dapat menjadi **PLATFORM** sekaligus bagian dari span **PELAKU** (`cs shopee`). CRF berbasis BIO hanya mengizinkan satu label per token sehingga konflik ini tidak dapat diselesaikan. *Decoder* berbasis *span* seperti **Efficient GlobalPointer**, yang menilai setiap pasangan posisi awal dan akhir *(i, j)* untuk tiap tipe entitas, diperlukan untuk menangani kasus ini.

**Signifikansi, dengan koreksi penting.** Angka di atas dihitung dengan pola yang sengaja longgar (terutama OBJEK dan PELAKU), sehingga **cenderung melebihkan** dan bersifat **estimasi**, bukan *ground truth*. Selisih dengan pembanding Play Store (30,4% berbanding 3,0% untuk minimal tiga tipe) **tidak** dijadikan bukti, karena pola pelaku, platform, modus, dan nominal juga dipakai aturan seleksi, dan kandidat korban rata-rata dua kali lebih panjang. Yang dapat dilaporkan adalah prevalensi deskriptif di dalam kandidat korban. Pada X, pembanding bukan kontrol netral karena berasal dari kueri penipuan yang sama, sehingga perbandingan X tidak ditafsirkan. Karena CRF berbasis BIO sanggup menangani beberapa entitas **terpisah** (*disjoint*) dalam satu kalimat, angka multientitas **bukan** bukti kebutuhan GlobalPointer. Yang tidak bisa ditangani CRF hanyalah **tumpang tindih sejati** (*true overlap/nesting*). Karena itu:
> - Kandidat bertumpuk 15,5% disajikan sebagai batas atas kasar, bukan sebagai bukti.
> - Tingkat **overlap sejati** akan **dilaporkan setelah pilot anotasi ganda**, dan angka inilah yang menjadi justifikasi kuantitatif decoder *span-based*.
> - Justifikasi Efficient GlobalPointer tetap kokoh dari tiga dasar lain: menangani *overlap* sejati, menghilangkan *cascade error* CRF, dan efisiensi parameter (lihat Bagian 5 dan 7).

### 3.7 Hasil negatif: fragmentasi *subword* bukan masalah utama

> **Catatan.** Rumusan awal masalah ini adalah OOV: IndoBERT dianggap memecah kosakata penipuan menjadi *subword* acak tanpa makna. Analisis prapenelitian tidak mendukung rumusan itu, sehingga dilaporkan sebagai hasil negatif dan tidak dipakai sebagai premis.

| Kelompok | Token kata terpecah (IndoBERT) | *Subword* per kata (IndoBERT) | Token kata terpecah (IndoBERTweet) |
|---|---|---|---|
| Korban Play Store | 8,8% | 1,11 | 5,6% |
| Pembanding Play Store | 10,2% | 1,12 | 6,6% |
| Korban X | 12,2% | 1,15 | 6,8% |
| Pembanding X | 13,1% | 1,16 | 8,1% |
| Wikipedia (formal) | 14,6% | 1,22 | 20,5% |

Token [UNK] tidak muncul sama sekali (0%). Keluhan korban justru **lebih sedikit** terpecah daripada teks pembanding: selisih −1,4 poin persen pada Play Store (IK 95% −1,6 sampai −1,1) dan −0,8 poin persen pada X (IK 95% −1,5 sampai −0,2).

**Kata khas korban.** Analisis *log-odds* dengan *prior* Dirichlet (Monroe et al., 2008) menemukan 244 kata yang lebih khas pada kandidat korban Play Store dibanding pembanding (kata kunci seleksi dikeluarkan). Dari 200 kata khas teratas, 16,0% dipecah IndoBERT dibanding 13,0% pada kata pembanding berfrekuensi setara (selisih +3,0 poin persen; IK 95% −4,0 sampai +10,0; **tidak bermakna**). Pada IndoBERTweet, selisihnya bermakna: 14,5% dibanding 2,5% (IK 95% +7,0 sampai +17,5 poin persen). Contoh pemecahan oleh IndoBERT: *carousell* (car ##ouse ##ll), *kredivo* (kred ##iv ##o), *kebobolan* (kebo ##bola ##n), *penipunya* (penipu ##nya). Pemecahan ini sebagian besar berupa nama merek dan afiks, bukan potongan acak tanpa makna. Analisis yang sama pada X hanya menghasilkan 26 kata khas, terlalu sedikit untuk disimpulkan.

**Kesimpulan.** Rumusan awal "IndoBERT memecah kosakata penipuan menjadi *subword* acak" **tidak didukung** dan tidak dipakai lagi. Dua catatan: (1) token gabungan angka dan huruf (*2jt*, *500rb*, *hati2*) belum diukur fragmentasinya karena dikeluarkan dari analisis kata alfabetis; (2) fragmentasi rendah tidak berarti makna dipahami model.

### 3.8 Masalah lain yang tidak dijawab arsitektur

Masalah lain dari data **tidak dijawab arsitektur** (atau hanya sebagian) dan ditangani di tempat lain:

| Masalah | Ditangani oleh |
|---|---|
| Belum ada dataset (M1) | Kontribusi data (K1) |
| MODUS dan PELAKU berupa uraian panjang | Panduan anotasi (batas MODUS sekitar 5 kata; PELAKU tanpa kata kerja), lalu diukur di pilot |
| Kata ambigu *dana* | Konteks encoder; diukur dengan metrik akurasi kata ambigu |
| Nama baru di luar daftar | Konteks encoder; **risiko bertambah bila leksikon dipakai**, diukur dengan *recall* entitas di luar data latih dan leksikon (H5) |
| Teks X panjang | *Sliding window* (prapemrosesan) |
| PELAKU berupa pengenal hampir tidak ada (0,0% Play Store, 7,1% X) | Definisi PELAKU diputuskan sebelum panduan anotasi (Lampiran A.4) |

### 3.9 Keterbatasan data prapenelitian

(1) Ketepatan kandidat korban belum diukur. (2) Data X dikumpulkan dengan kueri bertarget sehingga tidak mewakili seluruh keluhan di X, dan pembanding X bukan kontrol netral. (3) Deteksi entitas, nominal, dan kata tidak baku berbasis pola dan kamus, sehingga bersifat perkiraan. (4) Data telah dipseudonim dengan format sama. (5) Wikipedia hanya mewakili ragam formal dan kemungkinan termasuk data pralatih model, sehingga perbandingan yang adil untuk efek domain adalah korban terhadap pembanding dari platform yang sama.

---

## 4. Rumusan Masalah dan Tujuan Penelitian

### 4.1 Rumusan masalah

> Bagaimana meningkatkan akurasi ekstraksi entitas pada teks yang ditulis pengguna dan memuat kata tidak baku, variasi penulisan nama, ungkapan numerik tidak baku, serta entitas bertumpuk secara bersamaan, padahal arsitektur *named entity recognition* yang ada baru menangani sebagian karakteristik tersebut dan belum ada yang menangani keempatnya dalam satu model?

### 4.2 Tujuan penelitian

> Merancang dan mengevaluasi arsitektur ekstraksi entitas yang menggabungkan IndoBERTweet, CharCNN, Leksikon Toleran, dan Efficient GlobalPointer dalam satu model untuk meningkatkan akurasi pada teks yang ditulis pengguna dan memuat kata tidak baku, variasi penulisan nama, ungkapan numerik tidak baku, serta entitas bertumpuk secara bersamaan.

Rincian tujuan (dipakai bila diminta tujuan yang dirinci, tanpa menambah masalah baru):

1. Mengukur peningkatan akurasi arsitektur usulan dibandingkan *baseline* uji B-Tweet (*encoder* terpilih + Efficient GlobalPointer) dan rakitan R-MGBERT (MGBERT-Pointer tanpa *Entity Adapter*).
2. Mengukur kontribusi tiap komponen terhadap akurasi pada masing-masing karakteristik melalui uji ablasi Tahap 3 dan F1 subset.

### 4.3 Pemetaan rumusan ke tujuan

| Unsur rumusan masalah | Unsur tujuan | Dijawab oleh |
|---|---|---|
| Bagaimana meningkatkan akurasi | Merancang arsitektur untuk meningkatkan akurasi | Usulan vs B-Tweet dan R-MGBERT (H1) |
| Keempat karakteristik secara bersamaan | Disebut ulang persis | F1 total dan F1 subset (Bagian 8) |
| Belum ada yang menangani keempatnya dalam satu model | Menggabungkan komponen dalam satu model | Ablasi Tahap 3 |
| (pembuktian) | Mengevaluasi | Uji *paired bootstrap* |

### 4.4 Batasan istilah

| Istilah | Definisi operasional |
|---|---|
| Entitas | Lima tipe: PELAKU, NOMINAL, PLATFORM, MODUS, OBJEK. Istilah "entitas bernama" tidak dipakai karena MODUS dan PELAKU deskriptif bukan nama diri |
| Kata tidak baku | Kata di luar ragam baku (*gak*, *udh*, *tf*), sesuai Ciri 01 |
| Variasi penulisan nama | Satu nama entitas ditulis dalam bentuk berbeda: dipisah spasi (*buka lapak*), singkatan (*tokped*), atau salah ketik (*shoppe*), sesuai Ciri 02 |
| Ungkapan numerik tidak baku | Nominal di luar pola Rp baku (*2jt*, *500rb*, *100k*, *sejuta*), sesuai Ciri 03 |
| Entitas bertumpuk | Entitas yang seluruh rentangnya berada di dalam entitas lain; terbatas pada PLATFORM di dalam PELAKU dan NOMINAL di dalam MODUS, sesuai Ciri 04. Bila pilot anotasi menemukan *span* bersilang, istilah diperluas menjadi "entitas bertumpuk dan tumpang tindih" |
| Akurasi | F1 *micro strict span*, bukan akurasi per token |
| Arsitektur (dalam satu model) | Komponen disisipkan di dalam model dan dilatih bersama (*end-to-end*), dibedakan dari *pipeline* dengan normalisasi teks sebagai tahap terpisah |

### 4.5 Dasar celah dan karya terdekat

Penelusuran awal (LeapSpace/Scopus dan pencarian web, 21 Oktober 2026) tidak menemukan model tunggal yang mengevaluasi keempat karakteristik sekaligus. Karya terdekat yang wajib disebut di latar belakang:

| Karya | Kata tidak baku | Variasi nama | Numerik tidak baku | Bertumpuk |
|---|---|---|---|---|
| DaN+ (Plank dkk., 2020, COLING) | Ya | Normalisasi terpisah (*pipeline*) | Tidak | Ya |
| HelaNER 1.0 dan 2.0 (Priyadarshana & Ranathunga, 2021 EUROCON; 2022 IJACSA), media sosial Sinhala | Ya | Fitur karakter, tidak dievaluasi khusus | Tidak | Ya |
| InferNER; Aguilar dkk. (2017, 2018) | Ya | Ya | Tidak | Tidak |
| NER medis Tionghoa: RoBERTa + fusi karakter-kata + kamus + EGP (*Informatica*) | Tidak | Sebagian | Tidak | Ya |
| NumER (Julavanich & Aizawa, 2021); NuER (Sundararaman dkk., 2022) | Tidak | Tidak | Numerik formal saja | Tidak |

Konsekuensi untuk pembelaan celah:

1. Kombinasi teks media sosial dan entitas bertumpuk sudah dikerjakan (DaN+, HelaNER), sehingga celah bertumpu pada **ungkapan numerik tidak baku** dan pada penanganan **di dalam model**, bukan normalisasi terpisah.
2. Susunan "*encoder* + fitur karakter + kamus + EGP" sudah ada pada teks formal (NER medis Tionghoa), sehingga kombinasi komponen tetap bukan kebaruan utama (Bagian 9).
3. Perlu tambahan susunan pembanding "normalisasi terpisah + *encoder* + EGP" di Tahap 3, dan F1 subset nominal informal pada B-Tweet untuk membuktikan karakteristik numerik memang menurunkan akurasi.
4. Klausa "belum ada yang menangani keempatnya" baru aman setelah penelusuran sistematis di Scopus, ACL Anthology, dan Google Scholar selesai; UHIF, BFSN2ER, CEAF, dan TCSF belum diperiksa.
5. Bila program studi meminta lebih dari satu rumusan, pecah menjadi dua mengikuti garis bentuk tulisan dan struktur entitas: (a) akurasi pada entitas yang ditulis tidak baku, padahal arsitektur untuk teks tidak baku umumnya hanya menangani entitas datar; (b) akurasi pada entitas bertumpuk yang bagian dalamnya ditulis tidak baku, padahal arsitektur entitas bertumpuk umumnya dirancang dan dievaluasi pada teks baku.

---

## 5. Metode yang Sudah Ada dan Keterbatasannya

Bagian ini memetakan penelitian terdahulu dalam dua kelompok. Tabel pertama (NER bahasa Indonesia) menunjukkan apa yang sudah dikerjakan pada teks Indonesia. Tabel kedua (NER global lintas bahasa) menunjukkan bahwa ragam media sosial, fitur tingkat huruf, dan dekoder *span* untuk entitas bertumpuk sudah punya dasar, yang melandasi pemilihan IndoBERTweet, CharCNN, dan Efficient GlobalPointer. Berdasarkan penelusuran literatur penulis, yang belum ditemukan adalah data NER keluhan korban penipuan daring dan pengujian gabungan komponen tersebut pada teks informal berbahasa Indonesia.

### NER Bahasa Indonesia

| Metode | Domain | F1 | Keterbatasan | Sumber |
|---|---|---|---|---|
| IndoBERT-BiGRU-CRF (IPerFEX-2023) | Keuangan personal (pos Quora, 15 entitas) | 0,73 (dataset kecil); turun 0,04 saat 552 kalimat ditambahkan | CRF hanya entitas datar; IndoBERT dipakai sebagai fitur (*feature-based*) | Dave & Chowanda, 2024 |
| XLM-R (IndoLER) | Putusan pengadilan (sekitar 1.000 dokumen, 20 tipe entitas) | 0,9295 | Teks formal, tanpa entitas penipuan | Yulianti et al., 2024 (*IJECE* 14(5)) |
| NER + SVM (berita kriminal) | Berita kriminal | 0,908 (ekstraksi lokasi; tanggal 0,941; klasifikasi jenis kejahatan 92% memakai SVM, bukan NER; dicocokkan dengan abstrak tesis S2 penulis yang sama) | Teks formal, entitas umum (jenis, lokasi, waktu), metode non-*transformer* | Sedik & Romadhony, 2023 |
| TWBiL (Word2Vec + Bi-LSTM + Transformer + *attention*) | Berita Detik.com | 85,11 | *Embedding* statis, label per kata (tidak bisa bertumpuk), teks formal; pembanding Bi-LSTM 75,18 | Zainuddin et al., 2025 (*JOIV* 9(3)) |
| IndoBERTweet-CRF | Aset kripto di X (1.461 tweet emas, 27.226 tweet perak) | 70,76 | CRF tidak bisa bertumpuk; bukan domain penipuan; tidak ada makalah terkait | Davin (2026), *Mendeley Data*, DOI 10.17632/rtw4d5c6hj.1 (set data; tidak ada makalah terkait, sehingga tautan perlu dicek keterbukaannya sebelum dikutip) |
| Ekstraksi entitas orang bertumpuk (*nested*; CRF, BiLSTM-CRF, IndoBERT) | Terjemahan Al-Qur'an berbahasa Indonesia, entitas orang | Tidak dicantumkan di sini (hanya abstrak yang diperiksa); BiLSTM-CRF terbaik, CRF kesulitan pada entitas bertumpuk | Teks formal, hanya satu jenis entitas (orang), bukan domain penipuan, jumlah tingkat tumpukan dan keterbukaan set data belum diverifikasi | Dzidny, Bijaksana & Lhaksmana, 2022 (*BITS* 4(1): 241 sampai 246) |
| GLiNER bahasa Indonesia (berbasis *span*, diberi label lewat *prompt*) | NER Indonesia umum | Lihat makalah (*ETASR*) | Ragam teks tidak dirinci di sini, mampu menangani entitas bertumpuk secara arsitektur, belum diuji pada entitas bertumpuk informal maupun keluhan penipuan | GLiNER-ID (*ETASR*) |

> **Kesimpulan.** Penelitian NER berbahasa Indonesia telah mencakup domain keuangan personal, hukum, berita, kriminal, dan kripto, termasuk teks media sosial. Namun, berdasarkan penelusuran literatur yang dilakukan penulis, dua hal belum ditemukan. Pertama, dataset NER untuk keluhan korban penipuan daring. Kedua, dataset dan evaluasi NER untuk entitas bertumpuk (*nested*), yaitu entitas yang memuat entitas lain di dalamnya (misalnya nama platform di dalam nama akun), pada teks informal. Penelitian entitas bertumpuk yang teridentifikasi baru menggunakan teks formal dengan satu jenis entitas (Dzidny dkk., 2022). Kedua hal tersebut menjadi celah penelitian yang dijawab dalam penelitian ini.

### NER Global (Lintas Bahasa)

| Metode | Domain | F1 | Pendukung penelitian ini | Sumber |
|---|---|---|---|---|
| **MGBERT-Pointer** (konvolusi karakter CA + EGP), *baseline* penelitian ini | NER bahasa Tionghoa (Weibo, Resume, OntoNotes, MSRA) | Weibo 73,22; Resume 96,23; OntoNotes 83,25; MSRA 96,10 (BERT pada Weibo 67,27) | *Baseline*: dasar gabungan fitur karakter berbasis konvolusi dan EGP, unggul 5,95 poin atas BERT pada Weibo | Zhang et al., 2024 |
| IndoBERTweet (BERT dilatih lanjut pada tweet) | Tweet bahasa Indonesia (pralatih) | Tidak dicantumkan | *Encoder* untuk ragam media sosial Indonesia (masalah 01) | Koto et al., 2021 (EMNLP) |
| Bi-LSTM-CNN-CRF (CNN karakter di dalam kata) | NER umum bahasa Inggris | Tidak dicantumkan | Asal fitur CharCNN untuk NER (masalah 02) | Ma & Hovy, 2016 |
| Model berfitur karakter (NER percakapan) | Teks percakapan bahasa Indonesia | Model karakter unggul hingga 4 poin F1, hingga 15 poin pada kata di luar kosakata | Bukti terdekat berbahasa Indonesia bahwa fitur karakter membantu NER percakapan, terutama pada kata di luar kosakata (masalah 02) | Kurniawan & Louvan, 2018 (W-NUT) |
| CharBERT (karakter + *subword* lewat modul interaksi) | Model pralatih, huruf Latin | Tidak dicantumkan | Informasi karakter masih berguna di atas *encoder transformer* | Ma et al., 2020 (COLING) |
| Biaffine NER (CNN karakter + BERT + fastText + dekoder *biaffine*) | ACE 2004, ACE 2005, GENIA (bertumpuk); CoNLL, OntoNotes (datar) | Tidak dicantumkan (terbaik pada 8 korpus, hingga +2,2 poin) | Fitur CNN karakter dan dekoder *span* sudah pernah digabung; dasar pembanding B-Biaffine di Tahap 2 | Yu et al., 2020 (ACL) |
| DaN+ (MaChAmp *multi-label*, normalisasi leksikal MoNoise) | Denmark: berita, Reddit, Twitter, Arto (entitas bertumpuk) | F1 *span* bertumpuk (mlBERT): berita 80,73; Twitter 60,87; Arto 54,88; dengan normalisasi 61,74 dan 56,38 | NER entitas bertumpuk pada teks media sosial layak dikerjakan, dan normalisasi membantu pada data paling tidak baku (masalah 01 dan 04) | Plank dkk., 2020 (COLING) |
| DeepNNNER (BLSTM-CNN + normalisasi teks + leksikon) | Tweet bahasa Inggris | 47,24 | Fitur karakter dan leksikon dipakai pada teks media sosial (dasar Leksikon Toleran) | Dugas & Nichols, 2016 (WNUT) |
| GlobalPointer (proyeksi *query* dan *key* per tipe) | NER Tionghoa dan GENIA | *People's Daily* 95,51; CLUENER 79,44; CMeEE 65,98; GENIA 74,64 | Dekoder *span* untuk entitas bertumpuk; pembanding B-GP di Tahap 2 | Su et al., 2022 |
| **Efficient GlobalPointer** (*query* dan *key* dipakai bersama, vektor w_t per tipe) | NER Tionghoa | *People's Daily* 95,36; CLUENER 80,04; CMeEE 66,54 | Dekoder yang dipilih (masalah 04): akurasi setara GP dengan parameter per tipe jauh lebih sedikit | Su et al., 2022; dipakai MGBERT-Pointer (2024) dan GTBERT-Pointer (2025) |
| DMGP (*dual-masked* GlobalPointer) | Korpus sains Tionghoa (1.100 abstrak, 22.184 entitas) | DMGP 70,23; GlobalPointer 68,10; Biaffine 54,72; StructBERT-CRF 53,73 | Dekoder keluarga GlobalPointer mengungguli *biaffine* dan CRF pada satu korpus | Zhang et al., 2025 |
| CNN-NER (CNN di atas matriks skor *span*) | NER bertumpuk (rincian korpus tidak dicantumkan) | Tidak dicantumkan | Kandidat pembanding opsional B-CNNNER di Tahap 2 | Yan et al., 2023 |

> **Kesimpulan.** Setiap komponen arsitektur sudah didukung penelitian terdahulu: IndoBERTweet untuk teks media sosial Indonesia, fitur karakter untuk variasi ejaan, dan dekoder *span* keluarga GlobalPointer untuk entitas bertumpuk. Efficient GlobalPointer belum diuji pada bahasa Indonesia, sehingga manfaat tiap komponen diuji lewat ablasi dan EGP dibandingkan dengan CRF, GlobalPointer, dan *biaffine* pada Tahap 2 (Bagian 8).

**GlobalPointer (GP) dan Efficient GlobalPointer (EGP) berbeda dalam struktur, tetapi akurasinya tidak jauh berbeda.** Pada GP, setiap tipe entitas memiliki proyeksi *query* dan *key* sendiri, dengan penyandian posisi rotari (*rotary position encoding*) untuk menghitung skor *span* (Persamaan 5 pada makalah Su dkk., 2022). Pada EGP, *query* dan *key* dipakai bersama oleh semua tipe, dan setiap tipe hanya menambah satu vektor kecil (Persamaan 7). Dari segi akurasi, makalah yang sama (Tabel 5) menunjukkan selisih F1 yang kecil dan tidak searah: EGP sedikit lebih rendah pada *People's Daily* (95,36 berbanding 95,51), dan sedikit lebih tinggi pada CLUENER (80,04 berbanding 79,44) dan CMeEE (66,54 berbanding 65,98). Selisihnya berkisar dari −0,15 sampai +0,60 poin F1. Keunggulan EGP karena itu terutama pada efisiensi parameter, bukan akurasi. Keunggulan GP atas CRF pada data datar juga kecil (0,05 sampai 1,6 poin F1), sehingga alasan memilih dekoder *span* bertumpu pada kemampuannya menangani entitas bertumpuk, bukan pada akurasi.

---

## 6. *Baseline*: MGBERT-Pointer dan Kekurangannya

### Alasan memilih MGBERT-Pointer sebagai *baseline*

MGBERT-Pointer (Zhang et al., 2024; *Complex & Intelligent Systems*, Scopus) adalah model NER untuk teks Tionghoa yang menyisipkan *Multi-Granularity Adapter* (MGA) di antara lapisan pertama dan kedua BERT, lalu memakai Efficient GlobalPointer sebagai kepala prediksi. **Model ini dipilih karena strukturnya, bukan karena sudah teruji pada teks Indonesia.**

| No | Alasan | Penjelasan informatika |
|---|---|---|
| 1 | **Mendukung entitas bertumpuk** | EGP memprediksi entitas sebagai pasangan posisi awal dan akhir (*span*), bukan satu label per kata seperti CRF |
| 2 | **Menggabungkan beberapa jenis informasi** | Konteks kalimat dan pola karakter digabung dalam satu representasi token |
| 3 | **Arsitektur modular** | Adaptor disisipkan di antara lapisan Transformer, sehingga setiap komponen dapat diganti dan diuji terpisah |
| 4 | **Memanfaatkan leksikon** | Model dapat dibantu daftar nama yang disiapkan di luar data latih |

Rincian MGA dari teks lengkap makalah:

| Adaptor | Isi | Catatan |
|---|---|---|
| *Character Adapter* (CA) | Konvolusi dengan tiga kernel berbeda (ukuran tidak dirinci), *GlobalMaxPooling*, lalu atensi atas **urutan karakter kalimat** untuk memperkaya representasi tiap token | Fungsinya pengayaan konteks karakter; ablasi makalah menunjukkan kontribusinya kecil dibanding LA. Hanya dievaluasi pada teks Tionghoa |
| *Entity Adapter* (EA) | Triplet entitas (tipe, awal, akhir) | Sumber triplet saat inferensi tidak dijelaskan di makalah |
| *Lexicon Adapter* (LA) | Kata dari leksikon yang cocok **persis**, encoding posisi, bobot adaptif, atensi; terinspirasi LEBERT (ACL 2021) | Leksikon asli berupa kosakata kata umum (*embedding* Song et al., 2018). Varian "LA persis" pada tesis ini adalah implementasi sendiri mengikuti LEBERT, bukan kode makalah |

Kode MGBERT tidak publik, dan dimensi serta ukuran kernel CA tidak dirinci di makalah, sehingga reimplementasi disusun dari persamaan makalah dengan pilihan hiperparameter sendiri.

### Kekurangan *baseline* untuk keluhan korban berbahasa Indonesia

| No | Komponen MGBERT | Kekurangan | Bukti |
|---|---|---|---|
| 1 | **BERT** | Makalah memakai Chinese BERT-base dan hanya mengevaluasi pada empat dataset Tionghoa, sehingga kecocokannya dengan ragam informal Indonesia belum diketahui. **Pengganti: IndoBERTweet**, yaitu BERT bahasa Indonesia yang dilatih lanjut pada tweet Indonesia, diuji terhadap IndoBERT dan mBERT pada Tahap 1 | Zhang et al. (2024), hlm. 4484, bagian *Experimental settings*: "The model utilizes Chinese BERT-base as the Encoder"; dan "experiments were conducted on Weibo, OntoNotes, Resume, and MSRA" |
| 2 | ***Character Adapter*** | Bekerja pada urutan karakter kalimat dengan konvolusi, bukan huruf di dalam kata, dan hanya dievaluasi pada teks Tionghoa, sehingga kecocokannya dengan huruf Latin berejaan tidak baku belum diketahui. **Pengganti: CharCNN** (huruf di dalam kata), diuji terhadap CA sebagai pembanding A-CA di Tahap 3 | Zhang et al. (2024), hlm. 4477: "the CA utilizes a series of convolutional layers with different kernel sizes"; dataset uji hanya Tionghoa (hlm. 4484) |
| 3 | ***Lexicon Adapter*** | Kata dicari dari kamus eksternal tanpa disebut toleran (pembacaan penulis: pencocokan persis), sehingga variasi ejaan (misalnya "buka lapak" terhadap "bukalapak") berpotensi tidak dikenali. Kamus berasal dari Song dkk. (2018), bukan daftar nama entitas. **Modifikasi: Leksikon Toleran**, yaitu struktur LA dipertahankan dan hanya cara pencocokan kata diubah dari persis menjadi toleran | Zhang et al. (2024), hlm. 4479: "each character in the sentence is matched with an external lexicon to retrieve all potential words"; hlm. 4484: "LA used the dictionary from Song et al." |
| 4 | ***Entity Adapter*** | Membutuhkan daftar entitas yang benar sebagai masukan, padahal itulah yang harus dicari model. Makalah tidak menjelaskan bagaimana daftar ini diperoleh pada teks baru yang belum berlabel | Zhang et al. (2024), hlm. 4477: "EA acquires entity information from the model input, where individual entity information is represented as a triplet, including the entity type, start position, and end position" |

Halaman mengikuti penomoran terbitan (*Complex & Intelligent Systems* 10: 4473 sampai 4491).

Efficient GlobalPointer **sudah sesuai** dan dipertahankan, karena komponen ini inti untuk menangani entitas bertumpuk (masalah 04): entitas diprediksi sebagai pasangan posisi awal dan akhir (*span*), sehingga satu rentang dapat memuat entitas lain.

---

## 7. Arsitektur Usulan

### Rumusan

> **IndoBERTweet + CharCNN + Leksikon Toleran + Efficient GlobalPointer**

| Kotak MGBERT | Keputusan | Alasan |
|---|---|---|
| BERT | **Diganti IndoBERTweet** | Dilatih pada teks media sosial Indonesia (penyesuaian bahasa; tidak dihitung kontribusi) |
| *Character Adapter* (CA) | **Diuji, lalu diganti CharCNN bila CharCNN lebih baik** | Pada makalah MGBERT, CA hanya dievaluasi pada empat dataset Tionghoa (hlm. 4484), dan kontribusinya hampir nol pada data formal (−0,01 sampai −0,10) tetapi lebih terasa pada Weibo yang informal (−0,57; Tabel 4, hlm. 4487), sehingga layak diuji pada teks informal. CharCNN membaca huruf di dalam kata dan sudah punya bukti pada NER Indonesia (Kurniawan & Louvan, 2018). Mana yang lebih cocok dijawab oleh uji A-CA vs A-Char (Bagian 8), bukan diasumsikan |
| *Lexicon Adapter* (LA, cocok persis) | **Diganti Leksikon Toleran** | Pada pencocokan persis, *buka lapak* tidak cocok dengan entri *bukalapak* (contoh ilustrasi, bukan hasil makalah); pencocokan toleran menormalkan spasi, huruf berulang, dan ejaan mirip |
| *Entity Adapter* (EA) | **Dibuang** | Membutuhkan daftar entitas yang benar sebagai masukan; sumbernya pada teks baru tidak dijelaskan makalah (Zhang et al., 2024, hlm. 4477). Kontribusinya juga kecil pada ablasi makalah (Weibo −0,37) |
| Efficient GlobalPointer | **Dipertahankan** | Sudah menangani entitas bertumpuk |

Kontribusi arsitektur dirumuskan sebagai **dua kotak yang diuji penggantinya** di dalam adaptor: CA dibandingkan dengan CharCNN, dan LA persis dibandingkan dengan Leksikon Toleran. Keduanya tetap disisipkan di antara lapisan 1 dan 2 seperti MGA. Gerbang kontekstual (*Lexicon-Conditioned Gating*, LC-Gate) **tidak dipakai** karena pada uji konfirmasi dengan data simulasi tidak lebih baik dari gerbang konstan (−0,30 F1); fusi dilakukan secara aditif.

### Diagram

Berkas: `ARSITEKTUR_MGBERT_VS_USULAN.drawio` (MGBERT di kiri, usulan di kanan; abu-abu = sama dengan MGBERT, hijau = diganti). Isi kotak adaptor usulan: **CharCNN** dan **Leksikon Toleran**.

```
Teks keluhan → IndoBERTweet lapisan 1 → [CharCNN (huruf dalam kata) + Leksikon Toleran (pencocokan mirip)]
            → IndoBERTweet lapisan 2-12 → Efficient GlobalPointer
            → PELAKU, NOMINAL, PLATFORM, MODUS, OBJEK (termasuk bertumpuk)
```

### Komponen

**1. IndoBERTweet** (`indolem/indobertweet-base-uncased`). Encoder 12 lapis yang dilatih lanjut pada tweet Indonesia. Prapenelitian menunjukkan IndoBERTweet memecah kata keluhan korban lebih sedikit daripada IndoBERT (5,6% vs 8,8% token terpecah pada Play Store).

**2. CharCNN.** Untuk setiap kata w dengan huruf c₁ ... c_m:

1. setiap huruf diubah menjadi vektor *embedding* huruf;
2. konvolusi 1D dengan beberapa lebar kernel (misalnya 2, 3, 4) dijalankan di sepanjang huruf;
3. *max-pooling* menghasilkan satu vektor pola huruf per kata;
4. vektor itu diproyeksikan ke dimensi IndoBERTweet dan **ditambahkan** ke representasi setiap *subword* milik kata tersebut, di antara lapisan 1 dan 2.

Lapisan proyeksi diinisialisasi nol, sehingga keluaran awal model sama dengan IndoBERTweet + EGP. Dengan begitu, perbedaan hasil berasal dari apa yang dipelajari CharCNN.

**3. Leksikon Toleran.** Daftar nama dibangun dari **sumber eksternal** (nama penyelenggara berizin OJK, nama aplikasi Play Store, dan singkatan umum seperti *tokped*, *wa*, *ig*), lalu **dibekukan sebelum menyentuh data uji**. Langkahnya:

1. Setiap kalimat dinormalkan untuk pencocokan: huruf kecil, spasi dibuang, huruf berulang diringkas (*shoppee* → *shope*).
2. Jendela 1 sampai 3 kata dicocokkan dengan entri. Cocok bila hasil normalisasinya sama **atau** kemiripan *trigram* huruf (Jaccard) ≥ 0,7. Dengan cara ini *buka lapak* (dua kata) cocok dengan entri *bukalapak*.
3. Setiap token dalam jendela yang cocok menerima vektor entri: *embedding* entri berasal dari rata-rata *subword* IndoBERTweet yang dibekukan, diproyeksikan ke dimensi encoder (proyeksi diinisialisasi nol), lalu **ditambahkan** ke representasi token di antara lapisan 1 dan 2.
4. Token tanpa kecocokan tidak berubah.

Ambang 0,7 dan panjang jendela adalah nilai awal dari uji simulasi dan ditetapkan di data validasi, bukan data uji. Rincian implementasi dikunci pada saat kode ditulis.

**4. Efficient GlobalPointer.** Untuk setiap pasangan token (i, j) dan tipe t: s_t(i,j) = q_iᵀ k_j + w_tᵀ[q_i; k_i; q_j; k_j], dengan posisi relatif dikodekan *Rotary Position Embedding*. *Span* dengan s_t(i,j) > 0 diprediksi sebagai entitas bertipe t. *Loss*: *multilabel categorical cross-entropy*.

**5. Prapemrosesan *sliding window*.** Dokumen yang melebihi batas encoder dipotong menjadi jendela (misalnya 256 token, tumpang tindih 64 sampai 128 token). Posisi entitas dikembalikan ke posisi karakter asli, entitas yang sama dari dua jendela digabung, dan bila berbeda dipilih jendela tempat entitas paling jauh dari tepi. Ini prapemrosesan, bukan komponen arsitektur.

### Contoh alur (ilustrasi desain, bukan hasil uji)

Kalimat: "ngaku CS **buka lapak**, suruh tf **2jt**"

1. Teks dipecah menjadi kata dan *subword*.
2. IndoBERTweet lapisan 1 menghasilkan representasi awal setiap token.
3. CharCNN membaca huruf setiap kata (misalnya pola nominal pada *2jt*) dan menambahkan hasilnya ke representasi kata tersebut.
4. Leksikon Toleran menormalkan *buka lapak* menjadi *bukalapak*, menemukan entri yang cocok, lalu menambahkan vektor entri ke token *buka* dan *lapak*.
5. IndoBERTweet lapisan 2 sampai 12 membaca ulang representasi yang sudah diperkaya bersama konteks kalimat.
6. EGP menilai setiap potongan kalimat:
   - *buka lapak* → PLATFORM;
   - *ngaku CS buka lapak* → PELAKU (PLATFORM bertumpuk di dalamnya);
   - *2jt* → NOMINAL;
   - *suruh tf 2jt* → MODUS (NOMINAL bertumpuk di dalamnya).

### Mengapa dua cabang, dan risiko leksikon

Dua cabang dipilih karena masing-masing diharapkan menutup kelemahan yang lain. Isi tabel berikut adalah **hipotesis desain** yang diuji lewat ablasi, bukan hasil pada data keluhan; satu-satunya dukungan literatur untuk CharCNN adalah Kurniawan & Louvan (2018) pada kata di luar kosakata:

| Jenis varian | CharCNN | Leksikon Toleran |
|---|---|---|
| Salah ketik (*shoppe*, *shopie*) | Diharapkan kuat | Diharapkan kuat (kemiripan trigram) |
| Nominal informal (*2jt*, *100k*) | Diharapkan kuat | Tidak relevan |
| **Dipisah spasi (*buka lapak*)** | **Diharapkan lemah** (membaca per kata) | **Diharapkan kuat** (spasi dinormalkan) |
| Singkatan (*tokped*, *wa*) | Sebagian | Diharapkan kuat bila singkatan ada di daftar |
| Nama baru di luar daftar | Sebagian | **Tidak membantu**, bahkan berisiko |
| Kata ambigu (*dana*) | Tidak membantu | **Berisiko**: kata biasa ikut ditandai sebagai nama |

Varian berspasi adalah 61% dari varian ejaan nama platform (287 dari 468), sehingga ini alasan terkuat menambahkan leksikon di samping CharCNN. Namun bukti dari simulasi harus dibaca apa adanya:

| Bukti (simulasi NERP, bukan data keluhan asli) | Arti untuk usulan |
|---|---|
| LA toleran 0,8200 vs LA persis 0,8119 vs tanpa leksikon 0,7920 (uji kotak LA) | Pencocokan toleran lebih baik dari persis, dan leksikon menaikkan F1 total |
| Semua susunan berkamus menurunkan *recall* entitas di luar kamus 5 sampai 11 poin; toleran polos paling parah (0,6115 vs 0,7197 tanpa kamus) | **Risiko utama.** Nama pinjol dan akun baru terus muncul, sehingga *recall* di luar daftar wajib dipantau (kriteria H5) |
| LA persis menurunkan akurasi kata ambigu −3,28 poin [−6,61; +0,06] | Kata seperti *dana* dapat salah ditandai (kriteria H4) |
| Gerbang konstan lebih baik dari toleran polos (+1,35 F1; *recall* di luar kamus 0,6673) | Bila H5 gagal, **susunan cadangan** memakai gerbang konstan (bukan gerbang kontekstual) |

Simulasi memakai leksikon yang cakupannya diatur (70% entitas), sehingga manfaat pada data asli bisa lebih kecil. Karena itu leksikon dilaporkan sebagai **komponen bersyarat ablasi**: bila H5 gagal pada data asli, usulan kembali ke IndoBERTweet + CharCNN + EGP. Uji simulasi lain (LC-Gate, *boundary smoothing*, modifikasi kepala EGP) tidak memberi perbaikan yang terkonfirmasi dan tidak dilanjutkan. CharCNN dan IndoBERTweet sendiri belum pernah diuji.

### Keterbatasan CharCNN yang diakui

Selain tabel di atas, model yang lebih sederhana (IndoBERTweet + EGP) mungkin sudah menangani sebagian besar masalah. Di simulasi uji kotak LA, model tanpa tambahan apa pun sudah mencapai *recall* entitas berejaan varian 0,77. Kontribusi CharCNN dan Leksikon Toleran karena itu **wajib dibuktikan lewat ablasi**, masing-masing terhadap IndoBERTweet + EGP.

---

## 8. Rencana Uji Coba

Seluruh uji dijalankan pada dataset keluhan asli (K1) dan belum ada hasil pada data itu. Uji pendahuluan *Character Adapter* (CA) pada data awal tidak menunjukkan keuntungan dan implementasinya perlu diperiksa, sehingga hasil itu tidak dipakai sebagai bukti.

### Cara membaca rencana ini

Setiap uji hanya mengubah satu hal, punya satu pertanyaan, dan punya satu pembanding yang jelas. Pemenang tiap tahap menjadi dasar tahap berikutnya, sehingga model dirakit bertahap dan setiap komponen dapat dinilai sendiri. Hasil dilaporkan apa adanya, termasuk bila komponen usulan tidak terbukti.

Dua istilah dibedakan agar tidak tertukar:

| Istilah | Isi | Fungsi |
|---|---|---|
| ***Baseline* uji (B-Tweet)** | *Encoder* terpilih + Efficient GlobalPointer (EGP), tanpa adaptor | Pembanding semua penambahan komponen di Tahap 3 |
| **Rujukan literatur (MGBERT-Pointer)** | BERT + CA + EA + LA + EGP (Zhang dkk., 2024) | Sumber struktur. Hanya dibandingkan lewat rakitan R-MGBERT di Tahap 3, karena EA dibuang (Bagian 7) |

Nama "B-Tweet" dipakai di seluruh dokumen. Bila *encoder* terpilih di Tahap 1 bukan IndoBERTweet, "B-Tweet" dibaca sebagai *encoder* terpilih, dan judul serta rumusan arsitektur disesuaikan.

### Aturan bersama semua uji

- **Data:** satu pembagian latih, validasi, dan uji untuk semua susunan, dibagi per kelompok duplikat agar tidak terjadi kebocoran (*leakage*) dan distratifikasi menurut sumber (Play Store dan X). Data uji tidak disentuh sebelum susunan dikunci.
- **Teks tidak dinormalkan:** semua *encoder* menerima teks yang sama tanpa normalisasi kata tidak baku, supaya perbedaan berasal dari model.
- **Penalaan:** anggaran yang sama untuk setiap susunan (misalnya *learning rate* 1e-5, 2e-5, 3e-5, dan 5e-5 pada data validasi), dengan *early stopping* pada F1 validasi.
- **Adaptor diperlakukan setara:** CA, CharCNN, dan leksikon memakai inisialisasi proyeksi yang sama (awal nol, sehingga keluaran awal identik dengan *baseline*) dan penalaan *learning rate* adaptor yang sama.
- **Dokumen panjang:** semua susunan memakai *sliding window* yang sama, dengan penggabungan prediksi yang sama pula, termasuk untuk CRF dan *biaffine*.
- **Prasyarat data:** ketepatan seleksi korban (sampel cek per sumber, interval Wilson 95%) dan pilot anotasi ganda dipenuhi sebelum eksperimen utama (Lampiran A).
- **Metrik:** F1 total (*micro*, *strict span*) dan per tipe entitas; F1 subset (varian ejaan nama, nominal informal, entitas bertumpuk, entitas di luar data latih, kata ambigu); galat batas; waktu latih dan parameter tambahan. Perbandingan memakai uji *paired bootstrap* di dalam satu notebook.
- **Jumlah pengulangan:** ditetapkan kemudian. Rencana ini hanya menentukan apa yang diuji dan untuk apa.

### Tahap 1: memilih *encoder* (kepala tetap EGP)

| ID | Susunan | Pertanyaan | Untuk apa |
|---|---|---|---|
| B-mBERT | mBERT + EGP | Seberapa jauh tanpa pralatih bahasa Indonesia? | Batas bawah |
| B-Indo | IndoBERT + EGP | Apakah pralatih bahasa Indonesia umum membantu? | Pembanding pralatih umum |
| **B-Tweet** | **IndoBERTweet + EGP** | **Apakah pralatih tweet mengungguli IndoBERT pada teks tidak baku dan tidak dinormalkan?** | **Memilih *encoder* (H7)** |
| B-XLMR (opsional) | XLM-R *base* + EGP | XLM-R terbaik pada NER dokumen hukum Indonesia (Yulianti dkk., 2024); apakah juga pada keluhan? | Pembanding tambahan |

IndoBERT dibandingkan dengan IndoBERTweet untuk menjawab satu hal: apakah pralatih media sosial memang diperlukan, atau pralatih umum sudah cukup. *Encoder* terbaik menurut F1 total dipakai di Tahap 2 dan 3.

### Tahap 2: membuktikan kepala prediksi (*encoder* terpilih)

EGP adalah komponen inti untuk entitas bertumpuk (*nested*) pada Bagian 6 dan 7, sehingga tahap ini membuktikan pilihan itu, bukan memilih ulang kepala dari F1 total saja.

| ID | Kepala | Representasi entitas bertumpuk | Pertanyaan | Untuk apa |
|---|---|---|---|---|
| B-Softmax | Klasifikasi token BIO | Satu label per token | Seberapa buruk pembanding paling sederhana? | Batas bawah kepala |
| B-CRF | CRF (BIO) | Satu label per token | Apa yang hilang bila kepala datar dipakai? | Pembanding NER Indonesia yang umum (Dave & Chowanda, 2024) |
| B-GP | GlobalPointer | *Span* | Apakah proyeksi per tipe lebih baik daripada proyeksi bersama? | Pembanding sesama keluarga GlobalPointer |
| B-Biaffine | Dekoder *biaffine* (Yu dkk., 2020) | *Span* | Apakah dekoder *span* lain setara atau lebih baik? | Pembanding sesama dekoder *span* |
| **B-Tweet** | **EGP** | ***Span*** | **Apakah unggul pada entitas bertumpuk?** | **Membuktikan pilihan kepala (H6)** |
| B-CNNNER (opsional) | *Biaffine* + CNN 2D (Yan dkk., 2023) | *Span* | Apakah galat batas EGP besar? | Dijalankan hanya bila tumpang tindih sejati dari pilot anotasi tinggi |

B-Softmax dan B-CRF hanya memberi satu label per token. Entitas bertumpuk diratakan dengan aturan tetap (misalnya mengambil *span* terluar), lalu dievaluasi terhadap label emas yang tetap bertumpuk, sehingga kehilangan akibat pemerataan ikut terhitung. Hasil B-Tweet dipakai ulang dari Tahap 1.

**Aturan keputusan (ditetapkan sebelum *run*):** EGP dipertahankan, kecuali kepala lain unggul signifikan pada F1 total **tanpa** kalah pada F1 subset entitas bertumpuk. Bila itu terjadi, rumusan arsitektur dan judul disesuaikan.

### Hasil Tahap 1 dan 2 adalah *baseline* uji

*Encoder* terpilih + EGP menjadi B-Tweet. Semua komponen tambahan di Tahap 3 dibandingkan dengan susunan ini.

### Tahap 3: menambah komponen satu per satu pada *baseline* uji

| ID | Susunan | Pertanyaan | Hipotesis |
|---|---|---|---|
| A-Char | B-Tweet + CharCNN | Apakah fitur huruf membantu nominal informal dan salah ketik nama? | H2 |
| A-Lex | B-Tweet + Leksikon Toleran | Apakah leksikon membantu varian berspasi dan singkatan, dan seberapa besar risikonya pada nama baru dan kata ambigu? | H2, H4, H5 |
| A-LAp | B-Tweet + *Lexicon Adapter* persis | Apakah pencocokan toleran lebih baik daripada persis? Dibandingkan dengan A-Lex | H3 |
| A-CA | B-Tweet + CA (reimplementasi) | Apakah CharCNN lebih baik daripada CA MGBERT pada teks Indonesia? Dibandingkan dengan A-Char | H8 (K3) |
| **Usulan** | **B-Tweet + CharCNN + Leksikon Toleran** | **Apakah gabungan lebih baik daripada *baseline* uji dan daripada masing-masing komponen?** | **H1** |
| R-MGBERT | B-Tweet + CA + LA persis (MGBERT-Pointer tanpa EA) | Apakah Usulan lebih baik daripada rakitan model rujukan? | Pembanding akhir, dilaporkan tanpa kriteria keputusan |
| A-Konstan (cadangan) | Usulan dengan gerbang konstan pada leksikon | Dijalankan hanya bila H5 gagal | H5 |

**Catatan CA.** A-CA dan R-MGBERT dijalankan setelah implementasi CA diperiksa dan diperbaiki, karena penurunan F1 besar pada uji pendahuluan IndoBERTweet lebih mungkin cacat implementasi daripada temuan. Keduanya memakai inisialisasi dan penalaan adaptor yang sama dengan CharCNN (aturan bersama). Bila CA ternyata sama baik atau lebih baik daripada CharCNN, CA dipertahankan dan klaim penggantian dicabut.

**Catatan R-MGBERT.** EA dibuang karena membutuhkan daftar entitas yang benar sebagai masukan (Bagian 7), sehingga rakitan ini disebut "MGBERT tanpa EA" dan tidak disebut MGBERT utuh.

Leksikon dibangun dari sumber eksternal dan dibekukan sebelum menyentuh data uji (nama penyelenggara berizin OJK, nama aplikasi Play Store, dan singkatan umum). Ambang kemiripan ditetapkan di data validasi, dan *recall* entitas di luar leksikon dilaporkan untuk setiap susunan.

### Tahap 4: analisis tambahan

- **Kurva belajar:** F1 terhadap 25%, 50%, 75%, dan 100% data latih untuk B-Tweet dan Usulan, untuk melihat apakah komponen tambahan membantu terutama saat data sedikit (M1).
- **Generalisasi antarsumber:** latih pada Play Store lalu uji pada X, dan sebaliknya, untuk B-Tweet dan Usulan.
- **Analisis galat:** 100 kesalahan acak dari susunan terbaik dikelompokkan menjadi batas meleset, tipe salah, entitas terlewat, kata ambigu, dan varian ejaan.

### Ringkasan susunan

Susunan wajib berjumlah 13: 3 *encoder* (B-mBERT, B-Indo, B-Tweet), 4 kepala tambahan (B-Softmax, B-CRF, B-GP, B-Biaffine), dan 6 susunan Tahap 3 (A-Char, A-Lex, A-LAp, A-CA, Usulan, R-MGBERT). Susunan opsional atau bersyarat: B-XLMR, B-CNNNER, A-Konstan. Sebelum CharCNN diaktifkan, penyebab lambatnya (23 kali lebih lambat dari *baseline* pada uji pendahuluan) didiagnosis dulu, karena itu menentukan kelayakan komputasi seluruh Tahap 3.

---

## 9. Kebaruan dan Karya Terdekat

### Pemetaan karya terhadap empat masalah

| Karya | 01 Kata tidak baku | 02 Ejaan nama bervariasi | 03 Nominal tidak baku | 04 Entitas bertumpuk |
|---|---|---|---|---|
| **MGBERT-Pointer** (Tionghoa, 2024), *baseline* | Ya, Weibo | Komponen karakter (CA), tidak dievaluasi khusus | Tidak dilaporkan | Dekoder EGP, tetapi dataset berlabel BIO (datar) |
| DaN+ (Denmark, 2020) | Ya, Twitter, Reddit, Arto | Normalisasi leksikal umum (MoNoise, tahap terpisah) | Tidak dilaporkan | Ya, dua tingkat |
| Aguilar dkk. (2017, Inggris) | Ya, media sosial *noisy* | Fitur urutan karakter | Tidak dilaporkan | Tidak dibahas (CRF) |
| SEMFF-NER (Inggris, 2024) | Ya, WNUT16 dan 17 | Tanpa fitur karakter | Tidak dilaporkan | Tidak dibahas (BIO, *softmax*) |
| Decoupled Attention dan Character-Word Mask (Tionghoa, 2026) | Weibo salah satu dataset uji | Pencocokan leksikon kata | Tidak dilaporkan | Metode berframing bertumpuk, dataset tidak dinyatakan bertumpuk |
| IDCNNLR + GlobalPointer (Tionghoa, 2024) | Tidak dilaporkan, tanpa data media sosial | Tanpa komponen karakter terpisah | Tidak dilaporkan | Ya, CMeEE (medis) |
| Yu dkk. (2020, Inggris) | Tidak, korpus formal | CNN karakter | Tidak dilaporkan | Ya, ACE dan GENIA |
| Kurniawan & Louvan (2018, Indonesia) | Ya, percakapan Indonesia | Model karakter, hingga +15 F1 pada kata di luar kosakata | Tidak dilaporkan | Tidak disebut di abstrak |
| **Usulan penelitian ini** | Target | Target | Target | Target |

> **Kesimpulan.** Berdasarkan penelusuran literatur penulis, setiap masalah (kata tidak baku, ejaan nama bervariasi, nominal tidak baku, dan entitas bertumpuk) telah disentuh oleh arsitektur yang berbeda, tetapi belum ditemukan arsitektur tunggal yang menanganinya sekaligus pada teks informal, baik berbahasa Indonesia maupun bahasa lain. Kebaruan penelitian ini karena itu diposisikan sebagai pengujian gabungan tersebut pada teks keluhan penipuan berbahasa Indonesia, dan kontribusinya diuji lewat ablasi.

*Catatan metode:* pemetaan memakai abstrak dan teks yang terbaca; penelusuran lewat mesin pencari dan halaman terbuka, belum mencakup Scopus, Web of Science, atau ACL Anthology secara sistematis (lihat akhir Bagian 9).

### Karya terdekat lain (hasil penelusuran; belum sistematis)

| Karya | Kombinasi | Beda dengan usulan |
|---|---|---|
| MGBERT-Pointer (Zhang et al., 2024) | BERT + CA (konvolusi karakter) + EA + LA + EGP | CA membaca urutan karakter kalimat dan hanya dievaluasi pada teks Tionghoa; usulan menguji CharCNN (huruf di dalam kata) sebagai pengganti, dan LA persis dibandingkan dengan pencocokan **toleran** |
| IDCNNLR + GlobalPointer (ASI, 2024) | Konvolusi berdilasi + **GlobalPointer** | Memakai GP, bukan EGP; bahasa Tionghoa |
| GTBERT-Pointer (Huang et al., 2025) | BERT + *Gazetteer Adapter* + *Type Adapter* + EGP | *Address parsing* Tionghoa; berbasis gazetir; teks lengkap belum terbaca |
| IndoBERTweet-CRF (proyek NER kripto) | IndoBERTweet + CRF | CRF, tanpa fitur karakter, bukan domain penipuan |
| GLiNER ringkas (ETASR) | NER *span* bahasa Indonesia | Bukan EGP; bukan teks keluhan |
| Pencocokan kamus toleran (Cohen & Sarawagi, 2004; Rijhwani et al., 2020; NetEase.AI, 2023) | Kemiripan string atau skor kontinu untuk kamus pada CRF, BiLSTM, atau koreksi teks | Bukan di dalam adaptor model kelas MGBERT dengan EGP; **pencocokan toleran sendiri bukan ide baru** |
| TWBiL (Zainuddin et al., 2025) | Word2Vec + Bi-LSTM + Transformer + *attention* | Label per kata, teks berita formal |
| CrimeNER (2026), AttackER (2024) | NER teks kejahatan dan keamanan siber | Teks resmi (siaran pers, laporan siber), bukan keluhan korban |

### Klaim kebaruan yang aman

1. **Objek dan data (celah global):** sejauh penelusuran, belum ditemukan NER pada **keluhan korban penipuan online yang ditulis langsung oleh pengguna**, dalam bahasa apa pun. Penelitian sejenis memakai teks resmi (CrimeNER, AttackER) atau memperlakukan penipuan sebagai klasifikasi dokumen (Arifman et al., 2026).
2. **Skema entitas:** lima tipe entitas penipuan dengan tumpukan terbatas (PLATFORM di dalam PELAKU, NOMINAL di dalam MODUS).
3. **Arsitektur (bersyarat ablasi):** belum ditemukan dalam penelusuran kombinasi encoder media sosial Indonesia + CharCNN tingkat huruf + pencocokan leksikon toleran di dalam adaptor + Efficient GlobalPointer. Kombinasi ini bukan kebaruan utama; semua komponennya sudah dikenal, termasuk pencocokan toleran.

**Yang tidak boleh diklaim:** "belum pernah ada CharCNN + EGP di dunia" (MGBERT sudah memakai konvolusi karakter + EGP), "pencocokan toleran adalah ide baru" (sudah ada di Cohen & Sarawagi, 2004), atau "leksikon toleran meningkatkan kinerja" sebelum H5 terpenuhi pada data asli.

Sebelum sidang, ulangi penelusuran sistematis di Scopus untuk setiap pasangan komponen dan objek (misalnya *scam victim complaint named entity recognition*, *character CNN efficient global pointer*, *IndoBERTweet named entity recognition*), lalu simpan daftar kueri dan hasilnya sebagai lampiran.

---

## 10. Kontribusi Penelitian

| Kode | Kontribusi | Status |
|---|---|---|
| **K1** | Dataset dan skema NER keluhan korban penipuan online berbahasa Indonesia (lima tipe, tumpukan terbatas), panduan anotasi, dan ukuran reliabilitas | **Klaim utama** |
| **K2** | Evaluasi ketat: perbandingan encoder, kepala *span* vs CRF, fitur karakter vs leksikon toleran, dengan beberapa *seed*, uji berpasangan, dan metrik subset | **Klaim utama** |
| K3 | Pertanyaan penelitian: apakah *Character Adapter* MGBERT-Pointer berfungsi pada teks Indonesia informal, dan apakah CharCNN tingkat huruf lebih baik darinya? | **Bersyarat** H1 dan H2; hasil negatif tetap dilaporkan |
| K4 | Pertanyaan penelitian: apakah Leksikon Toleran lebih baik dari *Lexicon Adapter* persis untuk varian ejaan nama? | **Bersyarat** H2, H3, H4, dan H5 |

Kontribusi lintas domain: data terstruktur dari keluhan korban (pelaku, platform, nominal, modus) dapat dipakai untuk pemetaan modus, pelacakan platform yang sering dicatut, dan dukungan bagi kanal pelaporan resmi seperti cekrekening.id dan Patrolisiber.id.

---

## 11. Antisipasi Pertanyaan Sidang

| Pertanyaan | Jawaban |
|---|---|
| **Kenapa MGBERT jadi *baseline* padahal untuk bahasa Tionghoa?** | Dipilih karena strukturnya: EGP untuk entitas bertumpuk, adaptor modular yang bisa diganti, dan penggabungan beberapa jenis informasi. Adaptornya hanya dievaluasi pada teks Tionghoa, jadi kecocokannya dengan teks Indonesia diuji, bukan diasumsikan. |
| **Dari mana tahu MGBERT menangani nominal tidak baku?** | Tidak diklaim. MGBERT punya adaptor karakter (CA), tetapi hanya dievaluasi pada teks Tionghoa. Karena itu CA diuji langsung pada data ini dan dibandingkan dengan CharCNN lewat ablasi. |
| **Kenapa CharCNN?** | Membaca huruf di dalam kata, sehingga tahan salah ketik (*shoppe*) dan pola nominal (*2jt*, *100k*) tanpa daftar nama. Fitur karakter sudah lazim di NER sejak Ma & Hovy (2016), di NER media sosial, dan pada NER teks percakapan Indonesia (Kurniawan & Louvan, 2018). |
| **Kenapa CA diganti CharCNN?** | Tidak diganti begitu saja. CA belum pernah diuji di luar bahasa Tionghoa, sehingga tidak ada bukti bahwa ia berfungsi pada ejaan tidak baku Indonesia. CharCNN punya rekam jejak pada NER Indonesia dan lebih sederhana. Keduanya dibandingkan langsung (A-CA vs A-Char); bila CA ternyata sama baik atau lebih baik, CA dipertahankan dan klaim penggantian dicabut. |
| **Kenapa EGP, bukan CRF?** | CRF memberi satu label per kata. Pada "tf dulu **100k**", *100k* harus menjadi NOMINAL sekaligus bagian MODUS, dan itu hanya bisa dengan prediksi berbasis *span*. Ada 107 pasangan bertumpuk pada 1.000 dokumen X (pra-anotasi). |
| **Kenapa EGP, bukan GlobalPointer biasa?** | EGP memakai *query* dan *key* bersama untuk semua tipe, sehingga parameternya lebih sedikit, cocok untuk data berlabel sedikit, dan sudah dipakai arsitektur rujukan. |
| **Kenapa leksikon dipakai padahal menurunkan *recall* di luar daftar?** | Di simulasi, leksikon menaikkan F1 total (LA persis +1,2; LA toleran +2,8 dibanding tanpa leksikon) dan menutup varian berspasi yang tidak terjangkau CharCNN, tetapi menurunkan *recall* di luar daftar 5 sampai 11 poin. Risiko ini diukur langsung (H5). Bila gagal pada data asli, leksikon dicoret atau diganti gerbang konstan (A-Konstan), dan usulan kembali ke IndoBERTweet + CharCNN + EGP. |
| **Apa bedanya leksikon toleran dengan LA MGBERT?** | LA MGBERT mencocokkan kata persis dari kosakata umum Tionghoa. Leksikon Toleran menormalkan spasi dan huruf berulang, memakai kemiripan *trigram* huruf, dan memakai daftar nama domain dari sumber eksternal. Idenya (pencocokan toleran) bukan baru, sehingga klaimnya hanya penerapan di dalam adaptor MGBERT untuk teks informal Indonesia. |
| **Kenapa tidak pakai LC-Gate?** | Gerbang kontekstual gugur pada uji konfirmasi dengan data simulasi: tidak lebih baik dari gerbang konstan (−0,30). Karena itu fusi dibuat aditif dan risiko ditangani lewat H5. |
| **Kalau IndoBERTweet + EGP saja sudah cukup?** | Itu diuji langsung (B-Tweet vs Usulan). Bila CharCNN tidak signifikan, hasil itu dilaporkan apa adanya dan tesis bertumpu pada dataset dan evaluasi (K1, K2). |
| **CharCNN gagal pada *buka lapak*?** | Benar, karena CharCNN membaca per kata. Karena itu Leksikon Toleran ditambahkan, yang menormalkan spasi. Varian berspasi sebagian besar ada di Play Store; hasilnya diukur di subset varian ejaan (H2). |
| **Bagaimana kata *dana*?** | Ditangani konteks encoder. CharCNN tidak membantu karena hurufnya sama, dan leksikon justru berisiko menandainya sebagai nama (LA persis −3,28 poin di simulasi). Akurasi kata ambigu diukur sebagai H4. |
| **Apa kebaruannya kalau semua komponen sudah ada?** | Kebaruan utama ada pada objek dan data (keluhan korban, celah global) serta skema entitas. Kombinasi arsitektur hanya kebaruan pendukung yang dibuktikan dengan ablasi. |
| **Bagaimana teks yang panjang?** | *Sliding window* dengan tumpang tindih di prapemrosesan; arsitekturnya tidak berubah. |
| **Label dari AI?** | Hanya pra-anotasi. Setiap dokumen diperiksa anotator manusia, dan kesepakatan antaranotator diukur. |

---

## 12. State of The Art

Tabel berikut merangkum 15 artikel ilmiah paling relevan dari tahun 2023 ke atas, terbit di jurnal atau prosiding yang terindeks Scopus. 

| No | Judul Artikel + Penulis (Tahun) | Objek dan Masalah | Metode Penyelesaian | Kinerja / Hasil | Relevansi terhadap penelitian | Link Akses |
|----|---------------------------------|-------------------|---------------------|-----------------|-------------------------|------------|
| 1 | **A hybrid machine learning approach for classifying Indonesian cybercrime discourse using a localized threat taxonomy** / Arifman, Mantoro & Handayani (2026) / *Information* (MDPI), Scopus Q2 | Wacana kejahatan siber berbahasa Indonesia di media sosial (X dan YouTube); taksonomi ancaman internasional (ENISA) tidak menangkap ancaman khas Indonesia | Taksonomi ICTT lima dimensi; label lemah dari pola regex (2.344 sampel); IndoBERT di-*fine-tune*; klasifikasi *hybrid* aturan + ML | Akurasi 96,8% pada 600 sampel beranotasi manual (IndoBERT saja juga 96,8%; berbasis aturan 66,7%); dari 124 sampel yang sah diklasifikasikan ke ICTT, 85 (68,5%) termasuk ancaman khas Indonesia, yaitu *phishing* WhatsApp (46) dan penipuan *deepfake* (39) | **Objek paling dekat**: teks kejahatan siber Indonesia di X. Riset penipuan berbahasa Indonesia baru sampai **klasifikasi**, belum **ekstraksi entitas**: celah objek tesis ini (K1) | [DOI](https://doi.org/10.3390/info17030301) |
| 2 | **IPerFEX-2023: Indonesian personal financial entity extraction using IndoBERT-BiGRU-CRF model** / Dave & Chowanda (2024) / *Journal of Big Data*, Scopus Q1 | NER finansial personal dari diskusi harian Indonesia; entitas numerik; 15 tipe entitas keuangan | IndoBERT (sebagai fitur, *feature-based*) + BiGRU + CRF; dataset dari Quora, ragam campuran formal dan percakapan | F1 makro 0,73 pada IPerFEX-*small* (1.857 kalimat, 1.299 kalimat latih), terbaik; turun menjadi 0,69 pada IPerFEX-*large* (2.645 kalimat) setelah 552 kalimat latih ditambahkan (Tabel 3 dan 7) | NER Indonesia pada teks **percakapan informal** dengan entitas **nominal**, mirip NOMINAL. Pembanding *decoder* CRF (susunan B-CRF) dan bukti bahwa data berlabel kecil membatasi kinerja (M1) | [Springer](https://link.springer.com/article/10.1186/s40537-024-00987-6) |
| 3 | **Information extraction from Indonesian crime news with named entity recognition** / Roy Rachman Sedik & Ade Romadhony (2023) / *Proc. 15th KST 2023* (IEEE) | Ekstraksi jenis, lokasi, dan waktu kejahatan dari berita *online* Indonesia; teks formal | **Kombinasi NER dan *Support Vector Machine* (SVM)** untuk mengekstrak lokasi dan waktu kejadian, lalu klasifikasi jenis kejahatan | F1 jenis kejahatan 92%; lokasi 90,8% (P 92,5%, R 89,2%); tanggal 94,1% | Satu-satunya ekstraksi informasi Indonesia pada domain **kriminal**; teks berita formal dengan tipe entitas umum dan metode non-*transformer*, bukan keluhan korban. Angka dicocokkan dengan abstrak tesis S2 penulis yang sama, karena teks lengkap makalah IEEE belum terbaca | [DOI](https://doi.org/10.1109/KST57286.2023.10086789) |
| 4 | **Named entity recognition on Indonesian legal documents: a dataset and study using transformer-based models** / Yulianti et al. (2024) / *IJECE* 14(5), Scopus Q3 | NER dokumen hukum Indonesia (putusan pengadilan) | Komparasi IndoBERT, IndoRoBERTa, XLM-R, M-BERT pada IndoLER | F1 = 0,9295 (XLM-R terbaik); teks formal | Preseden **pembangunan dataset NER domain baru** berbahasa Indonesia (K1) dan **perbandingan *encoder*** (dasar susunan B-Indo vs B-Tweet). XLM-R terbaik di sini, sehingga layak dipertimbangkan sebagai pembanding | [DOI](https://doi.org/10.11591/ijece.v14i5.pp5489-5501) |
| 5 | **Biomedical named entity recognition based on multi-cross attention feature fusion** / Zheng, Han, Yu & Li (2024) / *PLOS ONE* 19(5): e0304329, Scopus Q1 | NER biomedis berbahasa Inggris; CharCNN dan CharRNN biasanya dipakai terpisah dan hanya disambung ke fitur kata, sehingga interaksi fitur kata dan huruf diabaikan | DistilBioBERT (fitur kata) + **CharCNN** dan CharLSTM (fitur huruf), difusikan tiga kali dengan *cross-attention*, lalu BiLSTM + *multi-head attention*; *loss* gabungan *cross-entropy* + *Focal Loss* | F1 90,76% (NCBI-Disease), 89,79% (BC5CDR-Disease), 94,98% (BC5CDR-Chem), 80,27% (JNLPBA), 88,84% (BC2GM). Pada uji modul BC5CDR-Disease, CharCNN unggul atas CharLSTM bila dipakai sendiri | Satu-satunya bukti 2023 ke atas yang ditemukan untuk **fitur huruf CharCNN di atas *encoder transformer*** pada aksara Latin (masalah 02 dan 03). Perbedaan dengan usulan: fusi *cross-attention* di atas keluaran *encoder* (bukan aditif di antara lapisan 1 dan 2), domain formal, dan bukan *decoder span*. Dipakai sebagai bukti mekanisme, bukan bukti domain | [DOI](https://doi.org/10.1371/journal.pone.0304329) |
| 6 | **KnowCTI: Knowledge-based cyber threat intelligence entity and relation extraction** / Wang et al. (2024) / *Computers & Security* 141: 103824, Scopus Q1 | Ekstraksi entitas dan relasi CTI; model NLP umum tidak memahami semantik keamanan siber | *Knowledge base* siber + GAT + *gate mechanism* + BERT; entitas didekode sebagai pelabelan sekuens dengan CRF | F1 makro entitas 90,16% (P 92,96%, R 87,52%), relasi 81,83%; unggul 9,75 poin atas BERT-BiLSTM-CRF (Tabel 3) | **Preseden injeksi pengetahuan domain eksternal** pada ekstraksi entitas siber (bukan pencocokan kamus, sehingga **bukan** dasar langsung Leksikon Toleran). Mekanisme gerbangnya sejalan dengan LC-Gate yang gugur pada uji simulasi, sehingga artikel ini juga menjadi pembanding mengapa usulan memakai fusi aditif | [DOI](https://doi.org/10.1016/j.cose.2024.103824) |
| 7 | **Sequential lexicon enhanced BERT: Chinese NER using sequential lexicon enhanced BERT (SLEBERT)** / Liu et al. (2024) / *PeerJ CS*, Scopus Q1 (2024) | Kelemahan LEBERT: *noise words* dan *lexical conflict* | *Sequential lexicon* + *position encoding* + *adaptive attention* di atas *Lexicon Adapter* LEBERT; lapisan keluaran tidak dirinci di teks | Weibo F1 = 71,76% (+1,01 vs LEBERT), MSRA 95,78%, OntoNotes 82,68%, Resume 96,38% (Tabel 4; Tabel 5 menulis MSRA 95,88%, tidak konsisten di makalah) | **Garis keturunan *Lexicon Adapter*.** Peringatan risiko: bahkan pada Mandarin, LA membawa kata derau dan konflik leksikon (M4 menyebut *lexical conflict*), sehingga leksikon usulan diuji dengan H4 dan H5 | [DOI](https://doi.org/10.7717/peerj-cs.2344) |
| 8 | **Enhanced Chinese named entity recognition with multi-granularity BERT adapter and efficient global pointer** / Zhang, Xia, Ma, Yang & Ding (2024) / *Complex & Intelligent Systems*, Scopus Q1 | Chinese NER dengan entitas bersarang dan batas ambigu | *Multi-Granularity Adapter* (CA + EA + LA) di antara lapisan 1 dan 2 BERT + Efficient GlobalPointer | Weibo F1 = 73,22%, Resume 96,23%, OntoNotes 83,25%, MSRA 96,10% (Tabel 3); unggul 5,95 poin atas BERT pada Weibo; makalah mengakui adanya informasi redundan (hlm. 4488) | ***Baseline* rujukan struktur (dirakit sebagai R-MGBERT, tanpa EA).** Struktur dipertahankan (adaptor di antara lapisan 1 dan 2, kepala EGP). **CA dibandingkan dengan CharCNN** (CA hanya dievaluasi pada teks Tionghoa), **LA persis dibandingkan dengan Leksikon Toleran**, **EA dibuang** (butuh triplet entitas saat inferensi), **EGP dipertahankan** | [DOI](https://doi.org/10.1007/s40747-024-01383-6) |
| 9 | **LB-BMBC: MHBiaffine-CNN to capture span scores with BERT injected with lexical information for Chinese NER** / Guo & Zhang (2024) / *IJCIS*, Scopus Q2 | Chinese NER; relasi antar-*span* diabaikan Biaffine | *Lexicon Adapter* di lapisan Transformer BERT dengan koefisien γ skalar (Pers. 10) + BiLSTM + *Multi-Head Biaffine* + CNN pada matriks skor | F1 Resume 96,29; Weibo 68,64; OntoNotes 81,35; MSRA 95,50. Terbaik hanya di antara pembanding pada Tabel 3 dan 4; LEBERT (Weibo 70,75; OntoNotes 82,08) dan MGBERT-Pointer tidak dibandingkan dan lebih tinggi. CNN pada matriks skor menaikkan F1 Weibo 8,44 poin (B-MB ke B-MBC) | **Pembanding injeksi leksikon dan *decoder* span.** Menunjukkan ruang modifikasi leksikon sudah padat; CNN pada matriks skor adalah kandidat cadangan bila batas entitas bermasalah | [DOI](https://doi.org/10.1007/s44196-024-00521-9) |
| 10 | **Improving named entity recognition for social media with data augmentation** / Liu & Cui (2023) / *Applied Sciences* 13(9): 5360 (MDPI), Scopus Q3 (2023) | NER teks media sosial yang informal dan tidak terstruktur; data berlabel terbatas dan kelas tidak seimbang | Kerangka DA-NER: BERT + augmentasi data + Bi-LSTM + *self-attention* + CRF | F1 WNUT16 61,61%, WNUT17 63,04%, OntoNotes 91,03% | **Bukti NER teks informal sulit** (masalah 01) dan bahwa data berlabel sedikit membatasi kinerja (M1): F1 WNUT jauh di bawah teks formal. Catatan: artikel ini tidak menguji IndoBERTweet, sehingga tidak dipakai sebagai dasar pilihan *encoder* | [DOI](https://doi.org/10.3390/app13095360) |
| 11 | **A Chinese nested named entity recognition model for chicken disease based on multiple fine-grained feature fusion and efficient global pointer** / Wang, Peng, Li et al. (2024) / *Applied Sciences* 14(18): 8495 (MDPI), Scopus Q2 (2024) | NER teks penyakit ayam berbahasa Tionghoa; entitas bersarang, entitas khas domain, dan data berlabel langka. Dataset CDNER disusun dari 50 buku penyakit ayam (28 jenis penyakit) | MFGFF (fusi fitur berbutir halus) + BiLSTM + **Efficient GlobalPointer** untuk memprediksi posisi entitas | F1 79,68% untuk NER bersarang pada CDNER | Ini bukti EGP langsung pada **entitas bersarang dengan data berlabel terbatas** di domain khusus (masalah 04), sekaligus contoh pengayaan fitur sebelum EGP. Rincian MFGFF belum dibaca dari teks lengkap | [DOI](https://doi.org/10.3390/app14188495) |
| 12 | **Named entity recognition for Chinese scientific literature based on adversarial training and dual-masked global pointer** / Zhang et al. (2025) / *Complex & Intelligent Systems*, Scopus Q1 | NER literatur sains Cina; korpus berlabel minim dan entitas bersarang | StructBERT + *adversarial training* + *Dual-Masked Global Pointer* | F1 makro pada korpus sendiri (1.100 abstrak, 22.184 entitas): **GlobalPointer 68,10% > Biaffine 54,72% > CRF 53,73%**; DMGP penuh 70,23%; semua pembanding memakai *encoder* StructBERT (Tabel 6, terverifikasi dari teks lengkap) | **Bukti empiris *decoder* keluarga GlobalPointer** pada domain spesifik dengan data terbatas. Catatan: yang diuji adalah GP, bukan EGP | [DOI](https://doi.org/10.1007/s40747-025-02041-1) |
| 13 | **Indonesian hate speech detection using IndoBERTweet and BiLSTM on Twitter** / Kusuma & Chowanda (2023) / *JOIV* 7(3): 773 sampai 780, Scopus Q3 (2023) | Deteksi ujaran kebencian pada tweet Indonesia; dua dataset publik (Alfina et al., 713 data; Ibrohim & Budi, 13.169 data) | IndoBERTweet + BiLSTM, dibandingkan dengan IndoBERTweet yang di-*fine-tune* dan IndoBERTweet + CNN | Terbaik IndoBERTweet + BiLSTM: akurasi 93,7%, F1 93,3%. Penandaan dataset di teks dan di Tabel IX tidak konsisten | Bukti 2023 ke atas **pemakaian IndoBERTweet pada teks X berbahasa Indonesia** (masalah 01). **Keterbatasan penting:** tugasnya klasifikasi, bukan NER; kata tidak baku dan salah ketik dinormalkan dengan kamus **sebelum** masuk model; tidak ada pembanding IndoBERT dalam eksperimen yang sama; satu kali *run*. Karena itu artikel ini tidak membuktikan IndoBERTweet unggul atas IndoBERT, dan perbandingan itu tetap menjadi pertanyaan eksperimen (B-Indo vs B-Tweet) | [DOI](https://doi.org/10.30630/joiv.7.3.1035) |
| 14 | **An embarrassingly easy but strong baseline for nested named entity recognition** / Yan, Sun, Li & Qiu (2023) / *ACL 2023* | NER bersarang; skor span biaffine dihitung terpisah | Biaffine + CNN 2D di atas matriks skor span | Kuat pada dataset *nested* standar | **Cadangan untuk masalah 04.** Bila tumpang tindih sejati pada data anotasi ternyata tinggi atau batas *span* sering salah, CNN 2D di atas matriks skor EGP menjadi opsi (catatan: pada simulasi NERP, konvolusi 3×3 di atas matriks skor tidak memberi perbaikan signifikan) | [ACL](https://aclanthology.org/2023.acl-short.123/) |
| 15 | **Entity extraction in Indonesian online news using named entity recognition (NER) with hybrid method Transformer, Word2Vec, attention and Bi-LSTM** / Zainuddin, Mudassir & Tahir (2025) / *JOIV* 9(3), Scopus Q3 (2025) | NER bahasa Indonesia pada berita *online* (Detik.com), 3 tipe entitas, 5.000 kalimat | TWBiL: Word2Vec + Bi-LSTM + Transformer 1 lapis + *attention*, ditambah fitur kelas kata dari *POS tagging*; anotasi BILUO | F1 85,11 vs Bi-LSTM 75,18; angka antartabel tidak konsisten (F1 validasi BW 0,67 di atas Bi-LSTM 0,5985, tetapi F1 uji BW 72,50 di bawah 75,18; *learning rate* optimal ditulis 10 di teks dan 2,71E-03 di Gambar 6), tanpa pembanding IndoBERT, tidak melaporkan banyak *run* | **Preseden NER *hybrid* di Unhas** dan pola judul tesis; standar metodologis yang harus dilampaui (pembanding IndoBERT, banyak *seed*, uji signifikansi) | [JOIV](https://joiv.org/index.php/joiv/article/view/2902) |

#### Status Publikasi dan Indeks

| No | Venue | Jenis | Terindeks Scopus? | Catatan |
|---|---|---|---|---|
| 1 | *Information* (MDPI) | Jurnal | Ya | Q2 (*Information Systems*, 2023 sampai 2025) |
| 2 | *Journal of Big Data* (Springer) | Jurnal | Ya | Q1 (2023 sampai 2025) |
| 3 | IEEE KST 2023 | **Prosiding** | **Belum dicek langsung** | Terbit di IEEE Xplore, terkonfirmasi lewat Crossref (DOI 10.1109/KST57286.2023.10086789); status Scopus prosidingnya dicek langsung di Scopus |
| 4 | *IJECE* | Jurnal | Ya untuk terbitan 2024 | **Cakupan Scopus 2014 sampai 2025, dihentikan pada 2025** menurut SCImago; Q3 (2024) |
| 5 | *PLOS ONE* | Jurnal | Ya | Q1 (*Multidisciplinary*, 2023 sampai 2025) |
| 6 | *Computers & Security* (Elsevier) | Jurnal | Ya | Q1 (2023 sampai 2025) |
| 7 | *PeerJ Computer Science* | Jurnal | Ya | Q1 (2023 dan 2024), Q2 (2025); cakupan 2015 sampai 2025 |
| 8 | *Complex & Intelligent Systems* (Springer) | Jurnal | Ya | Q1 (2023 sampai 2025); *baseline* utama |
| 9 | *Int. J. of Computational Intelligence Systems* | Jurnal | Ya | Q2 (2023 dan 2024), Q1 (2025) |
| 10 | *Applied Sciences* (MDPI) | Jurnal | Ya | Q3 pada 2023 (*Computer Science Applications*) |
| 11 | *Applied Sciences* (MDPI) | Jurnal | Ya | Q2 pada 2024 (*Computer Science Applications*) |
| 12 | *Complex & Intelligent Systems* (Springer) | Jurnal | Ya | Q1 (2023 sampai 2025) |
| 13 | *JOIV* | Jurnal | Ya | Q3 pada 2023 (*Computer Science (miscellaneous)*); cakupan 2017 sampai 2026 |
| 14 | ACL 2023 | **Prosiding** | Ya | Cakupan Scopus ACL 2022 sampai 2025 (SCImago) |
| 15 | *JOIV* | Jurnal | Ya | Q3 pada 2025 (*Computer Science (miscellaneous)*); EID Scopus 2-s2.0-105011696441 |

**Ringkasan:** 13 jurnal dan 2 prosiding. Status Scopus dan kuartil 13 jurnal dan ACL 2023 dicocokkan langsung ke SCImago (21 Oktober 2026), memakai kuartil pada tahun terbit artikel; satu jurnal dapat berbeda kuartil antarkategori, sehingga tabel mencantumkan kategori yang dipakai. Satu prosiding, IEEE KST 2023, belum dicek di Scopus Sources karena SCImago tidak memuat prosiding tersebut. DOI nomor 1 wajib dibuka langsung sebelum dikutip.

#### Peta Relevansi terhadap Penelitian

| No | Objek (kejahatan siber / penipuan, bahasa Indonesia) | Masalah inti yang disentuh (01 tidak baku, 02 ejaan, 03 nominal, 04 bertumpuk) | Arsitektur (IndoBERTweet, CharCNN, Leksikon Toleran, EGP) |
|---|---|---|---|
| 1 Arifman 2026 | **Ya**: kejahatan siber Indonesia di X | 01 | IndoBERT (klasifikasi, bukan NER) |
| 2 Dave & Chowanda 2024 | Sebagian: keuangan pribadi Indonesia | 01, 03 | IndoBERT + CRF (pembanding B-CRF) |
| 3 Sedik & Romadhony 2023 | Sebagian: berita kriminal Indonesia | Tidak (teks formal) | NER + SVM (bukan *transformer*) |
| 4 Yulianti 2024 | Sebagian: dokumen hukum Indonesia | Tidak (teks formal) | Perbandingan *encoder* Indonesia |
| 5 Zheng et al. 2024 | Tidak | 02, 03 (fitur huruf) | **CharCNN** di atas *encoder transformer* |
| 6 KnowCTI 2024 | Sebagian: intelijen ancaman siber | Pengetahuan eksternal | Injeksi pengetahuan domain (pembanding fusi bergerbang) |
| 7 SLEBERT 2024 | Tidak | Konflik leksikon | Garis keturunan *Lexicon Adapter* (peringatan risiko **Leksikon Toleran**) |
| 8 MGBERT-Pointer 2024 | Tidak | 04 | ***Baseline*: CA diuji vs CharCNN, LA persis diuji vs Leksikon Toleran, EGP dipertahankan** |
| 9 LB-BMBC 2024 | Tidak | 04 | Pembanding injeksi leksikon + *decoder* span |
| 10 Liu & Cui 2023 | Tidak | **01** | NER media sosial informal (bukan bukti *encoder*) |
| 11 Wang et al. 2024 (*Applied Sciences*) | Tidak | **04** | **EGP** pada NER bersarang dengan data terbatas |
| 12 DMGP 2025 | Tidak | 04 | Bukti *decoder* keluarga **GlobalPointer** |
| 13 Kusuma & Chowanda 2023 | Sebagian: teks X berbahasa Indonesia | **01** | **IndoBERTweet** (klasifikasi, bukan NER) |
| 14 Yan et al. 2023 | Tidak | 04 | Cadangan modul interaksi span |
| 15 Zainuddin et al. 2025 | Sebagian: berita Indonesia | Tidak (teks formal) | Preseden *hybrid* Unhas |

Setiap komponen arsitektur kini didukung minimal satu artikel 2023 ke atas: IndoBERTweet (13), CharCNN (5), Leksikon Toleran (7 dan 9, sebagai dasar sekaligus peringatan risiko), dan EGP (8, 11, 12). Yang terhubung ke **objek** penelitian (kejahatan siber atau penipuan berbahasa Indonesia) hanya nomor 1, dan nomor itu tidak mengerjakan NER: inilah celah objek penelitian ini. **Tidak satu pun** artikel menyentuh keempat masalah inti sekaligus pada teks Indonesia.

### Pola yang Muncul dari 15 Artikel SOTA

**P1: NER bahasa Indonesia masih jauh dari matang untuk domain penipuan.** Budi & Suryono (2023) menemukan nol paper tentang domain penipuan online dari 241 dokumen awal; paper 2 (Dave & Chowanda, 2024) hanya mencapai F1 = 0,73 untuk domain keuangan; paper 3 dan 4 menunjukkan bahwa ekstraksi entitas Indonesia baru matang untuk teks formal (berita kriminal dengan NER + SVM, dan dokumen hukum dengan *transformer*). Data prapenelitian (Bagian 3) menegaskan jarak ragam itu: 74,9% sampai 92,9% keluhan korban memuat kata tidak baku, dibanding 2,4% teks Wikipedia.

**P2: Fitur karakter dan *decoder* span keluarga GlobalPointer sudah ada, tetapi terpisah dan belum pada teks Latin informal berbahasa Indonesia.** Paper 8 (MGBERT-Pointer) memakai *Character Adapter* atas karakter kalimat + EGP, hanya dievaluasi pada teks Tionghoa; paper 11 memakai fusi fitur berbutir halus + EGP untuk entitas bersarang dengan data terbatas, juga pada bahasa Tionghoa. Pada aksara Latin, paper 5 menunjukkan CharCNN masih dipakai bersama *encoder transformer* (2024), tetapi pada teks biomedis formal, dengan fusi *cross-attention* dan tanpa *decoder span*. Karena itu **gabungan komponen ini bukan klaim kebaruan utama**; kebaruan ada pada objek dan data (P3), sedangkan kegunaan CharCNN dan Leksikon Toleran di posisi adaptor MGBERT diuji lewat ablasi (K3 dan K4 bersyarat).

**P3: Riset penipuan berbahasa Indonesia baru sampai klasifikasi, dan IndoBERTweet baru teruji untuk klasifikasi.** Paper 1 (Arifman et al., 2026) adalah karya terdekat dari sisi objek, tetapi tugasnya klasifikasi wacana. Paper 13 memakai IndoBERTweet pada teks X Indonesia, juga untuk klasifikasi, dan menormalkan kata tidak baku sebelum masuk model. Dalam penelusuran belum ditemukan artikel Scopus 2023 ke atas yang menguji IndoBERTweet untuk NER, dan belum ditemukan dataset NER beranotasi untuk keluhan korban penipuan online berbahasa Indonesia, apalagi dengan entitas bertumpuk terbatas (PLATFORM di dalam PELAKU, NOMINAL di dalam MODUS). Inilah dasar kontribusi utama K1 (dataset dan skema) dan K2 (evaluasi ketat), termasuk perbandingan B-Indo vs B-Tweet pada teks yang **tidak** dinormalkan.

**P4: Jalur leksikon padat dan berisiko pada teks bising, sehingga leksikon dipakai bersyarat.** Paper 6, 7, dan 9 menunjukkan bahwa menyuntikkan kamus atau pengetahuan eksternal adalah jalur yang ramai, dengan perbaikan umumnya pada pembobotan atau gerbang (KnowCTI, SLEBERT, LB-BMBC). Pencocokan kamus toleran sudah ada di model lain (Cohen & Sarawagi, 2004; Rijhwani et al., 2020; Lu et al., 2023). Uji kelayakan pada data simulasi menunjukkan LA toleran lebih baik dari persis, tetapi semua susunan berkamus menurunkan *recall* entitas di luar kamus, dan gerbang kontekstual tidak lebih baik dari gerbang konstan. Karena itu usulan memakai Leksikon Toleran dengan fusi aditif, **tanpa klaim kebaruan pencocokan**, hanya sebagai komponen yang kegunaannya dan risikonya diukur lewat H2, H4, dan H5.

---

## 13. Daftar Pustaka

Format IEEE. Dokumen ini memakai sitasi nama dan tahun di dalam teks, sehingga daftar diurutkan menurut abjad nama belakang penulis pertama agar mudah dicocokkan. Bila nanti sitasi diubah menjadi nomor, urutan nomor mengikuti kemunculan pertama di teks. Seluruh entri diperiksa pada 21 Oktober 2026 terhadap Crossref, halaman penerbit, ACL Anthology, atau berita sumbernya.

[1] G. Aguilar, S. Maharjan, A. P. López-Monroy, and T. Solorio, "A multi-task approach for named entity recognition in social media data," in *Proc. 3rd Workshop Noisy User-generated Text (W-NUT)*, Copenhagen, Denmark, 2017, pp. 148–153, doi: 10.18653/v1/W17-4419.

[2] G. Aguilar, A. P. López-Monroy, F. González, and T. Solorio, "Modeling noisiness to recognize named entities using multitask neural networks on social media," in *Proc. NAACL-HLT*, New Orleans, LA, USA, 2018, pp. 1401–1412, doi: 10.18653/v1/N18-1127.

[3] Asosiasi Penyelenggara Jasa Internet Indonesia (APJII), survei penetrasi internet Indonesia 2024 (8.720 responden), dilaporkan dalam "Penipuan online dan pencurian data pribadi diprediksi dominasi 2024," *CNN Indonesia*, 1 Feb. 2024. [Online]. Available: https://www.cnnindonesia.com/teknologi/20240201105221-192-1057074/penipuan-online-dan-pencurian-data-pribadidiprediksi-dominasi-2024

[4] F. Arifman, T. Mantoro, and D. O. D. Handayani, "A hybrid machine learning approach for classifying Indonesian cybercrime discourse using a localized threat taxonomy," *Information*, vol. 17, no. 3, Art. no. 301, 2026, doi: 10.3390/info17030301.

[5] I. Budi and R. R. Suryono, "Application of named entity recognition method for Indonesian datasets: A review," *Bull. Elect. Eng. Informat.*, vol. 12, no. 2, pp. 969–978, 2023, doi: 10.11591/eei.v12i2.4529.

[6] W. W. Cohen and S. Sarawagi, "Exploiting dictionaries in named entity extraction: Combining semi-Markov extraction processes and data integration methods," in *Proc. 10th ACM SIGKDD Int. Conf. Knowl. Discovery Data Mining (KDD)*, Seattle, WA, USA, 2004, pp. 89–98, doi: 10.1145/1014052.1014065.

[7] E. Dave and A. Chowanda, "IPerFEX-2023: Indonesian personal financial entity extraction using indoBERT-BiGRU-CRF model," *J. Big Data*, vol. 11, no. 1, Art. no. 139, 2024, doi: 10.1186/s40537-024-00987-6.

[8] J. Davin, "Dataset and IndoBERTweet-CRF model for Indonesian cryptocurrency named entity recognition," Mendeley Data, V1, Jun. 2026, doi: 10.17632/rtw4d5c6hj.1.

[9] P. Deka, S. Rajapaksha, R. Rani, A. Almutairi, and E. Karafili, "AttackER: Towards enhancing cyber-attack attribution with a named entity recognition dataset," in *Web Information Systems Engineering (WISE 2024)* (Lecture Notes in Computer Science, vol. 15440). Singapore: Springer, 2024, pp. 255–270, doi: 10.1007/978-981-96-0576-7_20.

[10] F. Dugas and E. Nichols, "DeepNNNER: Applying BLSTM-CNNs and extended lexicons to named entity recognition in tweets," in *Proc. 2nd Workshop Noisy User-generated Text (W-NUT)*, Osaka, Japan, 2016, pp. 178–187.

[11] D. I. Dzidny, M. A. Bijaksana, and K. M. Lhaksmana, "Supervised learning approaches for nested people entity extraction in Indonesian translated Quran," *Building Informat., Technol. Sci. (BITS)*, vol. 4, no. 1, pp. 241–246, 2022, doi: 10.47065/bits.v4i1.1758.

[12] B. Efron and R. J. Tibshirani, *An Introduction to the Bootstrap*. Boca Raton, FL, USA: Chapman & Hall/CRC, 1994, doi: 10.1201/9780429246593.

[13] M. Fuadi, A. D. Wibawa, and S. Sumpeno, "Robust and efficient Indonesian span-based named entity recognition via compact GLiNER: Towards enhanced retrieval-augmented generation," *Eng., Technol. Appl. Sci. Res. (ETASR)*, vol. 16, no. 3, pp. 36225–36232, 2026, doi: 10.48084/etasr.18482.

[14] M. Maclean, J. Abraham, and M. van der Meer, "State of scams in Indonesia 2025," Global Anti-Scam Alliance (GASA), in partnership with Mastercard, Oct. 2025. [Online]. Available: https://gasa.org/knowledge-base/reports/state-of-scams-in-indonesia-2025

[15] T. Guo and Z. Zhang, "LB-BMBC: MHBiaffine-CNN to capture span scores with BERT injected with lexical information for Chinese NER," *Int. J. Comput. Intell. Syst.*, vol. 17, no. 1, Art. no. 144, 2024, doi: 10.1007/s44196-024-00521-9.

[16] J. Huang, S. Liu, Y. Qiao, and Y. Wu, "Gazetteer- and type-enhanced Chinese address parsing BERT with an efficient global pointer," *Int. J. Digit. Earth*, vol. 18, no. 2, Art. no. 2594917, 2025, doi: 10.1080/17538947.2025.2594917.

[17] T. Julavanich and A. Aizawa, "NumER: A fine-grained numeral entity recognition dataset," in *Natural Language Processing and Information Systems (NLDB 2021)* (Lecture Notes in Computer Science). Cham, Switzerland: Springer, 2021, vol. 12801, pp. 64–75, doi: 10.1007/978-3-030-80599-9_7.

[18] "Kejahatan siber merajalela, ada 572.185 fraud mayoritas di e-commerce," *Bisnis.com*, 3 Sep. 2024. Data aduan Kemenkominfo (kanal cekrekening.id). [Online]. Available: https://teknologi.bisnis.com/read/20240903/84/1796481/kejahatan-siber-merajalela-ada-572185-fraud-mayoritas-di-e-commerce

[19] F. Koto, J. H. Lau, and T. Baldwin, "IndoBERTweet: A pretrained language model for Indonesian Twitter with effective domain-specific vocabulary initialization," in *Proc. Conf. Empirical Methods Natural Lang. Process. (EMNLP)*, Online and Punta Cana, Dominican Republic, 2021, pp. 10660–10668, doi: 10.18653/v1/2021.emnlp-main.833.

[20] K. Kurniawan and S. Louvan, "Empirical evaluation of character-based model on neural named-entity recognition in Indonesian conversational texts," in *Proc. 2018 EMNLP Workshop W-NUT: 4th Workshop Noisy User-generated Text*, Brussels, Belgium, 2018, pp. 85–92, doi: 10.18653/v1/W18-6112.

[21] J. F. Kusuma and A. Chowanda, "Indonesian hate speech detection using IndoBERTweet and BiLSTM on Twitter," *JOIV: Int. J. Informat. Visualization*, vol. 7, no. 3, pp. 773–780, 2023, doi: 10.30630/joiv.7.3.1035.

[22] M. Li, F. Gao, N. Qun, and T. Nyima, "Decoupled attention and character-word mask for Chinese nested named entity recognition," *Appl. Sci.*, vol. 16, no. 17, Art. no. 8630, 2026, doi: 10.3390/app16178630.

[23] W. Li, J. Liu, Y. Gao, X. Zhang, and J. Gu, "Research on Chinese nested entity recognition based on IDCNNLR and GlobalPointer," *Appl. Syst. Innov.*, vol. 7, no. 1, Art. no. 8, 2024, doi: 10.3390/asi7010008.

[24] Y. Li, Y. Zhou, X. Hu, Q. Li, and J. Tian, "A method for named entity recognition in social media texts with syntactically enhanced multiscale feature fusion," *Sci. Rep.*, vol. 14, Art. no. 28216, 2024, doi: 10.1038/s41598-024-78948-5.

[25] W. Liu and X. Cui, "Improving named entity recognition for social media with data augmentation," *Appl. Sci.*, vol. 13, no. 9, Art. no. 5360, 2023, doi: 10.3390/app13095360.

[26] W. Liu, X. Fu, Y. Zhang, and W. Xiao, "Lexicon enhanced Chinese sequence labeling using BERT adapter," in *Proc. 59th Annu. Meeting Assoc. Comput. Linguistics 11th Int. Joint Conf. Natural Lang. Process. (ACL-IJCNLP)*, Online, 2021, pp. 5847–5858, doi: 10.18653/v1/2021.acl-long.454.

[27] X. Liu, J. Zhao, J. Yao, H. Zheng, and Z. Wang, "Sequential lexicon enhanced bidirectional encoder representations from transformers: Chinese named entity recognition using sequential lexicon enhanced BERT," *PeerJ Comput. Sci.*, vol. 10, Art. no. e2344, 2024, doi: 10.7717/peerj-cs.2344.

[28] M. Lopez-Duran *et al.*, "Zero- and few-shot named-entity recognition: Case study and dataset in the crime domain (CrimeNER)," arXiv:2603.02150, 2026.

[29] R. Lu, Z. Tang, G. Hu, D. Liu, and J. Li, "NetEase.AI at SemEval-2023 Task 2: Enhancing complex named entities recognition in noisy scenarios via text error correction and external knowledge," in *Proc. 17th Int. Workshop Semantic Eval. (SemEval-2023)*, 2023, pp. 897–904, doi: 10.18653/v1/2023.semeval-1.124.

[30] W. Ma, Y. Cui, C. Si, T. Liu, S. Wang, and G. Hu, "CharBERT: Character-aware pre-trained language model," in *Proc. 28th Int. Conf. Comput. Linguistics (COLING)*, Barcelona, Spain (Online), 2020, pp. 39–50, doi: 10.18653/v1/2020.coling-main.4.

[31] X. Ma and E. Hovy, "End-to-end sequence labeling via bi-directional LSTM-CNNs-CRF," in *Proc. 54th Annu. Meeting Assoc. Comput. Linguistics (ACL)*, Berlin, Germany, 2016, pp. 1064–1074, doi: 10.18653/v1/P16-1101.

[32] T. Meng, A. Fang, O. Rokhlenko, and S. Malmasi, "GEMNET: Effective gated gazetteer representations for recognizing complex entities in low-context input," in *Proc. NAACL-HLT*, Online, 2021, pp. 1499–1512, doi: 10.18653/v1/2021.naacl-main.118.

[33] B. L. Monroe, M. P. Colaresi, and K. M. Quinn, "Fightin' words: Lexical feature selection and evaluation for identifying the content of political conflict," *Political Anal.*, vol. 16, no. 4, pp. 372–403, 2008.

[34] Y. Munarko, M. S. Sutrisno, W. A. I. Mahardika, I. Nuryasin, and Y. Azhar, "Named entity recognition model for Indonesian tweet using CRF classifier," *IOP Conf. Ser.: Mater. Sci. Eng.*, vol. 403, Art. no. 012067, 2018, doi: 10.1088/1757-899X/403/1/012067.

[35] Otoritas Jasa Keuangan (OJK) and Indonesia Anti-Scam Centre (IASC), data 128.281 laporan dan kerugian Rp2,6 triliun hingga 23 Mei 2025, dilaporkan dalam "OJK blokir 47 ribu rekening terkait penipuan online, kerugian dilaporkan Rp2,6 T," *Katadata.co.id*, 25 Mei 2025. [Online]. Available: https://katadata.co.id/finansial/keuangan/6832adcd37c82/ojk-blokir-47-ribu-rekening-terkait-penipuan-online-kerugian-dilaporkan-rp2-6-t

[36] B. Plank, K. N. Jensen, and R. van der Goot, "DaN+: Danish nested named entities and lexical normalization," in *Proc. 28th Int. Conf. Comput. Linguistics (COLING)*, Barcelona, Spain (Online), 2020, pp. 6649–6662, doi: 10.18653/v1/2020.coling-main.583.

[37] Y. H. P. P. Priyadarshana, L. Ranathunga, C. R. J. Amalraj, and I. Perera, "HelaNER: A novel approach for nested named entity boundary detection," in *Proc. 19th IEEE Int. Conf. Smart Technol. (EUROCON)*, Lviv, Ukraine, 2021, pp. 119–124, doi: 10.1109/EUROCON52738.2021.9535565.

[38] Y. H. P. P. Priyadarshana and L. Ranathunga, "HelaNER 2.0: A novel deep neural model for named entity boundary detection," *Int. J. Adv. Comput. Sci. Appl. (IJACSA)*, vol. 13, no. 9, pp. 121–130, 2022, doi: 10.14569/IJACSA.2022.0130914.

[39] S. Rijhwani, S. Zhou, G. Neubig, and J. Carbonell, "Soft gazetteers for low-resource named entity recognition," in *Proc. 58th Annu. Meeting Assoc. Comput. Linguistics (ACL)*, Online, 2020, pp. 8118–8123, doi: 10.18653/v1/2020.acl-main.722.

[40] P. Rust, J. Pfeiffer, I. Vulić, S. Ruder, and I. Gurevych, "How good is your tokenizer? On the monolingual performance of multilingual language models," in *Proc. 59th Annu. Meeting Assoc. Comput. Linguistics 11th Int. Joint Conf. Natural Lang. Process. (ACL-IJCNLP)*, Online, 2021, pp. 3118–3135, doi: 10.18653/v1/2021.acl-long.243.

[41] J. Salazar, D. Liang, T. Q. Nguyen, and K. Kirchhoff, "Masked language model scoring," in *Proc. 58th Annu. Meeting Assoc. Comput. Linguistics (ACL)*, Online, 2020, pp. 2699–2712, doi: 10.18653/v1/2020.acl-main.240.

[42] N. A. Salsabila, Y. A. Winatmoko, A. A. Septiandri, and A. Jamal, "Colloquial Indonesian lexicon," in *Proc. Int. Conf. Asian Lang. Process. (IALP)*, Bandung, Indonesia, 2018, pp. 226–229, doi: 10.1109/IALP.2018.8629151.

[43] R. R. Sedik and A. Romadhony, "Information extraction from Indonesian crime news with named entity recognition," in *Proc. 15th Int. Conf. Knowl. Smart Technol. (KST)*, 2023, pp. 1–5, doi: 10.1109/KST57286.2023.10086789. Keberadaan dan metadata terverifikasi lewat Crossref; angka hasil dicocokkan dengan abstrak tesis S2 Universitas Telkom milik penulis yang sama (R. R. Sedik, 2023), karena teks lengkap makalah IEEE belum terbaca.

[44] M. Shahzad, A. Amin, D. Esteves, and A.-C. Ngonga Ngomo, "InferNER: An attentive model leveraging the sentence-level information for named entity recognition in microblogs," in *Proc. Int. FLAIRS Conf.*, vol. 34, 2021, doi: 10.32473/flairs.v34i1.128538.

[45] Y. Song, S. Shi, J. Li, and H. Zhang, "Directional skip-gram: Explicitly distinguishing left and right context for word embeddings," in *Proc. NAACL-HLT (Short Papers)*, New Orleans, LA, USA, 2018, pp. 175–180, doi: 10.18653/v1/N18-2028.

[46] J. Su *et al.*, "Global Pointer: Novel efficient span-based approach for named entity recognition," arXiv:2208.03054, 2022.

[47] J. Su, "Efficient GlobalPointer: Fewer parameters, more effect" (in Chinese), *Scientific Spaces (kexue.fm)*, Jan. 25, 2022. [Online]. Available: https://kexue.fm/archives/8877

[48] D. Sundararaman, V. Subramanian, G. Wang, L. Xu, and L. Carin, "Improving downstream task performance by treating numbers as entities," in *Proc. 31st ACM Int. Conf. Inf. Knowl. Manage. (CIKM)*, 2022, pp. 4535–4539.

[49] G. Wang, P. Liu, J. Huang, H. Bin, X. Wang, and H. Zhu, "KnowCTI: Knowledge-based cyber threat intelligence entity and relation extraction," *Comput. Secur.*, vol. 141, Art. no. 103824, 2024, doi: 10.1016/j.cose.2024.103824.

[50] X. Wang *et al.*, "A Chinese nested named entity recognition model for chicken disease based on multiple fine-grained feature fusion and efficient global pointer," *Appl. Sci.*, vol. 14, no. 18, Art. no. 8495, 2024, doi: 10.3390/app14188495.

[51] B. Wilie *et al.*, "IndoNLU: Benchmark and resources for evaluating Indonesian natural language understanding," in *Proc. 1st Conf. Asia-Pacific Chapter Assoc. Comput. Linguistics 10th Int. Joint Conf. Natural Lang. Process. (AACL-IJCNLP)*, Suzhou, China, 2020, pp. 843–857, doi: 10.18653/v1/2020.aacl-main.85.

[52] E. B. Wilson, "Probable inference, the law of succession, and statistical inference," *J. Amer. Statist. Assoc.*, vol. 22, no. 158, pp. 209–212, 1927, doi: 10.1080/01621459.1927.10502953.

[53] H. Yan, Y. Sun, X. Li, and X. Qiu, "An embarrassingly easy but strong baseline for nested named entity recognition," in *Proc. 61st Annu. Meeting Assoc. Comput. Linguistics (ACL), Short Papers*, Toronto, Canada, 2023, pp. 1442–1452, doi: 10.18653/v1/2023.acl-short.123.

[54] J. Yu, B. Bohnet, and M. Poesio, "Named entity recognition as dependency parsing," in *Proc. 58th Annu. Meeting Assoc. Comput. Linguistics (ACL)*, Online, 2020, pp. 6470–6476, doi: 10.18653/v1/2020.acl-main.577.

[55] E. Yulianti, N. Bhary, J. Abdurrohman, F. W. Dwitilas, E. Q. Nuranti, and H. S. Husin, "Named entity recognition on Indonesian legal documents: A dataset and study using transformer-based models," *Int. J. Elect. Comput. Eng.*, vol. 14, no. 5, pp. 5489–5501, 2024, doi: 10.11591/ijece.v14i5.pp5489-5501.

[56] Z. Zainuddin, Mudassir, and Z. Tahir, "Entity extraction in Indonesian online news using named entity recognition (NER) with hybrid method Transformer, Word2Vec, attention and Bi-LSTM," *JOIV: Int. J. Informat. Visualization*, vol. 9, no. 3, pp. 964–973, 2025, doi: 10.62527/joiv.9.3.2902.

[57] L. Zhang, P. Xia, X. Ma, C. Yang, and X. Ding, "Enhanced Chinese named entity recognition with multi-granularity BERT adapter and efficient global pointer," *Complex Intell. Syst.*, vol. 10, no. 3, pp. 4473–4491, 2024, doi: 10.1007/s40747-024-01383-6.

[58] M. Zhang, Y. Li, Z. Zhang, Y. Wang, Q. Yu, and L. Ding, "Named entity recognition for Chinese scientific literature based on adversarial training and dual-masked global pointer," *Complex Intell. Syst.*, vol. 11, no. 10, Art. no. 447, 2025, doi: 10.1007/s40747-025-02041-1.

[59] X. Zhang, F. Li, C. Li, and X. Yu, "Chinese medical named entity recognition using pre-trained language models and an efficient global pointer mechanism," *Informatica*, vol. 49, no. 19, 2025, doi: 10.31449/inf.v49i19.8043.

[60] Y. Zhang and J. Yang, "Chinese NER using lattice LSTM," in *Proc. 56th Annu. Meeting Assoc. Comput. Linguistics (ACL)*, Melbourne, Australia, 2018, pp. 1554–1564, doi: 10.18653/v1/P18-1144.

[61] D. Zheng, R. Han, F. Yu, and Y. Li, "Biomedical named entity recognition based on multi-cross attention feature fusion," *PLOS ONE*, vol. 19, no. 5, Art. no. e0304329, 2024, doi: 10.1371/journal.pone.0304329.

*Catatan.* Munarko dkk. (2018) dan Wilie dkk. (2020) hanya muncul pada Bagian 12 lama (Referensi Kunci), bukan di teks bagian lain. Keduanya tetap dimasukkan karena dokumen merujuk IndoBERT dan data NERP. Hapus keduanya dari daftar bila tidak dikutip di naskah akhir.

---

## Lampiran A. Data dan Metode Prapenelitian

Lampiran ini memuat metode dan keputusan anotasi di balik angka Bagian 3. Seluruh angka berasal dari korpus baru yang dibersihkan dengan aturan yang sama untuk semua sumber (`ATURAN_PEMBERSIHAN_DATA.md` v1.4) dan dianalisis dengan notebook `PRA_PENELITIAN_ANALISIS_DATA.ipynb` (versi pra-1.0).

### A.1 Korpus dan desain analisis

| Sumber | Terkumpul | Lolos pembersihan | Kandidat keluhan korban |
|---|---|---|---|
| Ulasan Play Store bintang 1 dan 2 (27 aplikasi, 4 sektor: *e-commerce*, media sosial, dompet digital, *fintech*) | 659.845 | 514.254 | 3.531 |
| X (Twitter), kueri bertarget berlapis Q1 sampai Q8 | 4.391 | 3.997 | 2.501 |
| **Total kandidat** | | | **6.032** |

Kandidat keluhan korban dipilih dengan aturan narasi korban (S-06) yang mensyaratkan tiga hal sekaligus: narasi kejadian yang dialami penulis atau orang dekatnya, adanya pihak ketiga yang menipu, dan adanya kerugian atau upaya kerugian. Data pribadi dipseudonim dengan format sama sebelum dianalisis.

> **Status ketepatan: belum diukur.** Ketepatan aturan seleksi korban baru diketahui setelah sampel cek (300 dokumen per sumber) dilabeli V/W/T/O dan dihitung dengan interval Wilson. Sampai saat itu, semua angka di bawah berlaku untuk **kandidat** keluhan korban, bukan korpus korban terverifikasi, dan belum boleh dikutip sebagai angka final.

**Desain analisis.** Setiap angka korban dibandingkan dengan **teks pembanding dari platform yang sama** (20.000 sampel acak dari 510.723 ulasan pembanding Play Store; 1.496 tweet pembanding X), supaya efek ragam bahasa platform tidak tertukar dengan efek domain penipuan. Sebanyak 5.001 paragraf Wikipedia Indonesia dipakai sebagai rujukan teks formal. Selisih dianggap bermakna bila interval kepercayaan 95% (*bootstrap* 1.000 ulangan atau Wilson) tidak memuat nol **dan** selisihnya minimal 1 poin persen. *Tokenizer* yang diuji: IndoBERT (`indobenchmark/indobert-base-p1`) dan IndoBERTweet (`indolem/indobertweet-base-uncased`).

### A.2 Definisi kelompok: korban, kandidat korban, dan pembanding

Istilah "korban" dan "bukan korban" mudah disalahpahami, jadi dokumen ini memakai tiga istilah yang dibedakan tegas.

**Korban (definisi konseptual, dipakai saat pelabelan manusia, label V).** Teks yang **menceritakan kejadian penipuan online yang dialami penulis atau orang dekatnya**, dengan tiga syarat sekaligus: (1) ada narasi kejadian, bukan sekadar peringatan atau opini; (2) ada pihak ketiga yang menipu, menyamar, atau memanipulasi; (3) ada kerugian atau upaya kerugian (uang, akun, data). Peretasan akun atau saldo terkuras dihitung bila ada pelaku atau modus, atau ada kerugian nyata. Tagihan atas pinjaman yang tidak pernah diambil dihitung bila ada penagihan atau penyalahgunaan data. Yang **bukan** korban: peringatan atau tuduhan tanpa cerita (label W), keluhan teknis atau layanan seperti *error*, limit turun, biaya, dan permintaan hapus data (label T), serta lainnya (label O).

| Istilah dalam dokumen | Definisi operasional | Isi sebenarnya | Yang **tidak boleh** disimpulkan |
|---|---|---|---|
| **Kandidat korban** | Teks yang lolos aturan narasi korban S-06 (Tingkat A). Ditentukan **aturan**, bukan manusia | Sebagian besar narasi korban, tetapi masih memuat salah positif (peringatan, keluhan layanan) yang proporsinya **belum diukur** | Tidak boleh disebut "korban terverifikasi" |
| **Pembanding Play Store** | Sampel acak 20.000 dari 510.723 ulasan bersih yang **tidak lolos** S-06 | Keluhan teknis dan layanan, ulasan umum, peringatan atau tuduhan penipuan (Tingkat B), **dan korban yang terlewat aturan** (jumlahnya belum diukur) | Tidak boleh disebut "bukan korban" atau "teks normal" |
| **Pembanding X** | Seluruh 1.496 tweet hasil kueri penipuan yang tidak lolos S-06 | *Spill* rekening tanpa narasi, peringatan, diskusi atau berita penipuan, dan korban yang terlewat | Bukan kontrol netral; tidak ditafsirkan sebagai teks umum di X |
| **Rujukan formal** | 5.001 paragraf Wikipedia Indonesia | Teks ensiklopedis baku | Hanya rujukan ragam formal, bukan pembanding domain |

Label "korban" dalam arti sebenarnya baru ada setelah pelabelan manusia (V/W/T/O) pada sampel cek. Sebelum itu, semua perbandingan adalah **kandidat korban terhadap pembanding**, bukan korban terhadap bukan korban.

### A.3 Risiko sirkularitas dan pembaur (wajib diakui)

Perbandingan kandidat korban dengan pembanding **tidak netral** untuk semua indikator, karena kelompok dibentuk oleh aturan S-06 yang memakai sebagian indikator itu sebagai syarat seleksi.

1. **Sirkularitas.** S-06 memakai ungkapan nominal, kata kerugian (*sudah transfer*, *uang hilang*), serta pola pelaku, platform, dan modus sebagai bukti narasi. Teks yang memuat nominal atau banyak unsur entitas karena itu **lebih mungkin lolos** sebagai kandidat korban. Akibatnya, selisih prevalensi nominal (23,2% berbanding 4,4%) dan multientitas (30,4% berbanding 3,0%) **sebagian dibuat oleh aturan seleksi itu sendiri** dan **tidak boleh** disebut ciri khas keluhan korban.
2. **Pembaur panjang teks.** Median panjang kandidat korban Play Store 34 kata, sedangkan pembanding 15 kata. Teks yang lebih panjang lebih mungkin memuat nominal dan banyak entitas, sehingga persentase per dokumen ikut terdongkrak.
3. **Indikator yang relatif aman.** Indikator yang diukur per token dan tidak dipakai aturan sebagai syarat (fragmentasi *subword*, proporsi token tidak baku, *pseudo-perplexity*) lebih aman dibandingkan. Proporsi format di dalam ungkapan nominal juga aman, dan hasilnya **sama** pada kedua kelompok (80,7% berbanding 80,4%), sehingga format nominal informal adalah sifat ragam platform, bukan khas korban.
4. **Cara memperbaiki sebelum dikutip.** (a) Hitung ulang dengan normalisasi panjang (per 100 kata) atau sampel berpasangan dengan panjang setara. (b) Setelah pelabelan, bandingkan dokumen berlabel V dengan dokumen berlabel W, T, dan O dari sampel acak berlabel, karena label manusia tidak bergantung pada aturan seleksi. (c) Prevalensi deskriptif **di dalam** kandidat korban (mis. 23,2% memuat nominal, 30,4% memuat minimal tiga tipe entitas) tetap boleh dilaporkan tanpa klaim perbandingan.

### A.4 Temuan desain: PELAKU berupa pengenal hampir tidak ada

| Indikator | Korban Play Store | Pembanding Play Store | Korban X | Pembanding X |
|---|---|---|---|---|
| Dokumen memuat nomor telepon atau deret angka minimal 10 digit | 0,0% (batas atas IK 0,11%) | 0,005% | 7,1% | 14,6% |

Narasi laporan resmi yang kaya pengenal (misalnya *"rekening BCA 1234567890 ... wa 081234567890"*) **tidak mewakili** korpus ulasan Play Store. Konsekuensinya, **definisi PELAKU harus diputuskan sebelum panduan anotasi ditulis**: jika PELAKU hanya berupa pengenal (nomor rekening, telepon, akun), kelas ini nyaris kosong di Play Store dan hanya sekitar 7% di X. Pilihan yang dipertimbangkan adalah memasukkan pelaku deskriptif (*penjual*, *oknum yang mengaku CS*, nama toko) dan/atau menambah sumber laporan korban yang memuat pengenal. Tingginya angka pada pembanding X disebabkan tweet *spill* rekening yang tidak memuat narasi korban.

### A.5 Data tambahan

Angka berikut dihitung dari berkas `ULASAN_KORBAN_PENIPUAN.jsonl` di `EKSPERIMEN/DATA/{PLAYSTORE,X}/KANDIDAT_KORBAN/` (nama asli sebelum penataan: `ulasan_korban_penipuan.jsonl`; Play Store 3.531 dan X 2.501 dokumen) dan pra-anotasi 1.000 dokumen X. Semuanya berlaku untuk **kandidat** keluhan korban, berasal dari pemindaian pola (perkiraan kasar, bukan anotasi), dan pra-anotasi hanya berupa label perak buatan AI.

| Topik | Temuan | Ditangani oleh |
|---|---|---|
| Ejaan nama platform (13 merek) | 468 dari 3.059 sebutan (15,3%) ditulis tidak baku: dipisah spasi 287 (sekitar 61%; *buka lapak* 122, *link aja* 42, *toko pedia* 31), singkatan 102 (*tokped* 73, *toped* 29), salah ketik 79 (*shoppe* 34, *carousel* 22). Varian spasi hampir seluruhnya dari Play Store; pada X yang dominan singkatan media sosial (*wa* 254 vs *whatsapp* 49, *ig* 117 vs *instagram* 17). Hanya 13 merek yang dipindai, sehingga angka bisa lebih tinggi | CharCNN (salah ketik), Leksikon Toleran (berspasi, singkatan), konteks *encoder* |
| Format nominal (6.032 dokumen) | Singkatan *rb/ribu* 566, angka + *juta* 513, *jt* 454, *k* 342, angka bertitik tanpa Rp 233, kata (*sejuta*) 161; Rp + angka baku hanya 73 | CharCNN; panduan anotasi |
| Kata ambigu *dana* | 1.040 kemunculan di 666 dokumen; dari 40 sampel acak, sekitar 43% bukan platform (sampel kecil, rentang sekitar ±15 poin) | Konteks *encoder*; metrik akurasi kata ambigu |
| Entitas bertumpuk (pra-anotasi 1.000 dokumen X) | 2.586 entitas (PELAKU 875, MODUS 519, NOMINAL 472, PLATFORM 466, OBJEK 254); 107 pasangan bertumpuk (PELAKU memuat PLATFORM 66, MODUS memuat NOMINAL 35), tanpa *span* bersilang | EGP |
| Batas entitas | Frasa penyamar (*mengaku*, *mengatasnamakan*) di 8,0% dokumen Play Store dan 10,4% dokumen X; MODUS median 4 kata, 24% berisi 6 kata atau lebih, maksimum 13; 195 PELAKU berupa nomor HP atau rekening asli; 214 entitas (8%) ditandai ragu | Panduan anotasi; EGP menilai *span* utuh |
| Distribusi dokumen | Tanpa MODUS spesifik (GENERAL_FRAUD) 41,0% Play Store dan 79,9% X; nama aplikasi yang diulas ikut disebut di 47% ulasan Play Store; kerugian gagal atau hampir terjadi 15,1% | Panduan anotasi; ketidakseimbangan kelas |
| Panjang teks | Median 33 kata (Play Store) dan 41 kata (X); pada 1.000 dokumen X, 4,4% melebihi 100 kata (terpanjang 553) | *Sliding window* (prapemrosesan) |
| Privasi | Teks X masih memuat nomor HP dan rekening asli (40 dan 62 dokumen per 1.000), padahal kolom `pii` kosong; akun `@` sudah disamarkan | Disamarkan dengan format setara sebelum anotasi dan rilis |

**Keputusan anotasi:** entitas bertumpuk diizinkan **terbatas** (PLATFORM di dalam PELAKU, NOMINAL di dalam MODUS); PELAKU mencakup bentuk **deskriptif** (*oknum yang mengaku CS*), bukan hanya pengenal; anotasi per dokumen; pilot anotasi ganda 300 sampai 500 kalimat.
