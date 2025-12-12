import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_random_forest_architecture():
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off') 

    data_color = '#a8dadc'    
    tree_color = '#457b9d'    
    avg_color = '#e63946'     
    output_color = '#1d3557'  
    text_color = '#333333'
    
    rect_data_back = patches.Rectangle((1, 3.2), 1.5, 2, linewidth=1, edgecolor='black', facecolor='white', zorder=1)
    rect_data_mid = patches.Rectangle((0.9, 3.1), 1.5, 2, linewidth=1, edgecolor='black', facecolor='white', zorder=2)
    rect_data_front = patches.Rectangle((0.8, 3.0), 1.5, 2, linewidth=2, edgecolor='black', facecolor=data_color, zorder=3)
    
    ax.add_patch(rect_data_back)
    ax.add_patch(rect_data_mid)
    ax.add_patch(rect_data_front)
    
    ax.text(1.55, 2.5, "Input Data\n(Features)", ha='center', fontsize=12, fontweight='bold', color=text_color)

    tree_positions = [5.5, 4.0, 2.5] 
    
    for i, y_pos in enumerate(tree_positions):
        
        ax.annotate("", xy=(4, y_pos + 0.5), xytext=(2.3, 4.0),
                    arrowprops=dict(arrowstyle="->", color="#555", lw=2, ls="--"))
        
        rect_tree = patches.FancyBboxPatch((4, y_pos), 2, 1, boxstyle="round,pad=0.1", 
                                           linewidth=2, edgecolor='black', facecolor=tree_color)
        ax.add_patch(rect_tree)
        
        ax.text(5, y_pos + 0.5, f"Decision Tree {i+1}", ha='center', va='center', 
                color='white', fontweight='bold', fontsize=10)
        
        ax.plot([4.2, 4.5, 5.0, 5.5, 5.8], [y_pos+0.8, y_pos+0.6, y_pos+0.3, y_pos+0.6, y_pos+0.2], 
                marker='o', markersize=4, color='white', linestyle='-', lw=1, alpha=0.6)

    ax.text(5, 1.8, "...", ha='center', fontsize=20, fontweight='bold', color='#555')
    
    for y_pos in tree_positions:
        ax.annotate("", xy=(8, 4.0), xytext=(6.1, y_pos + 0.5),
                    arrowprops=dict(arrowstyle="->", color="#555", lw=2))

    circle_avg = patches.Circle((8.5, 4.0), 0.8, linewidth=2, edgecolor='black', facecolor=avg_color)
    ax.add_patch(circle_avg)
    ax.text(8.5, 4.0, "Average\n(Mean)", ha='center', va='center', 
            color='white', fontweight='bold', fontsize=11)
    
    ax.annotate("", xy=(11, 4.0), xytext=(9.3, 4.0),
                arrowprops=dict(arrowstyle="->", color="black", lw=3))
    
    rect_output = patches.Rectangle((11, 3.5), 1.5, 1, linewidth=2, edgecolor='black', facecolor=output_color)
    ax.add_patch(rect_output)
    
    ax.text(11.75, 4.0, "Churn\nProb", ha='center', va='center', 
            color='white', fontweight='bold', fontsize=12)
            
    ax.text(11.75, 3.0, "Final Regression\nValue (0.0 - 1.0)", ha='center', fontsize=10, color=text_color)

    plt.title("Random Forest Regression Architecture", fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.show()

draw_random_forest_architecture()