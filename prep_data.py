import pandas as pd
import numpy as np

SRC = '/mnt/user-data/uploads/dashboard_marketplace_siap_tableau_v2.xlsx'
xl = pd.ExcelFile(SRC)

fact = xl.parse('Fact_Penjualan')
kat = xl.parse('Dim_Kategori_Tarif')
hpp = xl.parse('Dim_Asumsi_HPP')
ops = xl.parse('Dim_Biaya_Operasional_Lain')
makro = xl.parse('Dim_Data_Makro')
platform = xl.parse('Dim_Biaya_Platform')
pph22 = xl.parse('Dim_Pajak_PPh22')

# Only completed orders count for revenue/profit analysis (consistent with summary doc)
done = fact[fact['Status Pesanan'] == 'Selesai'].copy()

scenarios = {
    'efisien': ('Estimasi_HPP_Rp_Efisien_HPP35','Estimasi_Biaya_Ops_Lain_Rp_Efisien_HPP35','Estimasi_Profit_Bersih_Rp_Efisien_HPP35'),
    'umum': ('Estimasi_HPP_Rp_Umum_HPP55','Estimasi_Biaya_Ops_Lain_Rp_Umum_HPP55','Estimasi_Profit_Bersih_Rp_Umum_HPP55'),
    'ketat': ('Estimasi_HPP_Rp_Ketat_HPP70','Estimasi_Biaya_Ops_Lain_Rp_Ketat_HPP70','Estimasi_Profit_Bersih_Rp_Ketat_HPP70'),
}

# --- Overview KPIs ---
total_orders = len(fact)
completed_orders = len(done)
cancelled_orders = len(fact[fact['Status Pesanan']=='Batal'])
total_revenue = done['Total Pembayaran'].sum()
aov = done['Total Pembayaran'].mean()

overview_rows = []
for name,(hcol,ocol,pcol) in scenarios.items():
    profit = done[pcol].sum()
    margin = profit/total_revenue*100
    overview_rows.append({'scenario':name,'profit_net_rp':profit,'margin_pct':margin})
overview_df = pd.DataFrame(overview_rows)

summary = pd.DataFrame([{
    'total_orders': total_orders,
    'completed_orders': completed_orders,
    'cancelled_orders': cancelled_orders,
    'completed_pct': completed_orders/total_orders*100,
    'cancelled_pct': cancelled_orders/total_orders*100,
    'total_revenue_rp': total_revenue,
    'aov_rp': aov,
}])

# --- Monthly trend ---
monthly = done.groupby('Periode').agg(
    orders=('order_id','count'),
    revenue_rp=('Total Pembayaran','sum'),
).reset_index()
for name,(hcol,ocol,pcol) in scenarios.items():
    m = done.groupby('Periode')[pcol].sum().reset_index().rename(columns={pcol:f'profit_{name}_rp'})
    monthly = monthly.merge(m, on='Periode', how='left')
monthly['aov_rp'] = monthly['revenue_rp']/monthly['orders']
monthly = monthly.sort_values('Periode')

# --- Category breakdown ---
cat = done.groupby('Kategori_Utama').agg(
    orders=('order_id','count'),
    revenue_rp=('Total Pembayaran','sum'),
).reset_index()
for name,(hcol,ocol,pcol) in scenarios.items():
    c = done.groupby('Kategori_Utama')[pcol].sum().reset_index().rename(columns={pcol:f'profit_{name}_rp'})
    cat = cat.merge(c, on='Kategori_Utama', how='left')
    cat[f'margin_{name}_pct'] = cat[f'profit_{name}_rp']/cat['revenue_rp']*100
cat = cat.sort_values('revenue_rp', ascending=False)

# --- Regional breakdown ---
region = done.groupby(['Provinsi']).agg(
    orders=('order_id','count'),
    revenue_rp=('Total Pembayaran','sum'),
).reset_index()
for name,(hcol,ocol,pcol) in scenarios.items():
    r = done.groupby('Provinsi')[pcol].sum().reset_index().rename(columns={pcol:f'profit_{name}_rp'})
    region = region.merge(r, on='Provinsi', how='left')
    region[f'margin_{name}_pct'] = region[f'profit_{name}_rp']/region['revenue_rp']*100
region = region.sort_values('revenue_rp', ascending=False)

city = done.groupby(['Kota/Kabupaten','Provinsi']).agg(
    orders=('order_id','count'),
    revenue_rp=('Total Pembayaran','sum'),
).reset_index().sort_values('revenue_rp', ascending=False).head(30)

# --- Cost structure (scenario umum as base, but store all 3) ---
cost_rows = []
for name,(hcol,ocol,pcol) in scenarios.items():
    hpp_sum = done[hcol].sum()
    ops_sum = done[ocol].sum()
    ongkir_sum = done['Estimasi Potongan Biaya Pengiriman'].sum()
    komisi_sum = done['Estimasi_Biaya_Komisi_Rp'].sum()
    proses_sum = done['Estimasi_Biaya_Proses_Pesanan_Rp'].sum()
    profit_sum = done[pcol].sum()
    cost_rows.append({
        'scenario': name,
        'hpp_rp': hpp_sum, 'hpp_pct': hpp_sum/total_revenue*100,
        'ongkir_rp': ongkir_sum, 'ongkir_pct': ongkir_sum/total_revenue*100,
        'ops_lain_rp': ops_sum, 'ops_lain_pct': ops_sum/total_revenue*100,
        'komisi_rp': komisi_sum, 'komisi_pct': komisi_sum/total_revenue*100,
        'proses_rp': proses_sum, 'proses_pct': proses_sum/total_revenue*100,
        'profit_rp': profit_sum, 'profit_pct': profit_sum/total_revenue*100,
    })
cost_structure = pd.DataFrame(cost_rows)

# --- Payment method & shipping option ---
payment = done.groupby('Metode Pembayaran').agg(orders=('order_id','count'), revenue_rp=('Total Pembayaran','sum')).reset_index().sort_values('revenue_rp',ascending=False)
shipping = done.groupby('Opsi Pengiriman').agg(orders=('order_id','count'), revenue_rp=('Total Pembayaran','sum'), ongkir_ditanggung_toko_rp=('Estimasi Potongan Biaya Pengiriman','sum')).reset_index().sort_values('revenue_rp',ascending=False)

# --- YoY 2024 vs 2025 (Jan-Nov) ---
done['year'] = done['Periode'].str[:4]
done['month'] = done['Periode'].str[5:7]
jan_nov = done[done['month'].astype(int) <= 11]
yoy = jan_nov.groupby('year').agg(
    orders=('order_id','count'),
    revenue_rp=('Total Pembayaran','sum'),
).reset_index()
yoy['aov_rp'] = yoy['revenue_rp']/yoy['orders']
for name,(hcol,ocol,pcol) in scenarios.items():
    y = jan_nov.groupby('year')[pcol].sum().reset_index().rename(columns={pcol:f'profit_{name}_rp'})
    yoy = yoy.merge(y, on='year', how='left')
yoy = yoy[yoy['year'].isin(['2024','2025'])]

# Save all
overview_df.to_csv('data/overview_scenarios.csv', index=False)
summary.to_csv('data/summary_kpi.csv', index=False)
monthly.to_csv('data/monthly_trend.csv', index=False)
cat.to_csv('data/category_breakdown.csv', index=False)
region.to_csv('data/region_breakdown.csv', index=False)
city.to_csv('data/city_top30.csv', index=False)
cost_structure.to_csv('data/cost_structure.csv', index=False)
payment.to_csv('data/payment_method.csv', index=False)
shipping.to_csv('data/shipping_option.csv', index=False)
yoy.to_csv('data/yoy_comparison.csv', index=False)
kat.to_csv('data/dim_kategori_tarif.csv', index=False)
hpp.to_csv('data/dim_asumsi_hpp.csv', index=False)
ops.to_csv('data/dim_biaya_operasional.csv', index=False)
makro.to_csv('data/dim_data_makro.csv', index=False)
platform.to_csv('data/dim_biaya_platform.csv', index=False)
pph22.to_csv('data/dim_pajak_pph22.csv', index=False)

# also save a slim transaction-level file for the simulator (only needed cols)
slim_cols = ['order_id','Periode','Kategori_Utama','Provinsi','Kota/Kabupaten','Metode Pembayaran',
             'Opsi Pengiriman','Total Pembayaran','Estimasi Potongan Biaya Pengiriman',
             'Estimasi_Biaya_Komisi_Rp','Estimasi_Biaya_Proses_Pesanan_Rp']
done[slim_cols].to_csv('data/transactions_completed.csv', index=False)

print("DONE")
print("total_revenue", total_revenue)
print(overview_df)
print(cost_structure[['scenario','hpp_pct','ongkir_pct','ops_lain_pct','komisi_pct','proses_pct','profit_pct']])
print(yoy)
