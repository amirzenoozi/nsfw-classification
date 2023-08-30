# NSFW Classification ⛔

![](https://github.com/amirzenoozi/nsfw-classification/blob/main/main.png)

Fork of the https://github.com/amirzenoozi/nsfw-classification
I used aiogram to create telegram bot that uses model from original repo.

## Prequisites
To run bot you need CPU that supports AVX or AVX2 to run last versions of Tensorflow
Otherwise you'll see output like this in your console:
```bash
Illegal instruction (core dumped)
```
### Requirements 📦

```bash
pip install -r requirements.txt
```

## How To Serve Telegram Bot 🤖

Firstly, you need to get `API_TOKEN` from `Bot_Father` and put it in `.env` file .Then you just need to run: 
```bash
python main.py
```

## TODO
 * Run bot as service in systemd
