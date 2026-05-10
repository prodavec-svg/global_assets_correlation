import yfinance as yf
import pandas as pd
import os
from pathlib import Path

# Определяем набор активов
TICKERS = {
    'NG=F': 'Natural_Gas',
    'CL=F': 'Crude_Oil',
    'GC=F': 'Gold',
    '^GSPC': 'SP500',
    'BTC-USD': 'Bitcoin',
    'ETH-USD': 'Ethereum'
}
# Для абсолютного пути
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = str(PROJECT_ROOT / "data")


def download_and_save_parquet():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    print("Начинаем загрузку данных...")

    for symbol, name in TICKERS.items():
        print(f"Скачиваем {name} ({symbol})...")

        # Скачиваем часовые бары за последние 700 дней (ограничение yfinance для 1h)
        ticker = yf.Ticker(symbol)
        df = ticker.history(interval="1h", period="700d")

        if df.empty:
            print(f"Предупреждение: Нет данных для {name}")
            continue

        # Сбрасываем индекс, чтобы время стало обычной колонкой
        df = df.reset_index()

        # Оставляем только нужные колонки
        df = df[['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']]

        # Добавляем колонку с именем тикера
        df['Ticker'] = name

        # Сохраняем в Parquet
        # Формируем путь: data/ticker=Natural_Gas/data.parquet
        ticker_dir = os.path.join(DATA_DIR, f"ticker={name}")
        os.makedirs(ticker_dir, exist_ok=True)

        file_path = os.path.join(ticker_dir, "data.parquet")

        # engine='pyarrow' обеспечивает лучшую совместимость со Spark
        df.to_parquet(file_path, engine='pyarrow', index=False)
        print(f"Сохранено: {file_path}")


if __name__ == "__main__":
    download_and_save_parquet()