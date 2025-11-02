# my_server.py
from fastmcp import FastMCP

# Give your server a friendly name (clients will see this)
mcp = FastMCP("Render Demo")

# --- Example tools (add your own!) ---

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@mcp.tool
def echo(text: str) -> str:
    """Echo text back to the caller."""
    return text

@mcp.tool
def doc_titles() -> list[str]:
    """gives titles of all doc sections"""
    return ["Step-by-step tutorial", "Session specification", "Plots"]

@mcp.tool
def plot_types() -> list[str]:
    "gives the types of plot dbslice can handle"
    return ["Bar chart", "Scatter plot", "Histogram", "Grouped vertical bar chart", "Circle pack plot", "Response surface scatter plot", "Line plot", "Surface plot from unstructured data"]

SECTION_CONTENT: dict[str, str] = {
    "Step-by-step tutorial": (
        "Use this quickstart to spin up the Testbox demo locally.\n"
        "\n"
        "Data bundle layout:\n"
        "- Top level files: `index.html`, `session.json`, and a `data` directory.\n"
        "- `data/metaData.csv` stores the metadata table; each row has a folder like `case_0` with JSON payloads (for example `f_line_xmid.json`).\n"
        "\n"
        "Host the app:\n"
        "- From the project directory run `python -m SimpleHTTPServer 8000` (Python 2) or `python3 -m http.server 8000` (Python 3).\n"
        "- Open `http://localhost:8000` to render the single page app.\n"
        "\n"
        "`index.html` essentials:\n"
        "- Includes the dbslice bundle from the jsDelivr CDN and provides a `<div id=\"target\">` placeholder.\n"
        "- Calls `dbslice.start(\"target\", \"session.json\")`, so the static server must serve that JSON alongside the HTML.\n"
        "\n"
        "`session.json` primer:\n"
        "- `title` names the experience (for example \"3D box of data demo\").\n"
        "- `metaDataConfig` defines how metadata is loaded (`metaDataUrl`, `metaDataCsv`), how task IDs are generated (`generateTaskIds`, `taskIdRoot`, `taskIdFormat`), and how labels appear (`setLabelsToTaskIds`).\n"
        "- `uiConfig` toggles helper buttons such as `plotTasksButton`.\n"
        "- `plotRows` lists each layout row; a row can embed explicit `plots` or supply a `ctrl` block that auto-builds plots per filtered task.\n"
    ),
    "Session specification": (
        "Every dbslice session is described by a JSON document (commonly `session.json`).\n"
        "\n"
        "Core structure:\n"
        "- `metaDataConfig`: points to the metadata table (`metaDataUrl`), declares the format (`metaDataCsv`), and controls task identifier strategy (`generateTaskIds`, `taskIdRoot`, `taskIdFormat`, `setLabelsToTaskIds`).\n"
        "- `uiConfig`: enables or hides UI controls such as `plotTasksButton` and `saveTasksButton`.\n"
        "- `plotRows`: array of layout sections. Each entry may contain ready-made `plots` or a `ctrl` object that generates plots dynamically for each task.\n"
        "\n"
        "Plot anatomy reminders:\n"
        "- A `layout` object is always required. It defines size (`colWidth`, `height`), titles, and optional helpers like `highlightTasks` or dropdown selectors.\n"
        "- Choose between inline `data` and remote `fetchData`. Use `data` when the visualization relies solely on metadata, or `fetchData` when per-task files are needed.\n"
        "- `fetchData` accepts templates (`urlTemplate` with `${taskId}`), filtering controls (`tasksByFilter`, `maxTasks`), auto-refresh options, and transformation hooks via `dataFilterType` and `dataFilterConfig`.\n"
        "\n"
        "Refer to this structure when authoring or troubleshooting session files so that fields land in the correct block.\n"
    ),
    "Plots": (
        "Plot definitions fall into two families: metadata-driven charts that read directly from the filtered table, and detailed charts that fetch per-task assets.\n"
        "\n"
        "Metadata charts:\n"
        "- Bar chart (`cfD3BarChart`): set `data.property` to a categorical column; optional layout flags cover task highlighting, selectable properties, and custom colour maps.\n"
        "- Scatter plot (`cfD3Scatter`): requires `xProperty` and `yProperty` from continuous columns and a categorical `cProperty` for colour; supports fixed axis ranges, grouping, ordering, and opacity tweaks.\n"
        "- Histogram (`cfD3Histogram`): supply a continuous `data.property`; layout options enable property dropdowns, bar colour overrides, and hiding zero-count bins.\n"
        "- Grouped vertical bar (`cfD3GroupedVertBarChart`): pair categorical `xProperty`/`zProperty` with a continuous `yProperty`; optional `filterBy` applies extra categorical filters before plotting.\n"
        "- Circle pack (`cfD3CirclePack`): `data.property` sets the outer grouping while `layout.groupBy` defines inner levels; colouring can follow metadata values or a custom palette.\n"
        "- Response surface scatter (`cfD3ResSurfScatter`): specify the response metric (`xProperty`), predictor list (`inputProperties`), colour dimension (`cProperty`), and model type (for example `quadDiag`).\n"
        "\n"
        "Detailed data charts:\n"
        "- Line plot (`d3LineSeries`): fetch per-task JSON or CSV via `urlTemplate`; combine files with filters such as `lineSeriesFromLines` or `lineSeriesFromCsv`; `dataFilterConfig` can colour lines and map CSV columns.\n"
        "- Surface plot from unstructured data (`threeTriMesh`): deliver binary `.tm3` buffers; a `ctrl` block often iterates tasks, sets `buffer: true`, and limits `maxTasks` while `layout` handles size and optional camera sync.\n"
        "\n"
        "When adding new visuals, start with the nearest example above and adjust `plotType`, `data`, `fetchData`, and `layout` for your scenario.\n"
    ),
}

@mcp.tool
def get_section_content(section: str) -> str:
    """takes the section name and returns the content of that section"""
    key = section.strip()
    try:
        return SECTION_CONTENT[key]
    except KeyError as exc:
        raise ValueError(f"Unknown section: {section}") from exc

@mcp.tool
def bayesian_forcast_image() -> dict:
    return {"image_url": "bayesian_forecasting_testset.png"}

# Expose an ASGI application for deployment (served by uvicorn on Render)
app = mcp.http_app()

# Optional: local dev HTTP run (uncomment to run locally via `python my_server.py`)
# if __name__ == "__main__":
#     # For local testing over HTTP
#     # Visit http://127.0.0.1:8000 (MCP is a protocol; expect non-HTML responses)
#     mcp.run(transport="http", host="127.0.0.1", port=8000)
