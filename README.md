# Tugas Besar 1 IF2211 Strategi Algoritma

## Deskripsi Program
Diamonds merupakan suatu programming challenge yang mempertandingkan bot-bot. Setiap pemain akan memiliki sebuah bot dimana tujuan dari bot ini yaitu mengumpulkan diamond sebanyak-banyaknya. Agar memenangkan pertandingan, setiap pemain harus mengimplementasikan strategi tertentu pada masing-masing bot-nya.

## Strategi Greedy
Strategi greedy yang kami terapkan adalah Greedy by Most Profitable Diamond with Defense and Attack, dengan alur seperti berikut :
1. Deteksi diamond, teleporter, base pada permainan
2. Pilih base sebagai target jika diamond pada inventory sudah 5, atau diamond pada inventory ada 4 namun diamond target adalah red, atau diamond pada inventory ada 4 namun bot berada di sekitar base
3. Jika tidak memenuhi kondisi pada nomor 3, pilih target berupa diamond dengan profit terbesar
4. Jika terdapat bot lawan pada radius 8 kotak sekitar bot dan lawan memiliki lebih sedikit diamond, tabrak bot lawan, jika tidak hindari bot tersebut.
   
## Struktur Program
```
.
└── src/
    ├── tubes1-IF2211-bot-starter-pack-1.0.1/
    │   ├── game/
    │   │   ├── logic/
    │   │   │   ├── _init_.py
    │   │   │   ├── attackProfit
    │   │   │   ├── base.py
    │   │   │   ├── defense.py
    │   │   │   ├── defenseProfit1.py
    │   │   │   ├── defenseProfit2.py
    │   │   │   ├── defenseProfit3.py
    │   │   │   ├── dpa.py
    │   │   │   ├── mostProfitable.py
    │   │   │   ├── nearestBase.py
    │   │   │   ├── nearestBaseDef.py
    │   │   │   └── random.py
    │   │   ├── _init_.py
    │   │   ├── api.py
    │   │   ├── board_handler.py
    │   │   ├── bot_handler.py
    │   │   ├── models.py
    │   │   └── util.py
    │   ├── decode.py
    │   ├── main.py
    │   ├── README.md
    │   ├── requirements.txt
    │   ├── run-bots.bat
    │   └── run-bots.sh
    └── tubes1-IF2211-game-engine-1.1.0
```

## Program Requirements
| No |    Requirement   |
| -- |  --------------- |
|  1 |     Node.js      |
|  2 |       Yarn       |
|  3 |  Docker desktop  |

## Menjalankan Program
1. Clone repository ini
   ```
   https://github.com/kaylanamira/Tubes1_Snoopy.git
   ```
2. Buka folder repository pada terminal
3. Pindah ke direktori _src_ dengan `cd src`
4. Pindah ke direktori _tubes1-IF2211-game-engine-1.1.0_ dengan `cd tubes1-IF2211-game-engine-1.1.0`
5. Install dependencies dengan `yarn`
6. Setup default environment variable dengan menjalankan script (untuk Windows)
   ```
   ./scripts/copy-env.bat`
   ```
   (untuk Linux/MacOS)
   ```
   chmod +x ./scripts/copy-env.sh
   ./scripts/copy-env.sh
   ```
7. Buka aplikasi docker desktop kemudian lakukan setup local database dengan `docker compose up -d database`
8. Jalankan perintah (untuk Windows)
   ```
   ./scripts/setup-db-prisma.bat
   ```
   (untuk Linux/MacOS)
   ```
   chmod +x ./scripts/setup-db-prisma.sh
   ./scripts/setup-db-prisma.sh
   ```
9. Jalankan perintah `npm run build` dan `npm run start` pada terminal
10. Klik link localhost yang diberikan di output command dan buka game etimo diamond di platform yang diinginkan
11. Pindah ke direktori _tubes1-IF2211-bot-starter-pack-1.0.1/_ dengan `cd ../tubes1-IF2211-bot-starter-pack-1.0.1/`
12. Install dependencies dengan perintah `pip install -r requirements.txt`
13. Jalankan perintah untuk menjalankan beberapa bot (untuk Windows)
   ```
   ./run-bots.bat
   ```
   (untuk Linux/MacOS)
   ```
   ./run-bots.sh
   ```

## Pembuat Program
|        Name             |    NIM   | Kelas |
| --------------------    | -------- | ----- |
| Kayla Namira Mariadi    | 13522050 |   K2  |
| Andhita Naura Hariyanto | 13522060 |   K2  |
| Salsabiila              | 13522062 |   K2  |
