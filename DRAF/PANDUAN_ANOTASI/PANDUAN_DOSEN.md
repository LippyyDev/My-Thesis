# Panduan Pemeriksaan Label untuk Dosen

**Versi**: v0.2 (DRAF, **belum dikunci**) | **Tanggal**: 2 November 2026
**Program Studi**: Teknik Informatika S2, Universitas Hasanuddin
**Dokumen induk**: `DRAF/RENCANA_TESIS/RENCANA_SINGKAT_TESIS.md` rev8.3 (jika berbeda dengan set ini, dokumen induk menang, kecuali pada butir yang ditandai usulan, lihat `PROTOKOL_ANOTASI.md` Bagian 0.2)

**Isi berkas ini**: cara memeriksa label yang dibuat anotator AI. Aturan lengkap ada di `PANDUAN_ANOTASI.md`.

**Peta berkas.** Penomoran bagian dipertahankan di seluruh set. Rujukan "Bagian N" tanpa nama berkas menunjuk set ini; "dokumen induk" menunjuk `DRAF/RENCANA_TESIS/RENCANA_SINGKAT_TESIS.md`.

| Berkas | Isi | Pembaca | Masuk instruksi AI? |
|---|---|---|---|
| `PANDUAN_ANOTASI.md` | Bagian 1 sampai 8 dan Lampiran A: aturan penandaan | Anotator AI; dosen sebagai rujukan | **Ya**, seluruh isi berkas |
| `PROTOKOL_ANOTASI.md` | Bagian 0, 9, 11, 12, 13 dan Rujukan: keputusan, prosedur, pengukuran, versi | Penulis | Tidak |
| `PANDUAN_DOSEN.md` | Lembar ringkas dan Bagian 10: cara memeriksa label | Dosen | Tidak |

Aturan hanya ditulis lengkap di `PANDUAN_ANOTASI.md`. Lembar ringkas dosen merujuk nomor bagian dan tidak menyalin aturan.

---

## Daftar Isi

- Lembar ringkas (satu halaman)
10. Validasi oleh dosen
- Yang diukur dari pemeriksaan (ringkas)
- Rujukan

---

## Lembar ringkas (satu halaman)

Untuk memeriksa dengan cepat. **Aturan lengkap ada di `PANDUAN_ANOTASI.md`**; bila lembar ini berbeda dengan berkas itu, berkas itu yang berlaku.

| Tipe | Intinya | Bukan | Aturan lengkap |
|---|---|---|---|
| PELAKU | Pihak yang menipu, berupa frasa nomina tanpa kata kerja: peran (*penjual*), persona (*CS Shopee*), teman atau keluarga bila teks menyatakan ia menipu, nama, atau nilai pengenal (nomor, akun) | Kata ganti, *orang*, *pihak*; platform yang hanya dituduh atau hanya ditiru (*menyamar sebagai OVO*: PLATFORM saja, KP-13); pegawai yang hanya tidak membantu | Bagian 3.1 |
| NOMINAL | Semua ungkapan jumlah uang, termasuk bentuk tidak baku: *2jt*, *500rb*, *100k*, *sejuta*, *jutaan*; angka tanpa satuan tepat setelah *dp/tf* diberi tanda ragu (KP-15) | Nomor telepon atau rekening, tanggal, jumlah barang, bunga, poin | Bagian 3.2 |
| PLATFORM | Nama aplikasi, situs, atau layanan digital (termasuk bank dan dompet digital), dalam bentuk baku, singkatan, terpisah spasi, atau salah ketik; awalan *di-/ke-* yang menempel (*dishopeepay*) tidak ikut rentang (KP-14) | Kata jenis umum (*aplikasi*, *bank*), nama akun, kata *dana* yang berarti uang | Bagian 3.3 |
| MODUS | Cara, dalih, atau perbuatan inti pelaku; boleh memuat kata kerja; target 2 sampai 5 kata, paling banyak 8 | Akibat (*uang hilang*), pernyataan umum (*ditipu*), tindakan penulis, kata isyarat (*ngaku*, *kedok*) | Bagian 3.4 |
| OBJEK | Barang, jasa, atau aset yang spesifik (*tiket konser*, *iphone 13*). **Definisi ini belum disetujui** | Istilah uang umum, kata benda generik (*barang*, *pesanan*) | Bagian 3.5 |

Tumpukan yang diizinkan hanya dua: PLATFORM di dalam PELAKU (`[CS [Shopee]{PLATFORM}]{PELAKU}`) dan NOMINAL di dalam MODUS (`[suruh tf [2jt]{NOMINAL}]{MODUS}`). Aturan lengkap: Bagian 4 `PANDUAN_ANOTASI.md`.

---

## 10. Validasi oleh dosen (untuk dosen)

### 10.1 Ringkasan satu paragraf

Anotator AI memberi label awal pada teks keluhan. Bapak atau Ibu diminta memeriksa label itu terhadap aturan Bagian 3 sampai 5 di `PANDUAN_ANOTASI.md`, lalu memutuskan untuk tiap label: setuju, ubah batas, ubah tipe, atau hapus; dan menambahkan label yang terlewat. Pada sebagian pilot, Bapak atau Ibu melabeli dari awal tanpa melihat label AI. Hasil pemeriksaan diukur (`PROTOKOL_ANOTASI.md` Bagian 11) sehingga kualitas data dapat dipertanggungjawabkan dengan angka, bukan dengan pernyataan "sudah diperiksa". Beban kerja belum diukur; pilot menghasilkan angka waktu per dokumen yang dipakai menentukan ukuran sampel berikutnya.

### 10.2 Tahap validasi

| Tahap | Data | Pemeriksa | Bentuk |
|---|---|---|---|
| I | Pilot (300 sampai 500 dokumen) | Dosen **dan** penulis, masing-masing independen | Sebagian pilot (usulan: sepertiga) dilabeli **dari awal** tanpa label AI; sisanya memeriksa label AI |
| II | Hasil pilot | Penulis dan dosen | Rapat putusan kasus beda pendapat; panduan direvisi; hasil dicatat di `PROTOKOL_ANOTASI.md` Bagian 13 |
| III | **Seluruh data uji** | Manusia penuh | Label AI diperiksa dokumen demi dokumen. Bila dosen tidak sanggup semuanya, penulis memeriksa seluruhnya dan dosen memeriksa sampel acak hasil periksa penulis; pembagian ini **dinyatakan terbuka** di tesis |
| IV | Data latih | Sampel acak per sumber | Tingkat koreksi dilaporkan. Sisa data latih berlabel perak dan dinyatakan sebagai keterbatasan |

Catatan jujur: penulis juga penyusun aturan, sehingga penulis bukan anotator yang sepenuhnya independen dari panduan. Dosen berperan sebagai pembanding independen.

### 10.3 Perlindungan terhadap bias penerimaan (*anchoring*)

Pemeriksa yang hanya melihat label AI cenderung menyetujuinya, terutama pada batas rentang. Fort dan Sagot (2010) melaporkan, pada penandaan jenis kata, bahwa label awal otomatis mempercepat kerja dan menaikkan kualitas, tetapi menimbulkan bias terhadap label otomatis; besar bias bergantung pada anotator dan pada akurasi penanda otomatis (tugasnya bukan NER, sehingga hasilnya hanya menjadi alasan kehati-hatian, bukan perkiraan besar efek pada data ini). Karena itu:

1. Pada subset pilot tanpa label AI, simpan label dosen **sebelum** label AI diperlihatkan.
2. Bila tingkat koreksi dosen hampir nol pada data yang besar, curigai pemeriksaan yang terlalu longgar. Itu bukan bukti AI akurat.
3. Laporkan tingkat koreksi per tipe (`PROTOKOL_ANOTASI.md` Bagian 11).

### 10.4 Cara memeriksa satu label

Untuk setiap label AI, jawab lima pertanyaan berurutan. Jawaban **tidak** pada salah satunya berarti label dikoreksi.

| No | Pertanyaan |
|---|---|
| 1 | Apakah hal ini benar-benar ada di teks sebagai entitas bertipe itu (bukan dugaan, bukan akibat, bukan kata umum)? |
| 2 | Apakah tipenya sesuai definisi di Bagian 3 `PANDUAN_ANOTASI.md`? |
| 3 | Apakah batas awal dan akhirnya sesuai Bagian 2 `PANDUAN_ANOTASI.md` dan aturan batas tipe itu? |
| 4 | Apakah tumpukannya sesuai Bagian 4 `PANDUAN_ANOTASI.md`? |
| 5 | Apakah ada entitas lain yang terlewat di dokumen ini? |

Daftar singkat penolakan per tipe:

| Tipe | Koreksi bila |
|---|---|
| PELAKU | Memuat kata kerja atau klausa *yang*; berupa kata ganti, *orang*, *pihak*; berupa platform yang hanya dituduh; berupa pegawai platform yang hanya tidak membantu; kata isyarat ikut dalam rentang |
| NOMINAL | Berupa nomor, tanggal, jumlah barang, bunga, atau poin; memuat *sekitar*, *total*, *sebesar*; satuan ambigu ditandai tanpa dasar |
| PLATFORM | Kata jenis umum (*aplikasi*, *bank*) ikut; *dana* sebagai uang ditandai; akun ditandai sebagai PLATFORM; `varian` atau `kanonik` salah |
| MODUS | Berupa akibat (*uang hilang*) atau pernyataan umum (*ditipu*); tindakan penulis; lebih dari 8 kata; memuat PELAKU, PLATFORM, atau OBJEK pada tahap PRODUKSI |
| OBJEK | Berupa istilah uang umum atau kata benda generik; memuat PLATFORM atau NOMINAL |

### 10.5 Bagaimana mencatat putusan

Format lembar kerja per entitas (tabel atau berkas CSV, mengikuti alat yang dipilih):

```
doc_id,id_entitas,tipe_ai,mulai_ai,akhir_ai,teks_ai,putusan,tipe_akhir,mulai_akhir,akhir_akhir,teks_akhir,kode_alasan,catatan
```

| Putusan | Arti |
|---|---|
| `SETUJU` | Label benar apa adanya |
| `UBAH_BATAS` | Tipe benar, batas salah; isi `mulai_akhir` dan `akhir_akhir` |
| `UBAH_TIPE` | Rentang benar, tipe salah; isi `tipe_akhir` |
| `UBAH_KEDUANYA` | Tipe dan batas salah |
| `HAPUS` | Bukan entitas |
| `TAMBAH` | Entitas yang terlewat; isi baris baru dengan `tipe_akhir`, `mulai_akhir`, `akhir_akhir` |

| Kode alasan | Arti |
|---|---|
| `BATAS_KURANG` | Rentang AI terlalu pendek |
| `BATAS_LEBIH` | Rentang AI terlalu panjang |
| `TIPE_SALAH` | Tipe tidak sesuai definisi |
| `BUKAN_ENTITAS` | AI menandai yang bukan entitas |
| `TERLEWAT` | AI melewatkan entitas |
| `TUMPUKAN_SALAH` | Tumpukan tidak sesuai Bagian 4 `PANDUAN_ANOTASI.md` |
| `ATURAN_KURANG` | Panduan tidak mencukupi untuk memutuskan; kasus masuk daftar putusan kasus (`PROTOKOL_ANOTASI.md` Bagian 13) |
| `ATURAN_BERTENTANGAN` | Dua aturan memberi hasil berlawanan |

Kode `ATURAN_KURANG` dan `ATURAN_BERTENTANGAN` hanya dikumpulkan saat pilot. Setelah panduan dikunci, perubahan aturan tidak dilakukan; kasus semacam itu dicatat sebagai erata (`PROTOKOL_ANOTASI.md` Bagian 12).

### 10.6 Contoh pemeriksaan satu dokumen

Teks: `Kemarin ada yang ngaku CS Shopee chat saya, kedok akun kena blokir, suruh transfer 500rb.`

| Label AI | Putusan dosen | Kode alasan |
|---|---|---|
| PELAKU `ngaku CS Shopee` | `UBAH_BATAS` ke `CS Shopee` | `BATAS_LEBIH` (kata isyarat ikut) |
| PLATFORM `Shopee` | `SETUJU` | |
| MODUS `kedok akun kena blokir` | `UBAH_BATAS` ke `akun kena blokir` | `BATAS_LEBIH` (kata isyarat *kedok*) |
| MODUS `suruh transfer 500rb` | `SETUJU` | |
| NOMINAL `500rb` | `SETUJU` | |



---

## Yang diukur dari pemeriksaan (ringkas)

Hasil pemeriksaan dihitung menjadi: F1 *strict* antara penulis dan dosen pada pilot yang dilabeli dari awal; F1 label AI terhadap label akhir; tingkat koreksi per tipe; dan proporsi entitas yang bertumpuk atau bertumpang tindih. Rinciannya ada di `PROTOKOL_ANOTASI.md` Bagian 11.

---

## Rujukan

1. K. Fort and B. Sagot, "Influence of pre-annotation on POS-tagged corpus development," in *Proc. 4th Linguistic Annotation Workshop (LAW IV)*, Uppsala, Sweden, 2010, pp. 56–63. [Online]. Available: https://aclanthology.org/W10-1807/ (Temuan dibaca dari PDF ACL Anthology; halaman ACL Anthology tidak mencantumkan DOI, sehingga DOI tidak ditulis.)
