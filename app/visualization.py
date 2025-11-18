import base64
import io

import japanize_matplotlib
import matplotlib.pyplot as plt
import numpy as np

MOVES_LABEL = ["グー", "チョキ", "パー", "王様", "農民"]
COLORS = ["#e74c3c", "#f1c40f", "#2ecc71", "#9b59b6", "#34495e"]


def create_probability_chart(probs):
    """予測確率の棒グラフを作成しbase64文字列で返す"""
    plt.figure(figsize=(6, 3))

    # 棒グラフの描画
    bars = plt.bar(MOVES_LABEL, probs, color=COLORS, alpha=0.8)
    plt.ylim(0, 1.0)
    plt.grid(axis="y", linestyle="--", alpha=0.5)

    # 値のラベルを表示
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            height,
            f"{height*100:.0f} %",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    # 画像をバッファに保存
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close()
    buf.seek(0)

    # base64エンコード
    img_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return img_base64
