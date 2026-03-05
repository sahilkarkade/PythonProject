import pandas as pd
import matplotlib.pyplot as plt
import sys


def load_data(filename):
    """Load recruitment data from CSV file with error handling"""
    try:
        df = pd.read_csv(filename)
        print(f"✅ Successfully loaded data from {filename}")
        print(f"   Total records: {len(df)}\n")
        return df
    except FileNotFoundError:
        print(f"❌ Error: File '{filename}' not found!")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        sys.exit(1)


def display_dataset(df):
    """Display first few rows of dataset"""
    print("=" * 60)
    print("📋 DATASET PREVIEW")
    print("=" * 60)
    print(df.head(10))
    print(f"\nDataset shape: {df.shape}\n")


def group_by_company(df):
    """Group data by company and calculate total hires"""
    print("=" * 60)
    print("🏢 TOTAL HIRES BY COMPANY")
    print("=" * 60)
    company_group = df.groupby("Company")["Hires"].sum().sort_values(ascending=False)
    print(company_group)
    print()
    return company_group


def group_by_role(df):
    """Group data by role and calculate total hires"""
    print("=" * 60)
    print("👨‍💼 TOTAL HIRES BY ROLE")
    print("=" * 60)
    role_group = df.groupby("Role")["Hires"].sum().sort_values(ascending=False)
    print(role_group)
    print()
    return role_group


def calculate_quarterly_growth(df):
    """Calculate recruitment growth from Q1 to Q4"""
    print("=" * 60)
    print("📈 QUARTERLY BREAKDOWN BY COMPANY")
    print("=" * 60)
    growth = df.pivot_table(index="Company", columns="Quarter", values="Hires", aggfunc="sum")
    print(growth)
    print()
    return growth


def find_highest_growth(df):
    """Find company with highest growth in last quarter"""
    print("=" * 60)
    print("🎯 RECRUITMENT GROWTH ANALYSIS (Q1 to Q4)")
    print("=" * 60)
    
    growth = df.pivot_table(index="Company", columns="Quarter", values="Hires", aggfunc="sum")
    growth["Q1-Q4 Growth"] = growth["Q4"] - growth["Q1"]
    growth["Growth %"] = ((growth["Q4"] - growth["Q1"]) / growth["Q1"] * 100).round(2)
    
    print(growth[["Q1", "Q4", "Q1-Q4 Growth", "Growth %"]])
    print()
    
    highest_growth_company = growth["Q1-Q4 Growth"].idxmax()
    highest_growth_value = growth["Q1-Q4 Growth"].max()
    highest_growth_pct = growth.loc[highest_growth_company, "Growth %"]
    
    print(f"🏆 Company with Highest Recruitment Growth: {highest_growth_company}")
    print(f"   Growth: {highest_growth_value} hires ({highest_growth_pct}%)\n")
    
    return highest_growth_company, growth


def visualize_hiring_trends(company_group):
    """Create bar chart for hiring trends by company"""
    plt.figure(figsize=(10, 6))
    company_group.plot(kind="bar", color='steelblue', edgecolor='black')
    plt.title("Total Hiring by Company (Q1-Q4)", fontsize=14, fontweight='bold')
    plt.xlabel("Company", fontsize=12)
    plt.ylabel("Total Hires", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()


def visualize_role_distribution(role_group):
    """Create pie chart for role distribution"""
    plt.figure(figsize=(8, 6))
    role_group.plot(kind="pie", autopct='%1.1f%%', colors=['#FF9999', '#66B2FF'])
    plt.title("Hiring Distribution by Role", fontsize=14, fontweight='bold')
    plt.ylabel("")
    plt.tight_layout()
    plt.show()


def visualize_quarterly_trends(df):
    """Create line chart for quarterly trends"""
    quarterly_total = df.groupby("Quarter")["Hires"].sum()
    
    plt.figure(figsize=(10, 6))
    quarterly_total.plot(kind="line", marker="o", linewidth=2, markersize=8, color='green')
    plt.title("Total Hiring Trend by Quarter", fontsize=14, fontweight='bold')
    plt.xlabel("Quarter", fontsize=12)
    plt.ylabel("Total Hires", fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def visualize_company_quarterly_trends(df):
    """Create line chart for each company's quarterly trends"""
    plt.figure(figsize=(12, 6))
    
    for company in df["Company"].unique():
        company_data = df[df["Company"] == company].groupby("Quarter")["Hires"].sum()
        plt.plot(company_data.index, company_data.values, marker="o", label=company, linewidth=2)
    
    plt.title("Quarterly Hiring Trends by Company", fontsize=14, fontweight='bold')
    plt.xlabel("Quarter", fontsize=12)
    plt.ylabel("Total Hires", fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def display_menu():
    """Display menu options"""
    print("\n" + "=" * 60)
    print("🎯 RECRUITMENT & HR ANALYTICS PORTAL")
    print("=" * 60)
    print("1. View Dataset")
    print("2. Total Hires by Company")
    print("3. Total Hires by Role")
    print("4. Quarterly Breakdown")
    print("5. Find Highest Growth Company")
    print("6. Visualize Company Hiring Trends (Bar Chart)")
    print("7. Visualize Role Distribution (Pie Chart)")
    print("8. Visualize Quarterly Trends (Line Chart)")
    print("9. Visualize Company Quarterly Trends (Line Chart)")
    print("10. Run Full Analysis & All Visualizations")
    print("11. Exit")
    print("=" * 60)


def main():
    """Main program function"""
    df = load_data("recruitment_data.csv")
    
    while True:
        display_menu()
        choice = input("Select an option (1-11): ").strip()
        
        try:
            if choice == "1":
                display_dataset(df)
            elif choice == "2":
                group_by_company(df)
            elif choice == "3":
                group_by_role(df)
            elif choice == "4":
                calculate_quarterly_growth(df)
            elif choice == "5":
                find_highest_growth(df)
            elif choice == "6":
                company_group = group_by_company(df)
                visualize_hiring_trends(company_group)
            elif choice == "7":
                role_group = group_by_role(df)
                visualize_role_distribution(role_group)
            elif choice == "8":
                visualize_quarterly_trends(df)
            elif choice == "9":
                visualize_company_quarterly_trends(df)
            elif choice == "10":
                print("\n🚀 Running Full Analysis...\n")
                display_dataset(df)
                company_group = group_by_company(df)
                role_group = group_by_role(df)
                calculate_quarterly_growth(df)
                find_highest_growth(df)
                print("\n📊 Generating Visualizations...")
                visualize_hiring_trends(company_group)
                visualize_role_distribution(role_group)
                visualize_quarterly_trends(df)
                visualize_company_quarterly_trends(df)
            elif choice == "11":
                print("\n✅ Thank you for using HR Analytics Portal. Goodbye!")
                break
            else:
                print("❌ Invalid option! Please select 1-11.\n")
        except Exception as e:
            print(f"❌ An error occurred: {e}\n")


if __name__ == "__main__":
    main()
