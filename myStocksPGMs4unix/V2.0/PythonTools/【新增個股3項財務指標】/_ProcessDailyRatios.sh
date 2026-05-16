python3 01_getStocksDailyRatiosData_v2.py 20260511 20260515
python3 02_formatStocksDailyRatiosData_v2.py 20260511 20260515
python3 03_insertDailyRatiosToMySQLDB_v2.py 20260511 20260515

-- 檢視各 table 總筆數 --
select 'taiwan_data_polaris', count(*) FROM taiwan_data_polaris union
select 'taiwan_data_tsec', count(*) from taiwan_data_tsec union
select 'taiwan_data_tsec_margin', count(*) from taiwan_data_tsec_margin union
select 'taiwan_data_tsec_volume', count(*) from taiwan_data_tsec_volume union
select 'taiwan_data_stocks_daily_ratios', count(*) FROM taiwan_data_stocks_daily_ratios union
select 'stocks_bz_performance', count(*) from stocks_bz_performance union
select 'stocks_per_and_pbr', count(*) from stocks_per_and_pbr union
select 'stocks_year_add', count(*) from stocks_year_add union
select 'stocks_sale_month', count(*) from stocks_sale_month union
select 'stocks_dividend', count(*) from stocks_dividend ;