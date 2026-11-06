# Protokol Anotasi NER Keluhan Penipuan Online (untuk penulis)

**Versi**: v0.3 (DRAF, **belum dikunci**) | **Tanggal**: 2 November 2026
**Program Studi**: Teknik Informatika S2, Universitas Hasanuddin
**Dokumen induk**: `DRAF/RENCANA_TESIS/RENCANA_SINGKAT_TESIS.md` rev8.4 (jika berbeda dengan set ini, dokumen induk menang, kecuali pada butir yang ditandai usulan, lihat `PROTOKOL_ANOTASI.md` Bagian 0.2)

**Isi berkas ini**: status keputusan, prosedur anotasi oleh AI, pengukuran kualitas, pengendalian versi, dan log. Berkas ini **tidak** diberikan kepada anotator AI.

**Peta berkas.** Penomoran bagian dipertahankan di seluruh set. Rujukan "Bagian N" tanpa nama berkas menunjuk set ini; "dokumen induk" menunjuk `DRAF/RENCANA_TESIS/RENCANA_SINGKAT_TESIS.md`.

| Berkas | Isi | Pembaca | Masuk instruksi AI? |
|---|---|---|---|
| `PANDUAN_ANOTASI.md` | Bagian 1 sampai 8 dan Lampiran A: aturan penandaan | Anotator AI; dosen sebagai rujukan | **Ya**, seluruh isi berkas |
| `PROTOKOL_ANOTASI.md` | Bagian 0, 9, 11, 12, 13 dan Rujukan: keputusan, prosedur, pengukuran, versi | Penulis | Tidak |
| `PANDUAN_DOSEN.md` | Lembar ringkas dan Bagian 10: cara memeriksa label | Dosen | Tidak |

Aturan hanya ditulis lengkap di `PANDUAN_ANOTASI.md`. Lembar ringkas dosen merujuk nomor bagian dan tidak menyalin aturan.

---

## Daftar Isi

0. Status dokumen, keputusan terbuka, dan temuan pada dokumen induk
9. Prosedur anotasi oleh AI (untuk penulis)
11. Pengukuran kualitas
12. Pengendalian versi dan pencegahan kebocoran
13. Log perubahan dan putusan kasus
- Rujukan

---

## 0. Status dokumen, keputusan terbuka, dan temuan pada dokumen induk

### 0.1 Peta berkas

Lihat tabel "Peta berkas" di bagian atas berkas ini. Satu aturan, satu tempat: aturan penandaan hanya ditulis lengkap di `PANDUAN_ANOTASI.md`, supaya yang dibaca dosen identik dengan yang diberikan kepada AI. Jangan menyalin aturan ke berkas lain, karena salinan akan menyimpang.

### 0.2 Keputusan

**Ditetapkan oleh dokumen induk** (dipakai apa adanya):

| ID | Keputusan | Sumber dokumen induk |
|---|---|---|
| T1 | Lima tipe entitas: PELAKU, NOMINAL, PLATFORM, MODUS, OBJEK | Bagian 1 |
| T2 | Tumpukan terbatas: PLATFORM di dalam PELAKU, NOMINAL di dalam MODUS | Bagian 1, Lampiran A.5 |
| T3 | PELAKU mencakup bentuk deskriptif dan pengenal | Lampiran A.5 |
| T4 | Anotasi per dokumen; teks tidak dinormalkan | Lampiran A.5, Bagian 8 |
| T5 | Target MODUS 2 sampai 5 kata (batas keras 8); PELAKU berupa frasa nomina | Bagian 3.8 (rev8.3; rev8.2: "sekitar 5 kata; tanpa kata kerja") |
| T6 | Pilot anotasi ganda 300 sampai 500 satuan, diukur sebelum eksperimen utama | Lampiran A.5, Bagian 8 |
| T7 | Label AI hanya label awal; setiap dokumen diperiksa manusia; kesepakatan diukur | Bagian 11 |
| T8 | Metrik utama F1 *micro strict span* | Bagian 4.4 |
| T9 | Pembagian data per kelompok duplikat, stratifikasi sumber; data uji tidak disentuh sebelum susunan dikunci | Bagian 8 |

**Usulan yang membutuhkan keputusan penulis dan dosen.** Semua isi Bagian 3 sampai 5 di `PANDUAN_ANOTASI.md` yang bergantung pada butir ini berstatus usulan sampai kolom Status berisi DISETUJUI.

| ID | Isu | Usulan (rujukan ke `PANDUAN_ANOTASI.md`) | Dampak bila berubah | Status |
|---|---|---|---|---|
| KP-01 | **OBJEK tidak didefinisikan** di dokumen induk rev8.2; v0.3 memuat usulan penyempitan | Bagian 3.5: uji tiga pertanyaan (dapat dijual atau dipesan terpisah; jenis, merek, atau model disebut; disebut sebagai benda yang ditawarkan, dipesan, atau dibeli dalam peristiwa yang diceritakan). Istilah uang umum, kata benda generik, dan tema penipuan (`investasi`, `pinjaman`, `lowongan kerja`) bukan OBJEK | Mengubah jumlah dan batas OBJEK; label awal 254 OBJEK pada 1.000 dokumen X (Lampiran A.5 dokumen induk) memakai pola lain dan tidak sebanding lagi | BELUM (disetujui penulis, menunggu dosen) |
| KP-02 | PELAKU "tanpa kata kerja" (Bagian 3.8 dokumen induk) bertentangan dengan contoh yang berisi kata kerja (lihat 0.3) | Rentang PELAKU berupa frasa nomina; kata isyarat penyamar di luar rentang; dua rujukan pelaku dalam satu kalimat menjadi dua rentang | Contoh di Bagian 7 dokumen induk disesuaikan pada rev8.3 (lihat 0.4) | BELUM (diterapkan, menunggu dosen) |
| KP-03 | Cakupan PLATFORM | Termasuk *marketplace*, media sosial dan pesan, dompet digital, bank, pinjaman daring, transportasi daring, dan *game*. Institusi yang bukan layanan digital (kepolisian, dinas) tidak pernah PLATFORM | Jumlah PLATFORM dan jumlah tumpukan | BELUM |
| KP-04 | Nama aplikasi yang diulas (muncul di 47% ulasan Play Store, Lampiran A.5 dokumen induk) | Tetap PLATFORM bila disebut di teks | Dominasi PLATFORM di Play Store; subset varian ejaan | BELUM |
| KP-05 | Cakupan NOMINAL | Semua ungkapan jumlah uang, apa pun perannya (kerugian, harga, biaya, tawaran) | Jumlah NOMINAL; subset nominal informal | BELUM |
| KP-06 | Panjang MODUS | Target 2 sampai 5 kata; batas keras 8 kata; ditinjau setelah pilot | Rata-rata panjang rentang MODUS | BELUM |
| KP-07 | Tumpukan di luar dua pola | Tahap PILOT merekam dengan penanda; tahap PRODUKSI dikunci pada dua pola | Angka tumpang tindih sejati (Bagian 3.6 dokumen induk) bisa terukur atau bias | BELUM |
| KP-08 | Satuan pilot: dokumen induk menulis "per dokumen" dan "300 sampai 500 kalimat" | Satuan **dokumen**: 300 sampai 500 dokumen, kira-kira setengah Play Store dan setengah X, acak berstrata sumber dan kategori utama, diambil hanya dari data bukan uji | Ukuran dan komposisi pilot | BELUM |
| KP-09 | Atribut tambahan PLATFORM | `varian` dan `kanonik` (Bagian 8), hanya untuk analisis subset | Kemampuan menghitung F1 subset varian ejaan (H2) | BELUM |
| KP-10 | Bidang yang diberikan ke AI | Hanya `nerText` dan `source`. `evidence`, `kw_hits`, `tierDetail`, `primaryCategory`, `categories`, `victimRelation` **tidak** diberikan | Risiko sirkularitas (Lampiran A.3 dokumen induk) | BELUM |
| KP-11 | Ambang penerimaan kesepakatan | Angka ditetapkan penulis bersama dosen **sebelum** pilot; panduan ini tidak mengusulkan angka | Kriteria lulus pilot | BELUM |
| KP-12 | Alat anotasi untuk dosen | Dipilih penulis. Syarat: mendukung rentang bertumpuk dan impor label awal. Label Studio, doccano, dan INCEpTION adalah kandidat yang **belum diuji** dalam penyusunan panduan ini; periksa dulu dukungan rentang bertumpuk | Cara dosen bekerja | BELUM |
| KP-13 | Persona yang hanya nama platform (`menyamar sebagai OVO`) | PLATFORM saja, tanpa PELAKU (Bagian 3.1 dan 5.15), karena rentang identik dua tipe tidak diizinkan pada PRODUKSI | Pola ini cocok pada 91 dokumen (79 Play Store, 12 X) menurut `AUDIT_PANDUAN_DATA.py`; PELAKU akan kurang terhitung pada dokumen peniruan platform. Alternatif: izinkan pola ketiga (PLATFORM identik PELAKU) | BELUM |
| KP-14 | Awalan *di-/ke-/dr-* menempel pada nama platform (`dishopeepay`) | Rentang PLATFORM dimulai setelah awalan (Bagian 2.4) | 44 dokumen Play Store menurut pola; menyimpang dari aturan batas kata biasa, sehingga tokenisasi *subword* dan penyelarasan rentang ke token perlu diuji | BELUM |
| KP-15 | Angka tanpa satuan setelah kata transaksi (`dp 400`) | NOMINAL dengan `RAGU_ADA` (Bagian 3.2 butir 6) | 16 dokumen menurut pola (6 Play Store, 10 X); jumlah NOMINAL informal | BELUM |

### 0.3 Temuan pada dokumen induk

Temuan ini ditulis langsung karena memengaruhi aturan anotasi.

| No | Temuan | Dampak |
|---|---|---|
| 1 | Pada rev8.2, Bagian 3.8 dokumen induk menyatakan PELAKU tanpa kata kerja. Namun contoh alur di Bagian 7 dokumen induk menandai *ngaku CS buka lapak* sebagai PELAKU, dan Lampiran A.5 dokumen induk menyebut *oknum yang mengaku CS*. Keduanya memuat kata kerja | Tanpa keputusan, dua anotator akan menarik batas berbeda. Usulan: KP-02 |
| 2 | Pada rev8.2, pilot ditulis "300 sampai 500 kalimat" padahal anotasi dilakukan per dokumen | KP-08 |
| 3 | Pada rev8.2, OBJEK disebut sebagai tipe kelima tetapi tidak didefinisikan di bagian mana pun, termasuk Lampiran A dokumen induk | KP-01. Ini butir paling mendesak, karena OBJEK adalah tipe paling subjektif |
| 4 | Berkas label awal 1.000 dokumen X (sumber angka 2.586 entitas dan 107 pasangan bertumpuk) tidak ada di repositori. Angka itu tidak dapat diperiksa ulang dari repo | Mohon berkas itu ditambahkan, atau angkanya ditandai belum terverifikasi. Definisi OBJEK dan PELAKU yang dipakai saat itu perlu dicatat |
| 5 | Dokumen induk di repo memakai "keluhan penipuan", sedangkan instruksi proyek dan nama folder memakai "kandidat korban" | Panduan memakai istilah netral **dokumen kandidat**. Sampai pelabelan V/W/T/O selesai, tidak ada dokumen yang disebut "korban terverifikasi" |


### 0.4 Penyelarasan dokumen induk (rev8.3 dan rev8.4)

Permintaan penulis: panduan, dokumen induk, dan data harus saling cocok. Perubahan berikut dibuat pada `RENCANA_SINGKAT_TESIS.md`. Semuanya masih **menunggu persetujuan dosen**; bila ditolak, panduan dan dokumen induk dikembalikan bersama.

| No | Letak di dokumen induk | Sebelum | Sesudah | Alasan |
|---|---|---|---|---|
| 1 | Bagian 3.8, baris uraian panjang | "batas MODUS sekitar 5 kata; PELAKU tanpa kata kerja" | "target MODUS 2 sampai 5 kata dengan batas keras 8; PELAKU berupa frasa nomina, kata isyarat penyamar di luar rentang" | KP-02 dan KP-06 |
| 2 | Contoh alur, langkah 6 | "*ngaku CS buka lapak* → PELAKU" | "*CS buka lapak* → PELAKU" | *ngaku* adalah kata isyarat di luar rentang (KP-02) |
| 3 | Lampiran A.5, "Keputusan anotasi" | "300 sampai 500 kalimat" | "300 sampai 500 dokumen" | KP-08, anotasi per dokumen |
| 4 | Bagian 4.4, Batasan istilah | OBJEK tidak didefinisikan | Baris definisi OBJEK (rev8.3), disempitkan menjadi uji tiga pertanyaan pada rev8.4, ditandai usulan | KP-01 |
| 5 | Lampiran A.5, tabel | Tidak ada | Baris "Audit pola untuk panduan" yang menunjuk `AUDIT_PANDUAN_DATA.py`, berstatus hitungan pola | Kesesuaian data dengan panduan |
| 6 | Header | rev8.2 | rev8.3 | Pelacakan |
| 7 | Lampiran A.5, baris entitas bertumpuk | Angka OBJEK 254 tanpa catatan | Diberi catatan bahwa angka memakai pola OBJEK sebelum penyempitan | KP-01 |

Tidak ada angka hasil anotasi yang ditambahkan ke dokumen induk.
---


## 9. Prosedur anotasi oleh AI (untuk penulis)

### 9.1 Prasyarat, berurutan

1. Semua butir KP-01 sampai KP-12 berstatus DISETUJUI atau secara sadar diubah, dan panduan dinaikkan versinya.
2. **Bekukan pembagian** latih, validasi, dan uji (benih acak dicatat, pembagian per kelompok duplikat `dup_group`, stratifikasi sumber). Pilot diambil hanya dari data **bukan uji**. Alasannya, aturan akan disetel dengan data pilot; bila dokumen pilot ikut menjadi data uji, itu kebocoran.
3. **Samarkan data pribadi** (nomor telepon, rekening, nama asli) dengan format setara, lalu jadikan teks tersamarkan itu satu-satunya teks yang dianotasi dan dilatihkan. Hitungan pola `EKSPERIMEN/KODE/AUDIT_PANDUAN_DATA.py` menemukan nomor telepon atau deret angka panjang (rekening) yang tampak pada 227 dari 2.501 dokumen X (9,1%) dan 0 dokumen Play Store; kolom `pii` menandai PHONE pada 180 dokumen X (seluruhnya sama dengan telepon yang tampak menurut pola), tetapi hanya menandai dan tidak menyamarkan teks; 45 dokumen memuat deret angka 9 digit atau lebih tanpa tanda PHONE (kemungkinan rekening, belum dipastikan). Karena itu kolom `pii` tidak boleh dijadikan satu-satunya dasar penyamaran. Lampiran A.5 dokumen induk juga mencatat teks X masih memuat nomor HP dan rekening asli, dan data dikirim ke layanan pihak ketiga. Posisi karakter hanya valid terhadap teks yang persis sama.
4. Periksa kebijakan layanan AI yang dipakai terkait penyimpanan dan penggunaan data untuk pelatihan, dan pilih pengaturan tanpa penyimpanan bila tersedia. Panduan ini tidak memverifikasi kebijakan layanan tertentu.
5. Tetapkan ambang penerimaan (KP-11) dan catat dengan tanggal **sebelum** pilot dijalankan.
6. **Uji definisi OBJEK (KP-01)**: setelah pembagian data dibekukan (butir 2), ambil 30 dokumen acak dari data **latih** yang memuat kata beli, pesan, jual, atau tawar. Penulis dan satu orang lain menandai OBJEK dengan uji tiga pertanyaan (3.5), terpisah. Bandingkan, lalu perketat uji bila banyak yang berbeda. Sampel ini hanya menguji definisi: tidak diukur sebagai kesepakatan, tidak berasal dari data uji, dan **dikeluarkan dari sampel pilot** supaya kesepakatan pilot tidak terlalu bagus karena definisi disetel pada dokumen yang sama.

### 9.2 Pemilihan pilot

| Parameter | Usulan |
|---|---|
| Jumlah | 300 sampai 500 dokumen (KP-08) |
| Komposisi | Kira-kira setengah Play Store dan setengah X; acak berstrata menurut sumber dan kategori utama; kategori kecil digabung |
| Benih acak | Dicatat |
| Asal | Hanya dari data bukan uji |
| Dokumen di luar topik | Hitungan kata kunci kasar menemukan 969 dari 2.501 dokumen X (38,7%) dan 751 dari 3.531 dokumen Play Store (21,3%) tanpa satu pun isyarat daring. Angka ini batas atas yang berisik dan **bukan** penilaian relevansi. Pilot tidak menyaring dokumen seperti itu supaya estimasi kepadatan entitas tidak bias; ketepatan seleksi tetap diukur terpisah lewat sampel cek V/W/T/O |
| Sasaran X | Dokumen X memiliki kepadatan entitas lebih tinggi menurut label awal AI (2.586 entitas per 1.000 dokumen), sehingga komposisi setengah demi setengah memberi cukup entitas per tipe |

### 9.3 Menjalankan AI

1. **Satu dokumen per panggilan.** Jangan menumpuk beberapa dokumen dalam satu panggilan agar label tidak saling memengaruhi.
2. **Instruksi sistem** = seluruh isi `PANDUAN_ANOTASI.md`, apa adanya. Tambahkan nilai `tahap` dan `versi_panduan`.
3. **Masukan** = `doc_id`, `source`, dan `nerText` tersamarkan. **Bidang lain tidak diberikan** (KP-10): `evidence` dan `kw_hits` memuat kata yang dipakai aturan seleksi dan akan menjadi jangkar bagi AI.
4. **Contoh (*few-shot*)** hanya dari Bagian 7 `PANDUAN_ANOTASI.md`.
5. **Catat per proses**: nama dan versi model, tanggal, suhu dan parameter lain, hash SHA256 instruksi, versi panduan, tahap, dan waktu mulai dan selesai. Simpan sebagai berkas JSON berversi di `EKSPERIMEN/`. Tanpa catatan ini, data tidak dapat direproduksi.
6. Jalankan validator (Bagian 8.3 `PANDUAN_ANOTASI.md`). Gagal: ulangi sekali. Masih gagal: tandai dokumen gagal.
7. **Opsional**: jalankan dua anotator AI dengan model atau pengaturan berbeda. Dokumen yang keduanya tidak sepakat diprioritaskan untuk pemeriksaan manusia. Ketidaksepakatan dipakai sebagai petunjuk **prioritas**, bukan sebagai penentu benar atau salah.

### 9.4 Larangan

1. Jangan menyetel instruksi atau panduan dengan melihat data uji.
2. Jangan mengubah panduan atau instruksi di tengah satu putaran tanpa menaikkan versi dan mengulang seluruh putaran.
3. Jangan memakai AI sebagai validator akhir. Validator akhir adalah manusia (T7).
4. Jangan menyebut dokumen kandidat sebagai "korban" sampai pelabelan V/W/T/O selesai.

---


## 11. Pengukuran kualitas

### 11.1 Ukuran utama

Kesepakatan antar dua penanda dihitung dengan **F1 *strict span*** pada pasangan, bukan kappa. Hripcsak dan Rothschild (2005) menunjukkan bahwa pada tugas yang tidak memiliki jumlah kasus negatif terdefinisi, kappa sulit dipakai, bahwa rata-rata F-measure antar pasangan penilai secara numerik sama dengan *positive specific agreement*, dan bahwa ukuran inilah yang tepat untuk reliabilitas pada studi semacam itu. Penandaan rentang teks diperlakukan sebagai kategori ini; alasannya adalah penalaran penyusun panduan, bukan klaim makalah: jumlah "bukan entitas" tidak terdefinisi karena bergantung pada cara teks dipotong.

Ketat (*strict*): rentang dan tipe harus sama persis.

### 11.2 Pasangan yang dibandingkan

| Pasangan | Untuk apa |
|---|---|
| Penulis dan dosen (pilot, dari awal) | Keandalan antarmanusia (K1 mengklaim "ukuran reliabilitas") |
| AI dan label akhir manusia (pilot dan sampel) | Mutu label awal AI |
| AI-1 dan AI-2 (opsional) | Dasar prioritas pemeriksaan |

### 11.3 Rincian wajib

| Rincian | Isi |
|---|---|
| Per tipe | F1 untuk lima tipe dipisah |
| Per sumber | Play Store dan X dipisah |
| Tiga tingkat kelonggaran, hanya sebagai diagnosis | (a) *strict*: rentang dan tipe sama; (b) tipe diabaikan: rentang sama; (c) batas longgar: tumpang tindih rentang. Selisih (a) dan (b) menunjukkan masalah definisi tipe; selisih (a) dan (c) menunjukkan masalah batas. Hanya (a) yang menjadi ukuran utama |
| Tingkat koreksi AI | Persentase entitas AI yang `UBAH_*` atau `HAPUS`; persentase entitas yang `TAMBAH`; per tipe |
| Tumpang tindih sejati | Proporsi entitas yang berada di dalam entitas lain, dan jumlah pasangan bersilang. Angka ini menjadi dasar kuantitatif dekoder berbasis rentang (Bagian 3.6 dokumen induk) dan menentukan perlunya memperluas istilah "bertumpuk" |
| Dampak aturan v0.2 | Jumlah dan proporsi: MODUS yang dipotong atau dibatalkan karena memuat PLATFORM, PELAKU, atau OBJEK (penanda `TUMPANG_LAIN` pada PILOT); dokumen persona hanya nama platform (KP-13); rentang dengan awalan menempel (KP-14); NOMINAL tanpa satuan (KP-15). Angka ini menentukan apakah aturan PRODUKSI dikunci atau direvisi |
| Interval kepercayaan | *Bootstrap* atas dokumen, 1.000 ulangan (seperti Lampiran A.1 dokumen induk) |

### 11.4 Perkiraan jumlah entitas pada pilot

Perkiraan kasar dengan mengekstrapolasi label awal AI pada 1.000 dokumen X (Lampiran A.5 dokumen induk) ke 300 dokumen, **bukan hasil anotasi**: PELAKU sekitar 262, MODUS 156, NOMINAL 142, PLATFORM 140, OBJEK 76 (memakai pola OBJEK sebelum v0.3, sehingga jumlah OBJEK hampir pasti lebih kecil dan tidak sebanding). Konsekuensinya, F1 per tipe untuk OBJEK dan MODUS pada pilot 300 dokumen akan memiliki interval kepercayaan lebar. Laporkan intervalnya, jangan hanya titik. Bila interval OBJEK terlalu lebar untuk memutuskan definisi, perbesar pilot ke arah 500 dokumen. Angka Play Store dapat berbeda.

### 11.5 Ambang penerimaan (KP-11)

Penulis dan dosen mengisi tabel ini dan mencatat tanggalnya **sebelum** pilot. Panduan ini sengaja tidak mengusulkan angka, sebab belum ada sumber terverifikasi untuk ambang pada dataset dengan skema seperti ini.

| Ukuran | Ambang | Tanggal ditetapkan |
|---|---|---|
| F1 *strict* penulis dan dosen, per tipe | ___ | ___ |
| F1 *strict* AI dan label akhir, per tipe | ___ | ___ |
| Tindakan bila ambang tidak tercapai | Revisi aturan, ulangi pilot (usulan: paling banyak dua putaran) | ___ |

### 11.6 Pelaporan di tesis

1. Nyatakan bahwa data latih berlabel perak sebagian (keterbatasan, Bagian 10.2 tahap IV di `PANDUAN_DOSEN.md`).
2. Laporkan hasil negatif apa adanya, termasuk bila kesepakatan rendah pada tipe tertentu.
3. Tidak menyebut data "terbukti berkualitas" tanpa angka pada Bagian 11.3.
4. Tidak menyebut dokumen kandidat sebagai "korban" sebelum pelabelan V/W/T/O.

---


## 12. Pengendalian versi dan pencegahan kebocoran

| No | Aturan |
|---|---|
| 12.1 | **Versi**: `v0.x` draf; `v1.0` dikunci setelah pilot selesai dan KP-01 sampai KP-12 diputuskan. Setiap perubahan mencatat tanggal, alasan, dan dampaknya pada label di Bagian 13 |
| 12.2 | **Penguncian**: panduan dikunci **sebelum** anotasi penuh. Setelah v1.0, perubahan hanya berupa erata yang tidak mengubah label. Bila suatu perubahan akan mengubah label, buat versi baru dan anotasi ulang seluruh data yang terdampak |
| 12.3 | **Pilot bukan uji**: dokumen pilot tidak boleh masuk data uji. Pembagian dibekukan sebelum pilot (9.1) |
| 12.4 | **Tidak menyetel pada data uji**: dilarang melihat kesalahan pada data uji lalu merevisi aturan, instruksi, atau leksikon. Itu *leakage* dan *HARKing* |
| 12.5 | **Hipotesis dan ambang ditetapkan lebih dulu**: ambang 11.5 dan daftar subset F1 (varian ejaan nama, nominal informal, entitas bertumpuk, entitas di luar data latih, kata ambigu) ditetapkan sebelum melihat hasil model |
| 12.6 | **`kanonik` bukan sumber leksikon**: Leksikon Toleran dibangun dari sumber eksternal dan dibekukan sebelum menyentuh data uji (Bagian 7 dokumen induk) |
| 12.7 | **Anotasi ulang**: bila panduan naik versi sesudah anotasi penuh, seluruh label yang terdampak diulang dan hasil lama diarsipkan, tidak ditimpa |
| 12.8 | **Jejak**: catatan proses AI (9.3 butir 5) dan lembar putusan dosen disimpan bersama versi panduannya |

---


## 13. Log perubahan dan putusan kasus

### 13.1 Log perubahan

| Versi | Tanggal | Perubahan |
|---|---|---|
| v0.1 | 2 November 2026 | Draf awal. Semua usulan KP-01 sampai KP-12 belum diputuskan |
| v0.2 | 2 November 2026 | Uji terhadap korpus (`AUDIT_PANDUAN_DATA.py`). Koreksi: teman atau keluarga boleh menjadi PELAKU bila teks menyatakan ia menipu (sebelumnya selalu bukan PELAKU; 16 dokumen X berpola ini). Usulan baru: KP-13 persona hanya platform, KP-14 awalan menempel, KP-15 angka tanpa satuan. Aturan nomor telepon dan rekening (2.12). Contoh 14 sampai 17. Penjelasan 5.5 untuk dokumen luar topik. Dokumen induk diselaraskan ke rev8.3 (0.4) |
| v0.3 | 6 November 2026 | OBJEK disempitkan: uji tiga pertanyaan menggantikan kata "spesifik" (Bagian 3.5). Produk keuangan abstrak dan lowongan kerja bukan OBJEK. Uji 3 tidak mensyaratkan peristiwanya penipuan, supaya selaras dengan 5.5. Contoh 18 dan 19. Langkah uji definisi 30 dokumen (9.1 butir 6). Dokumen induk rev8.4 |

### 13.2 Putusan kasus (diisi saat pilot)

| No | Kasus | Putusan | Aturan yang diubah | Versi | Tanggal |
|---|---|---|---|---|---|
| | | | | | |

---


## Rujukan

1. K. Fort and B. Sagot, "Influence of pre-annotation on POS-tagged corpus development," in *Proc. 4th Linguistic Annotation Workshop (LAW IV)*, Uppsala, Sweden, 2010, pp. 56–63. [Online]. Available: https://aclanthology.org/W10-1807/ (Temuan dibaca dari PDF ACL Anthology; halaman ACL Anthology tidak mencantumkan DOI, sehingga DOI tidak ditulis.)
2. G. Hripcsak and A. S. Rothschild, "Agreement, the F-measure, and reliability in information retrieval," *J. Am. Med. Inform. Assoc.*, vol. 12, no. 3, pp. 296–298, 2005, doi: 10.1197/jamia.M1733. (Metadata dan abstrak diperiksa lewat Europe PMC; teks lengkap belum dibaca.)
