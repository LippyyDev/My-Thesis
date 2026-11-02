#!/usr/bin/env python3
"""AUDIT_PANDUAN_DATA.py

Menghitung seberapa sering pola yang relevan bagi PANDUAN_ANOTASI.md muncul pada
korpus kandidat (ULASAN_KORBAN_PENIPUAN.jsonl, Play Store dan X).

STATUS HASIL: hitungan pola (regex), BUKAN anotasi dan BUKAN hasil data berlabel.
Angka dipakai untuk menguji apakah panduan menutup kasus yang nyata muncul di data,
bukan sebagai temuan penelitian. Tiap pola bersifat longgar atau ketat sesuai
komentar; hasil bisa melebihkan atau mengurangi.

Pemakaian:
    python3 AUDIT_PANDUAN_DATA.py
    python3 AUDIT_PANDUAN_DATA.py --data ../DATA --keluar ../DATA/AUDIT_PANDUAN_DATA.json
"""
import argparse
import json
import re
from pathlib import Path

SUMBER = {
    "PLAYSTORE": "PLAYSTORE/KANDIDAT_KORBAN/ULASAN_KORBAN_PENIPUAN.jsonl",
    "X": "X/KANDIDAT_KORBAN/ULASAN_KORBAN_PENIPUAN.jsonl",
}

# Daftar nama platform HANYA untuk menghitung pola audit ini.
# Bukan leksikon dan tidak boleh dipakai membangun Leksikon Toleran (PANDUAN_ANOTASI.md Bagian 3.3).
PLAT = (r"(?:shopeepay|shopee|tokopedia|tokped|toped|lazada|bukalapak|dana|ovo|gopay|linkaja|gojek|grab|"
        r"kredivo|akulaku|adakami|tiktok|instagram|whatsapp|telegram|facebook|bca|bri|bni|mandiri)")
KERABAT = r"(?:temen|teman|saudara|pacar|suami|istri|keluarga|kakak|adik|om|tante|tetangga)"
SATUAN = r"(?:rb|ribu|k|jt|juta|rp|\.|%)"

POLA = {
    # Bagian 3.1: kerabat atau teman yang menurut teks menipu
    "kerabat_disebut_penipu": rf"(?:ditipu|ketipu|nipu|kena tipu)\s+(?:sama|oleh)?\s*{KERABAT}\b",
    # Bagian 4.1 dan 5.15: persona yang hanya berupa nama platform
    "persona_hanya_platform": rf"(?:menyamar|mengaku|ngaku|mengatas ?namakan)\s+(?:sebagai\s+|dari\s+)?{PLAT}\b",
    # Bagian 2.4: awalan di-, ke-, dr menempel pada nama platform
    "awalan_menempel_platform": rf"\b(?:di|ke|dr){PLAT}\b",
    # Bagian 3.2 butir 6: angka 2 sampai 4 digit setelah kata transaksi, tanpa satuan
    "angka_tanpa_satuan": rf"\b(?:dp|tf|transfer|bayar|kirim|minta)\s+\d{{2,4}}\b(?!\s?{SATUAN})",
    # Bagian 5.12 dan Protokol Bagian 9: data pribadi yang tampak
    "telepon_tampak": r"(?<!\d)(?:\+62|62|0)\s?8\d{2}[\s\-]?\d{3,4}[\s\-]?\d{3,5}(?!\d)",
    "angka_9_digit_lebih": r"\d{9,}",
    "angka_9_digit_terpisah": r"(?<!\d)\d{3,4}[\s\-]\d{3,4}[\s\-]\d{3,5}(?!\d)",
    "email": r"[\w.+-]+@[\w-]+\.[\w.]+",
    # Konteks
    "tagar": r"#\w+",
    "mention": r"(?<!\w)@\w+",
    "nominal_jt_juta": r"\b\d+(?:[.,]\d+)?\s?(?:jt|juta)\b",
    "nominal_rb_ribu": r"\b\d+(?:[.,]\d+)?\s?(?:rb|ribu)\b",
    "kata_dana": r"\bdana\b",
}

# Isyarat daring (kasar): dokumen tanpa satu pun isyarat ini kemungkinan di luar topik.
ISYARAT = (r"transfer|\btf\b|rekening|\brek\b|olshop|online|\blink\b|\bdm\b|\bwa\b|whatsapp|shopee|tokopedia|"
           r"tiktok|akun|\bapk\b|otp|pinjol|\bapp|aplikasi|dana\b|gopay|ovo|marketplace|olx|instagram|\big\b|"
           r"\bdp\b|toko|seller|penjual|loker|tiket|paylater|bank|kartu|\bcod\b|situs|website")


def muat(path: Path):
    with path.open(encoding="utf-8") as f:
        return [json.loads(b) for b in f if b.strip()]


def hitung(rows, pola):
    rx = re.compile(pola, re.I)
    return sum(bool(rx.search(r["nerText"])) for r in rows)


def persentil(nilai, p):
    s = sorted(nilai)
    return s[min(len(s) - 1, int(len(s) * p))]


def audit(rows):
    n = len(rows)
    kata = [int(r["n_words"]) for r in rows]
    hasil = {
        "n_dokumen": n,
        "kata_median": sorted(kata)[n // 2],
        "kata_p99": persentil(kata, 0.99),
        "kata_maks": max(kata),
        "lebih_dari_128_kata": sum(k > 128 for k in kata),
        "lebih_dari_256_kata": sum(k > 256 for k in kata),
        "kolom_pii_tidak_kosong": sum(bool(r.get("pii")) for r in rows),
        "tanpa_isyarat_daring_kasar": hitung(rows, rf"^(?!.*(?:{ISYARAT}))"),
    }
    for nama, pola in POLA.items():
        hasil[nama] = hitung(rows, pola)
    # dokumen yang memuat telepon ATAU deret angka panjang (rekening), tanpa hitung ganda
    gabung = "|".join(f"(?:{POLA[k]})" for k in ("telepon_tampak", "angka_9_digit_lebih", "angka_9_digit_terpisah"))
    hasil["pii_tampak_gabungan"] = hitung(rows, gabung)
    return hasil


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", default=str(Path(__file__).resolve().parent.parent / "DATA"),
                    help="folder DATA (berisi PLAYSTORE dan X)")
    ap.add_argument("--keluar", default=None, help="jalur berkas JSON keluaran (opsional)")
    a = ap.parse_args()

    semua = {}
    for nama, rel in SUMBER.items():
        semua[nama] = audit(muat(Path(a.data) / rel))

    kunci = list(next(iter(semua.values())).keys())
    print(f"{'ukuran':34s}" + "".join(f"{s:>12s}" for s in semua))
    for k in kunci:
        print(f"{k:34s}" + "".join(f"{semua[s][k]:12d}" for s in semua))
    print("\nCatatan: hitungan pola, bukan anotasi. Lihat docstring.")

    if a.keluar:
        Path(a.keluar).write_text(json.dumps(semua, ensure_ascii=False, indent=2), encoding="utf-8")
        print("ditulis:", a.keluar)


if __name__ == "__main__":
    main()
