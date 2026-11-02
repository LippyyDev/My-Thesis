# EKSPERIMEN/DATA

Folder ini menampung data hasil *scraping* untuk tesis (Play Store dan X). Atas keputusan pemilik repo, data **dikomit ke GitHub**, kecuali `TERBATAS/` (garam pseudonim) dan empat berkas di atas 100 MB (batas GitHub). Status tiap berkas ada di kolom `status_git` pada `MANIFES_DATA.csv`; aturannya ada di `.gitignore`.

## Peringatan (repo publik)

| Hal | Dasar |
|---|---|
| Data pribadi | Teks X masih memuat nomor HP dan rekening asli (Lampiran A.5 pada `RENCANA_SINGKAT_TESIS.md`). *Checkpoint* Play Store memuat `userName` dan `userImage`; berkas X mentah memuat data akun penulis |
| Ketentuan penyedia | Ketentuan penyebaran ulang teks Play Store dan X **belum diperiksa**; periksa sebelum menyebarluaskan |
| Riwayat Git | Berkas yang sudah dikomit tetap tersimpan di riwayat walaupun dihapus kemudian. Menghapus data dari repo publik memerlukan penulisan ulang riwayat |

Pertimbangkan menjadikan repo privat (Settings, Danger Zone) selama masa penelitian. Rilis dataset untuk publik (K1) sebaiknya dirancang terpisah setelah anonimisasi.

**Berkas yang tidak ada di GitHub (lebih dari 100 MB):** `PLAYSTORE/BERSIH/ULASAN_BERSIH.csv` dan `.jsonl`, serta `PLAYSTORE/ARSIP/PIPELINE_LAMA/GABUNGAN_BERLABEL/RAW_ALL_REVIEWS.csv` dan `.json`. Simpan di cadangan pribadi dan periksa dengan `--verifikasi`.

## Struktur

```
EKSPERIMEN/DATA/
  README.md              (dikomit)
  MANIFES_DATA.csv       (dikomit)  ukuran, SHA256, jumlah baris, nama asal
  .gitignore             (dikomit)
  TERBATAS/              (LOKAL, tidak pernah dikomit)  PSEUDONYM_SALT.txt
  PLAYSTORE/  dan  X/
    MENTAH/CHECKPOINT/   data asli hasil scraping, belum diproses
    BERSIH/              keluaran pembersihan aturan v1.4
      ULASAN_BERSIH.csv / .jsonl
      CATATAN_PROSES.json
      RINGKASAN_TAHAPAN.csv
    KANDIDAT_KORBAN/     lolos aturan narasi korban S-06 (Tingkat A)
    PELABELAN/           sampel untuk pelabelan manusia (V/W/T/O)
    ARSIP/               data pengembangan dan keluaran lama
```

Aturan penamaan: nama berkas dan folder HURUF BESAR, spasi menjadi garis bawah, ekstensi tetap huruf kecil. Pengecualian yang tidak bisa diubah: `.gitignore`.

## Status isi (dari `CATATAN_PROSES.json`, aturan v1.4)

| Folder | Play Store | X |
|---|---|---|
| `MENTAH/CHECKPOINT` | 54 berkas per aplikasi dan skor, total 659.845 ulasan | 1 berkas, 4.391 tweet |
| `BERSIH/ULASAN_BERSIH` | 514.254 | 3.997 |
| `KANDIDAT_KORBAN/ULASAN_KORBAN_PENIPUAN` | 3.531 | 2.501 |
| `PELABELAN/SAMPEL_CEK_KETEPATAN` | 300 | 300 |
| `PELABELAN/SAMPEL_CEK_KORBAN_TERLEWAT` | 3.000 | 1.000 |
| `PELABELAN/CONTOH_BUKAN_KORBAN` | 1.000 | 1.000 |

Angka di atas cocok dengan Lampiran A.1 (kecuali yang tidak disebut di sana).

**Istilah.** Isi `KANDIDAT_KORBAN` ditentukan **aturan**, bukan manusia. Ketepatannya belum diukur (`audit_presisi: BELUM`), jadi jangan disebut "korban" sebelum pelabelan manusia selesai. Nama berkas `ULASAN_KORBAN_PENIPUAN` dipertahankan dari keluaran asli agar cocok dengan `CATATAN_PROSES.json` dan Lampiran A.5.

## Catatan yang perlu dikonfirmasi

1. **`ARSIP/PIPELINE_LAMA` (Play Store)** berisi `data/filtered/`, `data/reports/`, dan `data/raw/raw_all_reviews.*` dari ZIP. Penempatannya di arsip berdasarkan bukti: berkas bertanggal 13 sampai 14 September (aturan v1.4 bertanggal 1 Oktober); `RAW_ALL_REVIEWS` berisi 501.462 baris berkolom klasifikasi penipuan (`isFraudComplaint`, `confidenceScore`), padahal *checkpoint* asli berjumlah 659.845; `SUMMARY_REPORT.json` melaporkan 501.462 ulasan. Jadi berkas ini **bukan** data mentah dan bukan keluaran v1.4. Jangan dipakai tanpa konfirmasi dari Anda.
2. **`HASIL_CEK_KETEPATAN.csv`** disebut di `berkas.hasil_cek` pada `CATATAN_PROSES.json` tetapi tidak ada di ZIP. Wajar bila pelabelan belum dilakukan; berkas itu nantinya ditaruh di `PELABELAN/`.
3. **`checkpoints/com.twitter.android_*`** di Play Store adalah ulasan *aplikasi* Twitter di Play Store, jadi tetap masuk `PLAYSTORE`, bukan `X`.
4. **Nama berkas berubah.** Dokumen dan kode yang masih menyebut nama lama (`ulasan_korban_penipuan.jsonl`, `catatan_proses.json`, dan seterusnya) perlu diperbarui. Kolom `nama_asal` di `MANIFES_DATA.csv` memetakan nama lama ke nama baru. Isi `CATATAN_PROSES.json` sengaja tidak diubah (kunci `berkas` masih memakai nama lama).

## Cara memakai di komputer lain

1. Unduh ZIP dari cadangan, ekstrak sehingga ada folder `Playstore/` dan `X/`.
2. Jalankan dari `EKSPERIMEN/KODE`:

```
python ATUR_DATA.py --playstore PATH/Playstore --x PATH/X --tujuan ../DATA --uji-kering
python ATUR_DATA.py --playstore PATH/Playstore --x PATH/X --tujuan ../DATA
python ATUR_DATA.py --tujuan ../DATA --verifikasi
```

Tanpa `--pindah`, berkas disalin dan sumber tidak berubah. Dengan `--pindah`, salinan kedua `pseudonym_salt.txt` (identik) tetap tinggal di folder sumber; hapus secara manual setelah memastikan `TERBATAS/PSEUDONYM_SALT.txt` aman.

## Garam pseudonim

`TERBATAS/PSEUDONYM_SALT.txt` dipakai untuk membuat pseudonim data pribadi. Jangan dikomit, jangan ditempel ke obrolan atau dokumen, dan simpan cadangannya di tempat terpisah dari data. Hilangnya garam membuat pseudonimisasi tidak bisa direproduksi; bocornya garam melemahkan perlindungan pseudonim.
