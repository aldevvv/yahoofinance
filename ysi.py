import re
import yfinance as yf
import pandas as pd
import time
from urllib.parse import urlparse
from yfinance.exceptions import YFRateLimitError
import streamlit as st

def extract_ticker_from_url(url: str) -> str:
    path = urlparse(url).path
    match = re.search(r"/quote/([^/]+)/history", path)
    if not match:
        st.error("URL tidak valid. Pastikan formatnya seperti berikut: https://finance.yahoo.com/quote/TSLA/history")
        st.stop()
    return match.group(1).upper()

@st.cache_data(ttl=86400)
def fetch_and_clean_history(ticker: str) -> pd.DataFrame:
    df = yf.Ticker(ticker).history(period="max", interval="1d")
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

def convert_df_to_excel(df: pd.DataFrame, ticker: str):
    from io import BytesIO
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter', date_format='yyyy-mm-dd', datetime_format='yyyy-mm-dd') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')
        workbook = writer.book
        worksheet = writer.sheets['Data']
        date_fmt = workbook.add_format({'num_format': 'yyyy-mm-dd'})
        worksheet.set_column('A:A', 12, date_fmt)
        num_fmt = workbook.add_format({'num_format': '#,##0.00'})
        worksheet.set_column('B:F', 12, num_fmt)
        vol_fmt = workbook.add_format({'num_format': '#,##0'})
        worksheet.set_column('G:G', 15, vol_fmt)
    output.seek(0)
    return output

st.set_page_config(page_title="Yahoo Finance Historical Data - YSI")
st.title("📈 Yahoo Finance Historical Data Downloader - Version 1.0")
st.markdown(
    """
    ### ⚠️ Catatan Penting
    - Pastikan URL Yang Anda Masukkan Mengikuti Format Yang Benar
      `Contoh : https://finance.yahoo.com/quote/TSLA/history/`
    - Hindari Melakukan Scraping Data Terlalu Sering Dalam Waktu Singkat Untuk Menghindari Limit ( Maklum Karena Deploy Secara Gratis :p )
    - Jalankan Program Ini Pada LocalHost Anda Jika Terjadi Limit - Silahkan Kunjungi ( https://github.com/aldevvv/yahoofinance )
    """
)

url = st.text_input(
    "Masukkan Link/URL dan tekan 'Enter' untuk memulai",
    placeholder="https://finance.yahoo.com/quote/TSLA/history/"
)

if url:
    reset_time = st.session_state.get('limit_reset', 0)
    remaining = reset_time - time.time()
    if remaining > 0:
        mins, secs = divmod(int(remaining), 60)
        st.warning(f"⚠️ Rate Limit Masih Aktif - {mins}m {secs}s")
        st.stop()

    ticker = extract_ticker_from_url(url)
    st.success(f"✅ Berhasil Mendeteksi Kode Perusahaan/Saham : {ticker}")
    try:
        with st.spinner("⏳ Sedang Menjalankan Program Untuk Mengambil Data..."):
            df = fetch_and_clean_history(ticker)
    except YFRateLimitError:
        if 'limit_reset' not in st.session_state:
            st.session_state['limit_reset'] = time.time() + 3600
        st.error("❌ Anda Telah Mencapai Batas Penggunaan Program Scraping Yahoo Finance Historical Data (Rate Limit)")
        remaining = st.session_state['limit_reset'] - time.time()
        mins, secs = divmod(int(remaining), 60)
        st.info(f"⏳ Silahkan Coba Lagi Dalam : {mins}m {secs}s")
        st.stop()
    except Exception as e:
        st.error(f"❌ Terjadi Kesalahan Saat Mengambil Data : {e}")
        st.stop()

    st.markdown("**🗂️ Preview 5 Baris Pertama Historical Data ( Oldest to Newest )**")
    st.dataframe(df.head())

    st.write(f"📊 Jumlah Data (Max) : {len(df)}")

    csv = df.to_csv(index=False).encode('utf-8')
    xlsx = convert_df_to_excel(df, ticker)

    st.download_button("⬇️ Download CSV", csv, file_name=f"{ticker}_CleanedHistoricalData.csv", mime='text/csv')
    st.download_button("⬇️ Download Excel", xlsx, file_name=f"{ticker}_CleanedHistoricalData.xlsx", mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; font-size: 14px;'>
        © 2025 | Developed with ❤️ by AlDev - Muhammad Alif<br>
        Jika menemukan bug atau ingin memberikan saran, hubungi saya dibawah<br>
        <a href='https://www.instagram.com/mhdalif.id/' target='_blank'>https://instagram.com/mhdalif.id</a>
    </div>
    """,
    unsafe_allow_html=True
)
