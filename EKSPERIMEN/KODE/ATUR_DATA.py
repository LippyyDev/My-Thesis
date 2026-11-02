#!/usr/bin/env python3
"""ATUR_DATA.py: menata data hasil *scraping* ke struktur EKSPERIMEN/DATA.

Fungsi
------
1. Memetakan berkas dari folder sumber Playstore/ dan X/ (hasil unduhan ZIP)
   ke subfolder baru dengan penamaan HURUF BESAR (ekstensi tetap huruf kecil).
2. Membuat MANIFES_DATA.csv (ukuran, SHA256, jumlah baris, nama asal, status Git).
3. Memverifikasi data lokal terhadap manifes (--verifikasi).

Contoh
------
  # lihat rencana tanpa mengubah apa pun
  python ATUR_DATA.py --playstore D:/Unduhan/Playstore --x D:/Unduhan/X \
      --tujuan ../DATA --uji-kering

  # salin (aman, sumber tidak berubah) lalu tulis manifes
  python ATUR_DATA.py --playstore D:/Unduhan/Playstore --x D:/Unduhan/X --tujuan ../DATA

  # pindah (hemat ruang disk)
  python ATUR_DATA.py --playstore ... --x ... --tujuan ../DATA --pindah

  # periksa keutuhan data lokal terhadap manifes
  python ATUR_DATA.py --tujuan ../DATA --verifikasi

Catatan keamanan
----------------
pseudonym_salt.txt dipindahkan ke TERBATAS/ dan TIDAK PERNAH dikomit
(diabaikan oleh .gitignore). Isi berkas itu tidak dicetak oleh skrip ini.
Hanya Python standar yang dipakai.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import re
import shutil
import sys
from pathlib import Path

csv.field_size_limit(sys.maxsize)

# GitHub menolak berkas di atas 100 MB. Berkas yang lebih besar dari batas ini
# berstatus LOKAL (diabaikan .gitignore); sisanya DIKOMIT. TERBATAS/ tidak pernah dikomit.
BATAS_GITHUB = 95 * 1024 * 1024
NAMA_MANIFES = "MANIFES_DATA.csv"
FOLDER_TERBATAS = "TERBATAS"
BERKAS_DOKUMENTASI = {".gitignore", "README.md", NAMA_MANIFES}

PLATFORM = {"playstore": "PLAYSTORE", "x": "X"}

# (pola pada jalur relatif terhadap folder platform, folder tujuan di dalam platform)
# {g1} diisi grup regex pertama (dipakai untuk subfolder _arsip).
ATURAN = [
    (r"^checkpoints/[^/]+\.jsonl?$", "MENTAH/CHECKPOINT"),
    # Bukan data mentah sebenarnya: 501.462 baris berkolom klasifikasi penipuan (keluaran
    # pipeline lama). Data mentah sebenarnya adalah checkpoints/ (659.845 ulasan).
    (r"^data/raw/[^/]+$", "ARSIP/PIPELINE_LAMA/GABUNGAN_BERLABEL"),
    (r"^data/clean/(?:ulasan_bersih\.(?:csv|jsonl)|catatan_proses\.json|ringkasan_tahapan\.csv)$", "BERSIH"),
    (r"^data/clean/ulasan_korban_penipuan\.(?:csv|jsonl)$", "KANDIDAT_KORBAN"),
    (r"^data/clean/(?:sampel_cek_ketepatan|sampel_cek_korban_terlewat|contoh_bukan_korban|hasil_cek_ketepatan)\.csv$", "PELABELAN"),
    (r"^data/clean/_arsip/([^/]+)/[^/]+$", "ARSIP/{g1}"),
    (r"^data/filtered/[^/]+$", "ARSIP/PIPELINE_LAMA/FILTER_KATA_KUNCI"),
    (r"^data/reports/[^/]+$", "ARSIP/PIPELINE_LAMA/LAPORAN"),
]
SALT = r"^data/_restricted/pseudonym_salt\.txt$"


def besar(nama: str) -> str:
    """HURUF BESAR semua, ekstensi (setelah titik terakhir) huruf kecil."""
    p = Path(nama)
    if p.suffix and not nama.startswith("."):
        return p.stem.upper() + p.suffix.lower()
    return nama.upper()


def sha256(jalur: Path) -> str:
    h = hashlib.sha256()
    with jalur.open("rb") as f:
        for blok in iter(lambda: f.read(1 << 20), b""):
            h.update(blok)
    return h.hexdigest()


def hitung_baris(jalur: Path) -> str:
    """Jumlah catatan (tanpa header untuk CSV). Kosong bila format lain."""
    ext = jalur.suffix.lower()
    try:
        if ext == ".csv":
            with jalur.open("r", encoding="utf-8-sig", newline="") as f:
                return str(max(sum(1 for _ in csv.reader(f)) - 1, 0))
        if ext == ".jsonl":
            with jalur.open("r", encoding="utf-8") as f:
                return str(sum(1 for b in f if b.strip()))
    except (OSError, UnicodeDecodeError, csv.Error) as e:
        return f"GAGAL:{type(e).__name__}"
    return ""


def susun_rencana(sumber: Path, kunci: str):
    """Hasilkan (berkas_sumber, jalur_tujuan_relatif_DATA | None, catatan)."""
    for f in sorted(p for p in sumber.rglob("*") if p.is_file()):
        rel = f.relative_to(sumber).as_posix()
        if re.match(SALT, rel):
            yield f, f"{FOLDER_TERBATAS}/PSEUDONYM_SALT.txt", "salt"
            continue
        for pola, tujuan in ATURAN:
            m = re.match(pola, rel)
            if m:
                g1 = m.group(1) if m.groups() else ""
                bagian = [PLATFORM[kunci]] + [b.upper() for b in tujuan.format(g1=g1).split("/")]
                yield f, "/".join(bagian + [besar(f.name)]), ""
                break
        else:
            yield f, None, "TIDAK DIPETAKAN"


def jalankan_penataan(args) -> dict[str, str]:
    tujuan = Path(args.tujuan)
    asal: dict[str, str] = {}
    tak_terpetakan, dilewati, diproses = [], 0, 0
    for kunci in ("playstore", "x"):
        sumber = getattr(args, kunci)
        if not sumber:
            continue
        sumber = Path(sumber)
        if not sumber.is_dir():
            sys.exit(f"Folder sumber tidak ditemukan: {sumber}")
        for f, rel, catatan in susun_rencana(sumber, kunci):
            if rel is None:
                tak_terpetakan.append(f"{kunci}: {f.relative_to(sumber).as_posix()}")
                continue
            dest = tujuan / rel
            # Garam yang sama dari dua platform cukup disimpan sekali.
            if catatan == "salt" and dest.exists():
                if sha256(dest) == sha256(f):
                    print(f"[LEWAT] salt {kunci} identik dengan yang sudah ada")
                    dilewati += 1
                    continue
                dest = dest.with_name(f"PSEUDONYM_SALT_{PLATFORM[kunci]}.txt")
                print(f"[PERINGATAN] salt {kunci} BERBEDA dari yang sudah ada, disimpan terpisah")
            if dest.exists() and not args.timpa:
                if dest.stat().st_size == f.stat().st_size:
                    dilewati += 1
                    asal[dest.relative_to(tujuan).as_posix()] = f.name
                    continue
                sys.exit(f"Tujuan sudah ada dan ukurannya beda: {dest} (pakai --timpa bila disengaja)")
            aksi = "PINDAH" if args.pindah else "SALIN"
            tampil = rel if catatan != "salt" else f"{FOLDER_TERBATAS}/PSEUDONYM_SALT*.txt (isi tidak ditampilkan)"
            print(f"[{aksi}] {kunci}/{f.relative_to(sumber).as_posix()}  ->  {tampil}")
            if not args.uji_kering:
                dest.parent.mkdir(parents=True, exist_ok=True)
                (shutil.move if args.pindah else shutil.copy2)(str(f), str(dest))
            asal[dest.relative_to(tujuan).as_posix()] = f.name
            diproses += 1
    print(f"\nDiproses: {diproses} | dilewati (sudah ada): {dilewati} | tidak dipetakan: {len(tak_terpetakan)}")
    for t in tak_terpetakan:
        print(f"[TIDAK DIPETAKAN] {t}")
    return asal


def muat_asal_lama(jalur: Path) -> dict[str, str]:
    if not jalur.exists():
        return {}
    with jalur.open("r", encoding="utf-8-sig", newline="") as f:
        return {r["jalur"]: r["nama_asal"] for r in csv.DictReader(f)}


def tulis_manifes(tujuan: Path, asal: dict[str, str]) -> None:
    jalur_manifes = tujuan / NAMA_MANIFES
    asal_lama = muat_asal_lama(jalur_manifes)
    baris = []
    for f in sorted(p for p in tujuan.rglob("*") if p.is_file()):
        rel = f.relative_to(tujuan).as_posix()
        if rel.split("/")[0] == FOLDER_TERBATAS or rel in BERKAS_DOKUMENTASI:
            continue
        status = "LOKAL" if f.stat().st_size > BATAS_GITHUB else "DIKOMIT"
        print(f"[MANIFES] {rel}")
        baris.append({
            "jalur": rel,
            "nama_asal": asal.get(rel) or asal_lama.get(rel, ""),
            "ukuran_byte": f.stat().st_size,
            "sha256": sha256(f),
            "jumlah_baris": hitung_baris(f),
            "status_git": status,
        })
    kolom = ["jalur", "nama_asal", "ukuran_byte", "sha256", "jumlah_baris", "status_git"]
    with jalur_manifes.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=kolom, lineterminator="\n")
        w.writeheader()
        w.writerows(baris)
    print(f"\nManifes ditulis: {jalur_manifes} ({len(baris)} berkas)")


def verifikasi(tujuan: Path) -> int:
    jalur_manifes = tujuan / NAMA_MANIFES
    if not jalur_manifes.exists():
        sys.exit(f"Manifes tidak ada: {jalur_manifes}")
    hilang = rusak = ok = 0
    with jalur_manifes.open("r", encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            p = tujuan / r["jalur"]
            if not p.exists():
                print(f"[HILANG] {r['jalur']}")
                hilang += 1
            elif p.stat().st_size != int(r["ukuran_byte"]) or sha256(p) != r["sha256"]:
                print(f"[BEDA]   {r['jalur']}")
                rusak += 1
            else:
                ok += 1
    print(f"\nSesuai: {ok} | hilang: {hilang} | beda: {rusak}")
    return 0 if hilang == rusak == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--playstore", help="folder Playstore/ hasil ekstrak ZIP (berisi data/ dan checkpoints/)")
    ap.add_argument("--x", help="folder X/ hasil ekstrak ZIP (berisi data/ dan checkpoints/)")
    ap.add_argument("--tujuan", required=True, help="folder EKSPERIMEN/DATA")
    ap.add_argument("--pindah", action="store_true", help="pindahkan berkas (default: salin)")
    ap.add_argument("--timpa", action="store_true", help="timpa tujuan yang sudah ada")
    ap.add_argument("--uji-kering", action="store_true", help="tampilkan rencana saja")
    ap.add_argument("--hanya-manifes", action="store_true", help="lewati penataan, tulis ulang manifes")
    ap.add_argument("--verifikasi", action="store_true", help="periksa data lokal terhadap manifes")
    args = ap.parse_args()

    tujuan = Path(args.tujuan)
    if args.verifikasi:
        return verifikasi(tujuan)
    asal: dict[str, str] = {}
    if not args.hanya_manifes:
        if not (args.playstore or args.x):
            ap.error("isi --playstore dan/atau --x (atau pakai --hanya-manifes / --verifikasi)")
        asal = jalankan_penataan(args)
    if args.uji_kering:
        return 0
    tulis_manifes(tujuan, asal)
    return 0


if __name__ == "__main__":
    sys.exit(main())
