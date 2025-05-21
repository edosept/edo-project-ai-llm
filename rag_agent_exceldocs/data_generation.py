import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Create output directory if it doesn't exist
output_dir = "umkm_data"
os.makedirs(output_dir, exist_ok=True)

# 1. Generate tbl_bisnis
def generate_bisnis():
    data = {
        'bisnis_id': [1, 2, 3],
        'nama_bisnis': ['Warung Kopi Gembira', 'Warung Sayur Buah Sehat', 'Warung Sembako Berkah'],
        'jenis_usaha': ['Kuliner', 'Retail', 'Retail'],
        'alamat': ['Jl. Raya Bogor No. 123, Tangerang', 'Jl. Batavia No. 95, Tangerang', 'Jl. Merdeka No. 45, Tangerang'],
        'no_telepon': ['08XXXXXXXX1', '08XXXXXXXX2', '08XXXXXXXX3'],
        'email': ['kopigembira@email.com', 'sayurbuahsehat@email.com', 'sembakoberkah@email.com']
    }
    df = pd.DataFrame(data)
    return df

# 2. Generate tbl_produk
def generate_produk():
    # Coffee shop products
    kopi_products = [
        [1, 1, 'KP001', 'Kopi Hitam', 2000, 5000, 80],
        [2, 1, 'KP002', 'Kopi Susu', 3000, 7000, 75],
        [3, 1, 'KP003', 'Es Kopi', 2500, 6000, 65],
        [4, 1, 'KP004', 'Es Kopi Susu', 3500, 8000, 60],
        [5, 1, 'KP005', 'Teh Manis', 1500, 4000, 90],
        [6, 1, 'KP006', 'Es Teh Manis', 1800, 5000, 85],
        [7, 1, 'KP007', 'Es Jeruk', 2500, 6000, 70],
        [8, 1, 'KP008', 'Milo', 3000, 7000, 50],
        [9, 1, 'KP009', 'Es Milo', 3500, 8000, 45],
        [10, 1, 'KP010', 'Roti Bakar Coklat', 3500, 8000, 40],
        [11, 1, 'KP011', 'Roti Bakar Keju', 4000, 10000, 35],
        [12, 1, 'KP012', 'Pisang Goreng (3 pcs)', 3000, 7000, 45],
        [13, 1, 'KP013', 'Nasi Goreng', 8000, 15000, 30],
        [14, 1, 'KP014', 'Mie Goreng', 7000, 13000, 35],
        [15, 1, 'KP015', 'Air Mineral', 2000, 3000, 100]
    ]
    
    # Produce shop products
    sayur_products = [
        [16, 2, 'SB001', 'Bayam (ikat)', 2000, 3500, 30],
        [17, 2, 'SB002', 'Kangkung (ikat)', 1500, 3000, 35],
        [18, 2, 'SB003', 'Sawi (ikat)', 2000, 3500, 25],
        [19, 2, 'SB004', 'Brokoli (250gr)', 5000, 7500, 20],
        [20, 2, 'SB005', 'Wortel (250gr)', 3000, 4500, 40],
        [21, 2, 'SB006', 'Kentang (250gr)', 3500, 5000, 45],
        [22, 2, 'SB007', 'Tomat (250gr)', 3000, 4500, 50],
        [23, 2, 'SB008', 'Cabai Merah (100gr)', 3500, 5500, 30],
        [24, 2, 'SB009', 'Cabai Rawit (100gr)', 4000, 6000, 25],
        [25, 2, 'SB010', 'Jeruk (kg)', 15000, 20000, 40],
        [26, 2, 'SB011', 'Apel (kg)', 20000, 25000, 30],
        [27, 2, 'SB012', 'Pisang (sisir)', 12000, 16000, 25],
        [28, 2, 'SB013', 'Semangka (kg)', 6000, 9000, 60],
        [29, 2, 'SB014', 'Pepaya (kg)', 6000, 9000, 40],
        [30, 2, 'SB015', 'Mangga Harum Manis (kg)', 18000, 23000, 35]
    ]
    
    # Grocery store products
    sembako_products = [
        [31, 3, 'SM001', 'Beras (kg)', 11000, 13000, 200],
        [32, 3, 'SM002', 'Gula Pasir (kg)', 13000, 15000, 150],
        [33, 3, 'SM003', 'Minyak Goreng (L)', 16000, 18000, 100],
        [34, 3, 'SM004', 'Telur (kg)', 23000, 26000, 80],
        [35, 3, 'SM005', 'Tepung Terigu (kg)', 10000, 12000, 75],
        [36, 3, 'SM006', 'Kecap Manis ABC (botol)', 9000, 12000, 45],
        [37, 3, 'SM007', 'Saus Sambal ABC (botol)', 8000, 11000, 40],
        [38, 3, 'SM008', 'Indomie Goreng (pcs)', 2500, 3500, 200],
        [39, 3, 'SM009', 'Indomie Kuah (pcs)', 2300, 3300, 180],
        [40, 3, 'SM010', 'Sabun Mandi Lifebuoy (pcs)', 3000, 4500, 50],
        [41, 3, 'SM011', 'Shampo Sunsilk Sachet (pcs)', 1000, 1500, 100],
        [42, 3, 'SM012', 'Deterjen Rinso (sachet)', 2000, 3000, 80],
        [43, 3, 'SM013', 'Gas LPG 3kg', 18000, 20000, 25],
        [44, 3, 'SM014', 'Mie Sedaap (pcs)', 2400, 3400, 150],
        [45, 3, 'SM015', 'Bihun (pcs)', 6000, 8000, 60]
    ]
    
    all_products = kopi_products + sayur_products + sembako_products
    columns = ['produk_id', 'bisnis_id', 'kode_produk', 'nama_produk', 'harga_beli', 'harga_jual', 'stok_saat_ini']
    df = pd.DataFrame(all_products, columns=columns)
    
    return df

# 3 & 4. Generate tbl_penjualan and tbl_detail_penjualan
def generate_sales_data(start_date, end_date):
    # Generate date range
    dates = pd.date_range(start=start_date, end=end_date)
    
    # Initialize dataframes
    penjualan_columns = ['penjualan_id', 'bisnis_id', 'nomor_transaksi', 'tanggal_transaksi', 'total', 'metode_pembayaran', 'status_pembayaran']
    detail_columns = ['detail_id', 'penjualan_id', 'produk_id', 'kuantitas', 'harga_satuan', 'diskon_item', 'deskripsi_diskon', 'subtotal']
    
    penjualan_data = []
    detail_data = []
    
    penjualan_id = 1001
    detail_id = 2001
    
    # Get product information
    products_df = generate_produk()
    products = {row['produk_id']: {
        'bisnis_id': row['bisnis_id'],
        'harga_jual': row['harga_jual']
    } for _, row in products_df.iterrows()}
    
    # Group products by business
    products_by_business = {
        1: [pid for pid, p in products.items() if p['bisnis_id'] == 1],
        2: [pid for pid, p in products.items() if p['bisnis_id'] == 2],
        3: [pid for pid, p in products.items() if p['bisnis_id'] == 3]
    }
    
    # Define promotional periods
    promo_days = {
        1: ["Senin", "Jumat"],          # Warung Kopi: promos on Mondays and Fridays
        2: ["Selasa", "Sabtu"],         # Warung Sayur: promos on Tuesdays and Saturdays
        3: ["Rabu", "Minggu"]           # Warung Sembako: promos on Wednesdays and Sundays
    }
    
    # Define business hours patterns
    business_hours = {
        1: [(7, 22)],                   # Warung Kopi: 7 AM - 10 PM
        2: [(6, 18)],                   # Warung Sayur: 6 AM - 6 PM
        3: [(7, 21)]                    # Warung Sembako: 7 AM - 9 PM
    }
    
    # Seasonal patterns by month
    month_factors = {
        2: {'hot_drinks': 0.9, 'cold_drinks': 1.1, 'vegetables': 1.0, 'fruits': 1.1, 'groceries': 1.0},
        3: {'hot_drinks': 0.8, 'cold_drinks': 1.2, 'vegetables': 1.1, 'fruits': 1.2, 'groceries': 1.0},
        4: {'hot_drinks': 0.7, 'cold_drinks': 1.3, 'vegetables': 1.2, 'fruits': 1.3, 'groceries': 1.1}
    }
    
    # Define product categories
    product_categories = {
        'hot_drinks': [1, 2, 5, 8],              # Hot beverages
        'cold_drinks': [3, 4, 6, 7, 9],          # Cold beverages
        'vegetables': list(range(16, 25)),       # Vegetables
        'fruits': list(range(25, 31)),           # Fruits
        'groceries': list(range(31, 46))         # Grocery items
    }
    
    # Iterate through each date
    for date in dates:
        day_name = date.day_name()
        day_of_week = date.weekday()  # 0 is Monday, 6 is Sunday
        month = date.month
        
        # Weekend factor (more sales on weekends)
        weekend_factor = 1.2 if day_of_week >= 5 else 1.0
        
        # Generate transactions for each business
        for bisnis_id in range(1, 4):
            # Determine number of transactions based on day of week and business
            base_transactions = 10
            if bisnis_id == 1:  # Coffee shop: busier on weekends
                num_transactions = int(base_transactions * weekend_factor * random.uniform(0.9, 1.1))
            elif bisnis_id == 2:  # Produce shop: busier on weekends and early week
                market_day_factor = 1.2 if day_of_week in [0, 5] else 1.0  # Monday and Saturday are market days
                num_transactions = int(base_transactions * weekend_factor * market_day_factor * random.uniform(0.9, 1.1))
            else:  # Grocery store: consistent with slight weekend increase
                num_transactions = int(base_transactions * (weekend_factor * 0.8) * random.uniform(0.9, 1.1))
            
            # Spread transactions throughout business hours
            open_hour, close_hour = business_hours[bisnis_id][0]
            
            for tx_num in range(1, num_transactions + 1):
                # Generate transaction time with realistic patterns
                if bisnis_id == 1:  # Coffee shop: peak in morning and evening
                    if random.random() < 0.4:
                        hour = random.randint(open_hour, open_hour + 3)  # Morning peak
                    elif random.random() < 0.7:
                        hour = random.randint(close_hour - 4, close_hour - 1)  # Evening peak
                    else:
                        hour = random.randint(open_hour + 4, close_hour - 5)  # Afternoon
                elif bisnis_id == 2:  # Produce shop: peak in early morning
                    if random.random() < 0.6:
                        hour = random.randint(open_hour, open_hour + 4)  # Morning peak
                    else:
                        hour = random.randint(open_hour + 5, close_hour - 1)  # Rest of day
                else:  # Grocery store: spread throughout day with slight evening peak
                    if random.random() < 0.3:
                        hour = random.randint(close_hour - 4, close_hour - 1)  # Evening peak
                    else:
                        hour = random.randint(open_hour, close_hour - 5)  # Rest of day
                
                minute = random.randint(0, 59)
                tx_time = date.replace(hour=hour, minute=minute)
                
                # Transaction format
                tx_date_str = tx_time.strftime('%Y%m%d')
                tx_number = f"INV-{tx_date_str}-{tx_num:04d}"
                
                # Payment method - Tunai (60%), QRIS (40%)
                payment_method = "Tunai" if random.random() < 0.6 else "QRIS"
                
                # All transactions are paid (Lunas)
                payment_status = "Lunas"
                
                # Determine if this is a promo day
                is_promo_day = day_name in promo_days[bisnis_id]
                
                # Generate items for this transaction
                available_products = products_by_business[bisnis_id]
                
                # Determine number of items based on business type
                if bisnis_id == 1:  # Coffee shop: 1-3 items
                    num_items = random.choices([1, 2, 3], weights=[0.3, 0.5, 0.2])[0]
                elif bisnis_id == 2:  # Produce shop: 2-4 items
                    num_items = random.choices([1, 2, 3, 4], weights=[0.1, 0.4, 0.3, 0.2])[0]
                else:  # Grocery store: 2-5 items
                    num_items = random.choices([1, 2, 3, 4, 5], weights=[0.1, 0.2, 0.4, 0.2, 0.1])[0]
                
                # Select products considering seasonal and time-based patterns
                selected_products = []
                
                # Apply seasonal factors based on product categories
                for _ in range(num_items):
                    if bisnis_id == 1:  # Coffee shop
                        if hour < 12:  # Morning: higher chance of hot drinks
                            category = random.choices(['hot_drinks', 'cold_drinks'], 
                                                    weights=[0.7, 0.3])[0]
                        else:  # Afternoon/evening: higher chance of cold drinks
                            category = random.choices(['hot_drinks', 'cold_drinks'], 
                                                    weights=[0.3, 0.7])[0]
                            
                        # Apply monthly seasonal factors
                        category_factor = month_factors[month][category]
                        
                        # Filter products by category and select
                        category_products = [p for p in available_products if p in product_categories[category]]
                        if not category_products:  # Fallback if no products match
                            product_id = random.choice(available_products)
                        else:
                            product_id = random.choice(category_products)
                            
                    elif bisnis_id == 2:  # Produce shop
                        # Balance vegetables and fruits based on month
                        veg_weight = 0.6 * month_factors[month]['vegetables']
                        fruit_weight = 0.4 * month_factors[month]['fruits']
                        
                        category = random.choices(['vegetables', 'fruits'], 
                                               weights=[veg_weight, fruit_weight])[0]
                        
                        # Filter products by category and select
                        category_products = [p for p in available_products if p in product_categories[category]]
                        if not category_products:
                            product_id = random.choice(available_products)
                        else:
                            product_id = random.choice(category_products)
                            
                    else:  # Grocery store - more random selection
                        product_id = random.choice(available_products)
                    
                    # Avoid duplicate products in the same transaction
                    if product_id not in selected_products:
                        selected_products.append(product_id)
                
                # Ensure we have at least one product
                if not selected_products:
                    selected_products = [random.choice(available_products)]
                
                # Calculate transaction total and add details
                tx_total = 0
                tx_details = []
                
                for i, product_id in enumerate(selected_products):
                    harga_satuan = products[product_id]['harga_jual']
                    
                    # Handle weighted products (fruits & vegetables)
                    if product_id in range(25, 31):  # Fruits sold by kg
                        kuantitas = round(random.uniform(0.5, 2.5), 1)  # 0.5kg to 2.5kg
                    elif product_id in range(16, 25):  # Vegetables
                        if product_id in [16, 17, 18]:  # Items sold by ikat
                            kuantitas = random.randint(1, 3)
                        else:  # Items sold by weight
                            kuantitas = random.randint(1, 3)  # 1-3 packs of 250g/100g
                    elif bisnis_id == 3 and product_id in [31, 32, 33, 34, 35]:  # Staples like rice, sugar, oil
                        kuantitas = random.randint(1, 3)  # 1-3 kg/liters
                    else:  # Regular items
                        kuantitas = random.randint(1, 3)
                    
                    # Apply discounts (more likely on promo days)
                    if is_promo_day and random.random() < 0.3:
                        diskon_item = int(harga_satuan * random.uniform(0.1, 0.4))  # 10-40% discount
                        
                        # Discount descriptions
                        if hour < 10:
                            deskripsi_diskon = "Promo Pagi"
                        elif hour < 15:
                            deskripsi_diskon = "Promo Siang"
                        else:
                            deskripsi_diskon = "Promo Sore"
                    else:
                        diskon_item = 0
                        deskripsi_diskon = ""
                    
                    subtotal = (kuantitas * harga_satuan) - diskon_item
                    
                    # Ensure minimum price
                    if subtotal < 1000:
                        subtotal = 1000
                        diskon_item = (kuantitas * harga_satuan) - subtotal
                    
                    tx_total += subtotal
                    
                    tx_details.append({
                        'detail_id': detail_id,
                        'penjualan_id': penjualan_id,
                        'produk_id': product_id,
                        'kuantitas': kuantitas,
                        'harga_satuan': harga_satuan,
                        'diskon_item': diskon_item,
                        'deskripsi_diskon': deskripsi_diskon,
                        'subtotal': subtotal
                    })
                    
                    detail_id += 1
                
                # Add transaction record
                penjualan_data.append({
                    'penjualan_id': penjualan_id,
                    'bisnis_id': bisnis_id,
                    'nomor_transaksi': tx_number,
                    'tanggal_transaksi': tx_time,
                    'total': tx_total,
                    'metode_pembayaran': payment_method,
                    'status_pembayaran': payment_status
                })
                
                # Add details
                detail_data.extend(tx_details)
                
                penjualan_id += 1
    
    # Create DataFrames
    penjualan_df = pd.DataFrame(penjualan_data, columns=penjualan_columns)
    detail_df = pd.DataFrame(detail_data, columns=detail_columns)
    
    return penjualan_df, detail_df

# 5. Generate tbl_pengeluaran
def generate_expenses(start_date, end_date):
    expenses_columns = ['pengeluaran_id', 'bisnis_id', 'tanggal_pengeluaran', 'kategori', 'jumlah', 'deskripsi', 'metode_pembayaran']
    expenses_data = []
    pengeluaran_id = 501
    
    # Define expense categories and frequencies
    expense_categories = {
        1: {  # Warung Kopi
            'Bahan Baku': {'freq': 'weekly', 'min': 250000, 'max': 400000, 'desc': 'Belanja kopi dan bahan'},
            'Utilitas': {'freq': 'monthly', 'min': 120000, 'max': 180000, 'desc': 'Bayar listrik'},
            'Sewa': {'freq': 'monthly', 'min': 500000, 'max': 500000, 'desc': 'Sewa tempat'},
            'Gaji': {'freq': 'monthly', 'min': 800000, 'max': 800000, 'desc': 'Gaji karyawan'},
            'Peralatan': {'freq': 'occasional', 'min': 100000, 'max': 300000, 'desc': 'Peralatan kafe'}
        },
        2: {  # Warung Sayur
            'Bahan Baku': {'freq': '3-days', 'min': 400000, 'max': 700000, 'desc': 'Belanja sayur dan buah'},
            'Utilitas': {'freq': 'monthly', 'min': 100000, 'max': 150000, 'desc': 'Bayar listrik'},
            'Sewa': {'freq': 'monthly', 'min': 600000, 'max': 600000, 'desc': 'Sewa tempat'},
            'Gaji': {'freq': 'monthly', 'min': 750000, 'max': 750000, 'desc': 'Gaji karyawan'},
            'Peralatan': {'freq': 'occasional', 'min': 150000, 'max': 350000, 'desc': 'Peralatan display'}
        },
        3: {  # Warung Sembako
            'Bahan Baku': {'freq': 'weekly', 'min': 800000, 'max': 1500000, 'desc': 'Restock sembako'},
            'Utilitas': {'freq': 'monthly', 'min': 150000, 'max': 200000, 'desc': 'Bayar listrik'},
            'Sewa': {'freq': 'monthly', 'min': 700000, 'max': 700000, 'desc': 'Sewa tempat'},
            'Gaji': {'freq': 'monthly', 'min': 900000, 'max': 900000, 'desc': 'Gaji karyawan'},
            'Peralatan': {'freq': 'occasional', 'min': 200000, 'max': 500000, 'desc': 'Peralatan toko'}
        }
    }
    
    # Generate dates for each expense type
    current_date = start_date
    
    # Weekly expenses (every Monday)
    weekly_dates = pd.date_range(start=start_date, end=end_date, freq='W-MON')
    
    # 3-day expenses (every 3 days for fresh produce)
    three_day_dates = pd.date_range(start=start_date, end=end_date, freq='3D')
    
    # Monthly expenses (1st of each month)
    monthly_dates = pd.date_range(start=start_date.replace(day=1), end=end_date, freq='MS')
    
    # Occasional expenses (random dates)
    occasional_count = {
        1: 2,  # 2 occasional expenses for business 1
        2: 3,  # 3 occasional expenses for business 2
        3: 2   # 2 occasional expenses for business 3
    }
    
    # Generate all expenses
    for bisnis_id in range(1, 4):
        for category, details in expense_categories[bisnis_id].items():
            freq = details['freq']
            min_amount = details['min']
            max_amount = details['max']
            desc_template = details['desc']
            
            if freq == 'weekly':
                expense_dates = weekly_dates
            elif freq == '3-days':
                expense_dates = three_day_dates
            elif freq == 'monthly':
                expense_dates = monthly_dates
            elif freq == 'occasional':
                # Generate random dates for occasional expenses
                num_expenses = occasional_count[bisnis_id]
                all_days = pd.date_range(start=start_date, end=end_date, freq='D')
                expense_dates = sorted(np.random.choice(all_days, size=num_expenses, replace=False))
            
            for date in expense_dates:
                # Convert the date to Timestamp first to ensure compatibility
                date_ts = pd.Timestamp(date)
                
                # Check if the date is within our range
                if start_date <= date_ts.to_pydatetime() <= end_date:
                    # Monthly variation factor - using Timestamp to access month attribute
                    month_factor = 1.0 + ((date_ts.month - start_date.month) * 0.02)
                    
                    # Calculate amount with some randomness
                    amount = int(random.uniform(min_amount, max_amount) * month_factor)
                    
                    # Payment method - most recurring expenses by bank transfer, occasional by cash
                    if category in ['Utilitas', 'Sewa', 'Gaji'] or (category == 'Bahan Baku' and bisnis_id == 3):
                        payment_method = "Transfer Bank"
                    else:
                        payment_method = "Tunai"
                    
                    # Add slightly more detailed description
                    if category == 'Bahan Baku':
                        if bisnis_id == 1:
                            desc_variations = [
                                "Belanja kopi dan susu", 
                                "Restock gula dan bahan", 
                                "Belanja bahan minuman", 
                                "Restock kopi dan teh"
                            ]
                        elif bisnis_id == 2:
                            desc_variations = [
                                "Belanja sayur dan buah", 
                                "Restock buah-buahan", 
                                "Belanja sayuran", 
                                "Restock stok harian"
                            ]
                        else:
                            desc_variations = [
                                "Restock sembako", 
                                "Belanja mie dan kebutuhan pokok", 
                                "Restock beras dan minyak", 
                                "Belanja telur dan sembako"
                            ]
                        description = random.choice(desc_variations)
                    else:
                        description = desc_template
                    
                    expenses_data.append({
                        'pengeluaran_id': pengeluaran_id,
                        'bisnis_id': bisnis_id,
                        'tanggal_pengeluaran': date_ts.date(),  # Use Timestamp's date method
                        'kategori': category,
                        'jumlah': amount,
                        'deskripsi': description,
                        'metode_pembayaran': payment_method
                    })
                    
                    pengeluaran_id += 1
    
    # Sort by date
    expenses_df = pd.DataFrame(expenses_data, columns=expenses_columns)
    expenses_df = expenses_df.sort_values(by=['tanggal_pengeluaran', 'bisnis_id'])
    
    return expenses_df

# 6. Generate tbl_kas_harian
def generate_daily_cash(start_date, end_date, penjualan_df, pengeluaran_df):
    kas_columns = ['kas_id', 'bisnis_id', 'tanggal', 'saldo_awal', 'total_penjualan', 'total_pengeluaran', 'saldo_akhir']
    kas_data = []
    kas_id = 101
    
    # Initial balance for each business
    initial_balance = {
        1: 4500000,  # Warung Kopi
        2: 3800000,  # Warung Sayur
        3: 6200000   # Warung Sembako
    }
    
    # Current balance (will be updated for each day)
    current_balance = initial_balance.copy()
    
    # Generate daily cash records
    dates = pd.date_range(start=start_date, end=end_date)
    
    for date in dates:
        date_str = date.strftime('%Y-%m-%d')
        
        for bisnis_id in range(1, 4):
            # Get sales for this day and business
            day_sales = penjualan_df[(penjualan_df['bisnis_id'] == bisnis_id) & 
                                   (penjualan_df['tanggal_transaksi'].dt.date == date.date())]

            # Get expenses for this day and business
            day_expenses = pengeluaran_df[(pengeluaran_df['bisnis_id'] == bisnis_id) & 
                                       (pengeluaran_df['tanggal_pengeluaran'] == date.date())]
            
            # Calculate total sales and expenses
            total_sales = day_sales['total'].sum() if not day_sales.empty else 0
            total_expenses = day_expenses['jumlah'].sum() if not day_expenses.empty else 0
            
            # Calculate ending balance
            saldo_awal = current_balance[bisnis_id]
            saldo_akhir = saldo_awal + total_sales - total_expenses
            
            # Update current balance for the next day
            current_balance[bisnis_id] = saldo_akhir
            
            # Add daily cash record
            kas_data.append({
                'kas_id': kas_id,
                'bisnis_id': bisnis_id,
                'tanggal': date.date(),
                'saldo_awal': saldo_awal,
                'total_penjualan': total_sales,
                'total_pengeluaran': total_expenses,
                'saldo_akhir': saldo_akhir
            })
            
            kas_id += 1
    
    # Create DataFrame
    kas_df = pd.DataFrame(kas_data, columns=kas_columns)
    
    return kas_df

# Main function to generate all data
def generate_all_data():
    # Set date range for 3 months
    start_date = datetime(2025, 2, 1)
    end_date = datetime(2025, 4, 30)
    
    print("Generating business data...")
    bisnis_df = generate_bisnis()
    
    print("Generating product data...")
    produk_df = generate_produk()
    
    print("Generating sales data...")
    penjualan_df, detail_penjualan_df = generate_sales_data(start_date, end_date)
    
    print("Generating expense data...")
    pengeluaran_df = generate_expenses(start_date, end_date)
    
    print("Generating daily cash records...")
    kas_df = generate_daily_cash(start_date, end_date, penjualan_df, pengeluaran_df)
    
    # Save all data to Excel files
    print("Saving data to Excel files...")
    
    bisnis_df.to_excel(f"{output_dir}/tbl_bisnis.xlsx", index=False)
    produk_df.to_excel(f"{output_dir}/tbl_produk.xlsx", index=False)
    penjualan_df.to_excel(f"{output_dir}/tbl_penjualan.xlsx", index=False)
    detail_penjualan_df.to_excel(f"{output_dir}/tbl_detail_penjualan.xlsx", index=False)
    pengeluaran_df.to_excel(f"{output_dir}/tbl_pengeluaran.xlsx", index=False)
    kas_df.to_excel(f"{output_dir}/tbl_kas_harian.xlsx", index=False)
    
    print(f"Data generation complete! Files saved to '{output_dir}' directory.")
    
    # Print some statistics
    print("\nData Statistics:")
    print(f"Number of businesses: {len(bisnis_df)}")
    print(f"Number of products: {len(produk_df)}")
    print(f"Number of sales transactions: {len(penjualan_df)}")
    print(f"Number of sales line items: {len(detail_penjualan_df)}")
    print(f"Number of expenses: {len(pengeluaran_df)}")
    print(f"Number of daily cash records: {len(kas_df)}")
    
    return {
        'bisnis': bisnis_df,
        'produk': produk_df,
        'penjualan': penjualan_df,
        'detail_penjualan': detail_penjualan_df,
        'pengeluaran': pengeluaran_df,
        'kas_harian': kas_df
    }

# Run the data generation
if __name__ == "__main__":
    generate_all_data()