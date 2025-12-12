import matplotlib.pyplot as plt
import matplotlib.patches as patches

def plot_rf_internal_logic():
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')

    bbox_args = dict(boxstyle="round,pad=0.3", fc="white", ec="black", lw=2)
    leaf_args = dict(boxstyle="circle,pad=0.3", fc="#e63946", ec="black", lw=2) # Red for leaves
    arrow_args = dict(arrowstyle="->", color="#333", lw=2)

    ax.text(8, 9.5, "New Customer Instance", ha="center", fontsize=14, fontweight="bold")
    ax.text(8, 9.0, "Tenure: 55 Months\nMonthly Charges: $40\nContract: 2-Year", 
            ha="center", va="center", bbox=dict(boxstyle="round,pad=0.5", fc="#a8dadc", ec="black"))

    x_t1 = 3
    ax.text(x_t1, 7.5, "Tree #1", ha="center", fontsize=12, fontweight="bold", color="#1d3557")
    
    ax.text(x_t1, 6.5, "Tenure < 24?", ha="center", bbox=bbox_args, fontsize=9)
    ax.annotate("Yes", xy=(x_t1-1, 5.0), xytext=(x_t1, 6.2), arrowprops=arrow_args, fontsize=8, ha="right")
    ax.annotate("No", xy=(x_t1+1, 5.0), xytext=(x_t1, 6.2), arrowprops=dict(arrowstyle="->", color="green", lw=3), fontsize=8, ha="left") # Green path = active path
    
    ax.text(x_t1-1, 5.0, "High Risk", ha="center", alpha=0.3) # Faded
    ax.text(x_t1+1, 5.0, "Contract\nMonth-to-Month?", ha="center", bbox=bbox_args, fontsize=9)
    
    ax.annotate("Yes", xy=(x_t1+0.5, 3.5), xytext=(x_t1+1, 4.6), arrowprops=arrow_args, fontsize=8, ha="right")
    ax.annotate("No", xy=(x_t1+1.5, 3.5), xytext=(x_t1+1, 4.6), arrowprops=dict(arrowstyle="->", color="green", lw=3), fontsize=8, ha="left")
    
    ax.text(x_t1+1.5, 3.5, "0.10", ha="center", va="center", color="white", fontweight="bold", bbox=leaf_args) # Prediction 1
    ax.text(x_t1+1.5, 2.9, "Prediction 1", ha="center", fontsize=8)

    x_t2 = 8
    ax.text(x_t2, 7.5, "Tree #2", ha="center", fontsize=12, fontweight="bold", color="#1d3557")
    
    ax.text(x_t2, 6.5, "Charges > $80?", ha="center", bbox=bbox_args, fontsize=9)
    ax.annotate("Yes", xy=(x_t2-1, 5.0), xytext=(x_t2, 6.2), arrowprops=arrow_args, fontsize=8)
    ax.annotate("No", xy=(x_t2+1, 5.0), xytext=(x_t2, 6.2), arrowprops=dict(arrowstyle="->", color="green", lw=3), fontsize=8)
    ax.text(x_t2-1, 5.0, "High Cost", ha="center", alpha=0.3)
    ax.text(x_t2+1, 5.0, "Tenure > 12?", ha="center", bbox=bbox_args, fontsize=9)
    
    ax.annotate("No", xy=(x_t2+0.5, 3.5), xytext=(x_t2+1, 4.6), arrowprops=arrow_args, fontsize=8)
    ax.annotate("Yes", xy=(x_t2+1.5, 3.5), xytext=(x_t2+1, 4.6), arrowprops=dict(arrowstyle="->", color="green", lw=3), fontsize=8)
    ax.text(x_t2+1.5, 3.5, "0.15", ha="center", va="center", color="white", fontweight="bold", bbox=leaf_args) # Prediction 2
    ax.text(x_t2+1.5, 2.9, "Prediction 2", ha="center", fontsize=8)

    x_t3 = 13
    ax.text(x_t3, 7.5, "Tree #3", ha="center", fontsize=12, fontweight="bold", color="#1d3557")
    ax.text(x_t3, 6.5, "Support Calls > 2?", ha="center", bbox=bbox_args, fontsize=9)
    ax.annotate("Yes", xy=(x_t3-1, 5.0), xytext=(x_t3, 6.2), arrowprops=arrow_args, fontsize=8)
    ax.annotate("No", xy=(x_t3+1, 5.0), xytext=(x_t3, 6.2), arrowprops=dict(arrowstyle="->", color="green", lw=3), fontsize=8)
    ax.text(x_t3-1, 5.0, "Frustrated", ha="center", alpha=0.3)
    ax.text(x_t3+1, 5.0, "Payment\nMethod = Check?", ha="center", bbox=bbox_args, fontsize=9)
    ax.annotate("Yes", xy=(x_t3+0.5, 3.5), xytext=(x_t3+1, 4.6), arrowprops=dict(arrowstyle="->", color="green", lw=3), fontsize=8)
    ax.annotate("No", xy=(x_t3+1.5, 3.5), xytext=(x_t3+1, 4.6), arrowprops=arrow_args, fontsize=8)
    ax.text(x_t3-1, 5.0, "Frustrated", ha="center", alpha=0.3)
    ax.text(x_t3+1, 5.0, "Payment\nMethod = Check?", ha="center", bbox=bbox_args, fontsize=9)
    
    ax.annotate("Yes", xy=(x_t3+0.5, 3.5), xytext=(x_t3+1, 4.6), arrowprops=dict(arrowstyle="->", color="green", lw=3), fontsize=8)
    ax.annotate("No", xy=(x_t3+1.5, 3.5), xytext=(x_t3+1, 4.6), arrowprops=arrow_args, fontsize=8)

    ax.text(x_t3+0.5, 3.5, "0.20", ha="center", va="center", color="white", fontweight="bold", bbox=leaf_args) # Prediction 3
    ax.text(x_t3+0.5, 2.9, "Prediction 3", ha="center", fontsize=8)

    ax.annotate("", xy=(x_t1, 6.9), xytext=(8, 8.5), arrowprops=dict(arrowstyle="->", color="#555", ls="--"))
    ax.annotate("", xy=(x_t2, 6.9), xytext=(8, 8.5), arrowprops=dict(arrowstyle="->", color="#555", ls="--"))
    ax.annotate("", xy=(x_t3, 6.9), xytext=(8, 8.5), arrowprops=dict(arrowstyle="->", color="#555", ls="--"))

    ax.annotate("", xy=(8, 1.5), xytext=(x_t1+1.5, 3.1), arrowprops=dict(arrowstyle="->", color="#e63946", lw=2))
    ax.annotate("", xy=(8, 1.5), xytext=(x_t2+1.5, 3.1), arrowprops=dict(arrowstyle="->", color="#e63946", lw=2))
    ax.annotate("", xy=(8, 1.5), xytext=(x_t3+0.5, 3.1), arrowprops=dict(arrowstyle="->", color="#e63946", lw=2))
    
    ax.text(8, 1.5, "AVERAGE", ha="center", va="center", fontsize=12, fontweight="bold", 
            bbox=dict(boxstyle="round,pad=0.5", fc="#457b9d", ec="none", alpha=0.2))
            
    ax.text(8, 1.0, "(0.10 + 0.15 + 0.20) / 3", ha="center", fontsize=12, fontfamily="monospace")
    
    ax.text(8, 0.3, "Final Churn Probability: 0.15", ha="center", fontsize=14, fontweight="bold", 
            color="white", bbox=dict(boxstyle="round,pad=0.5", fc="#1d3557", ec="black"))

    plt.title("Inside Random Forest: How Decisions are Averaged", fontsize=16, pad=20)
    plt.tight_layout()
    plt.show()

plot_rf_internal_logic()