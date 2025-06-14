-- Schema for UMKM Database
CREATE SCHEMA umkm;

-- 1. Business Table (Core Entity)
CREATE TABLE umkm.bisnis (
    bisnis_id SERIAL PRIMARY KEY,
    nama_bisnis VARCHAR(100) NOT NULL,
    jenis_usaha VARCHAR(50) NOT NULL CHECK (jenis_usaha IN ('Kuliner', 'Retail', 'Jasa')),
    alamat TEXT NOT NULL,
    no_telepon VARCHAR(15) NOT NULL,
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Product Table
CREATE TABLE umkm.produk (
    produk_id SERIAL PRIMARY KEY,
    bisnis_id INTEGER NOT NULL REFERENCES umkm.bisnis(bisnis_id),
    kode_produk VARCHAR(10) NOT NULL,
    nama_produk VARCHAR(100) NOT NULL,
    harga_beli NUMERIC(12,2) NOT NULL CHECK (harga_beli >= 0),
    harga_jual NUMERIC(12,2) NOT NULL CHECK (harga_jual >= harga_beli),
    stok_saat_ini INTEGER NOT NULL CHECK (stok_saat_ini >= 0),
    kategori VARCHAR(50) GENERATED ALWAYS AS (
        CASE 
            WHEN produk_id BETWEEN 1 AND 15 THEN 'Minuman/Makanan'
            WHEN produk_id BETWEEN 16 AND 30 THEN 'Sayur/Buah'
            ELSE 'Sembako'
        END
    ) STORED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_kode_produk UNIQUE (bisnis_id, kode_produk)
);

-- 3. Sales Header Table
CREATE TABLE umkm.penjualan (
    penjualan_id SERIAL PRIMARY KEY,
    bisnis_id INTEGER NOT NULL REFERENCES umkm.bisnis(bisnis_id),
    nomor_transaksi VARCHAR(20) NOT NULL UNIQUE,
    tanggal_transaksi TIMESTAMP NOT NULL,
    total NUMERIC(12,2) NOT NULL CHECK (total > 0),
    metode_pembayaran VARCHAR(10) NOT NULL CHECK (metode_pembayaran IN ('Tunai', 'QRIS', 'Transfer')),
    status_pembayaran VARCHAR(10) NOT NULL DEFAULT 'Lunas' CHECK (status_pembayaran IN ('Lunas', 'Pending', 'Gagal')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Sales Detail Table
CREATE TABLE umkm.detail_penjualan (
    detail_id SERIAL PRIMARY KEY,
    penjualan_id INTEGER NOT NULL REFERENCES umkm.penjualan(penjualan_id) ON DELETE CASCADE,
    produk_id INTEGER NOT NULL REFERENCES umkm.produk(produk_id),
    kuantitas NUMERIC(8,2) NOT NULL CHECK (kuantitas > 0),
    harga_satuan NUMERIC(12,2) NOT NULL CHECK (harga_satuan > 0),
    diskon_item NUMERIC(12,2) DEFAULT 0 CHECK (diskon_item >= 0),
    deskripsi_diskon VARCHAR(50),
    subtotal NUMERIC(12,2) GENERATED ALWAYS AS (
        (kuantitas * harga_satuan) - COALESCE(diskon_item, 0)
    ) STORED,
    CONSTRAINT unique_line_item UNIQUE (penjualan_id, produk_id)
);

-- 5. Expenses Table
CREATE TABLE umkm.pengeluaran (
    pengeluaran_id SERIAL PRIMARY KEY,
    bisnis_id INTEGER NOT NULL REFERENCES umkm.bisnis(bisnis_id),
    tanggal_pengeluaran DATE NOT NULL,
    kategori VARCHAR(50) NOT NULL CHECK (kategori IN ('Bahan Baku', 'Utilitas', 'Sewa', 'Gaji', 'Peralatan')),
    jumlah NUMERIC(12,2) NOT NULL CHECK (jumlah > 0),
    deskripsi TEXT,
    metode_pembayaran VARCHAR(20) NOT NULL CHECK (metode_pembayaran IN ('Tunai', 'Transfer Bank', 'Kredit')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Daily Cash Flow Table
CREATE TABLE umkm.kas_harian (
    kas_id SERIAL PRIMARY KEY,
    bisnis_id INTEGER NOT NULL REFERENCES umkm.bisnis(bisnis_id),
    tanggal DATE NOT NULL,
    saldo_awal NUMERIC(12,2) NOT NULL,
    total_penjualan NUMERIC(12,2) NOT NULL DEFAULT 0,
    total_pengeluaran NUMERIC(12,2) NOT NULL DEFAULT 0,
    saldo_akhir NUMERIC(12,2) GENERATED ALWAYS AS (
        saldo_awal + total_penjualan - total_pengeluaran
    ) STORED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_daily_record UNIQUE (bisnis_id, tanggal)
);

-- Create indexes for performance
CREATE INDEX idx_produk_bisnis ON umkm.produk(bisnis_id);
CREATE INDEX idx_penjualan_bisnis ON umkm.penjualan(bisnis_id);
CREATE INDEX idx_penjualan_tanggal ON umkm.penjualan(tanggal_transaksi);
CREATE INDEX idx_detail_penjualan_produk ON umkm.detail_penjualan(produk_id);
CREATE INDEX idx_pengeluaran_tanggal ON umkm.pengeluaran(tanggal_pengeluaran);
CREATE INDEX idx_kas_harian_tanggal ON umkm.kas_harian(tanggal);

-- Display success message
SELECT 'UMKM database schema created successfully!' as message;