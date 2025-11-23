# Flet Stock App With Live Data & Charts - Alpha Vantage API
import flet as ft
import requests
from config import API_KEY


# Main Flet Interface -> Function based
def main(page: ft.Page):
    # App settings
    page.title = "Jonathan Stocks"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.window_width = 1400
    page.window_height = 900
    page.bgcolor = ft.Colors.GREY_50
    page.scroll = ft.ScrollMode.AUTO

    # State Variables - Widgets in our App
    stock_symbol = ft.Ref[ft.TextField]()
    chart_container = ft.Ref[ft.Container]()
    price_info = ft.Ref[ft.Container]()
    price_text_below = ft.Ref[ft.Container]()
    error_messages = ft.Ref[ft.Container]()
    time_range_dropdown = ft.Ref[ft.Dropdown]()

    # Time range for the stock
    def get_days_for_range(range_name):
        ranges = {
            "1 week": 7,
            "2 weeks": 14,
            "30 days": 30,
            "90 days": 90,
            "1 year": 365,
            "5 years": 1825,
        }
        return ranges.get(range_name, 30)

    def get_range_label(range_name):
        return range_name

    # Fetch the Stock with our API
    def fetch_stock_data(e):
        symbol = stock_symbol.current.value.upper().strip()
        time_range = time_range_dropdown.current.value or "30 days"
        days = get_days_for_range(time_range)

        # Mini error handle
        if not symbol:
            error_messages.current.content = ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.ERROR_OUTLINE, color=ft.Colors.RED_400, size=20),
                    ft.Text("Please enter a stock symbol", color=ft.Colors.RED_700, size=14, weight=ft.FontWeight.W_500)
                ], spacing=10),
                padding=15,
                bgcolor=ft.Colors.RED_50,
                border_radius=10,
                border=ft.border.all(1, ft.Colors.RED_200)
            )
            error_messages.current.visible = True
            price_info.current.visible = False
            price_text_below.current.visible = False
            chart_container.current.visible = False
            page.update()
            return

        error_messages.current.visible = False

        # Loading state with spinner
        loading_spinner = ft.Column([
            ft.ProgressRing(width=50, height=50, color=ft.Colors.BLUE_700),
            ft.Text("Loading Stock Data...", color=ft.Colors.BLUE_700, size=16, weight=ft.FontWeight.W_500)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15)

        chart_container.current.content = ft.Container(
            content=loading_spinner,
            padding=40,
            alignment=ft.alignment.center
        )
        chart_container.current.visible = True
        price_info.current.visible = False
        price_text_below.current.visible = False
        page.update()

        # Fetch the API Data
        try:
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
            response = requests.get(url)
            data = response.json()

            time_series = data["Time Series (Daily)"]

            dates = sorted(time_series.keys(), reverse=True)[:days]
            dates.reverse()

            # Prep the charts
            opens, highs, lows, closes = [], [], [], []

            for date in dates:
                day_data = time_series[date]
                opens_price = float(day_data["1. open"])
                high_price = float(day_data["2. high"])
                low_price = float(day_data["3. low"])
                close_price = float(day_data["4. close"])

                opens.append(opens_price)
                highs.append(high_price)
                lows.append(low_price)
                closes.append(close_price)

            latest_date = sorted(time_series.keys(), reverse=True)[0]
            latest_data = time_series[latest_date]

            # Calculate price change
            current_price = float(latest_data['4. close'])
            previous_price = closes[-2] if len(closes) > 1 else current_price
            price_change = current_price - previous_price
            price_change_percent = (price_change / previous_price) * 100 if previous_price != 0 else 0
            is_positive = price_change >= 0

            # Update price info with enhanced styling
            price_info.current.content = ft.Container(
                content=ft.Column([
                    # Stock header
                    ft.Row([
                        ft.Column([
                            ft.Text(symbol, color=ft.Colors.GREY_900, size=32, weight=ft.FontWeight.BOLD),
                            ft.Text(f"As of {latest_date}", color=ft.Colors.GREY_600, size=14),
                        ], spacing=5),
                        ft.Container(expand=True),
                        ft.Container(
                            content=ft.Column([
                                ft.Text(f"${current_price:.2f}", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_900),
                                ft.Row([
                                    ft.Icon(
                                        ft.Icons.ARROW_UPWARD if is_positive else ft.Icons.ARROW_DOWNWARD,
                                        size=16,
                                        color=ft.Colors.GREEN_600 if is_positive else ft.Colors.RED_600
                                    ),
                                    ft.Text(
                                        f"${abs(price_change):.2f} ({abs(price_change_percent):.2f}%)",
                                        size=16,
                                        weight=ft.FontWeight.W_500,
                                        color=ft.Colors.GREEN_600 if is_positive else ft.Colors.RED_600
                                    )
                                ], spacing=5)
                            ], horizontal_alignment=ft.CrossAxisAlignment.END, spacing=5)
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                    ft.Divider(height=1, color=ft.Colors.GREY_300),

                    # Price cards
                    ft.Row([
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Icon(ft.Icons.PLAY_ARROW, color=ft.Colors.BLUE_600, size=16),
                                    ft.Text("Open", size=13, color=ft.Colors.GREY_600, weight=ft.FontWeight.W_500)
                                ], spacing=5),
                                ft.Text(f"${float(latest_data['1. open']):.2f}", size=24, weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.GREY_900),
                            ], spacing=8),
                            padding=20,
                            bgcolor=ft.Colors.WHITE,
                            border_radius=12,
                            expand=True,
                            shadow=ft.BoxShadow(
                                spread_radius=0,
                                blur_radius=10,
                                color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                                offset=ft.Offset(0, 2)
                            )
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Icon(ft.Icons.TRENDING_UP, color=ft.Colors.GREEN_600, size=16),
                                    ft.Text("High", size=13, color=ft.Colors.GREY_600, weight=ft.FontWeight.W_500)
                                ], spacing=5),
                                ft.Text(f"${float(latest_data['2. high']):.2f}", size=24, weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.GREY_900),
                            ], spacing=8),
                            padding=20,
                            bgcolor=ft.Colors.WHITE,
                            border_radius=12,
                            expand=True,
                            shadow=ft.BoxShadow(
                                spread_radius=0,
                                blur_radius=10,
                                color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                                offset=ft.Offset(0, 2)
                            )
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Icon(ft.Icons.TRENDING_DOWN, color=ft.Colors.RED_600, size=16),
                                    ft.Text("Low", size=13, color=ft.Colors.GREY_600, weight=ft.FontWeight.W_500)
                                ], spacing=5),
                                ft.Text(f"${float(latest_data['3. low']):.2f}", size=24, weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.GREY_900),
                            ], spacing=8),
                            padding=20,
                            bgcolor=ft.Colors.WHITE,
                            border_radius=12,
                            expand=True,
                            shadow=ft.BoxShadow(
                                spread_radius=0,
                                blur_radius=10,
                                color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                                offset=ft.Offset(0, 2)
                            )
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Icon(ft.Icons.STOP_CIRCLE_OUTLINED, color=ft.Colors.PURPLE_600, size=16),
                                    ft.Text("Close", size=13, color=ft.Colors.GREY_600, weight=ft.FontWeight.W_500)
                                ], spacing=5),
                                ft.Text(f"${float(latest_data['4. close']):.2f}", size=24, weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.GREY_900),
                            ], spacing=8),
                            padding=20,
                            bgcolor=ft.Colors.WHITE,
                            border_radius=12,
                            expand=True,
                            shadow=ft.BoxShadow(
                                spread_radius=0,
                                blur_radius=10,
                                color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                                offset=ft.Offset(0, 2)
                            )
                        ),
                    ], spacing=15)
                ], spacing=20),
                padding=25,
                bgcolor=ft.Colors.WHITE,
                border_radius=15,
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=20,
                    color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                    offset=ft.Offset(0, 4)
                )
            )
            price_info.current.visible = True

            # Enhanced chart
            chart = ft.LineChart(
                data_series=[
                    ft.LineChartData(
                        data_points=[
                            ft.LineChartDataPoint(i, closes[i])
                            for i in range(len(closes))
                        ],
                        stroke_width=3,
                        color=ft.Colors.BLUE_700,
                        curved=True,
                        stroke_cap_round=True,
                        below_line_bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLUE_700),
                    ),
                ],
                border=ft.Border(
                    bottom=ft.BorderSide(2, ft.Colors.GREY_300),
                    left=ft.BorderSide(2, ft.Colors.GREY_300),
                ),
                left_axis=ft.ChartAxis(
                    labels_size=50,
                ),
                bottom_axis=ft.ChartAxis(
                    labels_size=40,
                    labels_interval=max(1, len(closes) // 10),
                ),
                tooltip_bgcolor=ft.Colors.with_opacity(.9, ft.Colors.GREY_900),
                min_y=min(closes) * .95,
                max_y=max(closes) * 1.05,
                min_x=0,
                max_x=len(closes) - 1,
                expand=True
            )

            chart_container.current.content = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.SHOW_CHART, color=ft.Colors.BLUE_700, size=24),
                        ft.Text(f"Closing Price - {get_range_label(time_range)}",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.GREY_900),
                    ], spacing=10),
                    ft.Container(
                        content=chart,
                        padding=ft.padding.only(top=20, right=10, bottom=10, left=0),
                        height=350
                    )
                ], spacing=15),
                padding=25,
                bgcolor=ft.Colors.WHITE,
                border_radius=15,
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=20,
                    color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                    offset=ft.Offset(0, 4)
                )
            )
            chart_container.current.visible = True
            price_text_below.current.visible = False

        except Exception as e:
            error_messages.current.content = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.ERROR_OUTLINE, color=ft.Colors.RED_400, size=24),
                        ft.Text("Error Fetching Data", color=ft.Colors.RED_700, size=16, weight=ft.FontWeight.BOLD)
                    ], spacing=10),
                    ft.Text(str(e), color=ft.Colors.RED_600, size=14)
                ], spacing=10),
                padding=20,
                bgcolor=ft.Colors.RED_50,
                border_radius=12,
                border=ft.border.all(1, ft.Colors.RED_200),
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=10,
                    color=ft.Colors.with_opacity(0.1, ft.Colors.RED),
                    offset=ft.Offset(0, 2)
                )
            )
            error_messages.current.visible = True
            price_info.current.visible = False
            price_text_below.current.visible = False
            chart_container.current.visible = False

        page.update()

    # UI Layout
    page.add(
        ft.Column([
            # Header with gradient
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.TRENDING_UP, size=36, color=ft.Colors.WHITE),
                        ft.Text("Jonathan Stocks", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ], spacing=12),
                    ft.Text("Real-time stock market data and visualization",
                            size=16,
                            color=ft.Colors.with_opacity(0.9, ft.Colors.WHITE),
                            weight=ft.FontWeight.W_400)
                ], spacing=8, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=40,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_left,
                    end=ft.alignment.bottom_right,
                    colors=[ft.Colors.BLUE_700, ft.Colors.BLUE_900]
                ),
                alignment=ft.alignment.center
            ),

            # Main content area
            ft.Container(
                content=ft.Column([
                    # Search controls
                    ft.Container(
                        content=ft.Row([
                            ft.TextField(
                                ref=stock_symbol,
                                label="Stock Symbol",
                                hint_text="AAPL, GOOGL, MSFT",
                                width=280,
                                autofocus=True,
                                on_submit=fetch_stock_data,
                                border_radius=10,
                                prefix_icon=ft.Icons.SEARCH,
                                bgcolor=ft.Colors.WHITE,
                                border_color=ft.Colors.GREY_300,
                                focused_border_color=ft.Colors.BLUE_700,
                            ),
                            ft.Dropdown(
                                ref=time_range_dropdown,
                                label="Time Range",
                                width=180,
                                options=[
                                    ft.dropdown.Option("1 week"),
                                    ft.dropdown.Option("2 weeks"),
                                    ft.dropdown.Option("30 days"),
                                    ft.dropdown.Option("90 days"),
                                    ft.dropdown.Option("1 year"),
                                    ft.dropdown.Option("5 years"),
                                ],
                                value="30 days",
                                border_radius=10,
                                bgcolor=ft.Colors.WHITE,
                                border_color=ft.Colors.GREY_300,
                                focused_border_color=ft.Colors.BLUE_700,
                            ),
                            ft.ElevatedButton(
                                "Get Stock Data",
                                icon=ft.Icons.SHOW_CHART,
                                on_click=fetch_stock_data,
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.BLUE_700,
                                    padding=20,
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                ),
                                height=56,
                            ),
                        ], spacing=15, alignment=ft.MainAxisAlignment.CENTER),
                        padding=30,
                        bgcolor=ft.Colors.WHITE,
                        border_radius=15,
                        shadow=ft.BoxShadow(
                            spread_radius=0,
                            blur_radius=20,
                            color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                            offset=ft.Offset(0, 4)
                        )
                    ),

                    # Error messages
                    ft.Container(
                        ref=error_messages,
                        content=ft.Text(""),
                        visible=False
                    ),

                    # Price info
                    ft.Container(
                        ref=price_info,
                        visible=False
                    ),

                    # Chart container
                    ft.Container(
                        ref=chart_container,
                        visible=False
                    ),

                    # Price text below (hidden in new design)
                    ft.Container(
                        ref=price_text_below,
                        visible=False
                    ),
                ], spacing=25),
                padding=30,
                expand=True
            )
        ], spacing=0, scroll=ft.ScrollMode.AUTO)
    )

if __name__ == '__main__':
    ft.app(target=main)
