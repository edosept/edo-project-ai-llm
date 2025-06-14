import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Create output directory if it doesn't exist
os.makedirs("data", exist_ok=True)

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

# 2. Generate tbl_produk with realistic Indonesian pricing
def generate_produk():
    # Coffee shop products - realistic Indonesian pricing
    kopi_products = [
        [1, 1, 'KP001', 'Kopi Hitam', 3000, 8000, 30],
        [2, 1, 'KP002', 'Kopi Susu', 4000, 10000, 25],
        [3, 1, 'KP003', 'Es Kopi', 3500, 9000, 25],
        [4, 1, 'KP004', 'Es Kopi Susu', 4500, 12000, 20],
        [5, 1, 'KP005', 'Teh Manis', 2000, 5000, 40],
        [6, 1, 'KP006', 'Es Teh Manis', 2500, 6000, 35],
        [7, 1, 'KP007', 'Es Jeruk', 3000, 8000, 30],
        [8, 1, 'KP008', 'Milo', 4000, 10000, 20],
        [9, 1, 'KP009', 'Es Milo', 4500, 12000, 18],
        [10, 1, 'KP010', 'Roti Bakar Coklat', 4000, 10000, 15],
        [11, 1, 'KP011', 'Roti Bakar Keju', 5000, 12000, 12],
        [12, 1, 'KP012', 'Pisang Goreng (3 pcs)', 3000, 8000, 20],
        [13, 1, 'KP013', 'Nasi Goreng', 10000, 18000, 15],
        [14, 1, 'KP014', 'Mie Goreng', 8000, 15000, 18],
        [15, 1, 'KP015', 'Air Mineral', 2000, 4000, 50]
    ]
    
    # Produce shop products - realistic market pricing
    sayur_products = [
        [16, 2, 'SB001', 'Bayam (ikat)', 2000, 4000, 15],
        [17, 2, 'SB002', 'Kangkung (ikat)', 1500, 3000, 20],
        [18, 2, 'SB003', 'Sawi (ikat)', 2000, 4000, 12],
        [19, 2, 'SB004', 'Brokoli (250gr)', 5000, 8000, 10],
        [20, 2, 'SB005', 'Wortel (250gr)', 3000, 5000, 18],
        [21, 2, 'SB006', 'Kentang (250gr)', 3500, 6000, 20],
        [22, 2, 'SB007', 'Tomat (250gr)', 4000, 7000, 15],
        [23, 2, 'SB008', 'Cabai Merah (100gr)', 4000, 8000, 12],
        [24, 2, 'SB009', 'Cabai Rawit (100gr)', 5000, 10000, 10],
        [25, 2, 'SB010', 'Jeruk (kg)', 12000, 18000, 25],
        [26, 2, 'SB011', 'Apel (kg)', 18000, 25000, 15],
        [27, 2, 'SB012', 'Pisang (sisir)', 8000, 12000, 20],
        [28, 2, 'SB013', 'Semangka (kg)', 8000, 12000, 30],
        [29, 2, 'SB014', 'Pepaya (kg)', 6000, 10000, 25],
        [30, 2, 'SB015', 'Mangga Harum Manis (kg)', 15000, 22000, 18]
    ]
    
    # Grocery store products - realistic sembako pricing
    sembako_products = [
        [31, 3, 'SM001', 'Beras (kg)', 12000, 15000, 80],
        [32, 3, 'SM002', 'Gula Pasir (kg)', 14000, 17000, 60],
        [33, 3, 'SM003', 'Minyak Goreng (L)', 17000, 20000, 40],
        [34, 3, 'SM004', 'Telur (kg)', 25000, 30000, 30],
        [35, 3, 'SM005', 'Tepung Terigu (kg)', 11000, 14000, 35],
        [36, 3, 'SM006', 'Kecap Manis ABC (botol)', 9000, 12000, 25],
        [37, 3, 'SM007', 'Saus Sambal ABC (botol)', 8000, 11000, 20],
        [38, 3, 'SM008', 'Indomie Goreng (pcs)', 2800, 4000, 80],
        [39, 3, 'SM009', 'Indomie Kuah (pcs)', 2500, 3500, 75],
        [40, 3, 'SM010', 'Sabun Mandi Lifebuoy (pcs)', 3500, 5000, 30],
        [41, 3, 'SM011', 'Shampo Sunsilk Sachet (pcs)', 1200, 2000, 50],
        [42, 3, 'SM012', 'Deterjen Rinso (sachet)', 2500, 4000, 40],
        [43, 3, 'SM013', 'Gas LPG 3kg', 19000, 22000, 15],
        [44, 3, 'SM014', 'Mie Sedaap (pcs)', 2600, 3800, 60],
        [45, 3, 'SM015', 'Bihun (pcs)', 7000, 10000, 25]
    ]
    
    all_products = kopi_products + sayur_products + sembako_products
    columns = ['produk_id', 'bisnis_id', 'kode_produk', 'nama_produk', 'harga_beli', 'harga_jual', 'stok_saat_ini']
    df = pd.DataFrame(all_products, columns=columns)
    
    return df

# 3 & 4. Generate tbl_penjualan and tbl_detail_penjualan for full year 2024
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
        1: ["Monday", "Friday"],          # Warung Kopi: promos on Mondays and Fridays
        2: ["Tuesday", "Saturday"],       # Warung Sayur: promos on Tuesdays and Saturdays
        3: ["Wednesday", "Sunday"]        # Warung Sembako: promos on Wednesdays and Sundays
    }
    
    # Business-appropriate promo descriptions
    promo_descriptions = {
        1: ["Promo Minuman", "Happy Hour"],
        2: ["Promo Hari Ini", "Promo Segar"],
        3: ["Promo Tetangga"]
    }
    
    # Define business hours patterns
    business_hours = {
        1: [(6, 23)],                   # Warung Kopi: 6 AM - 11 PM
        2: [(6, 17)],                   # Warung Sayur: 6 AM - 5 PM
        3: [(7, 21)]                    # Warung Sembako: 7 AM - 9 PM
    }
    
    # Indonesian holiday and special period effects
    def get_period_factor(date):
        month = date.month
        day = date.day
        
        # Ramadan effect (March 11 - April 9, 2024)
        ramadan_start = datetime(2024, 3, 11).date()
        ramadan_end = datetime(2024, 4, 9).date()
        
        # Lebaran effect (April 10-12, 2024)
        lebaran_start = datetime(2024, 4, 10).date()
        lebaran_end = datetime(2024, 4, 12).date()
        
        # New Year effect
        new_year_effect = datetime(2024, 1, 1).date()
        
        # Independence Day effect
        independence_day = datetime(2024, 8, 17).date()
        
        # Christmas/New Year end effect
        christmas_effect = datetime(2024, 12, 25).date()
        
        date_only = date.date()
        
        if ramadan_start <= date_only <= ramadan_end:
            return {'kopi': 0.7, 'sayur': 1.1, 'sembako': 1.2}  # Less coffee, more groceries
        elif lebaran_start <= date_only <= lebaran_end:
            return {'kopi': 1.5, 'sayur': 1.3, 'sembako': 1.8}  # All businesses busy
        elif date_only == new_year_effect:
            return {'kopi': 0.5, 'sayur': 0.8, 'sembako': 1.4}  # Holiday effect
        elif date_only == independence_day:
            return {'kopi': 1.2, 'sayur': 1.1, 'sembako': 1.3}  # National holiday
        elif date_only == christmas_effect:
            return {'kopi': 1.1, 'sayur': 1.2, 'sembako': 1.4}  # Christmas shopping
        else:
            return {'kopi': 1.0, 'sayur': 1.0, 'sembako': 1.0}  # Normal days
    
    # Seasonal patterns by month
    month_factors = {
        1: {'hot_drinks': 0.9, 'cold_drinks': 1.1, 'vegetables': 1.0, 'fruits': 1.1, 'groceries': 1.0},
        2: {'hot_drinks': 0.9, 'cold_drinks': 1.1, 'vegetables': 1.0, 'fruits': 1.1, 'groceries': 1.0},
        3: {'hot_drinks': 0.8, 'cold_drinks': 1.2, 'vegetables': 1.1, 'fruits': 1.2, 'groceries': 1.0},
        4: {'hot_drinks': 0.7, 'cold_drinks': 1.3, 'vegetables': 1.2, 'fruits': 1.3, 'groceries': 1.1},
        5: {'hot_drinks': 0.6, 'cold_drinks': 1.4, 'vegetables': 1.1, 'fruits': 1.3, 'groceries': 1.0},
        6: {'hot_drinks': 0.6, 'cold_drinks': 1.4, 'vegetables': 1.0, 'fruits': 1.2, 'groceries': 1.0},
        7: {'hot_drinks': 0.6, 'cold_drinks': 1.4, 'vegetables': 1.0, 'fruits': 1.2, 'groceries': 1.0},
        8: {'hot_drinks': 0.6, 'cold_drinks': 1.4, 'vegetables': 1.0, 'fruits': 1.2, 'groceries': 1.1},
        9: {'hot_drinks': 0.7, 'cold_drinks': 1.3, 'vegetables': 1.1, 'fruits': 1.2, 'groceries': 1.0},
        10: {'hot_drinks': 0.8, 'cold_drinks': 1.2, 'vegetables': 1.0, 'fruits': 1.1, 'groceries': 1.0},
        11: {'hot_drinks': 0.9, 'cold_drinks': 1.1, 'vegetables': 1.0, 'fruits': 1.0, 'groceries': 1.1},
        12: {'hot_drinks': 1.0, 'cold_drinks': 1.0, 'vegetables': 1.0, 'fruits': 1.0, 'groceries': 1.2}
    }
    
    # Define product categories
    product_categories = {
        'hot_drinks': [1, 2, 5, 8],              # Hot beverages
        'cold_drinks': [3, 4, 6, 7, 9],          # Cold beverages
        'vegetables': list(range(16, 25)),       # Vegetables
        'fruits': list(range(25, 31)),           # Fruits
        'groceries': list(range(31, 46))         # Grocery items
    }
    
    # Payday effect (1st and 15th of month)
    def is_payday(date):
        return date.day in [1, 15]
    
    # Iterate through each date
    for date in dates:
        day_name = date.day_name()
        day_of_week = date.weekday()  # 0 is Monday, 6 is Sunday
        month = date.month
        
        # Get period factors (holidays, special events)
        period_factors = get_period_factor(date)
        
        # Weekend factor (more sales on weekends)
        weekend_factor = 1.5 if day_of_week >= 5 else 1.0
        
        # Payday factor
        payday_factor = 1.3 if is_payday(date) else 1.0
        
        # Generate transactions for each business
        for bisnis_id in range(1, 4):
            # Business-specific period factor
            if bisnis_id == 1:
                business_factor = period_factors['kopi']
            elif bisnis_id == 2:
                business_factor = period_factors['sayur']
            else:
                business_factor = period_factors['sembako']
            
            # Determine number of transactions based on day of week and business
            base_transactions = 12  # Increased base for full year
            if bisnis_id == 1:  # Coffee shop: busier on weekends and paydays
                num_transactions = int(base_transactions * weekend_factor * payday_factor * business_factor * random.uniform(0.8, 1.2))
            elif bisnis_id == 2:  # Produce shop: busier on weekends and early week
                market_day_factor = 1.3 if day_of_week in [0, 5] else 1.0  # Monday and Saturday are market days
                num_transactions = int(base_transactions * weekend_factor * market_day_factor * business_factor * random.uniform(0.8, 1.2))
            else:  # Grocery store: consistent with payday spikes
                num_transactions = int(base_transactions * (weekend_factor * 0.9) * payday_factor * business_factor * random.uniform(0.8, 1.2))
            
            # Ensure minimum transactions
            num_transactions = max(3, num_transactions)
            
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
                # Include business ID to ensure uniqueness across all businesses
                tx_number = f"INV-{tx_date_str}-B{bisnis_id}-{tx_num:04d}"
                
                # Payment method - 70% Tunai, 30% QRIS
                payment_method = "Tunai" if random.random() < 0.7 else "QRIS"
                
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
                    if is_promo_day and random.random() < 0.25:  # 25% chance on promo days
                        diskon_item = int(harga_satuan * random.uniform(0.1, 0.3))  # 10-30% discount
                        
                        # Business-appropriate discount descriptions
                        deskripsi_diskon = random.choice(promo_descriptions[bisnis_id])
                    else:
                        diskon_item = 0
                        deskripsi_diskon = ""
                    
                    subtotal = (kuantitas * harga_satuan) - diskon_item
                    
                    # Ensure minimum price
                    if subtotal < 2000:
                        subtotal = 2000
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

# 5. Generate tbl_pengeluaran with more realistic patterns
def generate_expenses(start_date, end_date):
    expenses_columns = ['pengeluaran_id', 'bisnis_id', 'tanggal_pengeluaran', 'kategori', 'jumlah', 'deskripsi', 'metode_pembayaran']
    expenses_data = []
    pengeluaran_id = 501
    
    # Define expense categories and frequencies
    expense_categories = {
        1: {  # Warung Kopi
            'Bahan Baku': {'freq': 'weekly', 'min': 300000, 'max': 500000, 'desc': 'Belanja kopi dan bahan'},
            'Utilitas': {'freq': 'monthly', 'min': 150000, 'max': 250000, 'desc': 'Bayar listrik'},
            'Sewa': {'freq': 'monthly', 'min': 800000, 'max': 800000, 'desc': 'Sewa tempat'},
            'Gaji': {'freq': 'monthly', 'min': 1200000, 'max': 1200000, 'desc': 'Gaji karyawan'},
            'Peralatan': {'freq': 'occasional', 'min': 150000, 'max': 400000, 'desc': 'Peralatan kafe'}
        },
        2: {  # Warung Sayur
            'Bahan Baku': {'freq': '3-days', 'min': 500000, 'max': 800000, 'desc': 'Belanja sayur dan buah'},
            'Utilitas': {'freq': 'monthly', 'min': 120000, 'max': 200000, 'desc': 'Bayar listrik'},
            'Sewa': {'freq': 'monthly', 'min': 1000000, 'max': 1000000, 'desc': 'Sewa tempat'},
            'Gaji': {'freq': 'monthly', 'min': 1000000, 'max': 1000000, 'desc': 'Gaji karyawan'},
            'Peralatan': {'freq': 'occasional', 'min': 200000, 'max': 500000, 'desc': 'Peralatan display'}
        },
        3: {  # Warung Sembako
            'Bahan Baku': {'freq': 'weekly', 'min': 1200000, 'max': 2000000, 'desc': 'Restock sembako'},
            'Utilitas': {'freq': 'monthly', 'min': 200000, 'max': 300000, 'desc': 'Bayar listrik'},
            'Sewa': {'freq': 'monthly', 'min': 1200000, 'max': 1200000, 'desc': 'Sewa tempat'},
            'Gaji': {'freq': 'monthly', 'min': 1500000, 'max': 1500000, 'desc': 'Gaji karyawan'},
            'Peralatan': {'freq': 'occasional', 'min': 300000, 'max': 800000, 'desc': 'Peralatan toko'}
        }
    }
    
    # Generate dates for each expense type
    # Weekly expenses (every Monday)
    weekly_dates = pd.date_range(start=start_date, end=end_date, freq='W-MON')
    
    # 3-day expenses (every 3 days for fresh produce)
    three_day_dates = pd.date_range(start=start_date, end=end_date, freq='3D')
    
    # Monthly expenses (1st of each month)
    monthly_dates = pd.date_range(start=start_date.replace(day=1), end=end_date, freq='MS')
    
    # Occasional expenses (random dates)
    occasional_count = {
        1: 6,  # 6 occasional expenses for business 1 (full year)
        2: 8,  # 8 occasional expenses for business 2 (full year)
        3: 6   # 6 occasional expenses for business 3 (full year)
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
                    month_factor = 1.0 + ((date_ts.month - start_date.month) * 0.01)
                    
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
    
    # Initial balance for each business (more realistic for established businesses)
    initial_balance = {
        1: 8000000,  # Warung Kopi - 8 million
        2: 6500000,  # Warung Sayur - 6.5 million
        3: 12000000  # Warung Sembako - 12 million (needs more capital for stock)
    }
    
    # Current balance (will be updated for each day)
    current_balance = initial_balance.copy()
    
    # Generate daily cash records
    dates = pd.date_range(start=start_date, end=end_date)
    
    for date in dates:
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
    # Set date range for full year 2024
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    
    print("Generating UMKM data for full year 2024...")
    print(f"Period: {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}")
    print("=" * 60)
    
    print("Generating business data...")
    bisnis_df = generate_bisnis()
    
    print("Generating product data with realistic Indonesian pricing...")
    produk_df = generate_produk()
    
    print("Generating sales data with seasonal patterns...")
    penjualan_df, detail_penjualan_df = generate_sales_data(start_date, end_date)
    
    print("Generating expense data...")
    pengeluaran_df = generate_expenses(start_date, end_date)
    
    print("Generating daily cash records...")
    kas_df = generate_daily_cash(start_date, end_date, penjualan_df, pengeluaran_df)
    
    # Save all data to Excel files
    print("\nSaving data to Excel files...")
    
    bisnis_df.to_excel("data/tbl_bisnis.xlsx", index=False)
    produk_df.to_excel("data/tbl_produk.xlsx", index=False)
    penjualan_df.to_excel("data/tbl_penjualan.xlsx", index=False)
    detail_penjualan_df.to_excel("data/tbl_detail_penjualan.xlsx", index=False)
    pengeluaran_df.to_excel("data/tbl_pengeluaran.xlsx", index=False)
    kas_df.to_excel("data/tbl_kas_harian.xlsx", index=False)
    
    print(f"\nData generation complete! Files saved to 'data' directory.")
    
    # Print comprehensive statistics
    print("\n" + "=" * 60)
    print("COMPREHENSIVE DATA STATISTICS")
    print("=" * 60)
    print(f"Period: Full Year 2024 ({(end_date - start_date).days + 1} days)")
    print(f"Businesses: {len(bisnis_df)}")
    print(f"Products: {len(produk_df)}")
    print(f"Sales transactions: {len(penjualan_df):,}")
    print(f"Sales line items: {len(detail_penjualan_df):,}")
    print(f"Expense records: {len(pengeluaran_df):,}")
    print(f"Daily cash records: {len(kas_df):,}")
    
    # Business breakdown
    print(f"\nSALES BREAKDOWN BY BUSINESS:")
    sales_by_business = penjualan_df.groupby('bisnis_id').agg({
        'penjualan_id': 'count',
        'total': 'sum'
    }).round(0)
    
    business_names = {1: 'Warung Kopi Gembira', 2: 'Warung Sayur Buah Sehat', 3: 'Warung Sembako Berkah'}
    for bisnis_id in range(1, 4):
        transactions = sales_by_business.loc[bisnis_id, 'penjualan_id']
        revenue = sales_by_business.loc[bisnis_id, 'total']
        print(f"  {business_names[bisnis_id]}: {transactions:,} transactions, Rp {revenue:,.0f} revenue")
    
    # Payment method breakdown
    payment_breakdown = penjualan_df['metode_pembayaran'].value_counts()
    print(f"\nPAYMENT METHODS:")
    for method, count in payment_breakdown.items():
        percentage = (count / len(penjualan_df)) * 100
        print(f"  {method}: {count:,} transactions ({percentage:.1f}%)")
    
    # Discount statistics
    discounted_items = detail_penjualan_df[detail_penjualan_df['diskon_item'] > 0]
    discount_rate = (len(discounted_items) / len(detail_penjualan_df)) * 100
    print(f"\nDISCOUNT STATISTICS:")
    print(f"  Items with discount: {len(discounted_items):,} of {len(detail_penjualan_df):,} ({discount_rate:.1f}%)")
    
    if len(discounted_items) > 0:
        avg_discount = discounted_items['diskon_item'].mean()
        total_discounts = discounted_items['diskon_item'].sum()
        print(f"  Average discount amount: Rp {avg_discount:,.0f}")
        print(f"  Total discounts given: Rp {total_discounts:,.0f}")
        
        # Discount by business
        discount_by_business = discounted_items.groupby('penjualan_id').first().reset_index()
        discount_by_business = discount_by_business.merge(penjualan_df[['penjualan_id', 'bisnis_id']], on='penjualan_id')
        discount_by_business = discount_by_business.groupby('bisnis_id')['diskon_item'].agg(['count', 'sum'])
        
        print(f"  Discount breakdown by business:")
        for bisnis_id in range(1, 4):
            if bisnis_id in discount_by_business.index:
                count = discount_by_business.loc[bisnis_id, 'count']
                total = discount_by_business.loc[bisnis_id, 'sum']
                print(f"    {business_names[bisnis_id]}: {count:,} discounts, Rp {total:,.0f}")
    
    # File size estimation
    total_records = len(bisnis_df) + len(produk_df) + len(penjualan_df) + len(detail_penjualan_df) + len(pengeluaran_df) + len(kas_df)
    estimated_size_mb = total_records * 150 / (1024 * 1024)  # Rough estimation
    print(f"\nESTIMATED TOTAL FILE SIZE: ~{estimated_size_mb:.1f} MB")
    
    print("\nReady to load into PostgreSQL database!")
    
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