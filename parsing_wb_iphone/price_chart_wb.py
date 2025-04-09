import pandas as pd
import plotly.graph_objects as go
import plotly.offline as pyo
from pathlib import Path

def generate_html_with_filters():
    df = pd.read_excel('wildberries_price_history.xlsx')
    unique_ids = df['ID'].unique()
    price_columns = df.columns[3:]

    bar_data = []
    line_fig = go.Figure()

    for uid in unique_ids:
        product_row = df[df['ID'] == uid]
        if product_row.empty:
            continue

        name_raw = product_row['Name'].values[0][:60]
        name = f"{name_raw} (ID: {uid})"
        raw_prices = product_row[price_columns].iloc[0]

        try:
            prices = raw_prices.dropna().apply(lambda x: float(str(x).replace('₽', '').replace(' ', '').replace(',', '.')))
            dates = pd.to_datetime(prices.index, errors='coerce')
        except Exception:
            continue

        if prices.empty or len(prices) < 2:
            continue

        price_changed = any(prices.diff().fillna(0) != 0)
        line_color = 'crimson' if price_changed else 'gray'

        line_fig.add_trace(go.Scatter(
            x=dates,
            y=prices,
            mode='lines+markers',
            name=name,
            line=dict(width=2, color=line_color),
            marker=dict(size=6),
            hovertemplate=f'<b>{name}</b><br>Дата: %{{x|%d.%m.%Y}}<br>Цена: %{{y:.0f}} ₽<extra></extra>'
        ))

        bar_data.append({
            'Name': name_raw,
            'ID': uid,
            'MinPrice': prices.min(),
            'MaxPrice': prices.max()
        })

    # Подготовим bar chart’ы
    bar_df = pd.DataFrame(bar_data)
    chunks = [bar_df[i:i + 20] for i in range(0, len(bar_df), 20)]

    html_parts = []

    # Добавим общий линейный график
    line_fig.update_layout(
        title='📈 История изменения цен всех товаров',
        xaxis_title='Дата',
        yaxis_title='Цена (₽)',
        template='plotly_white',
        height=600
    )
    html_parts.append(pyo.plot(line_fig, include_plotlyjs='cdn', output_type='div'))

    # Добавим bar-чарты по 20 товаров
    for idx, chunk in enumerate(chunks, 1):
        fig_bar = go.Figure()

        fig_bar.add_trace(go.Bar(
            x=chunk['Name'] + ' (ID: ' + chunk['ID'].astype(str) + ')',
            y=chunk['MinPrice'],
            name='Минимальная цена',
            marker_color='steelblue'
        ))

        fig_bar.add_trace(go.Bar(
            x=chunk['Name'] + ' (ID: ' + chunk['ID'].astype(str) + ')',
            y=chunk['MaxPrice'],
            name='Максимальная цена',
            marker_color='orange'
        ))

        fig_bar.update_layout(
            title=f'📊 Цены товаров (группа {idx})',
            xaxis_title='Товар',
            yaxis_title='Цена (₽)',
            barmode='group',
            template='plotly_white',
            xaxis_tickangle=45,
            height=600
        )

        html_parts.append(pyo.plot(fig_bar, include_plotlyjs=False, output_type='div'))

    # Сортировка: топ по максимальной цене
    top_max = bar_df.sort_values(by='MaxPrice', ascending=False).head(20)
    fig_top = go.Figure([
        go.Bar(
            x=top_max['Name'] + ' (ID: ' + top_max['ID'].astype(str) + ')',
            y=top_max['MaxPrice'],
            name='Топ-20 по максимальной цене',
            marker_color='darkred'
        )
    ])
    fig_top.update_layout(
        title='🔥 Топ-20 товаров по максимальной цене',
        xaxis_title='Товар',
        yaxis_title='Цена (₽)',
        xaxis_tickangle=45,
        template='plotly_white',
        height=600
    )
    html_parts.insert(1, pyo.plot(fig_top, include_plotlyjs=False, output_type='div'))

    # Объединяем всё в один HTML
    full_html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>Wildberries Price Charts</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                padding: 20px;
                max-width: 1200px;
                margin: auto;
            }}
            h1 {{
                text-align: center;
            }}
            .chart {{
                margin-bottom: 60px;
                border-bottom: 1px solid #ddd;
                padding-bottom: 40px;
            }}
        </style>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    </head>
    <body>
        <h1>📊 Динамика цен товаров Wildberries</h1>
        {''.join(f'<div class="chart">{chart}</div>' for chart in html_parts)}
    </body>
    </html>
    """

    output_path = Path('wildberries_price_report.html')
    output_path.write_text(full_html, encoding='utf-8')
    print(f"✅ HTML сохранён как: {output_path.resolve()}")
