# Panduan Anotasi NER Keluhan Penipuan Online Berbahasa Indonesia

**Versi**: v0.1 (DRAF, **belum dikunci**) | **Tanggal**: 2 November 2026
**Program Studi**: Teknik Informatika S2, Universitas Hasanuddin
**Dokumen induk**: `DRAF/RENCANA_TESIS/RENCANA_SINGKAT_TESIS.md` rev8.2 (jika berbeda dengan set ini, dokumen induk menang, kecuali pada butir yang ditandai usulan, lihat `PROTOKOL_ANOTASI.md` Bagian 0.2)

**Isi berkas ini**: aturan penandaan yang diberikan kepada anotator AI (seluruh isi berkas dipakai sebagai instruksi) dan menjadi rujukan dosen.

> **Untuk anotator AI.** Penanda "KP-xx" dan kata "usulan" menunjuk keputusan yang menunggu persetujuan penulis. Terapkan aturan yang tertulis di sini apa adanya, dan jangan memasukkan penanda itu ke keluaran.

**Peta berkas.** Penomoran bagian dipertahankan di seluruh set. Rujukan "Bagian N" tanpa nama berkas menunjuk set ini; "dokumen induk" menunjuk `DRAF/RENCANA_TESIS/RENCANA_SINGKAT_TESIS.md`.

| Berkas | Isi | Pembaca | Masuk instruksi AI? |
|---|---|---|---|
| `PANDUAN_ANOTASI.md` | Bagian 1 sampai 8 dan Lampiran A: aturan penandaan | Anotator AI; dosen sebagai rujukan | **Ya**, seluruh isi berkas |
| `PROTOKOL_ANOTASI.md` | Bagian 0, 9, 11, 12, 13 dan Rujukan: keputusan, prosedur, pengukuran, versi | Penulis | Tidak |
| `PANDUAN_DOSEN.md` | Lembar ringkas dan Bagian 10: cara memeriksa label | Dosen | Tidak |

Aturan hanya ditulis lengkap di `PANDUAN_ANOTASI.md`. Lembar ringkas dosen merujuk nomor bagian dan tidak menyalin aturan.

---

## Daftar Isi

1. Tujuan, lingkup, dan prinsip
2. Aturan umum rentang
3. Definisi lima tipe entitas
4. Entitas bertumpuk
5. Kasus khusus
6. Urutan keputusan
7. Contoh beranotasi
8. Format keluaran dan pemeriksaan otomatis
- Lampiran A. Kata isyarat dan daftar pendamping

---

## 1. Tujuan, lingkup, dan prinsip

### 1.1 Tujuan

Menandai rentang teks yang merupakan entitas dari lima tipe pada kolom `nerText` setiap dokumen kandidat, sehingga data dapat dipakai melatih dan mengevaluasi model ekstraksi entitas (kontribusi K1 dan K2 dokumen induk).

### 1.2 Satuan kerja

Satu dokumen adalah satu nilai `nerText` (ulasan Play Store atau unggahan X), dianotasi utuh. Pemotongan menjadi jendela untuk model dilakukan kemudian oleh kode (*sliding window*) dan bukan urusan anotator.

| Sumber | Dokumen kandidat | Median kata | Persentil ke-99 | Terpanjang |
|---|---|---|---|---|
| Play Store | 3.531 | 33 | 87 | 162 |
| X | 2.501 | 41 | 494 | 1.187 |

Angka dihitung dari `ULASAN_KORBAN_PENIPUAN.jsonl` (aturan pembersihan v1.4).

### 1.3 Yang bukan tugas anotasi ini

| Bukan tugas | Alasan |
|---|---|
| Menilai apakah penulis benar korban (label V/W/T/O) | Dikerjakan terpisah pada sampel cek (Lampiran A.2 dokumen induk). Entitas ditandai menurut isi teks, tidak peduli penulisnya korban atau bukan |
| Menetapkan kategori modus dokumen | Itu keluaran aturan seleksi (`primaryCategory`) |
| Menormalkan atau membetulkan ejaan | Teks tidak diubah (T4) |
| Menghubungkan entitas (relasi) atau menyatukan sebutan yang sama | Hanya penandaan rentang |
| Memeriksa kebenaran faktual | Ditandai apa yang tertulis |

### 1.4 Prinsip

1. **Teks adalah satu-satunya sumber.** Tandai hanya yang tertulis di `nerText`. Jangan menambahkan entitas dari pengetahuan umum atau dari dugaan.
2. **Teks tidak diubah.** Huruf besar, salah ketik, singkatan, dan tanda baca tetap seperti aslinya.
3. **Ikuti definisi, bukan kesan.** Putuskan dengan aturan di Bagian 3 sampai 6, bukan dengan perasaan bahwa sesuatu "penting".
4. **Konsisten pada permukaan.** Setiap kemunculan yang memenuhi aturan ditandai, termasuk bila disebut berulang.
5. **Ragu pada keberadaan**: tandai entitasnya dan beri penanda `RAGU_ADA`. Alasannya, pemeriksa manusia lebih mudah menemukan label berlebih yang ditandai daripada label yang hilang.
6. **Ragu pada batas**: ambil rentang terpendek yang masih memenuhi definisi dan beri penanda `RAGU_BATAS`.
7. **Metadata bukan sumber label.** Kolom `source` (nama aplikasi yang diulas) hanya boleh dipakai untuk memutus kata ambigu (misalnya *dana*, Bagian 3.3). Jangan menandai nama yang hanya ada di metadata.
8. **Jangan memaksa.** Dokumen tanpa entitas adalah keluaran sah (daftar kosong).

---


## 2. Aturan umum rentang

Istilah: **rentang** adalah potongan teks kontigu yang ditandai (dalam literatur disebut *span*).

| No | Aturan | Contoh |
|---|---|---|
| 2.1 | Posisi dihitung dalam karakter Unicode pada `nerText` persis, mulai dari 0; `mulai` inklusif, `akhir` eksklusif. Isi `teks` harus sama dengan potongan `nerText[mulai:akhir]` | `nerText[23:32]` = `CS Shopee` |
| 2.2 | Rentang tidak diawali atau diakhiri spasi atau tanda baca. Pengecualian: tanda yang menjadi bagian token, yaitu titik dan koma di dalam angka (`1.500.000`, `1,5`), titik dalam singkatan (`a.n.`), garis bawah dan `@` pada nama akun (`@user123`, `HOKI_88`), dan lambang mata uang (`Rp`, `$`) | `Rp 50.000` utuh; `"Grab"` ditandai `Grab` tanpa tanda kutip |
| 2.3 | Rentang harus kontigu. Tidak boleh melompati kata | `CS di Shopee` tidak boleh ditandai sebagai satu rentang yang melompati `di` |
| 2.4 | Rentang berawal dan berakhir di batas kata. Batas kata: spasi, tanda baca, garis miring, dan garis hubung yang memisahkan dua kata. Klitik yang menempel (*-nya*, *-lah*, *-kah*, *-pun*) ikut kata | `penjualnya` ditandai utuh; `CS-Shopee`: `Shopee` boleh menjadi rentang dalam |
| 2.5 | Kata penunjuk dan sapaan di tepi dikeluarkan: *si*, *sang*, *para*, *seorang*, *ini*, *itu*, *tersebut*, *yang*, serta sapaan *bapak*, *ibu*, *pak*, *bu*, *kak*, *mas*, *mbak* sebelum nama. Kata pengantar nama (*a.n.*, *atas nama*, *nama*, *nomor*, *no.*, *rek*) juga dikeluarkan | `si penjual` → `penjual`; `a.n. Budi Santoso` → `Budi Santoso` |
| 2.6 | Tandai **setiap** kemunculan yang memenuhi aturan | `Shopee` muncul tiga kali: tiga rentang |
| 2.7 | Kata ganti dan rujukan ulang tidak ditandai: *dia*, *ia*, *mereka*, *kamu*, *orang itu*, *pihak tersebut*, dan kata ganti *-nya* yang berdiri sendiri | `dia kabur`: tanpa label |
| 2.8 | Hanya dokumen dengan `is_dup_rep` bernilai True yang dianotasi. Dokumen bukan perwakilan kelompok duplikat dilewati (9 dokumen: 1 Play Store dan 8 X, dihitung dari berkas yang sama) | |
| 2.9 | Dokumen tanpa entitas menghasilkan `entitas: []` | `Mengecewakan banget, ditipu lagi` |
| 2.10 | Teks pseudonim dipakai apa adanya: `@userNNNNN` untuk akun, `penggunaNNNN@contoh.com` untuk surel. Tanda kurung siku di dalam teks (`[THREAD]`, `[SCAMMER]`) adalah bagian teks asli, bukan penanda anotasi | |
| 2.11 | Emoji, tagar, dan tautan tidak menjadi bagian rentang. Tagar (`#penipuan`) tidak ditandai. Tautan (URL) tidak ditandai pada v0.1; bila sering muncul, tandai `DI_LUAR_ATURAN` agar dicatat di pilot | |

---


## 3. Definisi lima tipe entitas

Setiap tipe berisi: definisi, tabel keputusan, aturan batas, dan hubungannya dengan tumpukan (Bagian 4). Notasi contoh: `[teks]{TIPE}`, tumpukan ditulis `[CS [Shopee]{PLATFORM}]{PELAKU}`.

### 3.1 PELAKU

**Definisi.** Pihak yang, menurut isi teks, menipu, menyamar, memanipulasi, atau mengambil uang, akun, atau data penulis atau pihak lain. Rentang berupa **frasa nomina tanpa kata kerja** (T5). Ada dua bentuk (T3): **deskriptif** (peran, persona, nama) dan **pengenal** (nomor, akun, surel).

| Situasi | Keputusan | Contoh |
|---|---|---|
| Peran pelaku yang jelas | Tandai | `[penjual]{PELAKU} kabur`; `[kurir gadungan]{PELAKU}`; `[oknum]{PELAKU}`; `[scammer]{PELAKU}` |
| Persona atau identitas yang diklaim pelaku | Tandai seluruh frasa persona | `ngaku [CS [Shopee]{PLATFORM}]{PELAKU}`; `mengaku [polisi]{PELAKU}` |
| Peran dan persona sekaligus | Dua rentang; kata isyarat dan penghubung tidak masuk | `[oknum]{PELAKU} yang mengaku [CS [Shopee]{PLATFORM}]{PELAKU}` |
| Nama orang yang disebut sebagai pelaku | Tandai nama tanpa sapaan dan tanpa kata pengantar | `a.n. [Budi Santoso]{PELAKU}` |
| Pengenal: telepon, rekening, akun, surel | Tandai **nilai** pengenal saja | `nomor [081234567890]{PELAKU}`; `akun IG [@user123]{PELAKU}` |
| Nama toko atau akun penjual yang dituduh | Tandai nama diri; kata *toko* ikut hanya bila bagian frasa peran tanpa nama diri | `nama toko [HOKI_88]{PELAKU}`; `[toko penipu]{PELAKU}` |
| Platform dituduh menipu (`Shopee penipu`) | **Bukan** PELAKU. Tandai hanya PLATFORM | `[Shopee]{PLATFORM} penipu` |
| Predikat *penipu* pada aplikasi (`aplikasinya penipu`) | Bukan PELAKU | tanpa label |
| Pegawai atau layanan pelanggan platform yang hanya tidak membantu | Bukan PELAKU | `CS [Shopee]{PLATFORM} tidak membantu` |
| Kata terlalu umum: *orang*, *seseorang*, *pihak*, *dia*, *mereka* | Bukan PELAKU. Dengan penjelas ia boleh: `orang tidak dikenal` | `ditipu orang`: tanpa label |
| *penipu*, *scammer*, *penjual*, *pembeli* yang menunjuk pelaku | Tandai | `[penipunya]{PELAKU}` |
| *penipuan*, *tipuan*, *scam* sebagai peristiwa | Bukan PELAKU | `kena penipuan`: tanpa label |
| Korban, penulis, penolong, teman, keluarga | Bukan PELAKU | |
| Institusi bukan layanan digital yang dicatut (dinas, kepolisian) | PELAKU sebagai persona | `mengatasnamakan [DISHUB]{PELAKU}` |

**Aturan batas.**
1. Mulai dari kata inti pertama, akhiri di kata inti terakhir; keluarkan kata penunjuk (2.5).
2. Jangan sertakan klausa relatif (*yang ...*) atau kata kerja. `penjual yang kabur` → `penjual`.
3. Kata isyarat penyamar (*ngaku*, *mengaku*, *mengatasnamakan*, *berkedok*) tidak masuk rentang (Lampiran A.1).
4. Persona yang berpola `[peran] (dari) [platform]` ditandai satu rentang dan memuat PLATFORM (Bagian 4). Bila dihubungkan kata depan lokatif *di* (`penjual di Shopee`), PELAKU dan PLATFORM berdiri sendiri-sendiri.

### 3.2 NOMINAL

**Definisi.** Setiap ungkapan jumlah uang dalam teks, apa pun perannya (kerugian, harga, biaya, tawaran, pinjaman). Tujuannya agar model mengenali batas jumlah uang di luar pola Rp baku (Ciri 03 dokumen induk).

| Format | Contoh | Rentang |
|---|---|---|
| Rp + angka | `Rp 500.000`, `Rp500rb`, `rp. 1jt` | Seluruhnya termasuk `Rp` |
| Angka + singkatan | `2jt`, `500rb`, `100k`, `10 rb`, `1,5 juta` | Seluruhnya, termasuk spasi antara angka dan satuan |
| Akhiran *-an* | `10 rban`, `100k an` | Termasuk akhiran |
| Angka bertitik tanpa Rp | `50.000`, `1.500.000` | Hanya bila konteks jelas uang (ada kata transfer, bayar, harga, rugi, dan sejenisnya) |
| Terbilang | `sejuta`, `lima ratus ribu`, `setengah juta` | Seluruh frasa |
| Perkiraan tanpa angka | `jutaan`, `ratusan ribu`, `puluhan juta` | Seluruh frasa |
| Mata uang asing | `200 dollar`, `$50`, `5 usdt` | Seluruhnya |

**Bukan NOMINAL**: nomor telepon dan rekening, tanggal (`23/12/24`), jumlah barang (`60 nasi box`), persentase dan bunga (`bunga 20%`), tenor (`12 bulan`), poin dan *diamond* dan koin, jumlah pengikut atau penonton (`1 juta views`), serta kata kabur tanpa satuan (*banyak*, *sedikit*, *dikit*).

**Aturan batas.**
1. Keluarkan *sekitar*, *kurang lebih*, *total*, *sebesar*, *senilai*, *seharga*, *sebanyak*, *cuma*, *hanya*.
2. `100-200rb` (tanpa spasi) satu rentang. `100rb sampai 200rb`, `50k dan 30k`, dan `Rp 50.000 + 5.000` adalah rentang terpisah.
3. Satuan ambigu (`5 m`, `10 k`): tandai hanya bila konteks jelas uang, dan beri `RAGU_ADA` bila belum yakin.
4. NOMINAL yang berada di dalam frasa MODUS ditumpuk (Bagian 4). NOMINAL di dalam OBJEK, PELAKU, atau PLATFORM tidak ditumpuk: pisahkan OBJEK dari NOMINAL (`[voucher]{OBJEK} [50rb]{NOMINAL}`).
5. Nominal pada peristiwa gagal atau hampir terjadi tetap ditandai (`hampir ketipu [200 dollar]{NOMINAL}`).

### 3.3 PLATFORM

**Definisi (usulan KP-03).** Nama aplikasi, situs, atau layanan digital yang disebut sebagai tempat kejadian, saluran kontak, sarana pembayaran, pihak yang dicatut, atau pihak yang dikeluhkan.

| Kategori | Contoh nama |
|---|---|
| *Marketplace* dan jual beli | Shopee, Tokopedia, Lazada, Bukalapak, OLX, Carousell |
| Media sosial dan pesan | WhatsApp, Instagram, Facebook, TikTok, Telegram, X |
| Dompet digital dan bank | DANA, OVO, GoPay, ShopeePay, LinkAja, BCA, BRI, BNI, Mandiri |
| Pinjaman daring dan *fintech* | Kredivo, Adakami, Akulaku, Indodana |
| Transportasi daring | Grab, Gojek, Maxim |
| *Game* dan layanan lain yang menerima pembayaran | Free Fire |

**Yang ditandai.** Nama dalam bentuk apa pun: baku, huruf besar atau kecil, singkatan (`tokped`, `wa`, `ig`), dipisah spasi (`buka lapak`, `toko pedia`), atau salah ketik (`shoppe`, `carousel`). Sub merek yang membentuk satu nama layanan ditandai utuh (`ShopeePay`, `TikTok Shop`).

**Yang tidak ditandai.** Kata jenis umum (*aplikasi*, *bank*, *marketplace*, *toko online*, *pinjol*, *dompet digital*), pronomina (`aplikasi ini`), nama akun (itu PELAKU), tautan, serta institusi yang bukan layanan digital (kepolisian, dinas).

**Kata jenis di depan nama dikeluarkan**: `bank BNI` → `BNI`; `aplikasi DANA` → `DANA`.

**Kata ambigu: uji substitusi.** Ganti kata itu dengan nama platform lain (OVO, GoPay). Bila kalimat masih wajar dan makna sama, itu PLATFORM. Bila lebih wajar diganti *uang* atau *dana (kas)*, itu bukan PLATFORM.

| Kalimat | Keputusan |
|---|---|
| `pengembalian dana belum masuk` | `dana` bukan PLATFORM (*dana* = uang) |
| `saldo dana saya hilang` dan `source` = DANA | `[dana]{PLATFORM}` (kolom `source` boleh dipakai memutus ambigu) |
| `saldo dana saya hilang` dan `source` bukan dompet digital, tanpa petunjuk lain | Tandai `[dana]{PLATFORM}` dengan `RAGU_TIPE` agar manusia yang memutuskan (prinsip 1.4 butir 5) |
| `akun dana saya dibobol` | `akun [dana]{PLATFORM}` |
| `kirim link aja` | Bukan PLATFORM |
| `saldo link aja` | `[link aja]{PLATFORM}` (varian spasi dari LinkAja) |
| `X` huruf tunggal | PLATFORM hanya bila jelas menunjuk layanan X; selain itu tidak |

**Atribut khusus PLATFORM (KP-09).** Setiap PLATFORM diberi `kanonik` (nama baku, misalnya *Tokopedia*) dan `varian` salah satu dari:

| Nilai | Arti | Contoh |
|---|---|---|
| `BAKU` | Sama dengan nama baku, abaikan huruf besar atau kecil | `Shopee` |
| `SINGKATAN` | Singkatan atau bentuk pendek lazim | `tokped`, `toped`, `wa`, `ig` |
| `SPASI` | Nama baku yang ditulis terpisah | `buka lapak`, `toko pedia`, `link aja` |
| `SALAH_KETIK` | Salah ketik atau variasi huruf | `shoppe`, `carousel` |
| `LAINNYA` | Bentuk lain yang tidak masuk empat di atas | |

> `kanonik` hanya untuk menghitung F1 subset varian ejaan. **Dilarang** memakainya untuk membangun Leksikon Toleran: leksikon harus berasal dari sumber eksternal dan dibekukan sebelum menyentuh data uji (Bagian 7 dan 8 dokumen induk). Memakainya akan menjadi kebocoran (*leakage*).

### 3.4 MODUS

**Definisi.** Frasa yang menyebut **cara, dalih, atau perbuatan pelaku** untuk memperdaya penulis atau memindahkan uang, akun, atau data. Berbeda dengan PELAKU, rentang MODUS **boleh memuat kata kerja**.

| Jenis | Contoh |
|---|---|
| Permintaan atau perintah | `[suruh transfer [500rb]{NOMINAL}]{MODUS}`, `[minta kode OTP]{MODUS}`, `[tf dulu [100k]{NOMINAL}]{MODUS}` |
| Dalih atau alasan palsu | `kedok [akun kena blokir]{MODUS}`, `[pemenang undian]{MODUS}` |
| Tawaran atau iming-iming | `[hadiah gratis]{MODUS}`, `[kerja sampingan gaji besar]{MODUS}` |
| Sarana tipuan | `[kirim link palsu]{MODUS}`, `[file APK]{MODUS}` |
| Perbuatan pelaku yang menjadi inti penipuan | `[barang gak dikirim]{MODUS}`, `[kabur setelah dp]{MODUS}` |

**Bukan MODUS**:

| Jenis | Contoh | Alasan |
|---|---|---|
| Akibat atau kerugian di sisi korban | `uang hilang`, `saldo terkuras`, `limit kosong` | Itu dampak, bukan cara |
| Pernyataan umum tanpa cara | `ditipu`, `kena tipu`, `penipuan`, `dibobol`, `diretas`, `kena scam` | Tidak menyebut cara. Dokumen seperti ini sah tanpa MODUS (41,0% Play Store dan 79,9% X tanpa modus spesifik menurut Lampiran A.5) |
| Tindakan penulis | `saya transfer dulu`, `saya klik link` | Itu tindakan korban |
| Kata isyarat | `ngaku`, `mengaku`, `mengatasnamakan`, `berkedok`, `kedok`, `dalih`, `modus`, `katanya` | Isyarat, bukan isi (Lampiran A.1) |
| Opini | `sangat mengecewakan` | |

**Aturan batas.**
1. Panjang target 2 sampai 5 kata; **batas keras 8 kata** (usulan KP-06; dokumen induk menyebut sekitar 5 kata). Bila uraian lebih panjang, ambil klausa inti yang masih bermakna sendiri.
2. Berhenti sebelum kata penghubung klausa: *buat*, *untuk*, *agar*, *supaya*, *biar*, *karena*, *sehingga*, *padahal*, *tapi*, *tetapi*, *lalu*, *terus*, *kemudian* (Lampiran A.2).
3. Jangan sertakan PELAKU, PLATFORM, atau OBJEK di dalam rentang. Bila frasa wajar memuatnya, potong menjadi bagian yang tidak memuatnya. Contoh: `minta transfer ke rekening BCA 123` → `[minta transfer]{MODUS}`.
4. Bila hasil pemotongan kurang dari dua kata atau kehilangan makna, jangan beri MODUS, beri penanda `DI_LUAR_ATURAN` pada dokumen (tahap PRODUKSI). Pada tahap PILOT, lihat Bagian 4.3.
5. NOMINAL yang menjadi bagian frasa permintaan ditumpuk di dalam MODUS (Bagian 4).
6. Dua tindakan berbeda yang dihubungkan *lalu*, *terus*, atau titik adalah dua rentang MODUS. Dua objek yang dikoordinasi pada satu tindakan (`minta OTP dan PIN`) tetap satu rentang bila tidak melewati 8 kata.

### 3.5 OBJEK

> **Definisi ini usulan penuh (KP-01).** Dokumen induk tidak mendefinisikan OBJEK. Setujui, ubah, atau tolak sebelum anotasi dimulai.

**Definisi usulan.** Barang, jasa, produk keuangan, atau aset digital **yang spesifik** yang menjadi sasaran atau sarana penipuan: yang dijual, dipesan, dijanjikan, ditawarkan, dipinjam, atau diambil.

| Tandai | Contoh |
|---|---|
| Barang spesifik (jenis, merek, atau model) | `[iphone 13]{OBJEK}`, `[tiket konser]{OBJEK}`, `[nasi box]{OBJEK}` |
| Pulsa, voucher, paket data | `[pulsa]{OBJEK}`, `[voucher]{OBJEK}` |
| Produk keuangan atau layanan | `[investasi]{OBJEK}`, `[pinjaman]{OBJEK}`, `[jasa joki]{OBJEK}`, `[lowongan kerja]{OBJEK}` |
| Aset digital yang bukan akun platform | `[diamond]{OBJEK}`, `[bitcoin]{OBJEK}` |

**Bukan OBJEK**:

| Jenis | Contoh | Alasan |
|---|---|---|
| Istilah uang umum | `uang`, `duit`, `dana`, `saldo`, `rupiah`, `transferan` | Terlalu umum dan hampir ada di setiap dokumen; jumlahnya sudah ditangkap NOMINAL |
| Kata benda generik | `barang`, `pesanan`, `orderan`, `produk`, `item`, `paket`, `data`, `akun` | Tidak menyebut jenis apa pun |
| Frasa yang memuat nama platform | `akun Instagram`, `saldo DANA` | OBJEK tidak boleh memuat entitas lain (Bagian 4). Tandai PLATFORM saja, dan lewati OBJEK |
| Frasa yang memuat nominal | `voucher 50rb` | Pisahkan: `[voucher]{OBJEK} [50rb]{NOMINAL}` |

**Aturan batas.** 1 sampai 4 kata; ambil frasa nomina tanpa kata sifat penilaian (`iphone 13 pro`, bukan `iphone 13 pro murah banget`). Kata sifat ukuran atau tipe yang membentuk jenis ikut (`tiket konser`, `sepatu bekas`).

---


## 4. Entitas bertumpuk

### 4.1 Dua pola yang diizinkan (T2)

| Pola | Syarat | Contoh |
|---|---|---|
| PLATFORM di dalam PELAKU | Frasa persona berpola `[peran] (dari) [platform]`, atau nama toko atau akun yang memuat nama platform. Kata penghubung hanya boleh *dari*. Kata depan *di*, *lewat*, *via*, *pakai* membuat keduanya berdiri sendiri | `[CS [Shopee]{PLATFORM}]{PELAKU}`; `[CS dari [Shopee]{PLATFORM}]{PELAKU}`; tetapi `[penjual]{PELAKU} di [Shopee]{PLATFORM}` |
| NOMINAL di dalam MODUS | Jumlah uang menjadi bagian frasa permintaan atau tawaran yang kontigu | `[suruh tf [2jt]{NOMINAL}]{MODUS}` |

Rentang dalam harus **sepenuhnya berada di dalam** rentang luar. Rentang yang identik tidak boleh diberi dua tipe (4.3).

### 4.2 Pengenal tidak bertumpuk

Pengenal yang memuat nama bank atau platform tidak ditumpuk: nama platform menjadi PLATFORM terpisah dan nilai pengenal menjadi PELAKU.

`rekening [BCA]{PLATFORM} [1234567890]{PELAKU}`

### 4.3 Dua tahap: PILOT dan PRODUKSI (usulan KP-07)

Dokumen induk (Bagian 3.6) menjanjikan angka **tumpang tindih sejati** dari pilot sebagai dasar kuantitatif dekoder berbasis rentang. Bila panduan melarang semua pola lain sejak awal, angka itu hanya mencerminkan aturan, bukan teks.

| Hal | Tahap PILOT | Tahap PRODUKSI |
|---|---|---|
| Tumpukan selain dua pola (misalnya OBJEK di dalam MODUS) | Tandai kedua entitas sesuai definisi, **tanpa memotong**, dan beri penanda `TUMPANG_LAIN` pada kedua entitas | Tidak diizinkan; ikuti aturan batas (3.4 butir 3 dan 4) |
| Rentang bersilang sebagian | Boleh, dengan `TUMPANG_LAIN` | Tidak diizinkan; perbaiki batas, atau `DI_LUAR_ATURAN` |
| Rentang identik dua tipe | Boleh, dengan `SAMA_RENTANG` | Tidak diizinkan |

Hasil pilot menentukan apakah dua pola cukup. Bila `TUMPANG_LAIN` sering muncul, istilah dokumen induk diperluas menjadi "entitas bertumpuk dan tumpang tindih" (Bagian 4.4 dokumen induk) dan aturan PRODUKSI direvisi **sebelum dikunci**.

---


## 5. Kasus khusus

| No | Situasi | Keputusan |
|---|---|---|
| 5.1 | Nama platform yang sama dengan aplikasi yang diulas, tetapi tidak ditulis di teks | Jangan ditandai (prinsip 1.4 butir 7) |
| 5.2 | Nama aplikasi yang diulas disebut di teks (`Shopee penipu`, `bukalapak tolong`) | Tandai PLATFORM (KP-04) |
| 5.3 | Peringatan untuk orang lain (`hati2 akun @user123 jual tiket`) | Tandai seperti biasa. Apakah penulis korban tidak relevan |
| 5.4 | Peristiwa gagal atau hampir terjadi | Tandai seperti biasa, termasuk NOMINAL |
| 5.5 | Dokumen yang ternyata bukan penipuan (misalnya sindiran politik atau kiasan) | Tandai hanya entitas yang memenuhi definisi. Penyaringan dokumen dilakukan kemudian lewat label V/W/T/O, bukan oleh anotator NER |
| 5.6 | Akun `@userNNNNN` | PELAKU hanya bila akun itu dituduh sebagai pelaku. Akun penulis atau pihak penolong tidak ditandai |
| 5.7 | Salah ketik pada kata inti (`penipum`, `ditipuu`) | Tandai seperti kata yang dimaksud bila maknanya jelas; beri `RAGU_BATAS` atau `RAGU_TIPE` bila perlu |
| 5.8 | Huruf kapital semua (`HOKI_88`, `PENIPU`) | Tidak mengubah aturan |
| 5.9 | Singkatan transaksi (*tf*, *dp*, *cod*) | Bukan entitas sendiri. Menjadi bagian MODUS bila termasuk frasa tindakan (`tf dulu 100k`) |
| 5.10 | Campur kode bahasa Inggris (*scammer*, *refund*, *fake*) | Diperlakukan sama dengan kata Indonesia |
| 5.11 | Bahasa daerah atau teks yang tidak dapat dipahami | Tandai yang jelas; beri `TIDAK_JELAS` pada dokumen. Jangan menebak |
| 5.12 | Data pribadi tampak belum disamarkan (nomor telepon atau rekening yang tampak asli) | Tandai seperti biasa dan beri `DATA_PRIBADI_TERLIHAT` pada dokumen; jangan mengutip nomor itu dalam `alasan` |
| 5.13 | Penomoran dan format kronologi (`1.`, `Kronologi:`) | Diabaikan |
| 5.14 | Satu frasa dapat dipandang dua tipe | Putuskan dengan definisi. Bila tetap ragu, pilih tipe yang definisinya paling spesifik dan beri `RAGU_TIPE` |

---


## 6. Urutan keputusan

Kerjakan berurutan untuk setiap dokumen. Urutan dipilih dari yang paling mekanis ke yang paling subjektif, agar entitas mekanis menjadi jangkar bagi yang subjektif.

1. Baca seluruh dokumen. Tentukan apakah teks dapat dipahami (`TIDAK_JELAS` bila tidak).
2. **NOMINAL**: cari semua ungkapan jumlah uang menurut tabel 3.2. Periksa bukan nomor, tanggal, atau jumlah barang.
3. **PLATFORM**: cari semua nama layanan menurut 3.3. Terapkan uji substitusi untuk kata ambigu. Isi `varian` dan `kanonik`.
4. **PELAKU**: cari pihak yang dituduh menipu (peran, persona, nama, pengenal). Pastikan rentang berupa frasa nomina tanpa kata kerja. Keluarkan kata isyarat.
5. **MODUS**: cari cara, dalih, atau perbuatan inti pelaku. Tolak akibat dan pernyataan umum. Potong agar tidak memuat PELAKU, PLATFORM, atau OBJEK (tahap PRODUKSI).
6. **OBJEK**: cari barang, jasa, atau aset yang spesifik. Tolak istilah uang umum dan kata benda generik.
7. **Tumpukan**: periksa dua pola (Bagian 4). Pastikan tidak ada tumpukan lain di tahap PRODUKSI.
8. **Batas**: untuk setiap rentang, periksa 2.1 sampai 2.5 (tepi, kata penunjuk, tanda baca).
9. **Penanda**: beri penanda dan `alasan` untuk setiap keraguan.
10. Keluarkan JSON (Bagian 8). Jangan menambah penjelasan di luar JSON.

---


## 7. Contoh beranotasi

Semua contoh di bagian ini **dibuat untuk panduan** (ilustrasi buatan), bukan kutipan data. Bila contoh dipakai sebagai *few-shot* di instruksi AI, hanya contoh dari bagian ini yang boleh dipakai, **tidak boleh** diambil dari data uji atau data yang akan dipakai sebagai uji.

| No | Teks dengan notasi | Catatan |
|---|---|---|
| 1 | `Kemarin ada yang ngaku [CS [Shopee]{PLATFORM}]{PELAKU} chat saya, kedok [akun kena blokir]{MODUS}, [suruh transfer [500rb]{NOMINAL}]{MODUS}.` | `ngaku` dan `kedok` isyarat. Persona memuat PLATFORM. NOMINAL di dalam MODUS |
| 2 | `Ditipu [penjual]{PELAKU} di [tokped]{PLATFORM}, [barang gak dikirim]{MODUS} padahal udah tf [1,5 juta]{NOMINAL}.` | `di` memisahkan PELAKU dan PLATFORM. `tokped`: varian `SINGKATAN`, kanonik *Tokopedia*. `udah tf` tindakan korban, bukan MODUS. NOMINAL di luar MODUS berdiri sendiri |
| 3 | `Hati2 akun [IG]{PLATFORM} [@user12345]{PELAKU} jualan [tiket konser]{OBJEK}, [minta dp dulu [200k]{NOMINAL}]{MODUS}` | `IG`: varian `SINGKATAN`, kanonik *Instagram*. Pengenal tidak ditumpuk |
| 4 | `[Penipunya]{PELAKU} [minta transfer]{MODUS} ke rekening [BCA]{PLATFORM} [1234567890]{PELAKU} a.n. [Budi Santoso]{PELAKU}` | MODUS dipotong sebelum `ke rekening` karena kalimat berikutnya memuat PLATFORM dan PELAKU. `a.n.` dikeluarkan. Klitik `-nya` ikut kata |
| 5 | `Pengembalian dana belum masuk ke akun [dana]{PLATFORM} saya` | `dana` pertama = uang, bukan PLATFORM. Kedua menunjuk dompet digital |
| 6 | `Uang saya hilang [270ribu]{NOMINAL}, rugi [jutaan]{NOMINAL}` | `uang` tidak ditandai OBJEK. `hilang` akibat, bukan MODUS. `jutaan` perkiraan tanpa angka |
| 7 | `Untung batal transfer [300 rb]{NOMINAL} ke orang yg ngaku [polisi]{PELAKU}` | `orang` terlalu umum. `ngaku` isyarat. `polisi` persona |
| 8 | `Pesan [nasi box]{OBJEK} 60 buah seharga [3 juta]{NOMINAL}` | `60 buah` bukan NOMINAL. Objek spesifik ditandai |
| 9 | `[Shopee]{PLATFORM} penipu, aplikasinya penipu semua` | PELAKU tidak ditandai pada platform atau aplikasi |
| 10 | `CS [Shopee]{PLATFORM} tidak membantu sama sekali` | CS di sini bukan pelaku. Hanya PLATFORM |
| 11 | `Saya ditipu lewat telepon oleh [CS [Kredivo]{PLATFORM}]{PELAKU} atas nama [Budi]{PELAKU}` | Dua rujukan pelaku yang berbeda dilabeli sebagai dua rentang |
| 12 | `Mengecewakan banget, ditipu lagi` | Tanpa entitas: `entitas: []` |
| 13 (PILOT) | `[jual [iphone]{OBJEK} murah]{MODUS}` | OBJEK di dalam MODUS: tahap PILOT menandai keduanya dengan `TUMPANG_LAIN`. Tahap PRODUKSI: MODUS dipotong; bila tersisa kurang dari dua kata, hanya OBJEK ditandai dan dokumen diberi `DI_LUAR_ATURAN` |

---


## 8. Format keluaran dan pemeriksaan otomatis

### 8.1 Format

Satu objek JSON per dokumen. Keluarkan **hanya JSON**, tanpa teks lain.

Masukan (dari sistem, bukan keluaran):

```
doc_id: CONTOH:0001
source: Shopee
nerText: Kemarin ada yang ngaku CS Shopee chat saya, kedok akun kena blokir, suruh transfer 500rb.
```

Keluaran:

```json
{
  "doc_id": "CONTOH:0001",
  "versi_panduan": "v0.1",
  "tahap": "PILOT",
  "entitas": [
    {"id": "e1", "tipe": "PELAKU",   "mulai": 23, "akhir": 32, "teks": "CS Shopee",
     "varian": null, "kanonik": null, "penanda": [], "alasan": null},
    {"id": "e2", "tipe": "PLATFORM", "mulai": 26, "akhir": 32, "teks": "Shopee",
     "varian": "BAKU", "kanonik": "Shopee", "penanda": [], "alasan": null},
    {"id": "e3", "tipe": "MODUS",    "mulai": 50, "akhir": 66, "teks": "akun kena blokir",
     "varian": null, "kanonik": null, "penanda": [], "alasan": null},
    {"id": "e4", "tipe": "MODUS",    "mulai": 68, "akhir": 88, "teks": "suruh transfer 500rb",
     "varian": null, "kanonik": null, "penanda": [], "alasan": null},
    {"id": "e5", "tipe": "NOMINAL",  "mulai": 83, "akhir": 88, "teks": "500rb",
     "varian": null, "kanonik": null, "penanda": [], "alasan": null}
  ],
  "penanda_dokumen": [],
  "catatan": null
}
```

Posisi pada contoh sudah diverifikasi dengan potongan `nerText[mulai:akhir]`.

| Bidang | Aturan |
|---|---|
| `tipe` | Salah satu dari `PELAKU`, `NOMINAL`, `PLATFORM`, `MODUS`, `OBJEK` |
| `mulai`, `akhir` | Bilangan bulat; 0 ≤ `mulai` < `akhir` ≤ panjang `nerText` |
| `teks` | Harus sama dengan `nerText[mulai:akhir]` |
| `varian`, `kanonik` | **Wajib** untuk PLATFORM, **harus null** untuk tipe lain |
| `penanda` | Daftar dari tabel 8.2; boleh kosong |
| `alasan` | Satu kalimat; **wajib** bila `penanda` tidak kosong; tidak boleh memuat nomor telepon atau rekening |
| `penanda_dokumen`, `catatan` | Opsional |

### 8.2 Penanda

| Penanda | Dipakai bila |
|---|---|
| `RAGU_ADA` | Tidak yakin ini entitas (prinsip 1.4 butir 5) |
| `RAGU_BATAS` | Tidak yakin batas awal atau akhir (butir 6) |
| `RAGU_TIPE` | Tidak yakin tipe |
| `TUMPANG_LAIN` | Tumpukan atau tumpang tindih di luar dua pola (tahap PILOT) |
| `SAMA_RENTANG` | Dua tipe memiliki rentang identik (tahap PILOT) |
| `DI_LUAR_ATURAN` | Kasus tidak tercakup panduan; dicatat sebagai putusan kasus di `PROTOKOL_ANOTASI.md` Bagian 13 (tingkat entitas atau dokumen) |
| `TIDAK_JELAS` | Teks sulit dipahami (tingkat dokumen) |
| `DATA_PRIBADI_TERLIHAT` | Nomor atau data pribadi tampak belum disamarkan (tingkat dokumen) |

### 8.3 Pemeriksaan otomatis (validator)

Semua keluaran AI melewati pemeriksaan ini **sebelum** dilihat manusia. Kegagalan memicu satu kali pengulangan; bila masih gagal, dokumen ditandai gagal dan diperiksa manusia dari awal.

| No | Pemeriksaan | PILOT | PRODUKSI |
|---|---|---|---|
| V1 | JSON valid; semua bidang wajib ada | Gagal | Gagal |
| V2 | Posisi valid; `teks` sama dengan potongan | Gagal | Gagal |
| V3 | `tipe` termasuk lima tipe | Gagal | Gagal |
| V4 | Tidak diawali atau diakhiri spasi atau tanda baca (kecuali pengecualian 2.2) | Gagal | Gagal |
| V5 | Tepi berada di batas kata (2.4) | Gagal | Gagal |
| V6 | Tidak ada dua entitas dengan rentang identik | Peringatan bila bertanda `SAMA_RENTANG` | Gagal |
| V7 | Tumpukan hanya dua pola T2 | Peringatan bila bertanda `TUMPANG_LAIN` | Gagal |
| V8 | Tidak ada rentang bersilang sebagian | Peringatan bila bertanda `TUMPANG_LAIN` | Gagal |
| V9 | `varian` dan `kanonik` terisi untuk PLATFORM dan null untuk tipe lain | Gagal | Gagal |
| V10 | Penanda tidak kosong berarti `alasan` terisi | Gagal | Gagal |
| V11 | MODUS tidak lebih dari 8 kata | Peringatan | Gagal |
| V12 | PELAKU tidak memuat kata isyarat (Lampiran A.1) atau kata *yang* | Peringatan | Peringatan |
| V13 | Tidak ada rentang yang jatuh seluruhnya pada kata ganti atau kata terlalu umum (Lampiran A.3) | Peringatan | Peringatan |

---


## Lampiran A. Kata isyarat dan daftar pendamping

Bagian ini ikut masuk ke instruksi AI. Daftar bersifat **ilustrasi**, bukan tertutup; bila menemukan kata sejenis, perlakukan sama.

### A.1 Kata isyarat (tidak masuk rentang apa pun)

*ngaku*, *ngaku2*, *mengaku*, *mengatasnamakan*, *atas nama* (untuk persona), *berkedok*, *kedok*, *dalih*, *modus*, *katanya*, *dengan alasan*.

### A.2 Kata penghentian klausa MODUS

*buat*, *untuk*, *agar*, *supaya*, *biar*, *karena*, *sehingga*, *padahal*, *tapi*, *tetapi*, *lalu*, *terus*, *kemudian*, *setelah itu*.

### A.3 Kata terlalu umum atau rujukan ulang (bukan PELAKU)

*orang* (tanpa penjelas), *seseorang*, *pihak*, *dia*, *ia*, *mereka*, *kamu*, *anda*, *orang itu*, *pihak tersebut*.

### A.4 Kata penunjuk dan sapaan di tepi rentang

*si*, *sang*, *para*, *seorang*, *ini*, *itu*, *tersebut*, *yang*; *bapak*, *ibu*, *pak*, *bu*, *kak*, *mas*, *mbak*; pengantar nama: *a.n.*, *atas nama*, *nama*, *nomor*, *no.*, *rek*.

### A.5 Contoh variasi nama platform

Dari pemindaian pra-penelitian pada 13 merek (Lampiran A.5 dokumen induk): *buka lapak*, *link aja*, *toko pedia* (varian spasi); *tokped*, *toped*, *wa*, *ig* (singkatan); *shoppe*, *carousel* (salah ketik). Daftar ini hanya membantu anotator memahami bentuk variasi. **Bukan** leksikon dan tidak boleh dipakai membangun leksikon.
