from django.apps import AppConfig


class DashboardConfig(AppConfig):
    name = 'dashboard'

    def ready(self):
        import dashboard.dash_apps.finished_apps.bitcoin_dominance
        import dashboard.dash_apps.finished_apps.candlestick
        import dashboard.dash_apps.finished_apps.fear_greed_chart
        import dashboard.dash_apps.finished_apps.market_cap
        import dashboard.dash_apps.finished_apps.volume
        import dashboard.dash_apps.finished_apps.table
