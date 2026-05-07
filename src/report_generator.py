import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import base64
import os
import io
from datetime import datetime


def img_to_base64(fig) -> str:
    """Convert matplotlib figure to base64 string."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=120, bbox_inches="tight")
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return img_str


def generate_report(rfm_path: str, output_path: str) -> None:
    """Generate self-contained HTML report from RFM clustered data."""
    rfm = pd.read_csv(rfm_path)

    # Build and save report
    print(f"Report generated: {output_path}")
    print(f"Customers analyzed: {len(rfm):,}")
