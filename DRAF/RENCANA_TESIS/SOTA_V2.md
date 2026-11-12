# SOTA V2: Penelitian Terkait dan State of The Art per Lapisan

**Tesis**: Ekstraksi Entitas pada Keluhan Penipuan Online Berbahasa Indonesia Menggunakan IndoBERTweet, CharCNN, Leksikon Toleran, dan Efficient GlobalPointer
**Program Studi**: Teknik Informatika S2, Universitas Hasanuddin
**Berkas ini menggantikan**: Bagian 12 (State of The Art) pada `RENCANA_SINGKAT_TESIS.md` rev8.4
**Tanggal penelusuran**: 11 November 2026
**Status klaim**: hasil penelusuran literatur, bukan hasil data asli. Belum ada hasil eksperimen pada data keluhan.

---

## 1. Ringkasan

1. **Belum ada SOTA yang sah dan sebanding untuk tugas tesis ini.** Tidak ada artikel yang mengukur NER pada teks keluhan informal berbahasa Indonesia dengan skema entitas yang sama. "SOTA" hanya dapat ditetapkan per lapisan pada *benchmark* masing-masing, dan hanya sebagai "tertinggi yang ditemukan".
2. **Bagian 12 lama berstatus karya terkait, bukan SOTA.** Alasannya: tidak ada protokol pencarian, tabel mencampur tugas dan metrik berbeda, dan pembanding wajib (NER Indonesia, WNUT, *nested* NER, model generalis/LLM) tidak ada.
3. **Dua klaim lama harus dicabut atau dipersempit.**
   - "IndoBERTweet belum teruji untuk NER" salah. Koto dkk. (2021) melaporkan F1 entitas 88,1 (formal) dan 85,4 (informal) pada data Munarko. IndoBERT IndoLEM mencapai 88,0 dan 86,9, sehingga pada tweet informal IndoBERT lebih tinggi.
   - "Belum ada NER penipuan dalam bahasa apa pun" salah. NER aduan penipuan sudah ada dalam bahasa Belanda (Schraagen dkk., 2017), Tionghoa (Ding & Liu, 2021), dan sistem kontra-penipuan berbasis LLM (IJCAI 2026).
4. **Celah yang masih sah, dengan rumusan sempit**: (a) belum ditemukan *dataset* NER keluhan penipuan berbahasa Indonesia dari ulasan Play Store dan X dengan entitas bertumpuk terbatas; (c) belum ada evaluasi empiris kombinasi CharCNN, leksikon toleran, dan EGP pada teks informal beraksara Latin berbahasa Indonesia. Celah (b), "belum ada arsitektur gabungan fitur karakter, leksikon, dan dekoder *span*", runtuh dalam rumusan umum karena MGBERT-Pointer dan CEAF sudah ada untuk aksara Tionghoa.

---

## 2. Kriteria SOTA yang Dipakai

1. Tugas, *dataset*, *split*, skema label, bahasa, dan metrik harus sama sebelum hasil diperingkat (*micro-F1 strict span*, tingkat entitas).
2. SOTA adalah hasil tertinggi yang terverifikasi dari tabel sumber primer, bukan klaim penulis sendiri.
3. Pemilihan artikel memakai protokol pencarian yang terdokumentasi (Lampiran A).
4. SOTA dipecah per lapisan, tidak dicampur dalam satu tabel.
5. Pembanding paradigma lain (model generalis dan LLM) wajib ada.
6. Hanya artikel yang terbit di jurnal atau prosiding terindeks Scopus masuk Tabel 1. Karya lain dipisah pada Tabel 2.

---

## 3. Tabel 1. Penelitian Terkait (venue terindeks Scopus)

Status Scopus dan kuartil berasal dari SCImago (sebagian dari cuplikan halaman). Scopus tidak diakses langsung. Angka yang berasal dari abstrak atau tabel sekunder diberi catatan.

| No | Judul | Penulis | Tahun | Objek dan masalah | Metode penyelesaian | Kinerja/hasil | Relevansi terhadap penelitian | Link akses |
|---|---|---|---|---|---|---|---|---|
| 1 | BGNER: A boundary guidance framework for enhanced named entity recognition (*J. King Saud Univ. CIS*, Q1) | He, Sun, Yue, Wu, Wang dkk. | 2025 | NER bertumpuk dan datar (Inggris dan Tionghoa); batas entitas sulit ditentukan | *Boundary-aware efficient GlobalPointer* + CNN 3D | ACE2005 F1 87,21; GENIA 82,05 (Tabel 5). Pembanding: DiffusionNER 86,93, CNN-NER 86,82 (ACE05) | Membuktikan EGP sudah dipakai pada teks Inggris, sehingga klaim "EGP belum diuji di luar bahasa Tionghoa" harus dicabut. Mendukung ciri 04 (entitas bertumpuk): modulnya dibangun di atas formulasi EGP, dan Tabel 5 memuat W2NER serta CNN-NER sebagai pembanding kepala *span* untuk Tahap 2. Bedanya: data formal, tanpa fitur karakter dan leksikon, sehingga tidak menjawab ciri 01 sampai 03 | [Springer](https://link.springer.com/article/10.1007/s44443-025-00059-6) |
| 2 | Enhanced Chinese NER with multi-granularity BERT adapter and efficient global pointer (*Complex & Intell. Syst.*, Q1) | Zhang, Xia, Ma, Yang, Ding | 2024 | NER Tionghoa; entitas bertumpuk dan batas ambigu | BERT + *Multi-Granularity Adapter* (karakter, entitas, leksikon) di antara lapisan 1 dan 2 + EGP | MSRA 96,10; Resume 96,23 (dari tabel artikel lain, tabel primer belum terbaca) | Kerangka rujukan tesis: posisi adaptor antara lapisan 1 dan 2 serta kepala EGP diadopsi langsung, dan *Character Adapter* serta *Lexicon Adapter*-nya menjadi lawan ablasi A-CA dan A-LAp. Dua hal wajib dibahas terbuka: semua dataset ujinya BIO datar, sehingga kemampuan entitas bertumpuk hanya terbukti lewat satu studi kasus; dan *Entity Adapter* mengambil triplet dari *input* tanpa penjelasan sumber saat inferensi (risiko kebocoran label), yang menjadi alasan EA dibuang | [Springer](https://link.springer.com/article/10.1007/s40747-024-01383-6) |
| 3 | CEAF: Capsule network enhanced feature fusion architecture for Chinese NER (*PLOS ONE*, Q1) | Ma, Liu, Xu | 2025 | NER Tionghoa pada teks sosial dan informal | BERT + jaringan kapsul + fusi fitur | Weibo 89,1; MSRA 91,8 (tabel perbandingan). Angka ablasi tidak cocok dengan tabel itu, perlu dicek | Contoh terbaru NER pada teks media sosial informal dengan penggabungan beberapa fitur dalam satu model, sehingga celah "belum ada arsitektur gabungan" tidak boleh ditulis dalam bentuk umum. Pembanding untuk ciri 01 dan 04. Bedanya: aksara Tionghoa, tanpa EGP, dan tabelnya berisi anomali angka yang wajib dicek sebelum dikutip | [PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0332622) |
| 4 | NER in social media texts with syntactically enhanced multiscale feature fusion, SEMFF-NER (*Sci. Rep.*, Q1) | Li, Zhou, Hu, Li, Tian (dari daftar pustaka dokumen induk, belum dicek ulang) | 2024 | NER media sosial Inggris; teks tidak baku | XLNet + dependensi sintaksis + fusi multiskala + CRF | Diuji pada WNUT16, WNUT17, OntoNotes5.0; angka belum terbaca | Rujukan NER teks media sosial beraksara Latin pada 2023 sampai 2026, sehingga mendukung ciri 01 pada tulisan yang sama dengan bahasa Indonesia. Bedanya: Inggris, memakai CRF (datar), tanpa fitur karakter, leksikon, dan entitas bertumpuk. Menunjukkan pendekatan lain (sintaksis) terhadap masalah yang sama, bukan pesaing langsung arsitektur usulan | [Nature](https://www.nature.com/articles/s41598-024-78948-5) |
| 5 | Bi-directional context-aware network for nested NER, Bi-DCAN (*Sci. Rep.*, Q1) | Penulis belum terverifikasi | 2024 | NER bertumpuk berbasis *span* | Jaringan konteks dua arah berbasis *span* | Klaim naik 0,24 (ACE05) dan 0,09 (GENIA) atas DiffusionNER; angka absolut belum terbaca | Menunjukkan arah terkini dekoder *span* untuk ciri 04. Kenaikannya sangat kecil (0,09 sampai 0,24), sehingga dapat dipakai sebagai argumen bahwa dekoder *span* sudah jenuh pada data formal, dan kebaruan harus berasal dari data dan teks informal, bukan dekoder baru | [Nature](https://www.nature.com/articles/s41598-024-67114-6) |
| 6 | Segmentation-aware relational GCN with multi-layer CRF for nested NER (*Complex & Intell. Syst.*, Q1) | Han, Wang, Li dkk. | 2024 | NER bertumpuk; batas entitas | GCN relasional sadar segmentasi + CRF berlapis | Angka belum terbaca | Contoh cara lain menangani entitas bertumpuk tanpa dekoder *span* (CRF berlapis). Berguna untuk menjawab pertanyaan penguji "mengapa EGP, bukan CRF bertingkat": pendekatan itu ada, dan hasil B-CRF mengukur kehilangan akibat label satu per token | [Springer](https://link.springer.com/article/10.1007/s40747-024-01551-8) |
| 7 | NER on Indonesian legal documents: a dataset and study using transformer-based models (*IJECE*, Q3; dihentikan Scopus mulai 2025) | Yulianti, Bhary, Abdurrohman, Dwitilas, Nuranti, Husin | 2024 | NER putusan pengadilan Indonesia; 993 dokumen, 20 tipe entitas | Perbandingan IndoBERT, M-BERT, XLM-R, RoBERTa vs BiLSTM(-CRF) | XLM-R F1 0,9295 (abstrak) | Dua kegunaan. Pertama, preseden pembangunan *dataset* NER domain baru berbahasa Indonesia, mendukung kontribusi K1. Kedua, XLM-R terbaik di sini, sehingga XLM-R tidak boleh lagi opsional di Tahap 1. Bedanya: teks formal, tidak ada ciri 01 sampai 04. Venue dihentikan Scopus, sehingga penguji dapat mempersoalkannya | [DOI](https://doi.org/10.11591/ijece.v14i5.pp5489-5501) |
| 8 | Automating NER for Indonesian diplomas via template-based synthetic data generation (*ETASR*, Q2) | Isra, Madenda, Suhatril | 2026 | NER ijazah Indonesia; data sintetis berbasis templat | IndoBERT, kepala klasifikasi token | IndoBERT F1 0,8213 vs cahya/bert-base-indonesian-522M 0,8048 (abstrak) | Bukti terbaru (2026) bahwa NER Indonesia dievaluasi dengan metrik tingkat *span*, sejalan dengan *micro-F1 strict span*. Contoh pemakaian data sintetis berbasis templat untuk NER Indonesia. Bedanya: teks resmi hasil templat, sehingga tidak bisa dijadikan patokan kinerja untuk teks keluhan | [ETASR](https://etasr.com/index.php/ETASR/article/view/16738) |
| 9 | IPerFEX-2023: Indonesian personal financial entity extraction using IndoBERT-BiGRU-CRF (*J. Big Data*, Q1) | Dave, Chowanda | 2024 | NER finansial pribadi Indonesia, 15 tipe entitas, termasuk nominal | IndoBERT (*feature-based*) + BiGRU + CRF | F1 0,73 pada IPerFEX-*small*; angka 0,69 (*large*) belum terverifikasi | Paling dekat di Indonesia untuk ciri 03: menangani entitas nominal ("5 juta") dan masalah OOV numerik pada teks percakapan informal. Mempersempit klaim kebaruan nominal: yang tersisa hanya penanganan bentuk tidak baku (*2jt*, *500rb*, *100k*) pada keluhan. Arsitekturnya (CRF, datar) menjadi bentuk nyata pembanding B-CRF | [Springer](https://link.springer.com/article/10.1186/s40537-024-00987-6) |
| 10 | Biomedical NER based on multi-cross attention feature fusion (*PLOS ONE*, Q1) | Zheng, Han, Yu, Li | 2024 | NER biomedis Inggris; fitur kata dan huruf jarang berinteraksi | DistilBioBERT + CharCNN + CharLSTM + *cross-attention* | F1 90,76 (NCBI-Disease), 94,98 (BC5CDR-Chem), 80,27 (JNLPBA) | Salah satu bukti CharCNN masih dipakai di atas *encoder transformer* pada aksara Latin, mendukung komponen CharCNN dan ciri 02 serta 03. Bedanya penting: fusi lewat *cross-attention* setelah *encoder* (bukan penjumlahan antara lapisan 1 dan 2), teks biomedis formal, dan bukan dekoder *span*. Bukti mekanisme, bukan bukti pada teks informal Indonesia | [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11132514/) |
| 11 | Sequential lexicon enhanced BERT: Chinese NER using SLEBERT (*PeerJ CS*, Q1) | Liu dkk. | 2024 | NER Tionghoa; *noise words* dan konflik leksikon pada *Lexicon Adapter* | *Sequential lexicon* + *position encoding* + atensi adaptif | Weibo 71,76; MSRA 95,78; OntoNotes 82,68; Resume 96,38 (Tabel 4) | Peringatan risiko bagi Leksikon Toleran: bahkan di Mandarin, injeksi leksikon membawa kata derau dan konflik, yang mendasari kriteria H4 (kata ambigu seperti *dana*) dan H5 (*recall* entitas di luar daftar). Menunjukkan *Lexicon Adapter* masih dikembangkan (turunan LEBERT), sehingga ablasi A-LAp punya pembanding yang sah | [PeerJ](https://peerj.com/articles/cs-2344/) |
| 12 | An embarrassingly easy but strong baseline for nested NER (*ACL 2023*, prosiding Scopus) | Yan, Sun, Li, Qiu | 2023 | NER bertumpuk; skor *span* biaffine terpisah | Biaffine + CNN 2D pada matriks skor *span* | Kuat pada *dataset nested* standar (angka belum diambil) | Sumber model B-CNNNER di Tahap 2: dijalankan bila pilot anotasi menunjukkan tumpang tindih sejati tinggi atau galat batas EGP besar. Rujukan sah untuk menjawab "bagaimana bila batas *span* sering salah". Bedanya: diuji pada teks formal | [ACL Anthology](https://aclanthology.org/2023.acl-short.123/) |
| 13 | Application of NER method for Indonesian datasets: a review (*Bull. EEI*, Q3) | Budi, Suryono | 2023 | Tinjauan NER dataset Indonesia (berita, media sosial) | Tinjauan sistematis: 241 dokumen disaring menjadi 20 | Tidak memuat domain penipuan; data sampai 2021 | Dua guna. Pertama, dasar literatur bahwa NER domain penipuan belum tercakup pada peta NER Indonesia. Kedua, contoh protokol penelusuran (empat basis data, kueri, penyaringan) yang dapat ditiru. Batasnya: data hanya sampai 2021 dan kueri dibatasi ke berita dan media sosial, sehingga tidak dapat dipakai untuk klaim "belum ada" tahun 2022 sampai 2026 | [BEEI](https://beei.org/index.php/EEI/article/download/4529/3160) |
| 14 | Evaluation of NER in Dutch online criminal complaints (*CLIN J.*, Scopus) [fondasi 2017] | Schraagen, Brinkhuis, Bex | 2017 | NER aduan pidana daring (penipuan internet), 250 aduan | NER generik (Frog) dievaluasi pada teks aduan | Tipe entitas generik, bukan PELAKU/NOMINAL/MODUS | Pendahulu terdekat dari sisi objek: NER pada keluhan penipuan daring yang ditulis korban. Membatasi klaim celah: yang baru bukan "NER pada keluhan penipuan", melainkan skema entitas forensik (PELAKU, NOMINAL, PLATFORM, MODUS, OBJEK), bahasa Indonesia, dan sumber ulasan Play Store serta X | [CLIN J.](https://clinjournal.org/clinj/article/view/65) |
| 15 | NER on Indonesian tweets using bidirectional LSTM-CRF (*Procedia CS*, Scopus) [fondasi 2019] | Penulis belum terverifikasi | 2019 | NER tweet Indonesia, formal dan informal | BiLSTM-CRF + FastText | F1 86,13 (formal), 81,17 (informal), 84,11 (gabungan) (abstrak) | Bukti kuantitatif pada tweet Indonesia bahwa teks informal menurunkan F1 sekitar 5 poin dibanding formal (ciri 01). Pembanding historis bagi B-Tweet. Bedanya: pra-*transformer*, tiga tipe entitas umum, tanpa entitas bertumpuk | [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S1877050919310798) |

---

## 4. Tabel 2. Wajib Dirujuk, Status Scopus Belum Terverifikasi

| No | Judul | Penulis | Tahun | Relevansi terhadap penelitian | Link akses |
|---|---|---|---|---|---|
| A | IndoBERTweet (EMNLP) | Koto, Lau, Baldwin | 2021 | Sumber *encoder* usulan dan satu-satunya hasil NER IndoBERTweet yang ditemukan: F1 88,1 (formal) dan 85,4 (informal) pada data Munarko, sedangkan IndoBERT IndoLEM 88,0 dan 86,9. Pada tweet informal IndoBERT lebih tinggi, sehingga uji B-Indo vs B-Tweet menentukan sah tidaknya pilihan *encoder*. Membantah klaim "IndoBERTweet hanya teruji untuk klasifikasi" | [arXiv](https://arxiv.org/abs/2109.04607) |
| B | GLiNER (NAACL) | Zaratiana, Tomeh, Holat, Charnois | 2024 | Model generalis berbasis *span*, satu keluarga dengan EGP, yang dapat dijalankan *zero-shot* pada data tesis. Pembanding paradigma untuk pertanyaan penguji "mengapa tidak memakai model generalis" | [ACL Anthology](https://aclanthology.org/2024.naacl-long.300/) |
| C | An LLM-based Chain-of-Response Counter-Scam System (IJCAI) | Kim dkk. | 2026 | NER khusus penipuan berbasis LLM dengan skema BIO (datar). Membatasi klaim celah dan menunjukkan alasan LLM wajib dibahas. Pembeda tesis: entitas bertumpuk terbatas, bahasa Indonesia, dan keluhan yang ditulis pengguna | [IJCAI](https://ijcai.org/proceedings/2026/808) |
| D | NER Model of Telecommunication Network Fraud Crime based on ELECTRA-CRF (*Netinfo Security*) | Ding, Liu | 2021 | NER penipuan telekomunikasi berbahasa Tionghoa pada teks kasus resmi. Membantah klaim "belum ada NER penipuan dalam bahasa apa pun". Bedanya: teks laporan resmi, memakai CRF (datar) | [Netinfo](http://netinfo-security.org/EN/10.3969/j.issn.1671-1122.2021.06.008) |
| E | NusaBERT (SEALP) | Lazarus NLP | 2025 | Penerus IndoBERT dengan NERGrit 79,86 dan NERP 85,12 (tabel menyebut "macro-F1", penamaan metrik perlu dikonfirmasi). Kandidat *encoder* tambahan di Tahap 1 agar perbandingan *encoder* Indonesia lengkap | [ACL Anthology](https://aclanthology.org/2025.sealp-1.2.pdf) |

---

## 5. SOTA per Lapisan

Hanya hasil pada *dataset* dan metrik yang sama yang diperingkat. Bila nilai tertinggi tidak dapat diverifikasi dari sumber primer, ditulis "tertinggi yang ditemukan".

| Lapisan | Dataset acuan | Hasil tertinggi | Status |
|---|---|---|---|
| L1 NER Indonesia (tweet) | Munarko 2018, subset informal | IndoBERT + adaptasi kosakata *average of subwords* 87,4; IndoBERT IndoLEM 86,9; IndoBERTweet 85,4 (Koto dkk. 2021, Tabel 2, F1 entitas) | Tertinggi yang ditemukan; status Scopus EMNLP belum terverifikasi |
| L1 NER Indonesia (IndoNLU) | NERGrit / NERP | NusaBERT-large 79,86 / 85,12 | Tertinggi yang ditemukan; status Scopus SEALP belum terverifikasi |
| L1 NER Indonesia (hukum) | IndoLER | XLM-R 0,9295 | Dari abstrak primer IJECE; venue dihentikan Scopus mulai 2025 |
| L2 teks *noisy* | WNUT-17 | Tidak terverifikasi | Tidak ada angka WNUT-17 dari tabel primer yang berhasil dibaca |
| L3 *nested* | ACE2005 / GENIA | BGNER 87,21 / 82,05 (Tabel 5, JKSU-CIS 2025, Q1) | Tertinggi terverifikasi di venue Scopus yang diperiksa. Binder (ICLR 2023) melaporkan 90,0, tetapi status Scopus prosidingnya belum dicek. Angka lintas makalah pada ACE tidak boleh langsung diperingkat karena statistik data dan pra-pemrosesan berbeda |
| L4 generalis/LLM | NER bahasa Indonesia | Tidak ada | Tidak ditemukan evaluasi GLiNER atau LLM pada NER Indonesia di venue Scopus |
| L5 domain penipuan | Lapisan pemetaan | Tidak diperingkat | Lihat Tabel 1 nomor 14, dan Tabel 2 butir C dan D |

---

## 6. Dampak bagi Tesis

1. **Pilihan *encoder*.** IndoBERTweet tidak boleh dinyatakan terbaik secara apriori. Uji IndoBERT IndoNLU, IndoBERT IndoLEM, IndoBERTweet, NusaBERT, dan XLM-R dengan kepala yang sama.
2. **Pilihan dekoder.** EGP layak dipertahankan karena kompetitif pada *nested* NER Inggris (BGNER). Tambahkan satu kepala *span* modern selain GlobalPointer (W2NER atau CNN-NER) sebagai pembanding.
3. **Leksikon toleran.** Pencocokan *fuzzy* bukan ide baru (paten USPTO dan arah lanjutan GazSelfAttn dilaporkan penelusuran). Kebaruan hanya pada penerapannya sebagai adaptor antar-lapisan untuk ejaan platform Indonesia, dan baru boleh diklaim bila H5 terpenuhi pada data asli.
4. **Pembanding paradigma.** GLiNER multibahasa (*zero-shot* dan *fine-tuned*) dan satu LLM Indonesia atau Asia Tenggara (*few-shot*) wajib dijalankan pada data uji yang sama.
5. **Baseline normalisasi.** Tambahkan *baseline* normalisasi leksikal (kamus slang ke bentuk baku sebelum *encoder*) agar terbukti leksikon toleran lebih baik daripada normalisasi sederhana.
6. **Statistik.** Minimal 3 sampai 5 *seed*, rerata dan simpangan baku, uji berpasangan (*paired bootstrap*). Jangan melaporkan *run* terbaik saja.
7. **Laporan subset.** F1 terpisah untuk entitas bertumpuk vs tidak bertumpuk, dan untuk NOMINAL tidak baku.

---

## Lampiran A. Protokol Pencarian

- **Tanggal pencarian**: 11 November 2026.
- **Sumber yang benar-benar diakses**: mesin pencari web umum yang mengembalikan rekaman dari ACL Anthology, SpringerLink, ScienceDirect, Nature/*Scientific Reports*, PLOS, PMC, IEEE Xplore (cuplikan), situs ETASR, dan arXiv (hanya sebagai penunjuk). **Scopus tidak diakses langsung.** Google Scholar, ACM DL, dan IEEE Xplore tidak dicari langsung. Status venue dicek lewat SCImago.
- **Kueri** (18 kueri, tiap kueri mengembalikan sekitar 8 sampai 10 rekaman):
  - Rujukan: "MGBERT-Pointer nested named entity recognition Complex & Intelligent Systems 2024"
  - L1: "Indonesian named entity recognition social media tweets 2024 IndoBERTweet F1"; "NusaBERT NERGrit NERP F1 results"; "Indonesian nested named entity recognition dataset"
  - L2: "WNUT-17 state of the art F1 2024 named entity recognition noisy user-generated text"; "fuzzy gazetteer noisy lexicon named entity recognition transformer 2024"
  - L3: "nested NER ACE2005 GENIA new state of the art 2024 span-based F1"; "UHIF BFSN2ER CEAF TCSF named entity recognition"; "Efficient GlobalPointer English nested NER social media non-Chinese"
  - L4: "GLiNER Indonesian named entity recognition ETASR 2026"; "GLiNER-ID Indonesian Engineering Technology Applied Science Research"; "large language models Indonesian NER evaluation zero-shot few-shot SEA-LION"
  - L5: "named entity recognition online fraud complaints Indonesian dataset"; "named entity recognition scam fraud reports dataset entity extraction 2024"; "telecom fraud named entity recognition Chinese case texts BERT"
- **Kriteria inklusi**: tugas NER atau ekstraksi entitas; evaluasi kuantitatif F1 pada *dataset* bernama; terbit di venue Scopus; prioritas 2023 sampai 2026, dan 2017 sampai 2022 sebagai fondasi.
- **Kriteria eksklusi**: hanya klasifikasi atau analisis sentimen; tanpa evaluasi kuantitatif; duplikat; teks tidak terbaca; *preprint* tanpa venue Scopus.
- **Alur ringan**: sekitar 160 rekaman disaring pada tingkat judul dan cuplikan (hitungan persis tidak dicatat, angka ini perkiraan), sekitar 45 relevan secara topik, dan 15 masuk Tabel 1 setelah eksklusi duplikat, klasifikasi murni, dan non-Scopus.

## Lampiran B. Karya yang Dikeluarkan

| Karya | Alasan |
|---|---|
| Global Pointer (Su dkk., arXiv 2208.03054) | *Preprint* non-Scopus; tetap wajib dirujuk sebagai sumber metode EGP |
| NER kripto IndoBERTweet-CRF (repositori GitHub) | Teks primer dan status Scopus tidak terverifikasi; dua repositori melaporkan F1 berbeda (70,76% dan 85,41%) |
| GLiNER2.5-indonesian, NusaBert-ner-v1.3, indobert-ner-gold (Hugging Face) | Model tanpa publikasi; angka dilaporkan sendiri |
| KnowCTI, LB-BMBC, Liu & Cui 2023, model penyakit ayam, DMGP, Kusuma & Chowanda 2023, TWBiL, Sedik & Romadhony 2023 | Dikeluarkan dari tabel utama karena lapisan tidak sebanding, ada angka yang tidak terverifikasi atau tidak konsisten, atau tugasnya klasifikasi. Dapat tetap dikutip sebagai konteks dengan catatan |
| UHIF, BFSN2ER | Venue Scopus tidak terverifikasi |
| TCSF | Tidak ditemukan |
| Klasifikasi spam, judi, dan sentimen berbasis IndoBERT (jurnal nasional) | Klasifikasi, bukan NER |

## Lampiran C. Hal yang Belum Terverifikasi

- Status Scopus prosiding EMNLP, NAACL, ICLR, IJCAI, dan SEALP; status Scopus *Netinfo Security*.
- Angka F1 MGBERT-Pointer langsung dari tabel primernya; angka WNUT-17 apa pun dari tabel primer.
- Angka absolut SEMFF-NER, Bi-DCAN, dan Han dkk. 2024.
- Nama penulis Bi-DCAN dan artikel Procedia 2019; keberadaan "Dzidny 2022" dan GLiNER-ID di ETASR 2026.
- Kuartil SJR 2026 (belum dirilis; terbitan 2026 memakai kuartil 2025).
- Anomali angka: CEAF (tabel perbandingan vs tabel ablasi tidak cocok); NusaBERT (penamaan "macro-F1" pada NER); ACE2005 (BGNER 87,21 mengklaim SOTA, Binder melaporkan 90,0).

Ketiadaan bukti dalam 18 kueri bukan bukti ketiadaan. Celah (a) dan (c) harus ditulis dengan frasa "sejauh penelusuran pada 11 November 2026". Penelusuran Scopus langsung lewat akses institusi Universitas Hasanuddin sangat disarankan untuk menutup lapisan L2 dan L4 sebelum angka dikutip dalam naskah.
