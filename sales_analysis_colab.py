# ============================================================
#  Sales Data Analysis - Google Colab Script
#  Charts: Bar, Line, Pie | Source: sales_data.csv
# ============================================================

# ── STEP 1: Upload your sales_data.csv ──────────────────────
from google.colab import files
uploaded = files.upload()   # select sales_data.csv when prompted

# ── STEP 2: Install & Import ─────────────────────────────────
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import warnings
warnings.filterwarnings('ignore')

# ── STEP 3: Load & Clean Data ────────────────────────────────
df = pd.read_csv('sales_data.csv')
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.to_period('M')
df.dropna(inplace=True)

print("✅ Data loaded successfully!")
print(f"   Rows: {len(df)} | Columns: {list(df.columns)}")
print(df.head())

# ── STEP 4: Analysis ─────────────────────────────────────────
sales_by_product = df.groupby('Product')['Total_Sales'].sum().sort_values(ascending=False)
sales_by_month   = df.groupby('Month')['Total_Sales'].sum()
sales_by_region  = df.groupby('Region')['Total_Sales'].sum()

print("\n📊 Sales by Product:\n", sales_by_product)
print("\n📅 Sales by Month:\n",   sales_by_month)
print("\n🌍 Sales by Region:\n",  sales_by_region)

# ── STEP 5: Chart Style ──────────────────────────────────────
COLORS  = ['#534AB7','#1D9E75','#D85A30','#378ADD','#D4537E','#BA7517']
plt.rcParams.update({'figure.facecolor': 'white', 'axes.facecolor': '#F8F8FF',
                     'font.family': 'DejaVu Sans', 'axes.grid': True,
                     'grid.linestyle': '--', 'grid.alpha': 0.5})

fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle('Sales Performance Analysis', fontsize=16, fontweight='bold', y=1.02)

# ── Chart 1: Bar – Sales by Product ─────────────────────────
ax1 = axes[0]
bars = ax1.bar(sales_by_product.index, sales_by_product.values / 1000,
               color=COLORS[:len(sales_by_product)], edgecolor='white', linewidth=0.8,
               zorder=3)
ax1.set_title('Sales by Product Category', fontsize=13, fontweight='bold')
ax1.set_xlabel('Product')
ax1.set_ylabel('Revenue (₹ Thousands)')
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'₹{x:.0f}K'))
for bar in bars:
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50,
             f'₹{bar.get_height():.0f}K', ha='center', va='bottom',
             fontsize=8, fontweight='bold', color='#333')
ax1.set_axisbelow(True)

# ── Chart 2: Line – Monthly Trend ───────────────────────────
ax2 = axes[1]
months = [str(m) for m in sales_by_month.index]
values = sales_by_month.values / 1000
ax2.plot(months, values, color='#534AB7', linewidth=2.5, marker='o',
         markersize=8, markerfacecolor='white', markeredgewidth=2, zorder=3)
ax2.fill_between(months, values, alpha=0.1, color='#534AB7')
ax2.set_title('Monthly Sales Trend', fontsize=13, fontweight='bold')
ax2.set_xlabel('Month')
ax2.set_ylabel('Revenue (₹ Thousands)')
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'₹{x:.0f}K'))
for m, v in zip(months, values):
    ax2.annotate(f'₹{v:.0f}K', (m, v), textcoords='offset points',
                 xytext=(0, 10), ha='center', fontsize=8,
                 color='#534AB7', fontweight='bold')
ax2.set_axisbelow(True)

# ── Chart 3: Pie – Regional Distribution ────────────────────
ax3 = axes[2]
wedges, texts, autotexts = ax3.pie(
    sales_by_region.values,
    labels=sales_by_region.index,
    autopct='%1.1f%%',
    colors=COLORS[:len(sales_by_region)],
    startangle=140,
    pctdistance=0.75,
    wedgeprops={'edgecolor': 'white', 'linewidth': 2}
)
for t in autotexts:
    t.set_fontsize(9)
    t.set_fontweight('bold')
ax3.set_title('Sales by Region', fontsize=13, fontweight='bold')

plt.tight_layout()
plt.savefig('sales_charts.png', dpi=150, bbox_inches='tight')
plt.show()
print("\n✅ Charts saved as sales_charts.png")

# ── STEP 6: Key Insights ─────────────────────────────────────
total = df['Total_Sales'].sum()
print("\n" + "="*45)
print("         KEY INSIGHTS")
print("="*45)
print(f"  Total Revenue     : ₹{total:,.0f}")
print(f"  Total Orders      : {len(df)}")
print(f"  Avg Order Value   : ₹{df['Total_Sales'].mean():,.0f}")
print(f"  Best Product      : {sales_by_product.idxmax()}")
print(f"  Top Region        : {sales_by_region.idxmax()}")
print(f"  Peak Month        : {sales_by_month.idxmax()}")
print("="*45)

# ── STEP 7: Download chart ───────────────────────────────────
files.download('sales_charts.png')
