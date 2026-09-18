"""Public schema-normalization helpers; no benchmark questions or evaluator imports."""

def install(conn, revision):
    assert revision=='before'
    modern=False
    for g,cat in [(1,'office products'),(2,'electronics'),(3,'musical instruments')]:
        price='prc / 100.0' if g==2 else 'prc'
        status="'active'"
        image='img_ct' if g==2 else 'NULL'
        conn.execute(f"CREATE TEMP VIEW products_{g} AS SELECT '{cat}' category,ref_id,ttl title,{price} price,avg_rtg catalog_rating,{status} status,{image} image_count FROM items_g{g}")
        date="date(ts / 1000.0, 'unixepoch')" if g==1 else "date(ts, 'unixepoch')" if g==2 else 'ts'
        year=f"CAST(strftime('%Y',{date}) AS INTEGER)"
        month=f"CAST(strftime('%m',{date}) AS INTEGER)"
        verified="CASE WHEN vrf='true' THEN 1 ELSE 0 END" if g==2 else 'vrf'
        label=f"CASE WHEN {verified}=1 THEN 'verified' ELSE 'unverified' END"
        product_id='item_id' if g!=3 else 'ref_id'
        epoch='ts / 1000.0' if g==1 else 'ts' if g==2 else "CAST(strftime('%s',ts) AS REAL)"
        conn.execute(f"CREATE TEMP VIEW reviews_{g} AS SELECT '{cat}' category,ref_id,{product_id} product_id,uid user_id,rtg rating,body,{date} review_date,{year} year,{month} month,{verified} verified,{label} verification_label,{epoch} epoch_seconds FROM fdbk_g{g}")
    conn.execute('CREATE TEMP VIEW products AS SELECT * FROM products_1 UNION ALL SELECT * FROM products_2 UNION ALL SELECT * FROM products_3')
    conn.execute('CREATE TEMP VIEW reviews AS SELECT * FROM reviews_1 UNION ALL SELECT * FROM reviews_2 UNION ALL SELECT * FROM reviews_3')
    a3='attrs_g3'
    conn.execute(f"CREATE TEMP VIEW attributes AS SELECT 'office products' category,ref_id,attr_key,attr_val FROM attrs_g1 UNION ALL SELECT 'musical instruments',ref_id,attr_key,attr_val FROM {a3}")
    conn.execute("CREATE TEMP VIEW categories AS SELECT 'office products' category,ref_id,cat_lvl,cat_nm FROM taxn_g1 UNION ALL SELECT 'electronics',ref_id,cat_lvl,cat_nm FROM taxn_g2")
