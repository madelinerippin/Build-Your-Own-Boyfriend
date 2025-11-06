# Build-Your-Own-Boyfriend

## Scraping Commands 
1. python ao3_work_ids.py "https://archiveofourown.org/works/search?work_search%5Bquery%5D=Works+in+Jujutsu+Kaisen" --out_csv jjk
2. python ao3_get_fanfics.py .\jjk.csv --header "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AO3Scraper/1.0 (Contact: your_email@example.com)"
3. python ao3_get_fanfics.py 71695961 --header "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AO3Scraper/1.0 (Contact: your_email@example.com)" (if you just wanted 1 fanfic)

Running the 2nd and 3rd command will save the fanfics into a csv called fanfics.csv
It seems like for now even if the fanfiction has multiple chapters, only the first one will be saved which is probably fine because of length anyway
