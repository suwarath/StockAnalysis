from evidently.ui.workspace import Workspace
from evidently.ui.dashboards import DashboardPanelCounter, DashboardPanelPlot, CounterAgg, PanelValue, PlotType, ReportFilter
from evidently.renderers.html_widgets import WidgetSize

ws = Workspace("./monitoring/workspace")

if ws.search_project("Stock Trade Action Project") == []:
    project = ws.create_project("Stock Trade Action Project")
    project.save()
else:
    project = ws.search_project("Stock Trade Action Project")[0]
    
project.dashboard.add_panel(
    DashboardPanelCounter(
        filter=ReportFilter(metadata_values={}, tag_values=[]),
        agg=CounterAgg.NONE,
        title="Stock Trade Action Dashboard"
    )
)

project.dashboard.add_panel(
    DashboardPanelPlot(
        filter=ReportFilter(metadata_values={}, tag_values=[]),
        title="Number of Missing Values",
        values=[
            PanelValue(
                metric_id="DatasetSummaryMetric",
                field_path="current.number_of_missing_values",
                legend="count"
            ),
        ],
        plot_type=PlotType.LINE,
        size=WidgetSize.HALF,
    ),
)

project.dashboard.add_panel(
    DashboardPanelPlot(
        filter=ReportFilter(metadata_values={}, tag_values=[]),
        title="Open and Close Price",
        values=[
            PanelValue(
                metric_id="ColumnSummaryMetric",
                field_path="current_characteristics.mean",
                metric_args={"column_name.name": "Open"},
                legend="Open",
            ),
            PanelValue(
                metric_id="ColumnSummaryMetric",
                field_path="current_characteristics.mean",
                metric_args={"column_name.name": "Close"},
                legend="Close",
            ),
        ],
        plot_type=PlotType.LINE,
        size=WidgetSize.HALF,
    ),
)

project.save()