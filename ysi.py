import re
import yfinance as yf
import pandas as pd
import streamlit as st
from urllib.parse import urlparse
from yfinance.exceptions import YFRateLimitError

def extract_ticker_from_url(url: str) -> str:
    path = urlparse(url).path
    match = re.search(r"/quote/([^/]+)/history", path)
    if not match:
        st.error("URL tidak valid. Pastikan formatnya seperti berikut : https://finance.yahoo.com/quote/TSLA/history")
        st.stop()
    return match.group(1).upper()

@st.cache_data(ttl=3600) 
def fetch_and_clean_history(ticker: str) -> pd.DataFrame:
    try:
        df = yf.Ticker(ticker).history(period="max", interval="1d")
    except YFRateLimitError:
        st.error("❌ Anda telah mencapai batas akses Yahoo Finance. Harap tunggu beberapa menit dan silahkan coba lagi.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Gagal Mengambil Data : {e}")
        st.stop()

    if "Adj Close" not in df.columns:
        df["Adj Close"] = df["Close"]
    if "Open" not in df.columns:
        df["Open"] = pd.NA
    df = df[pd.to_numeric(df["Volume"], errors="coerce").notnull()]
    df.reset_index(inplace=True)
    if pd.api.types.is_datetime64_any_dtype(df["Date"]):
        df["Date"] = pd.to_datetime(df["Date"]).dt.tz_localize(None)
    df = df[["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]]
    return df

def convert_df_to_excel(df, ticker):
    from io import BytesIO
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter", date_format="yyyy-mm-dd", datetime_format="yyyy-mm-dd") as writer:
        df.to_excel(writer, index=False, sheet_name="Data")
        workbook = writer.book
        worksheet = writer.sheets["Data"]
        date_fmt = workbook.add_format({"num_format": "yyyy-mm-dd"})
        worksheet.set_column("A:A", 12, date_fmt)
        num_fmt = workbook.add_format({"num_format": "#,##0.00"})
        worksheet.set_column("B:F", 12, num_fmt)
        vol_fmt = workbook.add_format({"num_format": "#,##0"})
        worksheet.set_column("G:G", 15, vol_fmt)
    output.seek(0)
    return output

st.set_page_config(page_title="Yahoo Finance Historical Data - YSI")
st.title("📈 Yahoo Finance Historical Data Downloader")
st.markdown(
    """
    ### ⚠️ Catatan Penting
    - Pastikan URL yang Anda masukkan mengikuti format yang benar. Contoh URL yang valid adalah:
    `https://finance.yahoo.com/quote/TSLA/history/` 
    - Hanya URL yang sesuai dengan format yang benar yang dapat diproses oleh alat ini.
    - Data yang diunduh berisi informasi historical data yang dapat digunakan untuk analisis lebih lanjut.
    - Alat ini sepenuhnya gratis digunakan dan tidak memerlukan langganan atau akun premium di Yahoo Finance.
    - Jika Anda mengakses terlalu sering dalam waktu singkat, data mungkin akan gagal diambil (rate limit).
    """
)

url = st.text_input("Masukkan Link/URL dan Tekan Tombol 'Enter' Untuk Memulai", placeholder="https://finance.yahoo.com/quote/TSLA/history/", on_change=None, key=None, type="default", help="Masukkan Link/URL dibawah ini lalu tekan 'Enter' untuk memulai")

if url:
    ticker = extract_ticker_from_url(url)
    st.success(f"Berhasil Mendeteksi Kode Perusahaan/Saham : {ticker}")
    df = fetch_and_clean_history(ticker)

    st.markdown("🗂️ **Tabel Dibawah Ini Menampilkan 5 Baris Terakhir Dari Historical Data Yang Berhasil Diambil Dari Yahoo Finance.** (urutan datanya adalah dari terlama hingga terbaru)")
    st.dataframe(df.head())

    st.write(f"📊 Jumlah Baris Data History (Max) : {len(df)}")

    csv = df.to_csv(index=False).encode("utf-8")
    xlsx = convert_df_to_excel(df, ticker)

    st.download_button("⬇️ Download CSV", csv, file_name=f"{ticker}_CleanedHistoricalData.csv", mime="text/csv")
    st.download_button("⬇️ Download Excel", xlsx, file_name=f"{ticker}_CleanedHistoricalData.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; font-size: 14px;'>
        © 2025 | Developed with ❤️ by AlDev - Muhammad Alif<br>
        Jika Menemukan Bug/Error atau Bahkan Ingin Memberikan Saran, Silahkan Hubungi Instagram Saya<br>
        <a href='https://www.instagram.com/mhdalif.id/' target='_blank'>https://www.instagram.com/mhdalif.id</a>
    </div>
    """,
    unsafe_allow_html=True
)
