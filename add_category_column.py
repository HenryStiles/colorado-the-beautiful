# add_category_column.py
import os
import openpyxl
from openpyxl.worksheet.datavalidation import DataValidation

EXCEL_PATH = "/Users/henrys/source/colorado_the_beautiful/Outreach list.xlsx"

def main():
    if not os.path.exists(EXCEL_PATH):
        print(f"Error: Excel file not found at {EXCEL_PATH}")
        return

    print(f"Loading workbook: {EXCEL_PATH}...")
    wb = openpyxl.load_workbook(EXCEL_PATH)
    ws = wb['SUBMISSION Yeses']

    # Set up Column G header (Column 7)
    ws.cell(row=1, column=7, value="Category")
    
    # Define keywords for legislators (case-insensitive)
    legislator_keywords = ["representative", "senator", "congressman", "congresswoman", "rep.", "sen."]

    auto_legislator_count = 0
    auto_ff_count = 0
    auto_coalition_count = 0
    blank_count = 0

    print("Analyzing rows and applying category classifications...")
    
    # Iterate through rows starting from row 2
    for r_idx in range(2, ws.max_row + 1):
        name_val = ws.cell(row=r_idx, column=1).value
        type_val = ws.cell(row=r_idx, column=2).value
        
        # Skip if name is empty
        if not name_val:
            continue
            
        name_str = str(name_val).lower().strip()
        type_str = str(type_val).strip() if type_val else ""
        
        assigned_category = None
        
        # 1. Check for Legislator keywords first
        if any(kw in name_str for kw in legislator_keywords):
            assigned_category = "Legislators"
            auto_legislator_count += 1
            
        # 2. Check for Friend/Family based on Column B
        elif type_str == "Friend/Family":
            assigned_category = "Friends and family"
            auto_ff_count += 1
            
        # 3. Check for Coalition partner based on Column B
        elif type_str == "Coalition":
            assigned_category = "Coalition partners"
            auto_coalition_count += 1
            
        else:
            blank_count += 1
            
        # Write to Column G (Column 7)
        ws.cell(row=r_idx, column=7, value=assigned_category)

    # 4. Create the Data Validation dropdown menu for Column G
    print("Creating Excel dropdown validation for Column G...")
    
    # Options must be comma separated inside quotes
    options = '"Friends and family,Legislators,Professional photographers,Coalition partners"'
    
    dv = DataValidation(
        type="list",
        formula1=options,
        allow_blank=True,
        error="Your entry is not in the list",
        errorTitle="Invalid Entry",
        prompt="Please select a category from the dropdown menu",
        promptTitle="Category Selection"
    )
    
    # Add validation to the sheet
    ws.add_data_validation(dv)
    
    # Apply to G2 through G1000
    dv.add("G2:G1000")

    # Save workbook
    wb.save(EXCEL_PATH)
    
    print("\nSummary of categories applied:")
    print(f"  - Legislators (Auto-detected): {auto_legislator_count}")
    print(f"  - Friends & Family (From Column B): {auto_ff_count}")
    print(f"  - Coalition Partners (From Column B): {auto_coalition_count}")
    # We subtract 1 from blank_count to ignore header if it got evaluated, but here we skipped header
    print(f"  - Left blank for manual selection: {blank_count}")
    print(f"\nSuccessfully saved changes to: {EXCEL_PATH}")

if __name__ == "__main__":
    main()
