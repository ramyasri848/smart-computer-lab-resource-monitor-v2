import streamlit as st
from cpu_monitor import get_cpu_info
from memory_monitor import get_memory_info
from disk_monitor import get_disk_info, get_drive_info
from process_monitor import (
    get_processes,
    get_process_names,
    get_top_cpu_processes,
    get_top_memory_processes
)
from health_score import calculate_health_score
from alert_manager import get_alerts
from logger import log_system_data
import pandas as pd
import plotly.express as px
from analytics import get_analytics
from report_generator import (
    generate_report,
    generate_pdf_report
)
import os
from background_monitor import start_monitoring
from api_client import (
    get_summary,
    get_latest_machines,
    get_critical_machines
)

def show_live_graphs():

    try:

        df = pd.read_csv(
            "logs/system_log.csv"
        )

        if len(df) > 50:
            df = df.tail(50)

        st.subheader("CPU Usage Trend")

        cpu_fig = px.line(
            df,
            y="CPU Usage",
            title="CPU Usage Over Time"
        )

        st.plotly_chart(
            cpu_fig,
            width="stretch"
        )

        st.subheader("RAM Usage Trend")

        ram_fig = px.line(
            df,
            y="RAM Usage",
            title="RAM Usage Over Time"
        )

        st.plotly_chart(
            ram_fig,
            width="stretch"
        )

        st.subheader("Disk Usage Trend")

        disk_fig = px.line(
            df,
            y="Disk Usage",
            title="Disk Usage Over Time"
        )

        st.plotly_chart(
            disk_fig,
            width="stretch"
        )

    except Exception:

        st.info(
            "Not enough log data available yet."
        )

# Page Configuration
st.set_page_config(
    page_title="Smart Computer Lab Resource Monitoring & Analytics System",
    layout="wide"
)

start_monitoring()

# Title
st.title("Smart Computer Lab Resource Monitoring & Analytics System")

# Sidebar Navigation
st.sidebar.title("Navigation")

menu = st.sidebar.radio(
    "Select Module",
    [
        "Dashboard",
        "Central Dashboard",
        "CPU Monitor",
        "Memory Monitor",
        "Disk Monitor",
        "Process Monitor",
        "Network Monitor",
        "Analytics",
        "Reports"
    ]
)

# Dashboard
if menu == "Dashboard":

    st.header("Dashboard")

    log_system_data()

    st.write(
        "Welcome to the Smart Computer Lab Resource Monitoring & Analytics System"
    )

    health = calculate_health_score()

    st.subheader("System Health Score")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Health Score",
            f"{health['score']}/100"
        )

    with col2:
        st.metric(
            "System Status",
            health["status"]
        )

    st.divider()

    st.subheader("System Alerts")

    alerts = get_alerts()

    if alerts:

        for alert in alerts:
            st.warning(alert)

    else:
        st.success(
            "✅ No alerts detected. System is operating normally."
        )
        st.divider()

        show_live_graphs()
        #Central Dashboard
elif menu == "Central Dashboard":

    st.header(
        "Central Monitoring Dashboard"
    )

    summary = get_summary()
    
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Machines",
            summary["total_machines"]
        )

    with col2:
        st.metric(
            "Avg CPU",
            f"{summary['average_cpu_usage']}%"
        )

    with col3:
        st.metric(
            "Avg RAM",
            f"{summary['average_ram_usage']}%"
        )

    with col4:
        st.metric(
            "Avg Disk",
            f"{summary['average_disk_usage']}%"
        )

    st.divider()

    st.subheader(
        "Latest Machine Status"
    )

    latest = get_latest_machines()

    st.dataframe(
        latest["machines"],
        width="stretch"
    )

    st.divider()

    st.subheader(
        "Machines Requiring Attention"
    )

    critical = get_critical_machines()

    st.dataframe(
        critical["critical_machines"],
        width="stretch"
    )
# Memory Monitor
elif menu == "Memory Monitor":
    st.header("Memory Monitor")

    memory = get_memory_info()

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total RAM (GB)",
            memory["total_ram"]
        )

        st.metric(
            "Used RAM (GB)",
            memory["used_ram"]
        )

        st.metric(
            "RAM Usage (%)",
            f"{memory['ram_usage']}%"
        )

    with col2:
        st.metric(
            "Available RAM (GB)",
            memory["available_ram"]
        )

        st.metric(
            "Swap Total (GB)",
            memory["swap_total"]
        )

        st.metric(
            "Swap Used (GB)",
            memory["swap_used"]
        )

# Disk Monitor
elif menu == "Disk Monitor":
    st.header("Disk Monitor")

    disk = get_disk_info()

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Storage (GB)",
            disk["total"]
        )

        st.metric(
            "Used Storage (GB)",
            disk["used"]
        )

    with col2:
        st.metric(
            "Free Storage (GB)",
            disk["free"]
        )

        st.metric(
            "Disk Usage (%)",
            f"{disk['percent']}%"
        )

    st.subheader("Drive Information")

    drives = get_drive_info()

    for drive in drives:
        st.write(f"### {drive['drive']}")
        st.write(f"Total: {drive['total']} GB")
        st.write(f"Used: {drive['used']} GB")
        st.write(f"Free: {drive['free']} GB")
        st.write(f"Usage: {drive['percent']}%")


# Process Monitor
elif menu == "Process Monitor":

    st.header("Process Monitor")

    process_names = get_process_names()

    selected_process = st.selectbox(
        "Search Process",
        options=[""] + process_names
    )

    processes = get_processes(selected_process)

    st.subheader("Running Processes")

    st.dataframe(
        processes,
        width="stretch"
    )

    st.success(
        f"Total Processes Found: {len(processes)}"
    )

    st.divider()

    st.subheader("Top CPU Consumers")

    cpu_df = get_top_cpu_processes()

    st.dataframe(
        cpu_df,
        width="stretch"
    )

    st.divider()

    st.subheader("Top Memory Consumers")

    memory_df = get_top_memory_processes()

    st.dataframe(
        memory_df,
        width="stretch"
    )
# Network Monitor
elif menu == "Network Monitor":
    st.header("Network Monitor")
    st.info("Network Monitoring Module Coming Soon")

# Analytics
elif menu == "Analytics":

    st.header("Analytics Dashboard")

    analytics = get_analytics()

    if analytics:

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Average CPU Usage",
                f"{analytics['avg_cpu']}%"
            )

        with col2:
            st.metric(
                "Average RAM Usage",
                f"{analytics['avg_ram']}%"
            )

        with col3:
            st.metric(
                "Average Disk Usage",
                f"{analytics['avg_disk']}%"
            )

        st.divider()

        col4, col5, col6 = st.columns(3)

        with col4:
            st.metric(
                "Highest CPU Usage",
                f"{analytics['max_cpu']}%"
            )

        with col5:
            st.metric(
                "Highest RAM Usage",
                f"{analytics['max_ram']}%"
            )

        with col6:
            st.metric(
                "Highest Disk Usage",
                f"{analytics['max_disk']}%"
            )

    else:
        st.warning(
            "No analytics data available."
        )
    
# Reports
elif menu == "Reports":

    st.header("Reports")

    if st.button(
        "Generate Daily Report"
    ):

        success = generate_report()

        if success:

            st.success(
                "CSV Report Generated Successfully!"
            )

        else:

            st.error(
                "Unable to Generate CSV Report."
            )

    if st.button(
        "Generate PDF Report"
    ):

        success = generate_pdf_report()

        if success:

            st.success(
                "PDF Report Generated Successfully!"
            )

        else:

            st.error(
                "Unable to Generate PDF Report."
            )

    csv_path = (
        "reports/daily_report.csv"
    )

    if os.path.exists(
        csv_path
    ):

        with open(
            csv_path,
            "rb"
        ) as file:

            st.download_button(
                label="Download CSV Report",
                data=file,
                file_name="daily_report.csv",
                mime="text/csv"
            )

    pdf_path = (
        "reports/daily_report.pdf"
    )

    if os.path.exists(
        pdf_path
    ):

        with open(
            pdf_path,
            "rb"
        ) as file:

            st.download_button(
                label="Download PDF Report",
                data=file,
                file_name="daily_report.pdf",
                mime="application/pdf"
            )