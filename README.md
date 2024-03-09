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

## Pembuat Program
|        Name             |    NIM   | Kelas |
| --------------------    | -------- | ----- |
| Kayla Namira Mariadi    | 13522050 |   K2  |
| Andhita Naura Hariyanto | 13522060 |   K2  |
| Salsabiila              | 13522062 |   K2  |
